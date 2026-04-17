import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class GunRaporuPage extends ConsumerStatefulWidget {
  const GunRaporuPage({super.key});

  @override
  ConsumerState<GunRaporuPage> createState() => _GunRaporuPageState();
}

class _GunRaporuPageState extends ConsumerState<GunRaporuPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/gun-raporu')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📋 Gün Raporu'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(icon: Icon(Icons.wb_sunny, size: 18), text: 'Gün Başı'),
          Tab(icon: Icon(Icons.nights_stay, size: 18), text: 'Gün Sonu'),
        ]),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final d = snap.data ?? {};
          final gb = d['gun_basi'] as Map? ?? {};
          final gs = d['gun_sonu'] as Map? ?? {};

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: TabBarView(controller: _tabCtrl, children: [
              // GUN BASI
              ListView(padding: const EdgeInsets.all(16), children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(colors: [Color(0xFFFBBF24), Color(0xFFF59E0B)]),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('☀️ ${d['gun'] ?? ''}, ${d['tarih'] ?? ''}',
                        style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    const Text('Gün Başı Raporu', style: TextStyle(color: Colors.white70)),
                  ]),
                ),
                const SizedBox(height: 16),
                Row(children: [
                  _Stat(label: 'Öğrenci', val: '${gb['aktif_ogrenci'] ?? 0}', color: AppColors.primary, icon: Icons.people),
                  const SizedBox(width: 8),
                  _Stat(label: 'Öğretmen', val: '${gb['aktif_ogretmen'] ?? 0}', color: AppColors.info, icon: Icons.school),
                  const SizedBox(width: 8),
                  _Stat(label: 'Etkinlik', val: '${gb['bugun_etkinlik'] ?? 0}', color: AppColors.success, icon: Icons.event),
                  const SizedBox(width: 8),
                  _Stat(label: 'Randevu', val: '${gb['bugun_randevu'] ?? 0}', color: AppColors.gold, icon: Icons.calendar_today),
                ]),
                const SizedBox(height: 8),
                Row(children: [
                  _Stat(label: 'İhbar', val: '${gb['bekleyen_ihbar'] ?? 0}', color: AppColors.warning, icon: Icons.report),
                  const SizedBox(width: 8),
                  _Stat(label: 'Kritik Risk', val: '${gb['kritik_risk'] ?? 0}', color: AppColors.danger, icon: Icons.dangerous),
                  const SizedBox(width: 8),
                  const Expanded(child: SizedBox()),
                  const SizedBox(width: 8),
                  const Expanded(child: SizedBox()),
                ]),
                if ((gb['etkinlikler'] as List? ?? []).isNotEmpty) ...[
                  const SizedBox(height: 16),
                  const Text('🎉 Bugünkü Etkinlikler', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  ...(gb['etkinlikler'] as List).map((e) => ListTile(
                    dense: true, contentPadding: EdgeInsets.zero,
                    leading: const Icon(Icons.event, color: AppColors.success),
                    title: Text(e['baslik'] ?? '', style: const TextStyle(fontSize: 13)),
                    subtitle: Text(e['konum'] ?? '', style: const TextStyle(fontSize: 11)),
                  )),
                ],
                if ((gb['randevular'] as List? ?? []).isNotEmpty) ...[
                  const SizedBox(height: 16),
                  const Text('📅 Bugünkü Randevular', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  ...(gb['randevular'] as List).map((r) => ListTile(
                    dense: true, contentPadding: EdgeInsets.zero,
                    leading: Container(
                      padding: const EdgeInsets.all(6),
                      decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                      child: Text(r['saat'] ?? '', style: const TextStyle(color: AppColors.gold, fontWeight: FontWeight.bold, fontSize: 11)),
                    ),
                    title: Text(r['konu'] ?? '', style: const TextStyle(fontSize: 13)),
                    subtitle: Text('${r['veli']} ↔ ${r['ogretmen']}', style: const TextStyle(fontSize: 11)),
                  )),
                ],
              ]),

              // GUN SONU
              ListView(padding: const EdgeInsets.all(16), children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(colors: [Color(0xFF1E1B4B), Color(0xFF312E81)]),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('🌙 ${d['gun'] ?? ''}, ${d['tarih'] ?? ''}',
                        style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    const Text('Gün Sonu Raporu', style: TextStyle(color: Colors.white70)),
                  ]),
                ),
                const SizedBox(height: 16),
                Row(children: [
                  _Stat(label: 'Devamsız', val: '${gs['devamsiz'] ?? 0}', color: AppColors.danger, icon: Icons.close),
                  const SizedBox(width: 8),
                  _Stat(label: 'Geç Kalan', val: '${gs['gec'] ?? 0}', color: AppColors.warning, icon: Icons.access_time),
                  const SizedBox(width: 8),
                  _Stat(label: 'Yoklama', val: '${gs['yoklama_alinan'] ?? 0}', color: AppColors.success, icon: Icons.check),
                  const SizedBox(width: 8),
                  _Stat(label: 'Ödev', val: '${gs['verilen_odev'] ?? 0}', color: AppColors.info, icon: Icons.assignment),
                ]),
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(children: [
                    const Text('😊', style: TextStyle(fontSize: 32)),
                    const SizedBox(width: 12),
                    Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      const Text('Mood Ortalaması', style: TextStyle(fontWeight: FontWeight.bold)),
                      Text('${gs['mood_ortalama'] ?? 0} / 5.0 · ${gs['mood_katilim'] ?? 0} öğrenci',
                          style: const TextStyle(fontSize: 13)),
                    ])),
                  ]),
                ),
              ]),
            ]),
          );
        },
      ),
    );
  }
}


class _Stat extends StatelessWidget {
  final String label; final String val; final Color color; final IconData icon;
  const _Stat({required this.label, required this.val, required this.color, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
      child: Column(children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(height: 4),
        Text(val, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 9)),
      ]),
    ));
  }
}
