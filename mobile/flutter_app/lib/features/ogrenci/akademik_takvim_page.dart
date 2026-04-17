import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class AkademikTakvimPage extends ConsumerStatefulWidget {
  const AkademikTakvimPage({super.key});
  @override
  ConsumerState<AkademikTakvimPage> createState() => _AkademikTakvimPageState();
}

class _AkademikTakvimPageState extends ConsumerState<AkademikTakvimPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/bugun-okulda')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📅 Akademik Takvim')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final tarih = d['tarih'] ?? '';
          final gun = d['gun'] ?? '';
          final etkinlikler = (d['etkinlikler'] as List?) ?? [];
          final randevular = (d['randevular'] as List?) ?? [];
          final dersler = (d['ders_programi'] as List?) ?? [];
          final ist = d['istatistik'] as Map? ?? {};

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Tarih hero
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    const Icon(Icons.calendar_today, color: Colors.white, size: 24),
                    const SizedBox(width: 10),
                    Text('$gun', style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                  ]),
                  const SizedBox(height: 4),
                  Text(tarih, style: TextStyle(color: Colors.white.withOpacity(0.8))),
                  const SizedBox(height: 12),
                  Row(children: [
                    _MiniKart('${ist['toplam_ders_saati'] ?? 0}', 'Ders', AppColors.info),
                    const SizedBox(width: 8),
                    _MiniKart('${etkinlikler.length}', 'Etkinlik', AppColors.success),
                    const SizedBox(width: 8),
                    _MiniKart('${randevular.length}', 'Randevu', AppColors.gold),
                    const SizedBox(width: 8),
                    _MiniKart('${ist['bugun_devamsiz'] ?? 0}', 'Devamsız', AppColors.danger),
                  ]),
                ]),
              ),
              const SizedBox(height: 20),

              // Etkinlikler
              if (etkinlikler.isNotEmpty) ...[
                const Text('🎉 Bugünkü Etkinlikler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...etkinlikler.map((e) {
                  final ee = e as Map;
                  return Card(child: ListTile(
                    leading: Container(
                      width: 40, height: 40,
                      decoration: BoxDecoration(color: AppColors.success.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                      child: const Icon(Icons.event, color: AppColors.success, size: 20),
                    ),
                    title: Text(ee['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                    subtitle: Text('${ee['konum'] ?? ''} · ${ee['tur'] ?? ''}', style: const TextStyle(fontSize: 11)),
                  ));
                }),
                const SizedBox(height: 16),
              ] else ...[
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.success.withOpacity(0.08), borderRadius: BorderRadius.circular(12)),
                  child: const Row(children: [
                    Icon(Icons.check_circle, color: AppColors.success),
                    SizedBox(width: 10),
                    Text('Bugün özel etkinlik yok', style: TextStyle(fontSize: 14)),
                  ]),
                ),
                const SizedBox(height: 16),
              ],

              // Randevular
              if (randevular.isNotEmpty) ...[
                const Text('📅 Randevular', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...randevular.map((r) {
                  final rr = r as Map;
                  return Card(child: ListTile(
                    leading: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                      child: Text(rr['saat'] ?? '', style: const TextStyle(color: AppColors.gold, fontWeight: FontWeight.bold, fontSize: 12)),
                    ),
                    title: Text(rr['konu'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                    subtitle: Text('${rr['veli'] ?? ''} ↔ ${rr['ogretmen'] ?? ''}', style: const TextStyle(fontSize: 11)),
                  ));
                }),
                const SizedBox(height: 16),
              ],

              // Ders programi ozeti
              if (dersler.isNotEmpty) ...[
                const Text('📚 Bugünkü Dersler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...dersler.map((s) {
                  final ss = s as Map;
                  return Container(
                    margin: const EdgeInsets.only(bottom: 6),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: AppColors.info.withOpacity(0.06), borderRadius: BorderRadius.circular(8)),
                    child: Row(children: [
                      Container(
                        width: 30, height: 30,
                        decoration: BoxDecoration(color: AppColors.info.withOpacity(0.15), shape: BoxShape.circle),
                        child: Center(child: Text('${ss['saat']}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppColors.info))),
                      ),
                      const SizedBox(width: 10),
                      Text('${(ss['dersler'] as List?)?.length ?? 0} sınıf', style: const TextStyle(fontSize: 13)),
                    ]),
                  );
                }),
              ],
            ]),
          );
        },
      ),
    );
  }
}


class _MiniKart extends StatelessWidget {
  final String val; final String label; final Color color;
  const _MiniKart(this.val, this.label, this.color);

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(color: Colors.white.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
      child: Column(children: [
        Text(val, style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
        Text(label, style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 9)),
      ]),
    ));
  }
}
