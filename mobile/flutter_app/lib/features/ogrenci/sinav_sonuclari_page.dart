import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Ogrenci Sinav Sonuclari — yazili + deneme + online sinav
class SinavSonuclariPage extends ConsumerStatefulWidget {
  const SinavSonuclariPage({super.key});

  @override
  ConsumerState<SinavSonuclariPage> createState() => _SinavSonuclariPageState();
}

class _SinavSonuclariPageState extends ConsumerState<SinavSonuclariPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() {
      _future = ref.read(apiClientProvider)
          .get('/ogrenci/sinav-sonuclari')
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sinav Sonuclarim')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final data = snap.data ?? {};
          final sonuclar = (data['sonuclar'] as List?) ?? [];
          final dersOrt = Map<String, dynamic>.from(data['ders_ortalamalari'] as Map? ?? {});

          if (sonuclar.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.analytics_outlined, size: 64, color: AppColors.info),
                  SizedBox(height: 12),
                  Text('Henuz sinav sonucu yok', style: TextStyle(fontSize: 16)),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Ders ortalamalari
                if (dersOrt.isNotEmpty) ...[
                  const Text('Ders Ortalamalari',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),
                  Wrap(
                    spacing: 8, runSpacing: 8,
                    children: dersOrt.entries.map((e) {
                      final ort = (e.value as num).toDouble();
                      Color c = ort >= 85
                          ? AppColors.success
                          : ort >= 70
                              ? AppColors.info
                              : ort >= 50
                                  ? AppColors.warning
                                  : AppColors.danger;
                      return Container(
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                        decoration: BoxDecoration(
                          color: c.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: c.withOpacity(0.3)),
                        ),
                        child: Column(
                          children: [
                            Text(ort.toStringAsFixed(1),
                                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: c)),
                            Text(e.key, style: const TextStyle(fontSize: 11)),
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 20),
                ],

                // Sonuclar listesi
                Text('Son Sinavlar (${sonuclar.length})',
                    style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                const SizedBox(height: 10),
                ...sonuclar.map((s) {
                  final m = Map<String, dynamic>.from(s as Map);
                  return _SinavSonucKart(sonuc: m);
                }),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _SinavSonucKart extends StatelessWidget {
  final Map<String, dynamic> sonuc;
  const _SinavSonucKart({required this.sonuc});

  @override
  Widget build(BuildContext context) {
    final ad = sonuc['sinav_adi'] as String? ?? '';
    final ders = sonuc['ders'] as String? ?? '';
    final puan = (sonuc['puan'] as num?)?.toDouble() ?? 0;
    final dogru = sonuc['dogru'] as int?;
    final yanlis = sonuc['yanlis'] as int?;
    final bos = sonuc['bos'] as int?;
    final tarih = sonuc['tarih'] as String? ?? '';

    Color c = puan >= 85
        ? AppColors.success
        : puan >= 70
            ? AppColors.info
            : puan >= 50
                ? AppColors.warning
                : AppColors.danger;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Row(
          children: [
            // Puan dairesi
            Container(
              width: 56, height: 56,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: c.withOpacity(0.15),
                border: Border.all(color: c, width: 2.5),
              ),
              alignment: Alignment.center,
              child: Text(
                puan.toStringAsFixed(0),
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: c),
              ),
            ),
            const SizedBox(width: 14),
            // Bilgiler
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(ad, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                      maxLines: 1, overflow: TextOverflow.ellipsis),
                  Text(ders, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                  const SizedBox(height: 4),
                  if (dogru != null)
                    Row(
                      children: [
                        _MiniStat('D', '$dogru', AppColors.success),
                        const SizedBox(width: 6),
                        _MiniStat('Y', '$yanlis', AppColors.danger),
                        const SizedBox(width: 6),
                        _MiniStat('B', '$bos', Colors.grey),
                      ],
                    ),
                ],
              ),
            ),
            // Tarih
            Text(tarih.length >= 10 ? tarih.substring(0, 10) : tarih,
                style: const TextStyle(fontSize: 10, color: AppColors.textSecondaryDark)),
          ],
        ),
      ),
    );
  }
}


class _MiniStat extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _MiniStat(this.label, this.value, this.color);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text('$label:$value',
          style: TextStyle(fontSize: 10, color: color, fontWeight: FontWeight.bold)),
    );
  }
}
