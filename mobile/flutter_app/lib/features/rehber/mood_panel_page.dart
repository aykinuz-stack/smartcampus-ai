import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';


class MoodPanelPage extends ConsumerStatefulWidget {
  const MoodPanelPage({super.key});

  @override
  ConsumerState<MoodPanelPage> createState() => _MoodPanelPageState();
}

class _MoodPanelPageState extends ConsumerState<MoodPanelPage> {
  Future<Map<String, dynamic>>? _future;
  int _days = 14;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(rehberApiProvider).moodPanel(days: _days));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('😊 Mood Paneli'),
        actions: [
          PopupMenuButton<int>(
            icon: const Icon(Icons.calendar_today),
            onSelected: (v) { setState(() => _days = v); _load(); },
            itemBuilder: (_) => const [
              PopupMenuItem(value: 7, child: Text('Son 7 gün')),
              PopupMenuItem(value: 14, child: Text('Son 14 gün')),
              PopupMenuItem(value: 30, child: Text('Son 30 gün')),
            ],
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snap.data ?? {};
          final genOrt = (data['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
          final toplam = (data['toplam_checkin'] as num?)?.toInt() ?? 0;
          final aktif = (data['aktif_ogrenci_sayisi'] as num?)?.toInt() ?? 0;
          final riskli = List<Map<String, dynamic>>.from(
              (data['riskli_ogrenciler'] as List?) ?? []);

          Color moodColor;
          String moodLabel;
          if (genOrt >= 4.0) { moodColor = AppColors.success; moodLabel = 'İyi'; }
          else if (genOrt >= 3.0) { moodColor = AppColors.warning; moodLabel = 'Orta'; }
          else if (genOrt > 0) { moodColor = AppColors.danger; moodLabel = 'Dikkat!'; }
          else { moodColor = Colors.grey; moodLabel = 'Veri yok'; }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Ozet kart
                Container(
                  padding: const EdgeInsets.all(18),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [moodColor, moodColor.withOpacity(0.7)],
                    ),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Son $_days gün',
                          style: const TextStyle(color: Colors.white70, fontSize: 12)),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Text(
                            genOrt.toStringAsFixed(2),
                            style: const TextStyle(
                                color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(width: 8),
                          Padding(
                            padding: const EdgeInsets.only(top: 10),
                            child: Text('/ 5.0',
                                style: TextStyle(color: Colors.white.withOpacity(0.7))),
                          ),
                          const Spacer(),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(moodLabel,
                                style: const TextStyle(
                                    color: Colors.white, fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          _MiniStat(label: 'Check-in', value: '$toplam'),
                          const SizedBox(width: 16),
                          _MiniStat(label: 'Aktif Öğrenci', value: '$aktif'),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),
                Row(
                  children: [
                    const Text('Riskli Öğrenciler',
                        style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                    const Spacer(),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppColors.danger.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text('${riskli.length}',
                          style: const TextStyle(
                              color: AppColors.danger, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                const Text('3+ gün negatif mood (seviye 1-2)',
                    style: TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
                const SizedBox(height: 12),

                if (riskli.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(24),
                    child: Center(child: Text('🎉 Tüm öğrenciler iyi!')),
                  )
                else
                  ...riskli.map((r) {
                    final negatif = r['negatif_gun'] as int;
                    final total = r['toplam_kayit'] as int;
                    final ortalama = (r['ortalama'] as num).toDouble();
                    Color c;
                    if (negatif >= 7) c = AppColors.danger;
                    else if (negatif >= 5) c = AppColors.warning;
                    else c = AppColors.info;

                    return Card(
                      margin: const EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: c.withOpacity(0.15),
                          child: Text(
                            negatif.toString(),
                            style: TextStyle(color: c, fontWeight: FontWeight.bold),
                          ),
                        ),
                        title: Text(r['student_name'] ?? '?',
                            style: const TextStyle(fontWeight: FontWeight.w600)),
                        subtitle: Text(
                          '$negatif/$total gün negatif · ortalama ${ortalama.toStringAsFixed(1)}',
                          style: const TextStyle(fontSize: 12),
                        ),
                        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                      ),
                    );
                  }),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _MiniStat extends StatelessWidget {
  final String label;
  final String value;
  const _MiniStat({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(value,
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(width: 4),
        Text(label, style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 12)),
      ],
    );
  }
}
