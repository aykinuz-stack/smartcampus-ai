import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/veli_api.dart';
import '../../core/theme/app_theme.dart';


class RandevuPage extends ConsumerStatefulWidget {
  const RandevuPage({super.key});

  @override
  ConsumerState<RandevuPage> createState() => _RandevuPageState();
}

class _RandevuPageState extends ConsumerState<RandevuPage> with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(veliApiProvider).randevularim());
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
        title: const Text('📅 Randevularım'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(text: 'Aktif'),
            Tab(text: 'Geçmiş'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.add),
        label: const Text('Yeni Randevu'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        onPressed: () async {
          await showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            builder: (_) => const _YeniRandevuSheet(),
          );
          _load();
        },
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
          final data = snap.data ?? {};
          final aktif = (data['aktif'] as List?) ?? [];
          final gecmis = (data['gecmis'] as List?) ?? [];

          return TabBarView(
            controller: _tabCtrl,
            children: [
              _RandevuList(list: aktif, onIptal: (id) async {
                await ref.read(veliApiProvider).randevuIptal(id);
                _load();
              }),
              _RandevuList(list: gecmis, onIptal: null),
            ],
          );
        },
      ),
    );
  }
}


class _RandevuList extends StatelessWidget {
  final List list;
  final Function(String)? onIptal;
  const _RandevuList({required this.list, required this.onIptal});

  @override
  Widget build(BuildContext context) {
    if (list.isEmpty) {
      return const Center(
        child: Text('Randevu yok', style: TextStyle(fontSize: 15)),
      );
    }
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: list.length,
      itemBuilder: (_, i) => _RandevuKart(r: list[i], onIptal: onIptal),
    );
  }
}


class _RandevuKart extends StatelessWidget {
  final dynamic r;
  final Function(String)? onIptal;
  const _RandevuKart({required this.r, required this.onIptal});

  @override
  Widget build(BuildContext context) {
    final durum = (r['durum'] as String? ?? '').toLowerCase();
    Color c;
    IconData icon;
    String durumLabel;
    switch (durum) {
      case 'onaylandi':
        c = AppColors.success; icon = Icons.check_circle; durumLabel = 'Onaylandı';
        break;
      case 'beklemede':
        c = AppColors.warning; icon = Icons.access_time; durumLabel = 'Beklemede';
        break;
      case 'iptal':
        c = AppColors.danger; icon = Icons.cancel; durumLabel = 'İptal';
        break;
      case 'tamamlandi':
        c = AppColors.info; icon = Icons.done_all; durumLabel = 'Tamamlandı';
        break;
      default:
        c = Colors.grey; icon = Icons.help_outline; durumLabel = durum;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: c),
                const SizedBox(width: 8),
                Text(durumLabel,
                    style: TextStyle(color: c, fontWeight: FontWeight.bold)),
                const Spacer(),
                Text('${r['tarih']} · ${r['saat']}',
                    style: const TextStyle(color: AppColors.textSecondaryDark, fontSize: 13)),
              ],
            ),
            const SizedBox(height: 10),
            Text(r['konu'] ?? '',
                style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 4),
            Text('Öğretmen: ${r['ogretmen_adi']}',
                style: const TextStyle(fontSize: 13)),
            if ((r['notlar'] as String? ?? '').isNotEmpty) ...[
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(r['notlar'] as String, style: const TextStyle(fontSize: 12)),
              ),
            ],
            if (onIptal != null && durum != 'iptal') ...[
              const SizedBox(height: 10),
              Align(
                alignment: Alignment.centerRight,
                child: TextButton.icon(
                  onPressed: () => onIptal!(r['id'] as String),
                  icon: const Icon(Icons.cancel_outlined, color: AppColors.danger),
                  label: const Text('İptal Et', style: TextStyle(color: AppColors.danger)),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}


class _YeniRandevuSheet extends ConsumerStatefulWidget {
  const _YeniRandevuSheet();

  @override
  ConsumerState<_YeniRandevuSheet> createState() => _YeniRandevuSheetState();
}

class _YeniRandevuSheetState extends ConsumerState<_YeniRandevuSheet> {
  final _ogretmenIdCtrl = TextEditingController();
  final _ogretmenAdiCtrl = TextEditingController();
  final _konuCtrl = TextEditingController();
  DateTime _tarih = DateTime.now().add(const Duration(days: 1));
  TimeOfDay _saat = const TimeOfDay(hour: 14, minute: 0);
  bool _gondering = false;

  @override
  void dispose() {
    _ogretmenIdCtrl.dispose();
    _ogretmenAdiCtrl.dispose();
    _konuCtrl.dispose();
    super.dispose();
  }

  Future<void> _gonder() async {
    if (_konuCtrl.text.trim().length < 3 || _ogretmenAdiCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Öğretmen ve konu alanları zorunlu')),
      );
      return;
    }
    setState(() => _gondering = true);
    try {
      await ref.read(veliApiProvider).randevuAl(
        ogretmenId: _ogretmenIdCtrl.text.trim().isEmpty
            ? _ogretmenAdiCtrl.text.trim().toLowerCase().replaceAll(' ', '_')
            : _ogretmenIdCtrl.text.trim(),
        ogretmenAdi: _ogretmenAdiCtrl.text.trim(),
        tarih: DateFormat('yyyy-MM-dd').format(_tarih),
        saat: '${_saat.hour.toString().padLeft(2, '0')}:${_saat.minute.toString().padLeft(2, '0')}',
        konu: _konuCtrl.text.trim(),
      );
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Randevu talebi gönderildi'), backgroundColor: AppColors.success),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      if (mounted) setState(() => _gondering = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 20, right: 20, top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text('Yeni Randevu Talebi',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),
          TextField(
            controller: _ogretmenAdiCtrl,
            decoration: InputDecoration(
              labelText: 'Öğretmen Adı *',
              prefixIcon: const Icon(Icons.person),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _konuCtrl,
            decoration: InputDecoration(
              labelText: 'Konu *',
              prefixIcon: const Icon(Icons.topic),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
            ),
            maxLines: 2,
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(
                child: InkWell(
                  onTap: () async {
                    final t = await showDatePicker(
                      context: context,
                      initialDate: _tarih,
                      firstDate: DateTime.now(),
                      lastDate: DateTime.now().add(const Duration(days: 90)),
                    );
                    if (t != null) setState(() => _tarih = t);
                  },
                  child: InputDecorator(
                    decoration: InputDecoration(
                      labelText: 'Tarih',
                      prefixIcon: const Icon(Icons.calendar_today),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: Text(DateFormat('dd MMM yyyy').format(_tarih)),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: InkWell(
                  onTap: () async {
                    final t = await showTimePicker(context: context, initialTime: _saat);
                    if (t != null) setState(() => _saat = t);
                  },
                  child: InputDecorator(
                    decoration: InputDecoration(
                      labelText: 'Saat',
                      prefixIcon: const Icon(Icons.access_time),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    child: Text(_saat.format(context)),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          SizedBox(
            height: 48,
            child: ElevatedButton(
              onPressed: _gondering ? null : _gonder,
              child: _gondering
                  ? const SizedBox(width: 20, height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Text('RANDEVU TALEBİ GÖNDER'),
            ),
          ),
        ],
      ),
    );
  }
}
