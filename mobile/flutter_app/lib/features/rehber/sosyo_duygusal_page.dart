import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Sosyo-duygusal takip paneli - Rehber ogretmen gorunumu.
/// Ruh hali ortalamalari, devamsizlik trendi, sosyal beceri puanlari.
class SosyoDuygusalPage extends ConsumerStatefulWidget {
  const SosyoDuygusalPage({super.key});

  @override
  ConsumerState<SosyoDuygusalPage> createState() =>
      _SosyoDuygusalPageState();
}

class _SosyoDuygusalPageState extends ConsumerState<SosyoDuygusalPage> {
  Map<String, dynamic> _summary = {};
  List<Map<String, dynamic>> _students = [];
  bool _loading = true;
  String _selectedClass = 'hepsi';

  static const _classOptions = [
    'hepsi',
    '9-A',
    '9-B',
    '10-A',
    '10-B',
    '11-A',
    '11-B',
    '12-A',
    '12-B',
  ];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/sosyo-duygusal');
      final data = resp.data;
      if (data is Map && data.containsKey('students')) {
        _summary = Map<String, dynamic>.from(data['summary'] as Map? ?? {});
        _students = List<Map<String, dynamic>>.from(
          (data['students'] as List)
              .map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _setStatic();
      }
    } catch (_) {
      _setStatic();
    }
    if (mounted) setState(() => _loading = false);
  }

  void _setStatic() {
    _summary = {
      'mood_avg': 3.6,
      'devamsizlik_trend': -2.1,
      'sosyal_beceri_avg': 72,
    };
    _students = [
      {
        'id': 'sd_01',
        'ad_soyad': 'Elif Yilmaz',
        'sinif': '10-A',
        'son_mood': 'happy',
        'mood_skor': 4,
        'sosyal_skor': 85,
        'endise': false,
      },
      {
        'id': 'sd_02',
        'ad_soyad': 'Burak Kaya',
        'sinif': '11-B',
        'son_mood': 'sad',
        'mood_skor': 2,
        'sosyal_skor': 42,
        'endise': true,
      },
      {
        'id': 'sd_03',
        'ad_soyad': 'Zeynep Demir',
        'sinif': '9-A',
        'son_mood': 'neutral',
        'mood_skor': 3,
        'sosyal_skor': 65,
        'endise': false,
      },
      {
        'id': 'sd_04',
        'ad_soyad': 'Can Arslan',
        'sinif': '12-A',
        'son_mood': 'happy',
        'mood_skor': 5,
        'sosyal_skor': 91,
        'endise': false,
      },
      {
        'id': 'sd_05',
        'ad_soyad': 'Ayse Celik',
        'sinif': '10-B',
        'son_mood': 'sad',
        'mood_skor': 1,
        'sosyal_skor': 35,
        'endise': true,
      },
      {
        'id': 'sd_06',
        'ad_soyad': 'Mehmet Sahin',
        'sinif': '9-B',
        'son_mood': 'neutral',
        'mood_skor': 3,
        'sosyal_skor': 58,
        'endise': false,
      },
      {
        'id': 'sd_07',
        'ad_soyad': 'Selin Ozturk',
        'sinif': '11-A',
        'son_mood': 'sad',
        'mood_skor': 2,
        'sosyal_skor': 48,
        'endise': true,
      },
      {
        'id': 'sd_08',
        'ad_soyad': 'Ali Kocer',
        'sinif': '10-A',
        'son_mood': 'happy',
        'mood_skor': 4,
        'sosyal_skor': 78,
        'endise': false,
      },
    ];
  }

  String _moodEmoji(String mood) {
    switch (mood) {
      case 'happy':
        return '\u{1F60A}'; // smiling face
      case 'neutral':
        return '\u{1F610}'; // neutral face
      case 'sad':
        return '\u{1F61E}'; // sad face
      default:
        return '\u{2753}'; // question mark
    }
  }

  String _moodLabel(String mood) {
    switch (mood) {
      case 'happy':
        return 'Iyi';
      case 'neutral':
        return 'Normal';
      case 'sad':
        return 'Dusuk';
      default:
        return '-';
    }
  }

  Color _moodColor(String mood) {
    switch (mood) {
      case 'happy':
        return AppColors.success;
      case 'neutral':
        return AppColors.warning;
      case 'sad':
        return AppColors.danger;
      default:
        return Colors.grey;
    }
  }

  Color _skorColor(int skor) {
    if (skor >= 70) return AppColors.success;
    if (skor >= 50) return AppColors.warning;
    return AppColors.danger;
  }

  List<Map<String, dynamic>> get _filtered {
    if (_selectedClass == 'hepsi') return _students;
    return _students
        .where((s) => s['sinif'] == _selectedClass)
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final moodAvg =
        (_summary['mood_avg'] as num?)?.toDouble() ?? 0.0;
    final devTrend =
        (_summary['devamsizlik_trend'] as num?)?.toDouble() ?? 0.0;
    final sosyalAvg =
        (_summary['sosyal_beceri_avg'] as num?)?.toInt() ?? 0;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sosyo-Duygusal Takip'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(14),
                children: [
                  // -- Ozet kartlari --
                  Row(
                    children: [
                      Expanded(
                        child: _SummaryTile(
                          label: 'Ruh Hali Ort.',
                          value: moodAvg.toStringAsFixed(1),
                          icon: Icons.mood,
                          color: moodAvg >= 3.5
                              ? AppColors.success
                              : moodAvg >= 2.5
                                  ? AppColors.warning
                                  : AppColors.danger,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _SummaryTile(
                          label: 'Devamsizlik',
                          value:
                              '${devTrend >= 0 ? '+' : ''}${devTrend.toStringAsFixed(1)}%',
                          icon: devTrend <= 0
                              ? Icons.trending_down
                              : Icons.trending_up,
                          color: devTrend <= 0
                              ? AppColors.success
                              : AppColors.danger,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: _SummaryTile(
                          label: 'Sosyal Beceri',
                          value: '$sosyalAvg',
                          icon: Icons.people,
                          color: _skorColor(sosyalAvg),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // -- Sinif filtresi --
                  SizedBox(
                    height: 36,
                    child: ListView(
                      scrollDirection: Axis.horizontal,
                      children: _classOptions.map((c) {
                        final selected = c == _selectedClass;
                        return Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: ChoiceChip(
                            label: Text(
                                c == 'hepsi' ? 'Tum Siniflar' : c),
                            selected: selected,
                            selectedColor:
                                AppColors.primary.withOpacity(0.2),
                            onSelected: (_) =>
                                setState(() => _selectedClass = c),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                  const SizedBox(height: 14),

                  // -- Endise uyarisi --
                  if (_filtered.any((s) => s['endise'] == true))
                    Container(
                      margin: const EdgeInsets.only(bottom: 12),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 10),
                      decoration: BoxDecoration(
                        color: AppColors.danger.withOpacity(0.08),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                            color: AppColors.danger.withOpacity(0.3)),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.flag,
                              color: AppColors.danger, size: 20),
                          const SizedBox(width: 8),
                          Text(
                            '${_filtered.where((s) => s['endise'] == true).length} ogrenci endise verici durumda',
                            style: const TextStyle(
                              color: AppColors.danger,
                              fontSize: 13,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),

                  // -- Ogrenci listesi --
                  if (_filtered.isEmpty)
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Center(
                        child: Text('Ogrenci bulunamadi',
                            style: TextStyle(
                                color: AppColors.textSecondaryDark)),
                      ),
                    )
                  else
                    ..._filtered.map((s) => _StudentRow(
                          student: s,
                          moodEmoji:
                              _moodEmoji(s['son_mood'] as String),
                          moodLabel:
                              _moodLabel(s['son_mood'] as String),
                          moodColor:
                              _moodColor(s['son_mood'] as String),
                          skorColor:
                              _skorColor(s['sosyal_skor'] as int),
                        )),
                ],
              ),
            ),
    );
  }
}

// ---------------------------------------------------------------------------
// Summary Tile
// ---------------------------------------------------------------------------
class _SummaryTile extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;

  const _SummaryTile({
    required this.label,
    required this.value,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 10),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(height: 6),
          Text(
            value,
            style: TextStyle(
                fontSize: 20, fontWeight: FontWeight.bold, color: color),
          ),
          const SizedBox(height: 2),
          Text(label,
              style: const TextStyle(
                  fontSize: 11, color: AppColors.textSecondaryDark),
              textAlign: TextAlign.center),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Student Row
// ---------------------------------------------------------------------------
class _StudentRow extends StatelessWidget {
  final Map<String, dynamic> student;
  final String moodEmoji;
  final String moodLabel;
  final Color moodColor;
  final Color skorColor;

  const _StudentRow({
    required this.student,
    required this.moodEmoji,
    required this.moodLabel,
    required this.moodColor,
    required this.skorColor,
  });

  @override
  Widget build(BuildContext context) {
    final sosyalSkor = (student['sosyal_skor'] as num?)?.toInt() ?? 0;
    final endise = student['endise'] == true;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: IntrinsicHeight(
        child: Row(
          children: [
            if (endise) Container(width: 4, color: AppColors.danger),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  children: [
                    // Mood emoji
                    Container(
                      width: 42,
                      height: 42,
                      decoration: BoxDecoration(
                        color: moodColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Center(
                        child: Text(moodEmoji, style: const TextStyle(fontSize: 22)),
                      ),
                    ),
                    const SizedBox(width: 12),
                    // Info
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Expanded(
                                child: Text(
                                  student['ad_soyad'] as String? ?? '-',
                                  style: const TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w600),
                                ),
                              ),
                              if (endise)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: AppColors.danger.withOpacity(0.12),
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: const Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: [
                                      Icon(Icons.flag,
                                          size: 12,
                                          color: AppColors.danger),
                                      SizedBox(width: 2),
                                      Text(
                                        'Endise',
                                        style: TextStyle(
                                          fontSize: 10,
                                          color: AppColors.danger,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Row(
                            children: [
                              Text(
                                '${student['sinif']}',
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                              const SizedBox(width: 8),
                              Container(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 6, vertical: 1),
                                decoration: BoxDecoration(
                                  color: moodColor.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: Text(
                                  moodLabel,
                                  style: TextStyle(
                                      fontSize: 11,
                                      color: moodColor,
                                      fontWeight: FontWeight.w600),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 6),
                          // Sosyal skor bar
                          Row(
                            children: [
                              Expanded(
                                child: ClipRRect(
                                  borderRadius: BorderRadius.circular(4),
                                  child: LinearProgressIndicator(
                                    value: sosyalSkor / 100.0,
                                    minHeight: 6,
                                    backgroundColor:
                                        skorColor.withOpacity(0.15),
                                    valueColor: AlwaysStoppedAnimation<Color>(
                                        skorColor),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                '$sosyalSkor',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.bold,
                                  color: skorColor,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
