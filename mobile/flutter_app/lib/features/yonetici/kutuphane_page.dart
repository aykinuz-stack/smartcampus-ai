import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class KutuphanePage extends ConsumerStatefulWidget {
  const KutuphanePage({super.key});
  @override
  ConsumerState<KutuphanePage> createState() => _KutuphanePageState();
}

class _KutuphanePageState extends ConsumerState<KutuphanePage> {
  Future<Map<String, dynamic>>? _future;
  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/kutuphane/ozet').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📖 Kütüphane')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final oduncler = (d['son_odunc'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              Row(children: [
                _KPI(val: '${d['toplam_kitap'] ?? 0}', label: 'Kitap', color: AppColors.primary, icon: Icons.menu_book),
                const SizedBox(width: 8),
                _KPI(val: '${d['aktif_odunc'] ?? 0}', label: 'Ödünç', color: AppColors.info, icon: Icons.swap_horiz),
                const SizedBox(width: 8),
                _KPI(val: '${d['geciken'] ?? 0}', label: 'Geciken', color: AppColors.danger, icon: Icons.access_time),
              ]),
              const SizedBox(height: 16),
              const Text('Son Ödünç İşlemleri', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
              const SizedBox(height: 8),
              if (oduncler.isEmpty)
                const Padding(padding: EdgeInsets.all(24), child: Center(child: Text('Ödünç kaydı yok')))
              else
                ...oduncler.map((o) {
                  final oo = o as Map;
                  final durum = (oo['durum'] ?? '').toString();
                  Color c = durum == 'gecikti' ? AppColors.danger : durum == 'iade' ? AppColors.success : AppColors.info;
                  return Card(margin: const EdgeInsets.only(bottom: 6), child: ListTile(
                    dense: true,
                    leading: Icon(Icons.book, color: c, size: 20),
                    title: Text(oo['kitap'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                    subtitle: Text('${oo['ogrenci']} · ${oo['tarih']}', style: const TextStyle(fontSize: 11)),
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                      child: Text(durum, style: TextStyle(fontSize: 9, color: c, fontWeight: FontWeight.bold)),
                    ),
                  ));
                }),
            ]),
          );
        },
      ),
    );
  }
}

class _KPI extends StatelessWidget {
  final String val; final String label; final Color color; final IconData icon;
  const _KPI({required this.val, required this.label, required this.color, required this.icon});
  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
      child: Column(children: [
        Icon(icon, color: color, size: 18), const SizedBox(height: 4),
        Text(val, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 9)),
      ]),
    ));
  }
}
