import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/theme/app_theme.dart';

class NotlarPage extends ConsumerStatefulWidget {
  const NotlarPage({super.key});

  @override
  ConsumerState<NotlarPage> createState() => _NotlarPageState();
}

class _NotlarPageState extends ConsumerState<NotlarPage> {
  String? _selectedDonem;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() {
      _future = ref.read(ogrenciApiProvider).getNotlar(donem: _selectedDonem);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notlarım'),
        actions: [
          PopupMenuButton<String?>(
            icon: const Icon(Icons.filter_list),
            onSelected: (v) {
              setState(() => _selectedDonem = v);
              _load();
            },
            itemBuilder: (ctx) => [
              const PopupMenuItem(value: null, child: Text('Tüm Yıl')),
              const PopupMenuItem(value: '1. Donem', child: Text('1. Dönem')),
              const PopupMenuItem(value: '2. Donem', child: Text('2. Dönem')),
            ],
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final data = snap.data;
          if (data == null) return const SizedBox();

          final notlar = (data['notlar'] as List?) ?? [];
          final donemOrt = (data['donem_ortalamasi'] as num?)?.toDouble() ?? 0.0;
          final genelOrt = (data['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
          final dersOzetleri = (data['ders_ozetleri'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Ortalama kartlari
                Row(
                  children: [
                    Expanded(child: _AvgCard(
                      title: 'Dönem Ort.',
                      value: donemOrt,
                      color: AppColors.primary,
                    )),
                    const SizedBox(width: 12),
                    Expanded(child: _AvgCard(
                      title: 'Genel Ort.',
                      value: genelOrt,
                      color: AppColors.gold,
                    )),
                  ],
                ),
                const SizedBox(height: 16),

                // Ders özetleri
                if (dersOzetleri.isNotEmpty) ...[
                  const Text('Ders Ortalamalar',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),
                  ...dersOzetleri.map((d) => _DersOzetCard(data: d)),
                  const SizedBox(height: 16),
                ],

                // Son notlar
                const Text('Son Notlar',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                const SizedBox(height: 10),
                if (notlar.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(32),
                    child: Center(child: Text('Bu dönemde not yok')),
                  )
                else
                  ...notlar.take(30).map((n) => _NotKart(n: n)),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _AvgCard extends StatelessWidget {
  final String title;
  final double value;
  final Color color;
  const _AvgCard({required this.title, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: color.withOpacity(0.4)),
      ),
      child: Column(
        children: [
          Text(title, style: const TextStyle(fontSize: 13)),
          const SizedBox(height: 8),
          Text(
            value.toStringAsFixed(1),
            style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: color),
          ),
        ],
      ),
    );
  }
}


class _DersOzetCard extends StatelessWidget {
  final dynamic data;
  const _DersOzetCard({required this.data});

  @override
  Widget build(BuildContext context) {
    final ort = (data['ortalama'] as num).toDouble();
    Color c;
    if (ort >= 85) c = AppColors.success;
    else if (ort >= 70) c = AppColors.info;
    else if (ort >= 55) c = AppColors.warning;
    else c = AppColors.danger;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: c.withOpacity(0.15),
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Text(
              ort.toStringAsFixed(0),
              style: TextStyle(color: c, fontWeight: FontWeight.bold),
            ),
          ),
        ),
        title: Text(data['ders'] ?? '',
            style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('${data['not_sayisi']} not · '
            'En yüksek: ${(data['en_yuksek'] as num).toStringAsFixed(0)} · '
            'En düşük: ${(data['en_dusuk'] as num).toStringAsFixed(0)}'),
      ),
    );
  }
}


class _NotKart extends StatelessWidget {
  final dynamic n;
  const _NotKart({required this.n});

  @override
  Widget build(BuildContext context) {
    final puan = (n['puan'] as num).toDouble();
    final tarih = n['tarih'] as String;
    Color c;
    if (puan >= 85) c = AppColors.success;
    else if (puan >= 70) c = AppColors.info;
    else if (puan >= 55) c = AppColors.warning;
    else c = AppColors.danger;

    String turIcon;
    switch ((n['not_turu'] as String).toLowerCase()) {
      case 'yazili': turIcon = '📝'; break;
      case 'sozlu': turIcon = '🗣️'; break;
      case 'proje': turIcon = '📊'; break;
      case 'performans': turIcon = '🎯'; break;
      default: turIcon = '📋';
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Text(turIcon, style: const TextStyle(fontSize: 26)),
        title: Text(n['ders'] ?? '',
            style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('${n['not_turu']} ${n['not_sirasi']} · $tarih'),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: c.withOpacity(0.15),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            puan.toStringAsFixed(0),
            style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 18),
          ),
        ),
      ),
    );
  }
}
