import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Kazanim Borclarim — dusuk puanli dersler + telafi durumu
class KazanimBorclariPage extends ConsumerStatefulWidget {
  const KazanimBorclariPage({super.key});

  @override
  ConsumerState<KazanimBorclariPage> createState() => _KazanimBorclariPageState();
}

class _KazanimBorclariPageState extends ConsumerState<KazanimBorclariPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() {
      _future = ref.read(apiClientProvider)
          .get('/ogrenci/kazanim-borclari')
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kazanim Borclarim')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final data = snap.data ?? {};
          final borclar = (data['borclar'] as List?) ?? [];
          final kritik = (data['kritik'] as int?) ?? 0;
          final uyari = (data['uyari'] as int?) ?? 0;

          if (borclar.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.check_circle, size: 64, color: AppColors.success),
                  SizedBox(height: 12),
                  Text('Tebrikler! Kazanim borcun yok',
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                  SizedBox(height: 4),
                  Text('Tum derslerde 70 ustu ortalama',
                      style: TextStyle(fontSize: 13, color: AppColors.textSecondaryDark)),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Ozet
                Row(
                  children: [
                    _OzetKutu(
                      label: 'Kritik',
                      value: '$kritik',
                      color: AppColors.danger,
                      icon: Icons.error,
                    ),
                    const SizedBox(width: 10),
                    _OzetKutu(
                      label: 'Uyari',
                      value: '$uyari',
                      color: AppColors.warning,
                      icon: Icons.warning_amber,
                    ),
                    const SizedBox(width: 10),
                    _OzetKutu(
                      label: 'Toplam',
                      value: '${borclar.length}',
                      color: AppColors.info,
                      icon: Icons.assignment_late,
                    ),
                  ],
                ),
                const SizedBox(height: 20),

                // Aciklama
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.info.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: AppColors.info.withOpacity(0.2)),
                  ),
                  child: const Row(
                    children: [
                      Icon(Icons.info_outline, size: 18, color: AppColors.info),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          '70 altindaki dersler burada listelenir. Telafi gorevleriyle puan yukseltebilirsin.',
                          style: TextStyle(fontSize: 12, color: AppColors.info),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                // Borc listesi
                ...borclar.map((b) {
                  final m = Map<String, dynamic>.from(b as Map);
                  return _BorcKart(borc: m, onTelafi: () => context.push('/ogrenci/telafi'));
                }),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _OzetKutu extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  final IconData icon;
  const _OzetKutu({required this.label, required this.value,
                   required this.color, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 6),
            Text(value, style: TextStyle(fontSize: 22,
                fontWeight: FontWeight.bold, color: color)),
            Text(label, style: const TextStyle(fontSize: 11)),
          ],
        ),
      ),
    );
  }
}


class _BorcKart extends StatelessWidget {
  final Map<String, dynamic> borc;
  final VoidCallback onTelafi;
  const _BorcKart({required this.borc, required this.onTelafi});

  @override
  Widget build(BuildContext context) {
    final ders = borc['ders'] as String? ?? '';
    final puan = (borc['puan'] as num?)?.toDouble() ?? 0;
    final notTuru = borc['not_turu'] as String? ?? '';
    final renk = borc['renk'] as String? ?? 'YELLOW';
    final telafiVar = borc['telafi_var'] as bool? ?? false;

    Color c = renk == 'RED' ? AppColors.danger : AppColors.warning;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(color: c, width: 4)),
        ),
        padding: const EdgeInsets.all(14),
        child: Row(
          children: [
            // Puan
            Container(
              width: 48, height: 48,
              decoration: BoxDecoration(
                color: c.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
              ),
              alignment: Alignment.center,
              child: Text(puan.toStringAsFixed(0),
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: c)),
            ),
            const SizedBox(width: 12),
            // Bilgi
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(ders, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                  Text(notTuru, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                  if (telafiVar)
                    Container(
                      margin: const EdgeInsets.only(top: 4),
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.success.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: const Text('Telafi atandi',
                          style: TextStyle(fontSize: 10, color: AppColors.success,
                              fontWeight: FontWeight.bold)),
                    ),
                ],
              ),
            ),
            // Telafi butonu
            if (!telafiVar)
              TextButton.icon(
                onPressed: onTelafi,
                icon: Icon(Icons.replay, size: 16, color: c),
                label: Text('Telafi', style: TextStyle(fontSize: 12, color: c)),
              ),
          ],
        ),
      ),
    );
  }
}
