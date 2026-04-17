import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class DuyuruYemekPage extends ConsumerStatefulWidget {
  const DuyuruYemekPage({super.key});
  @override
  ConsumerState<DuyuruYemekPage> createState() => _DuyuruYemekPageState();
}

class _DuyuruYemekPageState extends ConsumerState<DuyuruYemekPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<List<dynamic>>? _duyuruFuture;
  Future<List<dynamic>>? _yemekFuture;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  void _load() {
    final api = ref.read(apiClientProvider);
    setState(() {
      _duyuruFuture = api.get('/kurum/duyurular').then((r) => r.data as List);
      _yemekFuture = api.get('/kurum/yemek-menusu').then((r) => r.data as List);
    });
  }

  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📢 Duyuru & Yemek'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(icon: Icon(Icons.campaign, size: 18), text: 'Duyurular'),
          Tab(icon: Icon(Icons.restaurant, size: 18), text: 'Yemek'),
        ]),
      ),
      body: TabBarView(controller: _tabCtrl, children: [
        // DUYURULAR
        FutureBuilder<List<dynamic>>(
          future: _duyuruFuture,
          builder: (_, snap) {
            if (snap.connectionState == ConnectionState.waiting)
              return const Center(child: CircularProgressIndicator());
            final duyurular = snap.data ?? [];
            if (duyurular.isEmpty)
              return const Center(child: Text('Duyuru yok'));
            return RefreshIndicator(
              onRefresh: () async => _load(),
              child: ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: duyurular.length,
                itemBuilder: (_, i) {
                  final d = duyurular[i] as Map;
                  final tur = (d['tur'] ?? '').toString();
                  Color c;
                  IconData ic;
                  switch (tur.toLowerCase()) {
                    case 'acil': c = AppColors.danger; ic = Icons.warning; break;
                    case 'onemli': c = AppColors.warning; ic = Icons.priority_high; break;
                    case 'etkinlik': c = AppColors.success; ic = Icons.event; break;
                    default: c = AppColors.info; ic = Icons.campaign;
                  }
                  return Card(
                    margin: const EdgeInsets.only(bottom: 10),
                    child: ListTile(
                      leading: Container(
                        width: 40, height: 40,
                        decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                        child: Icon(ic, color: c, size: 20),
                      ),
                      title: Text(d['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                      subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        if ((d['aciklama'] as String? ?? '').isNotEmpty)
                          Text(d['aciklama'], maxLines: 2, overflow: TextOverflow.ellipsis,
                              style: const TextStyle(fontSize: 12)),
                        const SizedBox(height: 4),
                        Row(children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                            decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                            child: Text(tur.isNotEmpty ? tur : 'Genel',
                                style: TextStyle(fontSize: 9, color: c, fontWeight: FontWeight.bold)),
                          ),
                          const SizedBox(width: 8),
                          Text(d['tarih'] ?? '', style: const TextStyle(fontSize: 10, color: AppColors.textSecondaryDark)),
                        ]),
                      ]),
                      isThreeLine: true,
                    ),
                  );
                },
              ),
            );
          },
        ),

        // YEMEK MENUSU
        FutureBuilder<List<dynamic>>(
          future: _yemekFuture,
          builder: (_, snap) {
            if (snap.connectionState == ConnectionState.waiting)
              return const Center(child: CircularProgressIndicator());
            final menuler = snap.data ?? [];
            if (menuler.isEmpty)
              return const Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                Icon(Icons.restaurant, size: 48, color: Colors.grey),
                SizedBox(height: 12),
                Text('Yemek menüsü henüz girilmemiş'),
              ]));
            return RefreshIndicator(
              onRefresh: () async => _load(),
              child: ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: menuler.length,
                itemBuilder: (_, i) {
                  final m = menuler[i] as Map;
                  return Card(
                    margin: const EdgeInsets.only(bottom: 8),
                    child: Padding(
                      padding: const EdgeInsets.all(14),
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Row(children: [
                          const Icon(Icons.restaurant_menu, color: AppColors.gold, size: 20),
                          const SizedBox(width: 8),
                          Text(m['gun'] ?? m['tarih'] ?? '',
                              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                        ]),
                        const SizedBox(height: 8),
                        if (m['corba'] != null)
                          _YemekSatir(ikon: '🍜', ad: 'Çorba', deger: m['corba']),
                        if (m['ana_yemek'] != null)
                          _YemekSatir(ikon: '🍽️', ad: 'Ana', deger: m['ana_yemek']),
                        if (m['yan_yemek'] != null || m['garnitur'] != null)
                          _YemekSatir(ikon: '🥗', ad: 'Yan', deger: m['yan_yemek'] ?? m['garnitur'] ?? ''),
                        if (m['tatli'] != null || m['meyve'] != null)
                          _YemekSatir(ikon: '🍰', ad: 'Tatlı', deger: m['tatli'] ?? m['meyve'] ?? ''),
                        if (m['icecek'] != null)
                          _YemekSatir(ikon: '🥤', ad: 'İçecek', deger: m['icecek']),
                      ]),
                    ),
                  );
                },
              ),
            );
          },
        ),
      ]),
    );
  }
}


class _YemekSatir extends StatelessWidget {
  final String ikon; final String ad; final String deger;
  const _YemekSatir({required this.ikon, required this.ad, required this.deger});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(children: [
        Text(ikon, style: const TextStyle(fontSize: 16)),
        const SizedBox(width: 8),
        SizedBox(width: 40, child: Text(ad, style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark))),
        Expanded(child: Text(deger, style: const TextStyle(fontSize: 13))),
      ]),
    );
  }
}
