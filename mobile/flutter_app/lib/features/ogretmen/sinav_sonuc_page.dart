import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


class SinavSonucPage extends ConsumerStatefulWidget {
  const SinavSonucPage({super.key});

  @override
  ConsumerState<SinavSonucPage> createState() => _SinavSonucPageState();
}

class _SinavSonucPageState extends ConsumerState<SinavSonucPage> {
  Future<Map<String, dynamic>>? _future;
  String? _selectedDers;
  String? _selectedSinif;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() => _future = ref.read(ogretmenApiProvider)
        .sinavSonuclari(ders: _selectedDers, sinif: _selectedSinif));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📊 Sınav Sonuçları')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
          final d = snap.data ?? {};
          final sonuclar = (d['sonuclar'] as List?) ?? [];
          final filtreler = d['filtreler'] as Map? ?? {};
          final dersler = List<String>.from((filtreler['dersler'] as List?) ?? []);
          final siniflar = List<String>.from((filtreler['siniflar'] as List?) ?? []);

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Filtreler
                Row(children: [
                  Expanded(
                    child: DropdownButtonFormField<String?>(
                      value: _selectedDers,
                      decoration: const InputDecoration(labelText: 'Ders', isDense: true,
                          border: OutlineInputBorder()),
                      items: [
                        const DropdownMenuItem(value: null, child: Text('Hepsi')),
                        ...dersler.map((d) => DropdownMenuItem(value: d, child: Text(d,
                            style: const TextStyle(fontSize: 12)))),
                      ],
                      onChanged: (v) { setState(() => _selectedDers = v); _load(); },
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: DropdownButtonFormField<String?>(
                      value: _selectedSinif,
                      decoration: const InputDecoration(labelText: 'Sınıf', isDense: true,
                          border: OutlineInputBorder()),
                      items: [
                        const DropdownMenuItem(value: null, child: Text('Hepsi')),
                        ...siniflar.map((s) => DropdownMenuItem(value: s, child: Text(s))),
                      ],
                      onChanged: (v) {
                        final parts = v?.split('/');
                        setState(() {
                          _selectedSinif = parts?.first;
                        });
                        _load();
                      },
                    ),
                  ),
                ]),
                const SizedBox(height: 16),

                Text('${d['toplam_sinav'] ?? 0} sınav',
                    style: const TextStyle(color: AppColors.textSecondaryDark, fontSize: 13)),
                const SizedBox(height: 10),

                if (sonuclar.isEmpty)
                  const Padding(padding: EdgeInsets.all(32),
                      child: Center(child: Text('Sınav sonucu yok')))
                else
                  ...sonuclar.map((s) {
                    final ss = s as Map;
                    final ort = (ss['ortalama'] as num?)?.toDouble() ?? 0.0;
                    final basari = (ss['basari_orani'] as num?)?.toDouble() ?? 0.0;
                    Color c = basari >= 80 ? AppColors.success : basari >= 60 ? AppColors.info :
                              basari >= 40 ? AppColors.warning : AppColors.danger;

                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ExpansionTile(
                        leading: Container(
                          width: 50, height: 50,
                          decoration: BoxDecoration(
                            color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                          child: Center(child: Text(ort.toStringAsFixed(0),
                              style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 18))),
                        ),
                        title: Text('${ss['ders']} · ${ss['sinav_adi']}',
                            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                        subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Text('${ss['sinif']} · ${ss['tarih']} · ${ss['ogrenci_sayisi']} öğrenci',
                              style: const TextStyle(fontSize: 11)),
                          const SizedBox(height: 4),
                          Row(children: [
                            _Mini(label: 'Ort', val: ort.toStringAsFixed(1), color: c),
                            const SizedBox(width: 6),
                            _Mini(label: 'Max', val: '${(ss['en_yuksek'] as num?)?.toStringAsFixed(0) ?? 0}',
                                color: AppColors.success),
                            const SizedBox(width: 6),
                            _Mini(label: 'Min', val: '${(ss['en_dusuk'] as num?)?.toStringAsFixed(0) ?? 0}',
                                color: AppColors.danger),
                            const SizedBox(width: 6),
                            _Mini(label: 'Başarı', val: '${basari.toStringAsFixed(0)}%', color: c),
                          ]),
                        ]),
                        children: [
                          Padding(
                            padding: const EdgeInsets.all(12),
                            child: Column(children: [
                              // Basari bar
                              ClipRRect(
                                borderRadius: BorderRadius.circular(6),
                                child: LinearProgressIndicator(
                                  value: basari / 100, minHeight: 8,
                                  backgroundColor: c.withOpacity(0.1),
                                  valueColor: AlwaysStoppedAnimation(c),
                                ),
                              ),
                              const SizedBox(height: 12),
                              // Ogrenci listesi
                              ...((ss['detay'] as List?) ?? []).map((dd) {
                                final p = (dd['puan'] as num?)?.toDouble() ?? 0.0;
                                Color pc = p >= 85 ? AppColors.success : p >= 70 ? AppColors.info :
                                           p >= 50 ? AppColors.warning : AppColors.danger;
                                return Padding(
                                  padding: const EdgeInsets.symmetric(vertical: 2),
                                  child: Row(children: [
                                    Expanded(child: Text(dd['ogrenci'] ?? '', style: const TextStyle(fontSize: 12))),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                      decoration: BoxDecoration(color: pc.withOpacity(0.15),
                                          borderRadius: BorderRadius.circular(4)),
                                      child: Text(p.toStringAsFixed(0),
                                          style: TextStyle(color: pc, fontWeight: FontWeight.bold, fontSize: 13)),
                                    ),
                                  ]),
                                );
                              }),
                            ]),
                          ),
                        ],
                      ),
                    );
                  }),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _Mini extends StatelessWidget {
  final String label; final String val; final Color color;
  const _Mini({required this.label, required this.val, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(4)),
      child: Text('$label $val', style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.bold)),
    );
  }
}
