import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class ButcePage extends ConsumerStatefulWidget {
  const ButcePage({super.key});

  @override
  ConsumerState<ButcePage> createState() => _ButcePageState();
}

class _ButcePageState extends ConsumerState<ButcePage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetch());
  }

  Future<Map<String, dynamic>> _fetch() async {
    final r = await ref.read(apiClientProvider).get('/yonetici/butce-gunluk');
    return Map<String, dynamic>.from(r.data);
  }

  String _para(num val) {
    final f = NumberFormat('#,##0.00', 'tr_TR');
    return '${f.format(val)} ₺';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('💰 Bütçe — Günlük Akış')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final d = snap.data ?? {};
          final toplamGelir = (d['toplam_gelir'] as num?)?.toDouble() ?? 0.0;
          final toplamGider = (d['toplam_gider'] as num?)?.toDouble() ?? 0.0;
          final net = (d['net'] as num?)?.toDouble() ?? 0.0;
          final gunluk = (d['gunluk_akis'] as List?) ?? [];
          final islemler = (d['son_islemler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Toplam kartları
                Row(
                  children: [
                    Expanded(
                      child: _ToplamKart(
                        label: 'Gelir',
                        val: _para(toplamGelir),
                        color: AppColors.success,
                        icon: Icons.trending_up,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: _ToplamKart(
                        label: 'Gider',
                        val: _para(toplamGider),
                        color: AppColors.danger,
                        icon: Icons.trending_down,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                _ToplamKart(
                  label: net >= 0 ? 'Net Kar' : 'Net Zarar',
                  val: _para(net),
                  color: net >= 0 ? AppColors.primary : AppColors.warning,
                  icon: net >= 0 ? Icons.account_balance_wallet : Icons.warning,
                  big: true,
                ),

                const SizedBox(height: 20),
                if (gunluk.isNotEmpty) ...[
                  const Text('Günlük Akış (Son 30)',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  ...gunluk.take(10).map((g) {
                    final gg = g as Map;
                    final netG = (gg['net'] as num?)?.toDouble() ?? 0.0;
                    return Card(
                      margin: const EdgeInsets.only(bottom: 6),
                      child: ListTile(
                        dense: true,
                        leading: Container(
                          padding: const EdgeInsets.all(6),
                          decoration: BoxDecoration(
                            color: (netG >= 0
                                    ? AppColors.success
                                    : AppColors.danger)
                                .withOpacity(0.15),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(
                            netG >= 0
                                ? Icons.arrow_upward
                                : Icons.arrow_downward,
                            color: netG >= 0
                                ? AppColors.success
                                : AppColors.danger,
                            size: 16,
                          ),
                        ),
                        title: Text(gg['tarih'] ?? '',
                            style: const TextStyle(fontSize: 13)),
                        subtitle: Text(
                          'Gelir: ${_para(gg['gelir'] ?? 0)} · Gider: ${_para(gg['gider'] ?? 0)}',
                          style: const TextStyle(fontSize: 11),
                        ),
                        trailing: Text(
                          _para(netG),
                          style: TextStyle(
                            color: netG >= 0
                                ? AppColors.success
                                : AppColors.danger,
                            fontWeight: FontWeight.bold,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    );
                  }),
                ],

                const SizedBox(height: 16),
                if (islemler.isNotEmpty) ...[
                  const Text('Son İşlemler',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  ...islemler.take(15).map((i) {
                    final ii = i as Map;
                    final gelir = ii['tip'] == 'gelir';
                    return Card(
                      margin: const EdgeInsets.only(bottom: 4),
                      child: ListTile(
                        dense: true,
                        leading: Icon(
                          gelir ? Icons.add_circle : Icons.remove_circle,
                          color:
                              gelir ? AppColors.success : AppColors.danger,
                        ),
                        title: Text(
                          ii['aciklama']?.toString() ??
                              ii['kategori']?.toString() ??
                              '-',
                          style: const TextStyle(fontSize: 13),
                        ),
                        subtitle: Text(
                          '${ii['tarih']} · ${ii['kategori']}',
                          style: const TextStyle(fontSize: 11),
                        ),
                        trailing: Text(
                          _para(ii['tutar'] ?? 0),
                          style: TextStyle(
                            color: gelir
                                ? AppColors.success
                                : AppColors.danger,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    );
                  }),
                ],

                if (gunluk.isEmpty && islemler.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(32),
                    child: Center(
                      child: Column(
                        children: [
                          Icon(Icons.account_balance_wallet_outlined,
                              size: 48, color: Colors.grey),
                          SizedBox(height: 12),
                          Text('Bütçe verisi yok'),
                          SizedBox(height: 6),
                          Text(
                              'Bütçe modülüne veri girildikçe burada görünür',
                              style: TextStyle(
                                  fontSize: 12,
                                  color: AppColors.textSecondaryDark)),
                        ],
                      ),
                    ),
                  ),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _ToplamKart extends StatelessWidget {
  final String label;
  final String val;
  final Color color;
  final IconData icon;
  final bool big;
  const _ToplamKart({
    required this.label,
    required this.val,
    required this.color,
    required this.icon,
    this.big = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(big ? 18 : 14),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: big ? 24 : 18),
              const SizedBox(width: 6),
              Text(label,
                  style: TextStyle(
                      color: color,
                      fontWeight: FontWeight.bold,
                      fontSize: big ? 14 : 12)),
            ],
          ),
          const SizedBox(height: 6),
          Text(val,
              style: TextStyle(
                  fontSize: big ? 20 : 16,
                  fontWeight: FontWeight.bold,
                  color: color)),
        ],
      ),
    );
  }
}
