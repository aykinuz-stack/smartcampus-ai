import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class DersProgramiPage extends ConsumerStatefulWidget {
  const DersProgramiPage({super.key});
  @override
  ConsumerState<DersProgramiPage> createState() => _DersProgramiPageState();
}

class _DersProgramiPageState extends ConsumerState<DersProgramiPage> {
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
        .get('/yonetici/ders-programi', params: params.isNotEmpty ? params : null)
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📚 Ders Programı')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final gunler = (d['gunler'] as List?) ?? [];
          final siniflar = List<String>.from((d['siniflar'] as List?) ?? []);

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              DropdownButtonFormField<String?>(
                value: _sinifFiltre,
                decoration: const InputDecoration(labelText: 'Sınıf Filtre', isDense: true, border: OutlineInputBorder()),
                items: [
                  const DropdownMenuItem(value: null, child: Text('Tüm Sınıflar')),
                  ...siniflar.map((s) => DropdownMenuItem(value: s, child: Text(s))),
                ],
                onChanged: (v) { setState(() => _sinifFiltre = v); _load(); },
              ),
              const SizedBox(height: 16),
              ...gunler.map((g) {
                final gg = g as Map;
                final dersler = (gg['dersler'] as List?) ?? [];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ExpansionTile(
                    leading: Container(
                      width: 40, height: 40,
                      decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                      child: Center(child: Text('${gg['ders_sayisi']}', style: const TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold))),
                    ),
                    title: Text(gg['gun'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text('${gg['ders_sayisi']} ders', style: const TextStyle(fontSize: 12)),
                    children: [
                      Padding(padding: const EdgeInsets.all(12), child: Column(
                        children: dersler.map((dd) {
                          final d = dd as Map;
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 3),
                            child: Row(children: [
                              Container(
                                width: 30, height: 30,
                                decoration: BoxDecoration(color: AppColors.info.withOpacity(0.15), shape: BoxShape.circle),
                                child: Center(child: Text('${d['saat']}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: AppColors.info))),
                              ),
                              const SizedBox(width: 10),
                              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                                Text('${d['ders']}', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                                Text('${d['sinif']} · ${d['ogretmen']}', style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
                              ])),
                            ]),
                          );
                        }).toList(),
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
