import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/theme/app_theme.dart';

class OdevPage extends ConsumerStatefulWidget {
  const OdevPage({super.key});

  @override
  ConsumerState<OdevPage> createState() => _OdevPageState();
}

class _OdevPageState extends ConsumerState<OdevPage> with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(ogrenciApiProvider).getOdevler());
  }

  Future<void> _teslim(String odevId) async {
    try {
      await ref.read(ogrenciApiProvider).teslimEt(odevId);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('✓ Ödev teslim edildi'),
          backgroundColor: AppColors.success,
        ),
      );
      _load();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    }
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ödevlerim'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(text: 'Bekleyen'),
            Tab(text: 'Geciken'),
            Tab(text: 'Teslim'),
          ],
        ),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
          final data = snap.data ?? {};

          final bekleyen = (data['bekleyen'] as List?) ?? [];
          final geciken = (data['geciken'] as List?) ?? [];
          final teslim = (data['teslim_edilen'] as List?) ?? [];

          return TabBarView(
            controller: _tabCtrl,
            children: [
              _OdevList(odevler: bekleyen, onTeslim: _teslim, type: 'bekleyen'),
              _OdevList(odevler: geciken, onTeslim: _teslim, type: 'geciken'),
              _OdevList(odevler: teslim, onTeslim: null, type: 'teslim'),
            ],
          );
        },
      ),
    );
  }
}


class _OdevList extends StatelessWidget {
  final List odevler;
  final Function(String)? onTeslim;
  final String type;
  const _OdevList({required this.odevler, required this.onTeslim, required this.type});

  @override
  Widget build(BuildContext context) {
    if (odevler.isEmpty) {
      String msg;
      switch (type) {
        case 'bekleyen': msg = '🎉 Bekleyen ödev yok'; break;
        case 'geciken': msg = '✓ Geciken ödev yok'; break;
        default: msg = 'Henüz teslim edilen ödev yok';
      }
      return Center(child: Text(msg, style: const TextStyle(fontSize: 15)));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: odevler.length,
      itemBuilder: (_, i) => _OdevKart(
        o: odevler[i],
        type: type,
        onTeslim: onTeslim,
      ),
    );
  }
}


class _OdevKart extends StatelessWidget {
  final dynamic o;
  final String type;
  final Function(String)? onTeslim;
  const _OdevKart({required this.o, required this.type, this.onTeslim});

  @override
  Widget build(BuildContext context) {
    Color c;
    IconData icon;
    switch (type) {
      case 'bekleyen': c = AppColors.info; icon = Icons.assignment_outlined; break;
      case 'geciken': c = AppColors.danger; icon = Icons.warning_amber_rounded; break;
      default:
        c = AppColors.success; icon = Icons.check_circle_outline;
    }

    final puan = o['puan'];
    final teslimTarihi = o['teslim_tarihi'] as String? ?? '';
    final gecTeslim = o['gec_teslim'] as bool? ?? false;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: c.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(icon, color: c, size: 22),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        o['baslik'] ?? '',
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '${o['ders']} · ${o['ogretmen_adi']}',
                        style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark),
                      ),
                    ],
                  ),
                ),
                if (puan != null)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.success.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      '${(puan as num).toStringAsFixed(0)}',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold, color: AppColors.success),
                    ),
                  ),
              ],
            ),
            if ((o['aciklama'] as String?)?.isNotEmpty == true) ...[
              const SizedBox(height: 10),
              Text(o['aciklama'] as String,
                  style: const TextStyle(fontSize: 13),
                  maxLines: 3, overflow: TextOverflow.ellipsis),
            ],
            const SizedBox(height: 10),
            Row(
              children: [
                const Icon(Icons.calendar_today, size: 14, color: AppColors.textSecondaryDark),
                const SizedBox(width: 6),
                Text(
                  type == 'teslim'
                      ? 'Teslim: ${o['teslim_tarih'] ?? '-'}${gecTeslim ? ' (geç)' : ''}'
                      : 'Son: $teslimTarihi',
                  style: TextStyle(
                    fontSize: 12,
                    color: gecTeslim ? AppColors.warning : AppColors.textSecondaryDark,
                  ),
                ),
                const Spacer(),
                if (onTeslim != null)
                  ElevatedButton.icon(
                    onPressed: () => onTeslim!(o['id'] as String),
                    icon: const Icon(Icons.check, size: 16),
                    label: const Text('Teslim Et'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                      backgroundColor: c,
                    ),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
