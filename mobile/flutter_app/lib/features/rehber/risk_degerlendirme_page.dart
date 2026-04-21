import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Ogrenci risk degerlendirme paneli.
/// Yuksek / Orta / Dusuk risk seviyeleri ile ogrenci listesi gosterir.
class RiskDegerlendirmePage extends ConsumerStatefulWidget {
  const RiskDegerlendirmePage({super.key});

  @override
  ConsumerState<RiskDegerlendirmePage> createState() =>
      _RiskDegerlendirmePageState();
}

class _RiskDegerlendirmePageState
    extends ConsumerState<RiskDegerlendirmePage> {
  List<Map<String, dynamic>> _students = [];
  bool _loading = true;
  String? _error;
  String _selectedLevel = 'hepsi'; // hepsi, yuksek, orta, dusuk

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/risk-degerlendirme');
      final data = resp.data;
      if (data is List) {
        _students = List<Map<String, dynamic>>.from(
          data.map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _students = _staticData();
      }
    } catch (_) {
      _students = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  List<Map<String, dynamic>> _staticData() => [
        {
          'id': '1',
          'ad_soyad': 'Ahmet Yilmaz',
          'sinif': '9',
          'sube': 'A',
          'risk_skor': 87,
          'risk_seviye': 'yuksek',
          'son_degerlendirme': '2026-04-18',
          'faktorler': ['akademik', 'davranissal'],
        },
        {
          'id': '2',
          'ad_soyad': 'Elif Kara',
          'sinif': '10',
          'sube': 'B',
          'risk_skor': 72,
          'risk_seviye': 'yuksek',
          'son_degerlendirme': '2026-04-15',
          'faktorler': ['sosyal', 'akademik'],
        },
        {
          'id': '3',
          'ad_soyad': 'Mehmet Demir',
          'sinif': '11',
          'sube': 'A',
          'risk_skor': 55,
          'risk_seviye': 'orta',
          'son_degerlendirme': '2026-04-17',
          'faktorler': ['akademik'],
        },
        {
          'id': '4',
          'ad_soyad': 'Zeynep Celik',
          'sinif': '9',
          'sube': 'C',
          'risk_skor': 48,
          'risk_seviye': 'orta',
          'son_degerlendirme': '2026-04-16',
          'faktorler': ['davranissal', 'sosyal'],
        },
        {
          'id': '5',
          'ad_soyad': 'Can Ozturk',
          'sinif': '12',
          'sube': 'A',
          'risk_skor': 45,
          'risk_seviye': 'orta',
          'son_degerlendirme': '2026-04-14',
          'faktorler': ['sosyal'],
        },
        {
          'id': '6',
          'ad_soyad': 'Ayse Sahin',
          'sinif': '10',
          'sube': 'A',
          'risk_skor': 22,
          'risk_seviye': 'dusuk',
          'son_degerlendirme': '2026-04-10',
          'faktorler': ['akademik'],
        },
        {
          'id': '7',
          'ad_soyad': 'Burak Arslan',
          'sinif': '11',
          'sube': 'B',
          'risk_skor': 15,
          'risk_seviye': 'dusuk',
          'son_degerlendirme': '2026-04-12',
          'faktorler': [],
        },
      ];

  Color _riskColor(String seviye) {
    switch (seviye) {
      case 'yuksek':
        return AppColors.danger;
      case 'orta':
        return AppColors.warning;
      case 'dusuk':
        return AppColors.success;
      default:
        return Colors.grey;
    }
  }

  String _riskLabel(String seviye) {
    switch (seviye) {
      case 'yuksek':
        return 'Yuksek';
      case 'orta':
        return 'Orta';
      case 'dusuk':
        return 'Dusuk';
      default:
        return seviye;
    }
  }

  IconData _faktorIcon(String faktor) {
    switch (faktor) {
      case 'akademik':
        return Icons.school;
      case 'davranissal':
        return Icons.warning_amber;
      case 'sosyal':
        return Icons.people;
      default:
        return Icons.info_outline;
    }
  }

  String _faktorLabel(String faktor) {
    switch (faktor) {
      case 'akademik':
        return 'Akademik';
      case 'davranissal':
        return 'Davranissal';
      case 'sosyal':
        return 'Sosyal';
      default:
        return faktor;
    }
  }

  List<Map<String, dynamic>> get _filtered {
    if (_selectedLevel == 'hepsi') return _students;
    return _students
        .where((s) => s['risk_seviye'] == _selectedLevel)
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final yuksekCount =
        _students.where((s) => s['risk_seviye'] == 'yuksek').length;
    final ortaCount =
        _students.where((s) => s['risk_seviye'] == 'orta').length;
    final dusukCount =
        _students.where((s) => s['risk_seviye'] == 'dusuk').length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Risk Degerlendirme'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _load,
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text('Hata: $_error'))
              : RefreshIndicator(
                  onRefresh: _load,
                  child: ListView(
                    padding: const EdgeInsets.all(14),
                    children: [
                      // -- Summary cards --
                      Row(
                        children: [
                          Expanded(
                            child: _SummaryCard(
                              label: 'Yuksek',
                              count: yuksekCount,
                              color: AppColors.danger,
                              icon: Icons.arrow_upward,
                              selected: _selectedLevel == 'yuksek',
                              onTap: () => setState(() => _selectedLevel =
                                  _selectedLevel == 'yuksek'
                                      ? 'hepsi'
                                      : 'yuksek'),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: _SummaryCard(
                              label: 'Orta',
                              count: ortaCount,
                              color: AppColors.warning,
                              icon: Icons.remove,
                              selected: _selectedLevel == 'orta',
                              onTap: () => setState(() => _selectedLevel =
                                  _selectedLevel == 'orta'
                                      ? 'hepsi'
                                      : 'orta'),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: _SummaryCard(
                              label: 'Dusuk',
                              count: dusukCount,
                              color: AppColors.success,
                              icon: Icons.arrow_downward,
                              selected: _selectedLevel == 'dusuk',
                              onTap: () => setState(() => _selectedLevel =
                                  _selectedLevel == 'dusuk'
                                      ? 'hepsi'
                                      : 'dusuk'),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),

                      // -- Filter indicator --
                      if (_selectedLevel != 'hepsi')
                        Padding(
                          padding: const EdgeInsets.only(bottom: 10),
                          child: Row(
                            children: [
                              Icon(Icons.filter_list,
                                  size: 16,
                                  color: _riskColor(_selectedLevel)),
                              const SizedBox(width: 6),
                              Text(
                                'Filtre: ${_riskLabel(_selectedLevel)} Risk',
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: FontWeight.w600,
                                  color: _riskColor(_selectedLevel),
                                ),
                              ),
                              const Spacer(),
                              GestureDetector(
                                onTap: () =>
                                    setState(() => _selectedLevel = 'hepsi'),
                                child: const Text('Temizle',
                                    style: TextStyle(
                                        fontSize: 12, color: AppColors.info)),
                              ),
                            ],
                          ),
                        ),

                      // -- Student list --
                      if (_filtered.isEmpty)
                        const Padding(
                          padding: EdgeInsets.only(top: 40),
                          child: Center(
                            child: Text('Bu seviyede ogrenci bulunamadi',
                                style: TextStyle(color: AppColors.textSecondaryDark)),
                          ),
                        )
                      else
                        ..._filtered.map((s) => _StudentRiskCard(
                              student: s,
                              riskColor: _riskColor(s['risk_seviye'] as String),
                              riskLabel:
                                  _riskLabel(s['risk_seviye'] as String),
                              faktorIcon: _faktorIcon,
                              faktorLabel: _faktorLabel,
                            )),
                    ],
                  ),
                ),
    );
  }
}

// ---------------------------------------------------------------------------
// Summary Card
// ---------------------------------------------------------------------------
class _SummaryCard extends StatelessWidget {
  final String label;
  final int count;
  final Color color;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;

  const _SummaryCard({
    required this.label,
    required this.count,
    required this.color,
    required this.icon,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 10),
        decoration: BoxDecoration(
          color: selected ? color.withOpacity(0.15) : Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: selected ? color : color.withOpacity(0.3),
            width: selected ? 2 : 1,
          ),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 6),
            Text(
              '$count',
              style: TextStyle(
                  fontSize: 22, fontWeight: FontWeight.bold, color: color),
            ),
            const SizedBox(height: 2),
            Text(label,
                style: const TextStyle(
                    fontSize: 12, color: AppColors.textSecondaryDark)),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Student Risk Card
// ---------------------------------------------------------------------------
class _StudentRiskCard extends StatelessWidget {
  final Map<String, dynamic> student;
  final Color riskColor;
  final String riskLabel;
  final IconData Function(String) faktorIcon;
  final String Function(String) faktorLabel;

  const _StudentRiskCard({
    required this.student,
    required this.riskColor,
    required this.riskLabel,
    required this.faktorIcon,
    required this.faktorLabel,
  });

  @override
  Widget build(BuildContext context) {
    final faktorler = List<String>.from(student['faktorler'] ?? []);
    final skor = student['risk_skor'] as int? ?? 0;
    final tarih = student['son_degerlendirme'] as String? ?? '-';

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: IntrinsicHeight(
        child: Row(
          children: [
            // Colored left border
            Container(width: 5, color: riskColor),
            // Content
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Header row
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 18,
                          backgroundColor: riskColor.withOpacity(0.15),
                          child: Text(
                            (student['ad_soyad'] as String? ?? '?')[0],
                            style: TextStyle(
                                color: riskColor,
                                fontWeight: FontWeight.bold,
                                fontSize: 16),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                student['ad_soyad'] as String? ?? '-',
                                style: const TextStyle(
                                    fontSize: 15, fontWeight: FontWeight.w600),
                              ),
                              Text(
                                '${student['sinif']}/${student['sube']}',
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                            ],
                          ),
                        ),
                        // Risk badge
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: riskColor.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.speed, size: 14, color: riskColor),
                              const SizedBox(width: 4),
                              Text(
                                '$skor',
                                style: TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: riskColor,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    // Info row
                    Row(
                      children: [
                        const Icon(Icons.calendar_today,
                            size: 13, color: AppColors.textSecondaryDark),
                        const SizedBox(width: 4),
                        Text('Son: $tarih',
                            style: const TextStyle(
                                fontSize: 12,
                                color: AppColors.textSecondaryDark)),
                        const SizedBox(width: 12),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: riskColor.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            riskLabel,
                            style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                                color: riskColor),
                          ),
                        ),
                      ],
                    ),
                    // Risk factors
                    if (faktorler.isNotEmpty) ...[
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 6,
                        runSpacing: 4,
                        children: faktorler.map((f) {
                          return Chip(
                            materialTapTargetSize:
                                MaterialTapTargetSize.shrinkWrap,
                            visualDensity: VisualDensity.compact,
                            avatar: Icon(faktorIcon(f), size: 14),
                            label: Text(faktorLabel(f),
                                style: const TextStyle(fontSize: 11)),
                            backgroundColor: Colors.grey.withOpacity(0.1),
                            side: BorderSide.none,
                            padding: EdgeInsets.zero,
                          );
                        }).toList(),
                      ),
                    ],
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
