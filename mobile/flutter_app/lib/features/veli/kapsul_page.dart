import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/veli_api.dart';
import '../../core/theme/app_theme.dart';


class KapsulPage extends ConsumerStatefulWidget {
  const KapsulPage({super.key});

  @override
  ConsumerState<KapsulPage> createState() => _KapsulPageState();
}

class _KapsulPageState extends ConsumerState<KapsulPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(veliApiProvider).getKapsuller());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📦 Günlük Kapsül')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
          final data = snap.data ?? {};
          final bugunku = data['bugunku'] as Map?;
          final kapsuller = (data['kapsuller'] as List?) ?? [];

          if (kapsuller.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.auto_awesome, size: 64, color: AppColors.primary),
                  SizedBox(height: 12),
                  Text('Henüz günlük kapsül yok', style: TextStyle(fontSize: 16)),
                  SizedBox(height: 4),
                  Padding(
                    padding: EdgeInsets.symmetric(horizontal: 32),
                    child: Text(
                      'Her akşam 18:00\'de AI tarafından hazırlanan gün özeti burada gözükecek.',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 13, color: AppColors.textSecondaryDark),
                    ),
                  ),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                if (bugunku != null) ...[
                  const Text('Bugün',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),
                  _KapsulKart(k: Map<String, dynamic>.from(bugunku), bugun: true),
                  const SizedBox(height: 20),
                ],
                const Text('Geçmiş Kapsüller',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                const SizedBox(height: 10),
                ...kapsuller
                    .where((k) => k['tarih'] != bugunku?['tarih'])
                    .map((k) => _KapsulKart(
                          k: Map<String, dynamic>.from(k as Map),
                          bugun: false,
                        )),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _KapsulKart extends StatelessWidget {
  final Map<String, dynamic> k;
  final bool bugun;
  const _KapsulKart({required this.k, required this.bugun});

  @override
  Widget build(BuildContext context) {
    final ozet = k['ai_ozet'] as String? ?? '';
    final tarih = k['tarih'] as String? ?? '';

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      color: bugun ? AppColors.primary.withOpacity(0.1) : null,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(
          color: bugun ? AppColors.primary : Colors.transparent,
          width: bugun ? 1.5 : 0,
        ),
      ),
      child: ExpansionTile(
        title: Row(
          children: [
            Icon(Icons.auto_awesome,
                color: bugun ? AppColors.primary : AppColors.gold),
            const SizedBox(width: 8),
            Text(bugun ? 'Bugün $tarih' : tarih,
                style: TextStyle(
                  fontWeight: bugun ? FontWeight.bold : FontWeight.w500,
                )),
          ],
        ),
        subtitle: ozet.isNotEmpty
            ? Padding(
                padding: const EdgeInsets.only(top: 6),
                child: Text(
                  ozet.length > 120 ? '${ozet.substring(0, 120)}...' : ozet,
                  style: const TextStyle(fontSize: 13),
                ),
              )
            : null,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (ozet.length > 120) ...[
                  Text(ozet, style: const TextStyle(fontSize: 14, height: 1.5)),
                  const SizedBox(height: 12),
                ],
                _Bolum(
                  baslik: '🎓 Akademik',
                  color: AppColors.primary,
                  data: k['akademik'] as Map? ?? {},
                ),
                _Bolum(
                  baslik: '❤️ Sosyal-Duygusal',
                  color: AppColors.danger,
                  data: k['sosyal_duygusal'] as Map? ?? {},
                ),
                _Bolum(
                  baslik: '🎉 Etkinlik',
                  color: AppColors.success,
                  data: k['etkinlik'] as Map? ?? {},
                ),
                _Bolum(
                  baslik: '📅 Yarın Hazırlık',
                  color: AppColors.warning,
                  data: k['yarin_hazirlik'] as Map? ?? {},
                ),
                _Bolum(
                  baslik: '⭐ Özel An',
                  color: AppColors.gold,
                  data: k['ozel_an'] as Map? ?? {},
                ),
                _Bolum(
                  baslik: '😊 Mood',
                  color: AppColors.info,
                  data: k['mood'] as Map? ?? {},
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


class _Bolum extends StatelessWidget {
  final String baslik;
  final Color color;
  final Map data;
  const _Bolum({required this.baslik, required this.color, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.isEmpty) return const SizedBox.shrink();

    final entries = data.entries.where((e) => e.value != null && '${e.value}'.isNotEmpty).toList();
    if (entries.isEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border(left: BorderSide(color: color, width: 3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(baslik,
              style: TextStyle(fontWeight: FontWeight.w600, color: color, fontSize: 13)),
          const SizedBox(height: 6),
          ...entries.map((e) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 2),
                child: Text('${e.key}: ${e.value}',
                    style: const TextStyle(fontSize: 12.5)),
              )),
        ],
      ),
    );
  }
}
