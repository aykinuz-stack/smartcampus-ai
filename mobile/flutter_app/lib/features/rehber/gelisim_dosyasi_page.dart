import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Ogrenci gelisim dosyasi / portfolyo sayfasi.
/// Her ogrenci icin rehberlik notlari, gelisim alanlari ve guclu yonleri gosterir.
class GelisimDosyasiPage extends ConsumerStatefulWidget {
  const GelisimDosyasiPage({super.key});

  @override
  ConsumerState<GelisimDosyasiPage> createState() =>
      _GelisimDosyasiPageState();
}

class _GelisimDosyasiPageState extends ConsumerState<GelisimDosyasiPage> {
  List<Map<String, dynamic>> _students = [];
  bool _loading = true;
  String _search = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/gelisim-dosyasi');
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
          'rehber_notlari': [
            {
              'tarih': '2026-04-15',
              'not':
                  'Akademik basarisinda dusus gozlemlendi. Motivasyon calismasi yapildi.',
            },
            {
              'tarih': '2026-03-22',
              'not':
                  'Aile gorusmesi gerceklestirildi. Evde calisma ortami duzenlendi.',
            },
          ],
          'gelisim_alanlari': [
            'Zaman yonetimi',
            'Ders calisma aliskanliklari',
            'Odaklanma',
          ],
          'guclu_yonleri': ['Sosyal iliskiler', 'Spor', 'Yaraticilik'],
        },
        {
          'id': '2',
          'ad_soyad': 'Elif Kara',
          'sinif': '10',
          'sube': 'B',
          'rehber_notlari': [
            {
              'tarih': '2026-04-10',
              'not':
                  'Sinav kaygisi hakkinda gorusme yapildi. Nefes egzersizleri ogretildi.',
            },
          ],
          'gelisim_alanlari': ['Sinav kaygisi yonetimi', 'Ozguven'],
          'guclu_yonleri': [
            'Akademik basari',
            'Liderlik',
            'Sorumlu davranis',
          ],
        },
        {
          'id': '3',
          'ad_soyad': 'Mehmet Demir',
          'sinif': '11',
          'sube': 'A',
          'rehber_notlari': [
            {
              'tarih': '2026-04-12',
              'not':
                  'Universite tercihleri hakkinda bilgilendirme yapildi. Muhendislik alanlarina ilgi duyuyor.',
            },
            {
              'tarih': '2026-03-28',
              'not':
                  'YKS hazirlik plani olusturuldu. Haftalik takip baslatildi.',
            },
            {
              'tarih': '2026-03-10',
              'not':
                  'Kariyer envanter testi uygulanarak sonuclar paylasidi.',
            },
          ],
          'gelisim_alanlari': ['Karar verme becerisi', 'Stres yonetimi'],
          'guclu_yonleri': [
            'Matematik yetkinligi',
            'Analitik dusunme',
            'Azimli calisma',
          ],
        },
        {
          'id': '4',
          'ad_soyad': 'Zeynep Celik',
          'sinif': '9',
          'sube': 'C',
          'rehber_notlari': [
            {
              'tarih': '2026-04-18',
              'not':
                  'Arkadaslik iliskileri hakkinda destek gorusmesi yapildi.',
            },
          ],
          'gelisim_alanlari': [
            'Sosyal beceriler',
            'Grup ici iletisim',
          ],
          'guclu_yonleri': ['Resim yetenegı', 'Empati', 'Muzik'],
        },
        {
          'id': '5',
          'ad_soyad': 'Can Ozturk',
          'sinif': '12',
          'sube': 'A',
          'rehber_notlari': [
            {
              'tarih': '2026-04-05',
              'not':
                  'YKS motivasyon gorusmesi. Hedef puan belirlendi. Haftalik kontrol planlandirildi.',
            },
          ],
          'gelisim_alanlari': ['Hedef belirleme', 'Planlama'],
          'guclu_yonleri': [
            'Fen bilimleri',
            'Takim calismasi',
            'Iletisim becerisi',
          ],
        },
      ];

  List<Map<String, dynamic>> get _filtered {
    if (_search.isEmpty) return _students;
    final q = _search.toLowerCase();
    return _students.where((s) {
      final ad = (s['ad_soyad'] as String? ?? '').toLowerCase();
      final sinif = '${s['sinif']}/${s['sube']}'.toLowerCase();
      return ad.contains(q) || sinif.contains(q);
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gelisim Dosyasi'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: Column(
                children: [
                  // -- Search bar --
                  Padding(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    child: TextField(
                      onChanged: (v) => setState(() => _search = v),
                      decoration: InputDecoration(
                        hintText: 'Ogrenci ara (ad, sinif)...',
                        prefixIcon:
                            const Icon(Icons.search, color: AppColors.info),
                        filled: true,
                        fillColor: AppColors.info.withOpacity(0.06),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: BorderSide.none,
                        ),
                        contentPadding:
                            const EdgeInsets.symmetric(vertical: 0, horizontal: 14),
                      ),
                    ),
                  ),

                  // -- Student count --
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16),
                    child: Row(
                      children: [
                        Icon(Icons.folder_shared,
                            size: 16, color: AppColors.primary.withOpacity(0.7)),
                        const SizedBox(width: 6),
                        Text(
                          '${_filtered.length} ogrenci dosyasi',
                          style: const TextStyle(
                              fontSize: 13,
                              color: AppColors.textSecondaryDark),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 6),

                  // -- Student list --
                  Expanded(
                    child: _filtered.isEmpty
                        ? const Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.search_off,
                                    size: 48, color: Colors.grey),
                                SizedBox(height: 12),
                                Text('Ogrenci bulunamadi',
                                    style: TextStyle(
                                        color: AppColors.textSecondaryDark)),
                              ],
                            ),
                          )
                        : ListView.builder(
                            padding: const EdgeInsets.fromLTRB(14, 4, 14, 20),
                            itemCount: _filtered.length,
                            itemBuilder: (_, i) =>
                                _StudentDosyaCard(student: _filtered[i]),
                          ),
                  ),
                ],
              ),
            ),
    );
  }
}

// ---------------------------------------------------------------------------
// Student Dosya Card (ExpansionTile)
// ---------------------------------------------------------------------------
class _StudentDosyaCard extends StatelessWidget {
  final Map<String, dynamic> student;

  const _StudentDosyaCard({required this.student});

  @override
  Widget build(BuildContext context) {
    final notlar = List<Map<String, dynamic>>.from(
      (student['rehber_notlari'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map)),
    );
    final gelisimAlanlari =
        List<String>.from(student['gelisim_alanlari'] ?? []);
    final gucluYonleri = List<String>.from(student['guclu_yonleri'] ?? []);

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: ExpansionTile(
        tilePadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
        childrenPadding: const EdgeInsets.fromLTRB(14, 0, 14, 14),
        leading: CircleAvatar(
          backgroundColor: AppColors.primary.withOpacity(0.12),
          child: Text(
            (student['ad_soyad'] as String? ?? '?')[0],
            style: const TextStyle(
              color: AppColors.primary,
              fontWeight: FontWeight.bold,
              fontSize: 16,
            ),
          ),
        ),
        title: Text(
          student['ad_soyad'] as String? ?? '-',
          style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
        ),
        subtitle: Row(
          children: [
            Text(
              '${student['sinif']}/${student['sube']}',
              style: const TextStyle(
                  fontSize: 12, color: AppColors.textSecondaryDark),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: AppColors.info.withOpacity(0.1),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                '${notlar.length} not',
                style: const TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: AppColors.info),
              ),
            ),
          ],
        ),
        children: [
          // -- Guclu Yonleri --
          if (gucluYonleri.isNotEmpty) ...[
            _SectionHeader(
                icon: Icons.star, label: 'Guclu Yonleri', color: AppColors.gold),
            const SizedBox(height: 6),
            Wrap(
              spacing: 6,
              runSpacing: 4,
              children: gucluYonleri.map((g) {
                return Chip(
                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  visualDensity: VisualDensity.compact,
                  label: Text(g, style: const TextStyle(fontSize: 11)),
                  backgroundColor: AppColors.success.withOpacity(0.1),
                  side: BorderSide(
                      color: AppColors.success.withOpacity(0.3), width: 0.5),
                  padding: EdgeInsets.zero,
                );
              }).toList(),
            ),
            const SizedBox(height: 12),
          ],

          // -- Gelisim Alanlari --
          if (gelisimAlanlari.isNotEmpty) ...[
            _SectionHeader(
                icon: Icons.trending_up,
                label: 'Gelisim Alanlari',
                color: AppColors.warning),
            const SizedBox(height: 6),
            Wrap(
              spacing: 6,
              runSpacing: 4,
              children: gelisimAlanlari.map((g) {
                return Chip(
                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  visualDensity: VisualDensity.compact,
                  label: Text(g, style: const TextStyle(fontSize: 11)),
                  backgroundColor: AppColors.warning.withOpacity(0.1),
                  side: BorderSide(
                      color: AppColors.warning.withOpacity(0.3), width: 0.5),
                  padding: EdgeInsets.zero,
                );
              }).toList(),
            ),
            const SizedBox(height: 12),
          ],

          // -- Rehber Notlari --
          if (notlar.isNotEmpty) ...[
            _SectionHeader(
                icon: Icons.notes,
                label: 'Rehber Notlari',
                color: AppColors.info),
            const SizedBox(height: 6),
            ...notlar.map((n) {
              return Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.info.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(8),
                  border: Border(
                    left: BorderSide(color: AppColors.info, width: 3),
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.calendar_today,
                            size: 12, color: AppColors.textSecondaryDark),
                        const SizedBox(width: 4),
                        Text(
                          n['tarih'] as String? ?? '-',
                          style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: AppColors.textSecondaryDark),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      n['not'] as String? ?? '',
                      style: const TextStyle(fontSize: 13),
                    ),
                  ],
                ),
              );
            }),
          ],
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Section Header
// ---------------------------------------------------------------------------
class _SectionHeader extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;

  const _SectionHeader({
    required this.icon,
    required this.label,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 16, color: color),
        const SizedBox(width: 6),
        Text(
          label,
          style: TextStyle(
              fontSize: 13, fontWeight: FontWeight.w600, color: color),
        ),
      ],
    );
  }
}
