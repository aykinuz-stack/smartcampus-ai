import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class TuketimDemirbasPage extends ConsumerStatefulWidget {
  const TuketimDemirbasPage({super.key});
  @override
  ConsumerState<TuketimDemirbasPage> createState() => _TuketimDemirbasPageState();
}

class _TuketimDemirbasPageState extends ConsumerState<TuketimDemirbasPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/tuketim-demirbas').then((r) => Map<String, dynamic>.from(r.data)));
  }

  String _para(num val) => NumberFormat('#,##0', 'tr_TR').format(val);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🗄️ Tüketim & Demirbaş')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final ozet = d['ozet'] as Map? ?? {};
          final uyarilar = (d['min_stok_uyari'] as List?) ?? [];
          final hareketler = (d['bugun_hareketler'] as List?) ?? [];
          final katDag = Map<String, dynamic>.from(d['kategori_dagilimi'] as Map? ?? {});
          final urunler = (d['urun_listesi'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // 6 KPI
              GridView.count(
                shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 3, crossAxisSpacing: 8, mainAxisSpacing: 8, childAspectRatio: 1.2,
                children: [
                  _KPI(val: '${ozet['toplam_urun'] ?? 0}', label: 'Ürün', color: AppColors.primary, icon: Icons.inventory),
                  _KPI(val: '${ozet['toplam_demirbas'] ?? 0}', label: 'Demirbaş', color: AppColors.info, icon: Icons.devices),
                  _KPI(val: '${ozet['aktif_zimmet'] ?? 0}', label: 'Zimmet', color: AppColors.gold, icon: Icons.assignment_ind),
                  _KPI(val: '${ozet['min_stok_uyari'] ?? 0}', label: 'Stok Uyarı', color: AppColors.danger, icon: Icons.warning),
                  _KPI(val: '${ozet['bugun_hareket'] ?? 0}', label: 'Bugün', color: AppColors.success, icon: Icons.swap_horiz),
                  _KPI(val: '${_para(ozet['toplam_deger'] ?? 0)}₺', label: 'Değer', color: AppColors.primary, icon: Icons.attach_money, small: true),
                ],
              ),
              const SizedBox(height: 16),

              // Kategori chips
              if (katDag.isNotEmpty) ...[
                const Text('Kategori Dağılımı', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                Wrap(spacing: 6, runSpacing: 6, children: katDag.entries.map((e) =>
                    Chip(label: Text('${e.key}: ${e.value}', style: const TextStyle(fontSize: 10)),
                        backgroundColor: AppColors.info.withOpacity(0.1))).toList()),
                const SizedBox(height: 16),
              ],

              // Min stok uyari
              if (uyarilar.isNotEmpty) ...[
                Row(children: [
                  const Icon(Icons.warning_amber, color: AppColors.danger, size: 20),
                  const SizedBox(width: 6),
                  Text('Minimum Stok Uyarısı (${uyarilar.length})',
                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: AppColors.danger)),
                ]),
                const SizedBox(height: 8),
                ...uyarilar.map((u) {
                  final uu = u as Map;
                  return Card(
                    color: AppColors.danger.withOpacity(0.05),
                    margin: const EdgeInsets.only(bottom: 6),
                    child: ListTile(
                      dense: true,
                      leading: const Icon(Icons.inventory_2, color: AppColors.danger, size: 20),
                      title: Text(uu['urun'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                      subtitle: Text('${uu['kategori']}', style: const TextStyle(fontSize: 11)),
                      trailing: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text('${uu['stok']}', style: const TextStyle(color: AppColors.danger, fontWeight: FontWeight.bold, fontSize: 16)),
                        Text('min: ${uu['min_stok']}', style: const TextStyle(fontSize: 9, color: AppColors.textSecondaryDark)),
                      ]),
                    ),
                  );
                }),
                const SizedBox(height: 16),
              ],

              // Bugun hareketler
              if (hareketler.isNotEmpty) ...[
                const Text('Bugünkü Hareketler', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                ...hareketler.map((h) {
                  final hh = h as Map;
                  final giris = (hh['tur'] ?? '').toString().toLowerCase().contains('giris');
                  return ListTile(
                    dense: true, contentPadding: EdgeInsets.zero,
                    leading: Icon(giris ? Icons.add_circle : Icons.remove_circle,
                        color: giris ? AppColors.success : AppColors.warning, size: 20),
                    title: Text(hh['urun'] ?? '', style: const TextStyle(fontSize: 13)),
                    subtitle: Text('${hh['yapan']} · ${hh['tur']}', style: const TextStyle(fontSize: 11)),
                    trailing: Text('${hh['miktar']}', style: TextStyle(
                        color: giris ? AppColors.success : AppColors.warning, fontWeight: FontWeight.bold)),
                  );
                }),
                const SizedBox(height: 16),
              ],

              // Urun listesi
              if (urunler.isNotEmpty) ...[
                const Text('Stok Durumu', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                const SizedBox(height: 8),
                ...urunler.map((u) {
                  final uu = u as Map;
                  final stok = (uu['stok'] as num?)?.toInt() ?? 0;
                  final min = (uu['min_stok'] as num?)?.toInt() ?? 0;
                  final kritik = stok <= min;
                  return Card(
                    margin: const EdgeInsets.only(bottom: 4),
                    child: ListTile(
                      dense: true,
                      title: Text(uu['urun'] ?? '', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500)),
                      subtitle: Text('${uu['kategori']} · ${uu['birim']}', style: const TextStyle(fontSize: 10)),
                      trailing: Row(mainAxisSize: MainAxisSize.min, children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: (kritik ? AppColors.danger : AppColors.success).withOpacity(0.15),
                            borderRadius: BorderRadius.circular(6)),
                          child: Text('$stok', style: TextStyle(
                              color: kritik ? AppColors.danger : AppColors.success,
                              fontWeight: FontWeight.bold)),
                        ),
                      ]),
                    ),
                  );
                }),
              ],
            ]),
          );
        },
      ),
    );
  }
}


class _KPI extends StatelessWidget {
  final String val; final String label; final Color color; final IconData icon;
  final bool small;
  const _KPI({required this.val, required this.label, required this.color,
              required this.icon, this.small = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(height: 4),
        Text(val, style: TextStyle(fontSize: small ? 12 : 16, fontWeight: FontWeight.bold, color: color),
            textAlign: TextAlign.center),
        Text(label, style: const TextStyle(fontSize: 9)),
      ]),
    );
  }
}
