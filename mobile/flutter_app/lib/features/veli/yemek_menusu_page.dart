import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class YemekMenusuPage extends ConsumerStatefulWidget {
  const YemekMenusuPage({super.key});

  @override
  ConsumerState<YemekMenusuPage> createState() => _YemekMenusuPageState();
}

class _YemekMenusuPageState extends ConsumerState<YemekMenusuPage> {
  Future<List<Map<String, dynamic>>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetchMenu());
  }

  Future<List<Map<String, dynamic>>> _fetchMenu() async {
    try {
      final r = await ref.read(apiClientProvider).get('/veli/yemek-menusu');
      final data = r.data;
      if (data is Map && data['haftalik_menu'] != null) {
        return List<Map<String, dynamic>>.from(data['haftalik_menu'] as List);
      }
      if (data is List) {
        return List<Map<String, dynamic>>.from(data);
      }
      return _staticData();
    } catch (_) {
      return _staticData();
    }
  }

  static List<Map<String, dynamic>> _staticData() {
    return [
      {
        'gun': 'Pazartesi',
        'gun_index': 1,
        'corba': 'Mercimek Corbasi',
        'ana_yemek': 'Tavuk Sote',
        'yan_yemek': 'Bulgur Pilavi',
        'tatli': 'Sutlac',
        'kalori': 720,
      },
      {
        'gun': 'Sali',
        'gun_index': 2,
        'corba': 'Domates Corbasi',
        'ana_yemek': 'Kofte',
        'yan_yemek': 'Makarna',
        'tatli': 'Meyve',
        'kalori': 680,
      },
      {
        'gun': 'Carsamba',
        'gun_index': 3,
        'corba': 'Yayla Corbasi',
        'ana_yemek': 'Etli Nohut',
        'yan_yemek': 'Pirinc Pilavi',
        'tatli': 'Komposto',
        'kalori': 750,
      },
      {
        'gun': 'Persembe',
        'gun_index': 4,
        'corba': 'Ezogelin Corbasi',
        'ana_yemek': 'Izgara Tavuk',
        'yan_yemek': 'Sebze Sote',
        'tatli': 'Puding',
        'kalori': 640,
      },
      {
        'gun': 'Cuma',
        'gun_index': 5,
        'corba': 'Tarhana Corbasi',
        'ana_yemek': 'Balik Tava',
        'yan_yemek': 'Salata',
        'tatli': 'Taze Meyve',
        'kalori': 610,
      },
    ];
  }

  int _todayWeekdayIndex() {
    // Monday=1 ... Friday=5, weekend returns 0
    final wd = DateTime.now().weekday;
    return wd >= 1 && wd <= 5 ? wd : 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Yemek Menusu')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final menu = snap.data ?? [];

          if (menu.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.restaurant_menu, size: 64, color: Colors.grey),
                  SizedBox(height: 12),
                  Text('Menu bilgisi bulunamadi',
                      style: TextStyle(fontSize: 15)),
                ],
              ),
            );
          }

          final todayIndex = _todayWeekdayIndex();

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Hero gradient header
                _buildHeroHeader(),
                const SizedBox(height: 16),

                // Day cards
                ...menu.map((day) => _buildDayCard(day, todayIndex)),

                const SizedBox(height: 24),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildHeroHeader() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.success, Color(0xFF10B981)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Icon(Icons.restaurant_menu,
                color: Colors.white, size: 28),
          ),
          const SizedBox(width: 14),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Haftalik Yemek Menusu',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w700)),
                SizedBox(height: 4),
                Text('Saglikli ve dengeli beslenme programi',
                    style: TextStyle(
                        color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
          const Icon(Icons.eco, color: Colors.white38, size: 32),
        ],
      ),
    );
  }

  Widget _buildDayCard(Map<String, dynamic> day, int todayIndex) {
    final gunAdi = day['gun'] as String? ?? '';
    final gunIndex = day['gun_index'] as int? ?? 0;
    final isToday = gunIndex == todayIndex;
    final kalori = day['kalori'];

    final items = <_MenuItem>[
      _MenuItem(
          icon: Icons.soup_kitchen,
          label: 'Corba',
          value: day['corba'] as String? ?? '-'),
      _MenuItem(
          icon: Icons.dinner_dining,
          label: 'Ana Yemek',
          value: day['ana_yemek'] as String? ?? '-'),
      _MenuItem(
          icon: Icons.rice_bowl,
          label: 'Yan Yemek',
          value: day['yan_yemek'] as String? ?? '-'),
      _MenuItem(
          icon: Icons.cake,
          label: 'Tatli',
          value: day['tatli'] as String? ?? '-'),
    ];

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: isToday
            ? const BorderSide(color: AppColors.primary, width: 2)
            : BorderSide.none,
      ),
      child: Container(
        decoration: BoxDecoration(
          border: Border(
            left: BorderSide(
              color: isToday ? AppColors.primary : AppColors.success,
              width: 4,
            ),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Day header
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: isToday
                    ? AppColors.primary.withOpacity(0.08)
                    : Colors.grey.withOpacity(0.04),
              ),
              child: Row(
                children: [
                  Icon(
                    isToday
                        ? Icons.today
                        : Icons.calendar_view_day,
                    size: 18,
                    color: isToday
                        ? AppColors.primary
                        : AppColors.textSecondaryLight,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    gunAdi,
                    style: TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                      color: isToday
                          ? AppColors.primary
                          : AppColors.textPrimaryLight,
                    ),
                  ),
                  if (isToday) ...[
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: AppColors.primary,
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: const Text('Bugun',
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.bold)),
                    ),
                  ],
                  const Spacer(),
                  if (kalori != null)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppColors.warning.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.local_fire_department,
                              size: 14, color: AppColors.warning),
                          const SizedBox(width: 3),
                          Text('$kalori kcal',
                              style: const TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.warning)),
                        ],
                      ),
                    ),
                ],
              ),
            ),

            // Menu items
            Padding(
              padding: const EdgeInsets.fromLTRB(14, 8, 14, 14),
              child: Column(
                children: items.map((item) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(vertical: 5),
                    child: Row(
                      children: [
                        Icon(item.icon,
                            size: 18, color: AppColors.success),
                        const SizedBox(width: 10),
                        SizedBox(
                          width: 85,
                          child: Text('${item.label}:',
                              style: TextStyle(
                                  fontSize: 13,
                                  color: Colors.grey[600])),
                        ),
                        Expanded(
                          child: Text(item.value,
                              style: const TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w500)),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


class _MenuItem {
  final IconData icon;
  final String label;
  final String value;

  const _MenuItem({
    required this.icon,
    required this.label,
    required this.value,
  });
}
