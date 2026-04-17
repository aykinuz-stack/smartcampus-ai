import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class SosyalEtkinlikPage extends ConsumerStatefulWidget {
  const SosyalEtkinlikPage({super.key});
  @override
  ConsumerState<SosyalEtkinlikPage> createState() => _SosyalEtkinlikPageState();
}

class _SosyalEtkinlikPageState extends ConsumerState<SosyalEtkinlikPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _tabCtrl = TabController(length: 2, vsync: this); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/sosyal/ozet').then((r) => Map<String, dynamic>.from(r.data)));
  }
  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🎭 Sosyal Etkinlik & Kulüpler'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(text: 'Kulüpler'), Tab(text: 'Etkinlikler'),
        ]),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final kulupler = (d['kulupler'] as List?) ?? [];
          final etkinlikler = (d['yaklasan_etkinlikler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: TabBarView(controller: _tabCtrl, children: [
              // KULUPLER
              ListView(padding: const EdgeInsets.all(16), children: [
                Row(children: [
                  _Mini(val: '${d['toplam_kulup'] ?? 0}', label: 'Kulüp', color: AppColors.primary),
                  const SizedBox(width: 8),
                  _Mini(val: '${d['toplam_etkinlik'] ?? 0}', label: 'Etkinlik', color: AppColors.success),
                  const SizedBox(width: 8),
                  _Mini(val: '${d['yaklasan'] ?? 0}', label: 'Yaklaşan', color: AppColors.gold),
                ]),
                const SizedBox(height: 16),
                if (kulupler.isEmpty)
                  const Center(child: Text('Kulüp verisi yok'))
                else
                  ...kulupler.map((k) {
                    final kk = k as Map;
                    final aktif = (kk['durum'] ?? '').toString().toUpperCase() == 'AKTIF';
                    return Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(
                      leading: Container(
                        width: 44, height: 44,
                        decoration: BoxDecoration(
                          color: (aktif ? AppColors.success : Colors.grey).withOpacity(0.15),
                          borderRadius: BorderRadius.circular(10)),
                        child: Center(child: Text('${kk['uye'] ?? 0}',
                            style: TextStyle(color: aktif ? AppColors.success : Colors.grey,
                                fontWeight: FontWeight.bold))),
                      ),
                      title: Text(kk['ad'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                      subtitle: Text('${kk['kademe']} · ${kk['gun']}',
                          style: const TextStyle(fontSize: 11)),
                      trailing: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: (aktif ? AppColors.success : Colors.grey).withOpacity(0.15),
                          borderRadius: BorderRadius.circular(4)),
                        child: Text(aktif ? 'AKTİF' : 'PASİF',
                            style: TextStyle(fontSize: 9, color: aktif ? AppColors.success : Colors.grey,
                                fontWeight: FontWeight.bold)),
                      ),
                    ));
                  }),
              ]),

              // ETKINLIKLER
              ListView(padding: const EdgeInsets.all(16), children: [
                if (etkinlikler.isEmpty)
                  const Padding(padding: EdgeInsets.all(32),
                      child: Center(child: Text('Yaklaşan etkinlik yok')))
                else
                  ...etkinlikler.map((e) {
                    final ee = e as Map;
                    return Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(
                      leading: Container(
                        width: 44, height: 44,
                        decoration: BoxDecoration(
                          color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                        child: const Icon(Icons.event, color: AppColors.gold, size: 20),
                      ),
                      title: Text(ee['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                      subtitle: Text('${ee['tarih'] ?? ''} · ${ee['konum'] ?? ''} · ${ee['kategori'] ?? ''}',
                          style: const TextStyle(fontSize: 11)),
                    ));
                  }),
              ]),
            ]),
          );
        },
      ),
    );
  }
}

class _Mini extends StatelessWidget {
  final String val; final String label; final Color color;
  const _Mini({required this.val, required this.label, required this.color});
  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
      child: Column(children: [
        Text(val, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 9)),
      ]),
    ));
  }
}
