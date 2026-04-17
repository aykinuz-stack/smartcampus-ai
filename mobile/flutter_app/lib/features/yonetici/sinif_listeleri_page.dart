import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class SinifListeleriPage extends ConsumerStatefulWidget {
  const SinifListeleriPage({super.key});
  @override
  ConsumerState<SinifListeleriPage> createState() => _SinifListeleriPageState();
}

class _SinifListeleriPageState extends ConsumerState<SinifListeleriPage> {
  Future<Map<String, dynamic>>? _future;
  String? _sinifFiltre;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    final params = <String, dynamic>{};
    if (_sinifFiltre != null) {
      final p = _sinifFiltre!.split('/');
      params['sinif'] = p[0];
      if (p.length > 1) params['sube'] = p[1];
    }
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/sinif-listeleri', params: params.isNotEmpty ? params : null)
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🏫 Sınıf Listeleri')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final siniflar = (d['siniflar'] as List?) ?? [];
          final sinifListesi = List<String>.from((d['sinif_listesi'] as List?) ?? []);

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Ozet
              Row(children: [
                Expanded(child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${d['toplam_ogrenci'] ?? 0}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.primary)),
                    const Text('Öğrenci', style: TextStyle(fontSize: 11)),
                  ]),
                )),
                const SizedBox(width: 8),
                Expanded(child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(color: AppColors.success.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${d['toplam_sinif'] ?? 0}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.success)),
                    const Text('Sınıf', style: TextStyle(fontSize: 11)),
                  ]),
                )),
              ]),
              const SizedBox(height: 12),

              // Filtre
              DropdownButtonFormField<String?>(
                value: _sinifFiltre,
                decoration: const InputDecoration(labelText: 'Sınıf Filtre', isDense: true, border: OutlineInputBorder()),
                items: [
                  const DropdownMenuItem(value: null, child: Text('Tüm Sınıflar')),
                  ...sinifListesi.map((s) => DropdownMenuItem(value: s, child: Text(s))),
                ],
                onChanged: (v) { setState(() => _sinifFiltre = v); _load(); },
              ),
              const SizedBox(height: 16),

              // Sinif kartlari
              ...siniflar.map((s) {
                final ss = s as Map;
                final ogrenciler = (ss['ogrenciler'] as List?) ?? [];
                return Card(
                  margin: const EdgeInsets.only(bottom: 10),
                  child: ExpansionTile(
                    leading: Container(
                      width: 50, height: 50,
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                        borderRadius: BorderRadius.circular(10)),
                      child: Center(child: Text(ss['sinif_sube'] ?? '',
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13))),
                    ),
                    title: Text('${ss['sinif_sube']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Row(children: [
                      Text('${ss['ogrenci_sayisi']} öğrenci', style: const TextStyle(fontSize: 12)),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                        decoration: BoxDecoration(color: AppColors.info.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                        child: Text('${ss['kiz'] ?? 0}K ${ss['erkek'] ?? 0}E', style: const TextStyle(fontSize: 9, color: AppColors.info)),
                      ),
                    ]),
                    children: [
                      Padding(padding: const EdgeInsets.all(12), child: Column(
                        children: [
                          // Baslik satiri
                          Row(children: [
                            const SizedBox(width: 30, child: Text('No', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                            const SizedBox(width: 8),
                            const Expanded(child: Text('Ad Soyad', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                            const SizedBox(width: 40, child: Text('C', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                          ]),
                          const Divider(),
                          ...ogrenciler.map((o) {
                            final oo = o as Map;
                            return Padding(
                              padding: const EdgeInsets.symmetric(vertical: 2),
                              child: Row(children: [
                                SizedBox(width: 30, child: Text('${oo['numara']}', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark))),
                                const SizedBox(width: 8),
                                Expanded(child: Text(oo['ad_soyad'] ?? '', style: const TextStyle(fontSize: 13))),
                                SizedBox(width: 40, child: Text(
                                  (oo['cinsiyet'] ?? '').toString().toLowerCase().startsWith('k') ? '👧' : '👦',
                                  textAlign: TextAlign.center,
                                )),
                              ]),
                            );
                          }),
                        ],
                      )),
                    ],
                  ),
                );
              }),
            ]),
          );
        },
      ),
    );
  }
}
