import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class NobetPage extends ConsumerStatefulWidget {
  const NobetPage({super.key});
  @override
  ConsumerState<NobetPage> createState() => _NobetPageState();
}

class _NobetPageState extends ConsumerState<NobetPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/nobet')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🛡️ Nöbet Yönetimi')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final bugun = d['bugun'] as Map? ?? {};
          final haftalik = (d['haftalik'] as List?) ?? [];
          final bugunNobetciler = (bugun['nobetciler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Bugun hero
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('📅 ${bugun['gun'] ?? ''} — Bugünkü Nöbet',
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                  const SizedBox(height: 12),
                  if (bugunNobetciler.isEmpty)
                    const Text('Bugün nöbetçi yok', style: TextStyle(color: Colors.white70))
                  else
                    ...bugunNobetciler.map((n) {
                      final nn = n as Map;
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 8),
                        child: Row(children: [
                          const Icon(Icons.shield, color: AppColors.gold, size: 20),
                          const SizedBox(width: 10),
                          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            Text(nn['ogretmen'] ?? '', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                            Text('${nn['yer']} · ${nn['saat']}', style: const TextStyle(color: Colors.white70, fontSize: 12)),
                          ])),
                        ]),
                      );
                    }),
                ]),
              ),

              const SizedBox(height: 20),
              const Text('Haftalık Nöbet Programı', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),

              ...haftalik.map((h) {
                final hh = h as Map;
                final nobetciler = (hh['nobetciler'] as List?) ?? [];
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ExpansionTile(
                    leading: Container(
                      width: 36, height: 36,
                      decoration: BoxDecoration(
                        color: nobetciler.isNotEmpty ? AppColors.success.withOpacity(0.15) : Colors.grey.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8)),
                      child: Center(child: Text('${nobetciler.length}',
                          style: TextStyle(color: nobetciler.isNotEmpty ? AppColors.success : Colors.grey, fontWeight: FontWeight.bold))),
                    ),
                    title: Text(hh['gun'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                    subtitle: Text('${nobetciler.length} nöbetçi', style: const TextStyle(fontSize: 11)),
                    children: [
                      if (nobetciler.isEmpty)
                        const Padding(padding: EdgeInsets.all(12), child: Text('Nöbetçi atanmamış'))
                      else
                        Padding(padding: const EdgeInsets.all(12), child: Column(
                          children: nobetciler.map((n) {
                            final nn = n as Map;
                            final durum = nn['durum'] ?? 'bekliyor';
                            Color dc = durum == 'tamamlandi' ? AppColors.success : durum == 'gelmedi' ? AppColors.danger : AppColors.warning;
                            return ListTile(
                              dense: true, contentPadding: EdgeInsets.zero,
                              leading: Icon(Icons.person, color: dc),
                              title: Text(nn['ogretmen'] ?? '', style: const TextStyle(fontSize: 13)),
                              subtitle: Text('${nn['yer']} · ${nn['saat']}', style: const TextStyle(fontSize: 11)),
                              trailing: Container(
                                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                decoration: BoxDecoration(color: dc.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                                child: Text(durum, style: TextStyle(fontSize: 9, color: dc, fontWeight: FontWeight.bold)),
                              ),
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
