import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class KayitOzetPage extends ConsumerStatefulWidget {
  const KayitOzetPage({super.key});

  @override
  ConsumerState<KayitOzetPage> createState() => _KayitOzetPageState();
}

class _KayitOzetPageState extends ConsumerState<KayitOzetPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/kayit-ozet')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🎯 Kayıt Modülü Özeti')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final d = snap.data ?? {};
          final pipeline = d['pipeline'] as Map? ?? {};
          final bugun = d['bugun'] as Map? ?? {};
          final toplam = d['toplam'] as Map? ?? {};

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [

              // BUGUN KARTI
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('📅 Bugün', style: TextStyle(color: Colors.white70, fontSize: 12)),
                  const SizedBox(height: 10),
                  Row(children: [
                    _BugunStat(val: '${bugun['aranan'] ?? 0}', label: 'Aranan', icon: Icons.phone),
                    _BugunStat(val: '${bugun['randevu'] ?? 0}', label: 'Randevu', icon: Icons.calendar_today),
                    _BugunStat(val: '${bugun['gorusme'] ?? 0}', label: 'Görüşme', icon: Icons.handshake),
                    _BugunStat(val: '${bugun['kayit'] ?? 0}', label: 'Kayıt', icon: Icons.check_circle),
                  ]),
                ]),
              ),
              const SizedBox(height: 16),

              // TOPLAM OZET
              Row(children: [
                _ToplamKart(label: 'Toplam Aday', val: '${toplam['aday_sayisi'] ?? 0}', color: AppColors.primary),
                const SizedBox(width: 8),
                _ToplamKart(label: 'Toplam Veli', val: '${toplam['veli_sayisi'] ?? 0}', color: AppColors.info),
              ]),
              const SizedBox(height: 8),
              Row(children: [
                _ToplamKart(label: 'Kesin Kayıt', val: '${toplam['kesin_kayit'] ?? 0}', color: AppColors.success),
                const SizedBox(width: 8),
                _ToplamKart(label: 'Dönüşüm', val: '%${toplam['donusum_orani'] ?? 0}', color: AppColors.gold),
              ]),
              const SizedBox(height: 20),

              // PIPELINE
              const Text('📊 Pipeline Durumu',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),

              _PipelineBar(label: 'Aday', val: pipeline['aday'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.info),
              _PipelineBar(label: 'Arandı', val: pipeline['arandi'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.primary),
              _PipelineBar(label: 'Randevu', val: pipeline['randevu'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.gold),
              _PipelineBar(label: 'Görüşme', val: pipeline['gorusme'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.warning),
              _PipelineBar(label: 'Fiyat Verildi', val: pipeline['fiyat_verildi'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: Color(0xFF8B5CF6)),
              _PipelineBar(label: 'Sözleşme', val: pipeline['sozlesme'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.info),
              _PipelineBar(label: 'Kesin Kayıt ✓', val: pipeline['kesin_kayit'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.success),
              _PipelineBar(label: 'Olumsuz ✗', val: pipeline['olumsuz'] ?? 0, total: toplam['aday_sayisi'] ?? 1, color: AppColors.danger),
            ]),
          );
        },
      ),
    );
  }
}


class _BugunStat extends StatelessWidget {
  final String val; final String label; final IconData icon;
  const _BugunStat({required this.val, required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Column(children: [
      Icon(icon, color: Colors.white70, size: 18),
      const SizedBox(height: 4),
      Text(val, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
      Text(label, style: const TextStyle(color: Colors.white70, fontSize: 10)),
    ]));
  }
}


class _ToplamKart extends StatelessWidget {
  final String label; final String val; final Color color;
  const _ToplamKart({required this.label, required this.val, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(children: [
        Text(val, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 11)),
      ]),
    ));
  }
}


class _PipelineBar extends StatelessWidget {
  final String label; final int val; final int total; final Color color;
  const _PipelineBar({required this.label, required this.val, required this.total, required this.color});

  @override
  Widget build(BuildContext context) {
    final oran = (val / total).clamp(0.0, 1.0);
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Expanded(child: Text(label, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500))),
          Text('$val', style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: color)),
        ]),
        const SizedBox(height: 4),
        ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: LinearProgressIndicator(
            value: oran, minHeight: 10,
            backgroundColor: color.withOpacity(0.1),
            valueColor: AlwaysStoppedAnimation(color),
          ),
        ),
      ]),
    );
  }
}
