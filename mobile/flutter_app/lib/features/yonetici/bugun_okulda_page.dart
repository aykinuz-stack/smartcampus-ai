import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class BugunOkuldaPage extends ConsumerStatefulWidget {
  const BugunOkuldaPage({super.key});

  @override
  ConsumerState<BugunOkuldaPage> createState() => _BugunOkuldaPageState();
}

class _BugunOkuldaPageState extends ConsumerState<BugunOkuldaPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetch());
  }

  Future<Map<String, dynamic>> _fetch() async {
    final r = await ref.read(apiClientProvider).get('/yonetici/bugun-okulda');
    return Map<String, dynamic>.from(r.data);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📅 Bugün Okulda')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final d = snap.data ?? {};
          final ist = d['istatistik'] as Map? ?? {};
          final dersler = (d['ders_programi'] as List?) ?? [];
          final etkinlikler = (d['etkinlikler'] as List?) ?? [];
          final randevular = (d['randevular'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Hero başlık
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primary, AppColors.primaryDark],
                    ),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${d['gun'] ?? ''}, ${d['tarih'] ?? ''}',
                        style: const TextStyle(
                            color: Colors.white, fontWeight: FontWeight.bold,
                            fontSize: 18),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          _MiniStat(
                            label: 'Ders Saati',
                            value: '${ist['toplam_ders_saati'] ?? 0}',
                          ),
                          const SizedBox(width: 16),
                          _MiniStat(
                            label: 'Yoklama Alınan',
                            value: '${ist['yoklama_alinan_sinif'] ?? 0}',
                          ),
                          const SizedBox(width: 16),
                          _MiniStat(
                            label: 'Devamsız',
                            value: '${ist['bugun_devamsiz'] ?? 0}',
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),

                // Ders programı
                _Bolum(
                  baslik: '📚 Ders Programı',
                  color: AppColors.info,
                  icerik: dersler.isEmpty
                      ? const Text('Bugün ders yok')
                      : Column(
                          children: dersler.map((saat) {
                            final s = saat as Map;
                            final saatNo = s['saat'];
                            final dersList = (s['dersler'] as List?) ?? [];
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 8),
                              child: Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: AppColors.info.withOpacity(0.08),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text('$saatNo. Ders',
                                        style: const TextStyle(
                                            fontWeight: FontWeight.bold,
                                            color: AppColors.info)),
                                    const SizedBox(height: 4),
                                    ...dersList.take(5).map((d) {
                                      final dd = d as Map;
                                      return Text(
                                        '  ${dd['sinif']} — ${dd['ders']} (${dd['ogretmen']})',
                                        style: const TextStyle(fontSize: 12),
                                      );
                                    }),
                                    if (dersList.length > 5)
                                      Text('  ... +${dersList.length - 5} ders',
                                          style: const TextStyle(fontSize: 11,
                                              color: AppColors.textSecondaryDark)),
                                  ],
                                ),
                              ),
                            );
                          }).toList(),
                        ),
                ),

                const SizedBox(height: 16),

                // Etkinlikler
                _Bolum(
                  baslik: '🎉 Bugünkü Etkinlikler',
                  color: AppColors.success,
                  icerik: etkinlikler.isEmpty
                      ? const Text('Bugün etkinlik yok')
                      : Column(
                          children: etkinlikler.map((e) {
                            final ee = e as Map;
                            return ListTile(
                              dense: true,
                              contentPadding: EdgeInsets.zero,
                              leading: const Icon(Icons.event,
                                  color: AppColors.success),
                              title: Text(ee['baslik'] ?? '',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.w600, fontSize: 13)),
                              subtitle: Text(
                                '${ee['konum'] ?? ''} · ${ee['tur'] ?? ''}',
                                style: const TextStyle(fontSize: 11),
                              ),
                            );
                          }).toList(),
                        ),
                ),

                const SizedBox(height: 16),

                // Randevular
                _Bolum(
                  baslik: '📅 Bugünkü Randevular',
                  color: AppColors.gold,
                  icerik: randevular.isEmpty
                      ? const Text('Bugün randevu yok')
                      : Column(
                          children: randevular.map((r) {
                            final rr = r as Map;
                            return ListTile(
                              dense: true,
                              contentPadding: EdgeInsets.zero,
                              leading: Container(
                                width: 50,
                                padding: const EdgeInsets.all(6),
                                decoration: BoxDecoration(
                                  color: AppColors.gold.withOpacity(0.15),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(rr['saat'] ?? '',
                                    textAlign: TextAlign.center,
                                    style: const TextStyle(
                                        color: AppColors.gold,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 12)),
                              ),
                              title: Text(rr['konu'] ?? '',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.w600, fontSize: 13)),
                              subtitle: Text(
                                '${rr['veli']} ↔ ${rr['ogretmen']} · ${rr['durum']}',
                                style: const TextStyle(fontSize: 11),
                              ),
                            );
                          }).toList(),
                        ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _MiniStat extends StatelessWidget {
  final String label;
  final String value;
  const _MiniStat({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(value,
            style: const TextStyle(
                color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
        Text(label,
            style: TextStyle(
                color: Colors.white.withOpacity(0.8), fontSize: 11)),
      ],
    );
  }
}


class _Bolum extends StatelessWidget {
  final String baslik;
  final Color color;
  final Widget icerik;
  const _Bolum(
      {required this.baslik, required this.color, required this.icerik});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(baslik,
                style: TextStyle(
                    fontSize: 16, fontWeight: FontWeight.bold, color: color)),
            const Divider(),
            icerik,
          ],
        ),
      ),
    );
  }
}
