import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/theme/app_theme.dart';

class DevamsizlikPage extends ConsumerStatefulWidget {
  const DevamsizlikPage({super.key});

  @override
  ConsumerState<DevamsizlikPage> createState() => _DevamsizlikPageState();
}

class _DevamsizlikPageState extends ConsumerState<DevamsizlikPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(ogrenciApiProvider).getDevamsizlik());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Devamsızlığım')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
          final data = snap.data;
          if (data == null) return const SizedBox();

          final kayitlar = (data['kayitlar'] as List?) ?? [];
          final ozursuz = (data['ozursuz'] as num?)?.toInt() ?? 0;
          final ozurlu = (data['ozurlu'] as num?)?.toInt() ?? 0;
          final gec = (data['gec'] as num?)?.toInt() ?? 0;
          final oran = (data['oran'] as num?)?.toDouble() ?? 0.0;
          final son30 = (data['son_30_gun'] as num?)?.toInt() ?? 0;

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Ozet cubuklari
                Row(
                  children: [
                    Expanded(child: _Sayac(label: 'Özürsüz', deger: ozursuz, color: AppColors.danger)),
                    const SizedBox(width: 8),
                    Expanded(child: _Sayac(label: 'Özürlü', deger: ozurlu, color: AppColors.info)),
                    const SizedBox(width: 8),
                    Expanded(child: _Sayac(label: 'Geç', deger: gec, color: AppColors.warning)),
                  ],
                ),
                const SizedBox(height: 16),

                // Oran karti
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: oran > 10 ? AppColors.danger.withOpacity(0.15) : AppColors.success.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Devamsızlık Oranı',
                              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
                          Text(
                            '${oran.toStringAsFixed(1)}%',
                            style: TextStyle(
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              color: oran > 10 ? AppColors.danger : AppColors.success,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 10),
                      LinearProgressIndicator(
                        value: (oran / 100).clamp(0, 1),
                        minHeight: 10,
                        backgroundColor: Colors.grey.withOpacity(0.2),
                        valueColor: AlwaysStoppedAnimation(
                          oran > 10 ? AppColors.danger : AppColors.success,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text('Son 30 gün: $son30 ders saati'),
                          if (oran > 10)
                            const Text('⚠️ Dikkat — Sınıf tekrarı riski',
                                style: TextStyle(color: AppColors.danger, fontSize: 12)),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),

                const Text('Kayıtlar',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                const SizedBox(height: 10),
                if (kayitlar.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(32),
                    child: Center(child: Text('🎉 Hiç devamsızlık yok!')),
                  )
                else
                  ...kayitlar.map((k) => _DevamKart(k: k)),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _Sayac extends StatelessWidget {
  final String label;
  final int deger;
  final Color color;
  const _Sayac({required this.label, required this.deger, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Text('$deger',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }
}


class _DevamKart extends StatelessWidget {
  final dynamic k;
  const _DevamKart({required this.k});

  @override
  Widget build(BuildContext context) {
    final turu = (k['turu'] as String).toLowerCase();
    Color c;
    IconData icon;
    switch (turu) {
      case 'devamsiz':
      case 'ozursuz':
        c = AppColors.danger; icon = Icons.close_rounded; break;
      case 'izinli':
      case 'raporlu':
      case 'ozurlu':
        c = AppColors.info; icon = Icons.medical_information_outlined; break;
      case 'gec':
        c = AppColors.warning; icon = Icons.access_time; break;
      default:
        c = Colors.grey; icon = Icons.help_outline;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 6),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: c.withOpacity(0.15),
          child: Icon(icon, color: c),
        ),
        title: Text('${k['ders']} · ${k['ders_saati']}. ders',
            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
        subtitle: Text('${k['tarih']} · ${turu.toUpperCase()}'),
      ),
    );
  }
}
