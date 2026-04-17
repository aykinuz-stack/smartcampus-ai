import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class RevirPage extends ConsumerStatefulWidget {
  const RevirPage({super.key});
  @override
  ConsumerState<RevirPage> createState() => _RevirPageState();
}

class _RevirPageState extends ConsumerState<RevirPage> {
  Future<Map<String, dynamic>>? _future;
  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/saglik/revir-ozet').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🏥 Revir / Okul Sağlığı')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final nedenDag = Map<String, dynamic>.from(d['neden_dagilimi'] as Map? ?? {});
          final ziyaretler = (d['son_ziyaretler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              Row(children: [
                _KPI(val: '${d['toplam'] ?? 0}', label: 'Toplam', color: AppColors.primary, icon: Icons.local_hospital),
                const SizedBox(width: 8),
                _KPI(val: '${d['bugun'] ?? 0}', label: 'Bugün', color: AppColors.info, icon: Icons.today),
                const SizedBox(width: 8),
                _KPI(val: '${d['supheli'] ?? 0}', label: 'Şüpheli', color: AppColors.danger, icon: Icons.warning),
              ]),
              const SizedBox(height: 16),
              if (nedenDag.isNotEmpty) ...[
                const Text('Neden Dağılımı', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                Wrap(spacing: 6, runSpacing: 6, children: nedenDag.entries.map((e) =>
                    Chip(label: Text('${e.key}: ${e.value}', style: const TextStyle(fontSize: 10)),
                        backgroundColor: AppColors.info.withOpacity(0.1))).toList()),
                const SizedBox(height: 16),
              ],
              const Text('Son Ziyaretler', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
              const SizedBox(height: 8),
              ...ziyaretler.map((z) {
                final zz = z as Map;
                final supheli = zz['supheli'] == true;
                return Card(
                  color: supheli ? AppColors.danger.withOpacity(0.05) : null,
                  margin: const EdgeInsets.only(bottom: 6),
                  child: ListTile(
                    dense: true,
                    leading: Icon(supheli ? Icons.warning : Icons.medical_services,
                        color: supheli ? AppColors.danger : AppColors.info, size: 20),
                    title: Text(zz['ogrenci'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                    subtitle: Text('${zz['neden']} · ${zz['tarih']}', style: const TextStyle(fontSize: 11)),
                    trailing: supheli ? const Text('⚠️', style: TextStyle(fontSize: 16)) : null,
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
