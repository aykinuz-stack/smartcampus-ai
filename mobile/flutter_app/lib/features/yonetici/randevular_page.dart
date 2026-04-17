import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class YoneticiRandevularPage extends ConsumerStatefulWidget {
  const YoneticiRandevularPage({super.key});

  @override
  ConsumerState<YoneticiRandevularPage> createState() =>
      _YoneticiRandevularPageState();
}

class _YoneticiRandevularPageState extends ConsumerState<YoneticiRandevularPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
    _load();
  }

  void _load() {
    setState(() => _future = _fetch());
  }

  Future<Map<String, dynamic>> _fetch() async {
    final r = await ref.read(apiClientProvider).get('/yonetici/randevular');
    return Map<String, dynamic>.from(r.data);
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📅 Randevular'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(text: 'Bugün'),
            Tab(text: 'Yaklaşan'),
            Tab(text: 'Bekleyen'),
          ],
        ),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final d = snap.data ?? {};
          final bugun = (d['bugun'] as List?) ?? [];
          final yaklasilan = (d['yaklasilan'] as List?) ?? [];
          final bekleyen = (d['bekleyen'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: TabBarView(
              controller: _tabCtrl,
              children: [
                _RList(list: bugun, bos: 'Bugün randevu yok'),
                _RList(list: yaklasilan, bos: 'Yaklaşan randevu yok'),
                _RList(list: bekleyen, bos: 'Bekleyen talep yok'),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _RList extends StatelessWidget {
  final List list;
  final String bos;
  const _RList({required this.list, required this.bos});

  @override
  Widget build(BuildContext context) {
    if (list.isEmpty) {
      return Center(child: Text(bos));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: list.length,
      itemBuilder: (_, i) {
        final r = list[i] as Map;
        final durum = (r['durum'] as String? ?? '').toLowerCase();
        Color c;
        switch (durum) {
          case 'beklemede':
            c = AppColors.warning;
            break;
          case 'onaylandi':
            c = AppColors.success;
            break;
          case 'iptal':
            c = AppColors.danger;
            break;
          default:
            c = AppColors.info;
        }

        return Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: Container(
              width: 58,
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: c.withOpacity(0.15),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(r['tarih']?.toString().substring(5) ?? '',
                      style: TextStyle(
                          color: c,
                          fontSize: 10,
                          fontWeight: FontWeight.bold)),
                  Text(r['saat'] ?? '',
                      style: TextStyle(
                          color: c,
                          fontWeight: FontWeight.bold,
                          fontSize: 13)),
                ],
              ),
            ),
            title: Text(r['konu'] ?? '',
                style: const TextStyle(
                    fontWeight: FontWeight.w600, fontSize: 14)),
            subtitle: Text(
              '${r['veli']} ↔ ${r['ogretmen']}',
              style: const TextStyle(fontSize: 12),
            ),
            trailing: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: c.withOpacity(0.15),
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(durum.toUpperCase(),
                  style: TextStyle(
                      color: c, fontSize: 10, fontWeight: FontWeight.bold)),
            ),
          ),
        );
      },
    );
  }
}
