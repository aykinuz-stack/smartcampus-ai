import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class BasariDuvariPage extends ConsumerStatefulWidget {
  const BasariDuvariPage({super.key});

  @override
  ConsumerState<BasariDuvariPage> createState() => _BasariDuvariPageState();
}

class _BasariDuvariPageState extends ConsumerState<BasariDuvariPage> {
  Future<List<Map<String, dynamic>>>? _future;
  String _selectedFilter = 'tumu';

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetchBasarilar());
  }

  Future<List<Map<String, dynamic>>> _fetchBasarilar() async {
    try {
      final r = await ref.read(apiClientProvider).get('/veli/basari-duvari');
      final data = r.data;
      if (data is Map && data['basarilar'] != null) {
        return List<Map<String, dynamic>>.from(data['basarilar'] as List);
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
        'ogrenci_adi': 'Elif Yilmaz',
        'basari_turu': 'akademik',
        'seviye': 'altin',
        'tarih': '2026-04-18',
        'baslik': 'Matematik Yarismasi Birincilik',
        'aciklama': 'Ilce geneli matematik yarismasi birincisi olmustur.',
      },
      {
        'ogrenci_adi': 'Elif Yilmaz',
        'basari_turu': 'sanat',
        'seviye': 'gumus',
        'tarih': '2026-04-10',
        'baslik': 'Resim Sergisi Katilim',
        'aciklama': 'Okul resim sergisinde eserleri sergilenmistir.',
      },
      {
        'ogrenci_adi': 'Ahmet Yilmaz',
        'basari_turu': 'spor',
        'seviye': 'altin',
        'tarih': '2026-04-15',
        'baslik': 'Futbol Turnuvasi Sampiyonluk',
        'aciklama': 'Okul futbol takimiyla il sampiyonu olmustur.',
      },
      {
        'ogrenci_adi': 'Ahmet Yilmaz',
        'basari_turu': 'sosyal',
        'seviye': 'bronz',
        'tarih': '2026-04-05',
        'baslik': 'Toplum Hizmeti Belgesi',
        'aciklama': 'Huzurevi ziyaretleri ve gonulluluk calismalarindan dolayi belge almistir.',
      },
      {
        'ogrenci_adi': 'Elif Yilmaz',
        'basari_turu': 'akademik',
        'seviye': 'gumus',
        'tarih': '2026-03-28',
        'baslik': 'Donem Birinciligi',
        'aciklama': '2. donemde sinif birincisi olmustur.',
      },
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Basari Duvari')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final allBasarilar = snap.data ?? [];

          // Filter
          final basarilar = _selectedFilter == 'tumu'
              ? allBasarilar
              : allBasarilar
                  .where((b) => b['basari_turu'] == _selectedFilter)
                  .toList();

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: Column(
              children: [
                // Filter chips
                _buildFilterBar(),
                // List
                Expanded(
                  child: basarilar.isEmpty
                      ? const Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.emoji_events_outlined,
                                  size: 64, color: Colors.grey),
                              SizedBox(height: 12),
                              Text('Basari bulunamadi',
                                  style: TextStyle(fontSize: 15)),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
                          itemCount: basarilar.length,
                          itemBuilder: (_, i) =>
                              _BasariKart(data: basarilar[i]),
                        ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildFilterBar() {
    const filters = [
      {'key': 'tumu', 'label': 'Tumu', 'icon': Icons.select_all},
      {'key': 'akademik', 'label': 'Akademik', 'icon': Icons.school},
      {'key': 'spor', 'label': 'Spor', 'icon': Icons.sports_soccer},
      {'key': 'sanat', 'label': 'Sanat', 'icon': Icons.palette},
      {'key': 'sosyal', 'label': 'Sosyal', 'icon': Icons.people},
    ];

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      child: Row(
        children: filters.map((f) {
          final key = f['key'] as String;
          final selected = _selectedFilter == key;
          return Padding(
            padding: const EdgeInsets.only(right: 8),
            child: FilterChip(
              selected: selected,
              label: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(f['icon'] as IconData,
                      size: 16,
                      color: selected ? Colors.white : AppColors.primary),
                  const SizedBox(width: 4),
                  Text(f['label'] as String),
                ],
              ),
              selectedColor: AppColors.primary,
              backgroundColor: Colors.white,
              labelStyle: TextStyle(
                color: selected ? Colors.white : AppColors.textPrimaryLight,
                fontWeight: selected ? FontWeight.w600 : FontWeight.normal,
              ),
              side: BorderSide(
                color: selected ? AppColors.primary : Colors.grey.shade300,
              ),
              onSelected: (_) => setState(() => _selectedFilter = key),
            ),
          );
        }).toList(),
      ),
    );
  }
}


class _BasariKart extends StatelessWidget {
  final Map<String, dynamic> data;
  const _BasariKart({required this.data});

  static const _goldColor = Color(0xFFFFD700);
  static const _silverColor = Color(0xFFC0C0C0);
  static const _bronzeColor = Color(0xFFCD7F32);

  @override
  Widget build(BuildContext context) {
    final seviye = (data['seviye'] as String? ?? '').toLowerCase();
    final basariTuru = (data['basari_turu'] as String? ?? '').toLowerCase();
    final ogrenciAdi = data['ogrenci_adi'] as String? ?? '';
    final baslik = data['baslik'] as String? ?? '';
    final aciklama = data['aciklama'] as String? ?? '';
    final tarih = data['tarih'] as String? ?? '';

    // Level colors
    Color seviyeColor;
    String seviyeLabel;
    String seviyeEmoji;
    switch (seviye) {
      case 'altin':
        seviyeColor = _goldColor;
        seviyeLabel = 'Altin';
        seviyeEmoji = '🏆';
        break;
      case 'gumus':
        seviyeColor = _silverColor;
        seviyeLabel = 'Gumus';
        seviyeEmoji = '🥈';
        break;
      case 'bronz':
        seviyeColor = _bronzeColor;
        seviyeLabel = 'Bronz';
        seviyeEmoji = '🥉';
        break;
      default:
        seviyeColor = AppColors.primary;
        seviyeLabel = seviye.isNotEmpty ? seviye : '';
        seviyeEmoji = '⭐';
    }

    // Type icon
    IconData typeIcon;
    Color typeColor;
    String typeLabel;
    switch (basariTuru) {
      case 'akademik':
        typeIcon = Icons.school;
        typeColor = AppColors.info;
        typeLabel = 'Akademik';
        break;
      case 'spor':
        typeIcon = Icons.sports_soccer;
        typeColor = AppColors.success;
        typeLabel = 'Spor';
        break;
      case 'sanat':
        typeIcon = Icons.palette;
        typeColor = AppColors.gold;
        typeLabel = 'Sanat';
        break;
      case 'sosyal':
        typeIcon = Icons.people;
        typeColor = AppColors.primary;
        typeLabel = 'Sosyal';
        break;
      default:
        typeIcon = Icons.star;
        typeColor = AppColors.warning;
        typeLabel = basariTuru;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: BoxDecoration(
          border: Border(
            left: BorderSide(color: seviyeColor, width: 4),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header row: emoji + title + level badge
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(seviyeEmoji, style: const TextStyle(fontSize: 28)),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(baslik,
                            style: const TextStyle(
                                fontSize: 15, fontWeight: FontWeight.w700)),
                        const SizedBox(height: 4),
                        Text(ogrenciAdi,
                            style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w500,
                                color: AppColors.textSecondaryLight)),
                      ],
                    ),
                  ),
                  // Level badge
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: seviyeColor.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(
                          color: seviyeColor.withOpacity(0.5), width: 1),
                    ),
                    child: Text(seviyeLabel,
                        style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: seviye == 'gumus'
                                ? Colors.grey[700]
                                : seviyeColor.withRed(
                                    (seviyeColor.red * 0.7).toInt()))),
                  ),
                ],
              ),
              const SizedBox(height: 10),

              // Description
              if (aciklama.isNotEmpty)
                Text(aciklama,
                    style: TextStyle(
                        fontSize: 13,
                        height: 1.4,
                        color: Colors.grey[700])),

              const SizedBox(height: 10),

              // Footer: type + date
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: typeColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(typeIcon, size: 14, color: typeColor),
                        const SizedBox(width: 4),
                        Text(typeLabel,
                            style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                                color: typeColor)),
                      ],
                    ),
                  ),
                  const Spacer(),
                  Icon(Icons.calendar_today,
                      size: 12, color: Colors.grey[500]),
                  const SizedBox(width: 4),
                  Text(tarih,
                      style: TextStyle(
                          fontSize: 12, color: Colors.grey[500])),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
