import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class DestekHizmetleriPage extends ConsumerStatefulWidget {
  const DestekHizmetleriPage({super.key});
  @override
  ConsumerState<DestekHizmetleriPage> createState() => _DestekHizmetleriPageState();
}

class _DestekHizmetleriPageState extends ConsumerState<DestekHizmetleriPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/destek-hizmetleri').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🔧 Destek Hizmetleri')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final ozet = d['ozet'] as Map? ?? {};
          final durumDag = Map<String, dynamic>.from(d['durum_dagilimi'] as Map? ?? {});
          final oncelikDag = Map<String, dynamic>.from(d['oncelik_dagilimi'] as Map? ?? {});
          final acikTicketlar = (d['acik_ticketlar'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // KPI
              Row(children: [
                _KPI(val: '${ozet['acik'] ?? 0}', label: 'Açık', color: AppColors.warning, icon: Icons.pending_actions),
                const SizedBox(width: 8),
                _KPI(val: '${ozet['toplam_ticket'] ?? 0}', label: 'Toplam', color: AppColors.primary, icon: Icons.confirmation_number),
                const SizedBox(width: 8),
                _KPI(val: '${ozet['bugun_acilan'] ?? 0}', label: 'Bugün', color: AppColors.info, icon: Icons.today),
              ]),
              const SizedBox(height: 8),
              Row(children: [
                _KPI(val: '${ozet['periyodik_gorev'] ?? 0}', label: 'Periyodik', color: AppColors.success, icon: Icons.repeat),
                const SizedBox(width: 8),
                _KPI(val: '${ozet['bakim_kaydi'] ?? 0}', label: 'Bakım', color: AppColors.gold, icon: Icons.build),
                const SizedBox(width: 8),
                const Expanded(child: SizedBox()),
              ]),
              const SizedBox(height: 16),

              // Durum dagilimi
              if (durumDag.isNotEmpty) ...[
                const Text('Durum Dağılımı', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                Wrap(spacing: 6, runSpacing: 6, children: durumDag.entries.map((e) {
                  Color c;
                  switch (e.key.toLowerCase()) {
                    case 'acik': case 'yeni': c = AppColors.warning; break;
                    case 'devam': case 'islemde': c = AppColors.info; break;
                    case 'tamamlandi': case 'kapandi': c = AppColors.success; break;
                    default: c = Colors.grey;
                  }
                  return Chip(
                    avatar: CircleAvatar(backgroundColor: c, radius: 8,
                        child: Text('${e.value}', style: const TextStyle(color: Colors.white, fontSize: 8))),
                    label: Text(e.key, style: const TextStyle(fontSize: 11)),
                    backgroundColor: c.withOpacity(0.1),
                  );
                }).toList()),
                const SizedBox(height: 12),
              ],

              // Oncelik
              if (oncelikDag.isNotEmpty) ...[
                const Text('Öncelik Dağılımı', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                Wrap(spacing: 6, runSpacing: 6, children: oncelikDag.entries.map((e) {
                  Color c;
                  switch (e.key.toLowerCase()) {
                    case 'kritik': c = AppColors.danger; break;
                    case 'yuksek': c = AppColors.warning; break;
                    case 'normal': c = AppColors.info; break;
                    case 'dusuk': c = AppColors.success; break;
                    default: c = Colors.grey;
                  }
                  return Chip(
                    avatar: CircleAvatar(backgroundColor: c, radius: 8,
                        child: Text('${e.value}', style: const TextStyle(color: Colors.white, fontSize: 8))),
                    label: Text(e.key, style: const TextStyle(fontSize: 11)),
                    backgroundColor: c.withOpacity(0.1),
                  );
                }).toList()),
                const SizedBox(height: 16),
              ],

              // Acik ticketlar
              Row(children: [
                const Text('Açık Talepler', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(color: AppColors.warning.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                  child: Text('${acikTicketlar.length}', style: const TextStyle(color: AppColors.warning, fontWeight: FontWeight.bold)),
                ),
              ]),
              const SizedBox(height: 8),

              if (acikTicketlar.isEmpty)
                const Padding(padding: EdgeInsets.all(24), child: Center(child: Text('Açık talep yok ✓')))
              else
                ...acikTicketlar.map((t) {
                  final tt = t as Map;
                  final oncelik = (tt['oncelik'] ?? 'Normal').toString();
                  Color oc;
                  switch (oncelik.toLowerCase()) {
                    case 'kritik': oc = AppColors.danger; break;
                    case 'yuksek': oc = AppColors.warning; break;
                    default: oc = AppColors.info;
                  }
                  return Card(
                    margin: const EdgeInsets.only(bottom: 8),
                    child: ListTile(
                      leading: Container(
                        width: 4, height: 50,
                        decoration: BoxDecoration(color: oc, borderRadius: BorderRadius.circular(2)),
                      ),
                      title: Text(tt['baslik'] ?? tt['ticket_no'] ?? '',
                          style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                      subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text('${tt['kategori']} · ${tt['tarih']}', style: const TextStyle(fontSize: 11)),
                        Row(children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                            decoration: BoxDecoration(color: oc.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                            child: Text(oncelik, style: TextStyle(fontSize: 9, color: oc, fontWeight: FontWeight.bold)),
                          ),
                          const SizedBox(width: 6),
                          Text(tt['durum'] ?? '', style: const TextStyle(fontSize: 10, color: AppColors.textSecondaryDark)),
                          const Spacer(),
                          Text(tt['talep_eden'] ?? '', style: const TextStyle(fontSize: 10)),
                        ]),
                      ]),
                      isThreeLine: true,
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
        Icon(icon, color: color, size: 18),
        const SizedBox(height: 4),
        Text(val, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 9)),
      ]),
    ));
  }
}
