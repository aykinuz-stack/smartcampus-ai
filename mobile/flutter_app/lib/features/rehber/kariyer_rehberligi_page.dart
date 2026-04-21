import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Kariyer rehberligi sayfasi - Rehber ogretmen gorunumu.
/// Mesleki ilgi envanterleri, universite rehberi, staj ve kariyer gunleri.
class KariyerRehberligiPage extends ConsumerStatefulWidget {
  const KariyerRehberligiPage({super.key});

  @override
  ConsumerState<KariyerRehberligiPage> createState() =>
      _KariyerRehberligiPageState();
}

class _KariyerRehberligiPageState
    extends ConsumerState<KariyerRehberligiPage> {
  Map<String, List<Map<String, dynamic>>> _sections = {};
  bool _loading = true;
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/kariyer-rehberligi');
      final data = resp.data;
      if (data is Map) {
        _sections = {};
        for (final key in data.keys) {
          final items = data[key];
          if (items is List) {
            _sections[key as String] = List<Map<String, dynamic>>.from(
              items.map((e) => Map<String, dynamic>.from(e as Map)),
            );
          }
        }
      } else {
        _sections = _staticData();
      }
    } catch (_) {
      _sections = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  Map<String, List<Map<String, dynamic>>> _staticData() => {
        'mesleki_ilgi': [
          {
            'id': 'mi_01',
            'baslik': 'Holland Mesleki Ilgi Envanteri',
            'aciklama': '6 mesleki kisilik tipi analizi',
            'katilimci_sayisi': 45,
            'tarih': '2026-04-10',
          },
          {
            'id': 'mi_02',
            'baslik': 'Coklu Zeka Envanteri',
            'aciklama': '8 zeka alani degerlendirmesi',
            'katilimci_sayisi': 38,
            'tarih': '2026-04-08',
          },
          {
            'id': 'mi_03',
            'baslik': 'Kisilik Tipleri Testi (MBTI)',
            'aciklama': '16 kisilik tipi belirleme',
            'katilimci_sayisi': 52,
            'tarih': '2026-03-25',
          },
          {
            'id': 'mi_04',
            'baslik': 'Mesleki Degerler Olcegi',
            'aciklama': 'Calisma degerleri ve oncelikler',
            'katilimci_sayisi': 30,
            'tarih': '2026-03-18',
          },
        ],
        'universite_rehberi': [
          {
            'id': 'ur_01',
            'baslik': 'YKS Puan Turleri Rehberi',
            'aciklama': 'TYT / AYT puan turleri ve bolum eslesmesi',
            'guncelleme': '2026-04-15',
          },
          {
            'id': 'ur_02',
            'baslik': 'Universite Taban Puanlari 2025',
            'aciklama': 'Tum universitelerin guncel taban puanlari',
            'guncelleme': '2026-03-01',
          },
          {
            'id': 'ur_03',
            'baslik': 'Burs Imkanlari',
            'aciklama': 'Devlet ve ozel universite burslari',
            'guncelleme': '2026-02-20',
          },
          {
            'id': 'ur_04',
            'baslik': 'Yurt Disi Universite Basvuru',
            'aciklama': 'AB, ABD, Ingiltere basvuru surecleri',
            'guncelleme': '2026-01-10',
          },
          {
            'id': 'ur_05',
            'baslik': 'Tercih Robotu',
            'aciklama': 'YKS puanina gore universite/bolum onerisi',
            'guncelleme': '2026-04-01',
          },
        ],
        'staj_programlari': [
          {
            'id': 'sp_01',
            'baslik': 'Yaz Staj Programi - Teknoloji',
            'aciklama': 'Yazilim, veri bilimi, siber guvenlik stajlari',
            'kontenjan': 20,
            'son_basvuru': '2026-05-15',
          },
          {
            'id': 'sp_02',
            'baslik': 'Saglik Sektoru Gozlem Programi',
            'aciklama': 'Hastane ve klinik gozlem firsatlari',
            'kontenjan': 10,
            'son_basvuru': '2026-05-20',
          },
          {
            'id': 'sp_03',
            'baslik': 'Is Dunyasi Mentor Eslestirme',
            'aciklama': 'Sektorde deneyimli mentorlerle eslestirme',
            'kontenjan': 15,
            'son_basvuru': '2026-06-01',
          },
        ],
        'kariyer_gunleri': [
          {
            'id': 'kg_01',
            'baslik': 'Muhendislik Kariyer Gunu',
            'aciklama': 'Insaat, makine, elektrik muhendisleri',
            'tarih': '2026-05-10',
            'konusmaci_sayisi': 5,
          },
          {
            'id': 'kg_02',
            'baslik': 'Saglik Meslekleri Tanitimi',
            'aciklama': 'Doktor, hemsire, eczaci meslekleri',
            'tarih': '2026-05-17',
            'konusmaci_sayisi': 4,
          },
          {
            'id': 'kg_03',
            'baslik': 'Hukuk ve Sosyal Bilimler',
            'aciklama': 'Avukat, hakim, sosyolog kariyer yollari',
            'tarih': '2026-05-24',
            'konusmaci_sayisi': 3,
          },
          {
            'id': 'kg_04',
            'baslik': 'Girisimcilik Paneli',
            'aciklama': 'Basarili girisimcilerle sohbet',
            'tarih': '2026-06-07',
            'konusmaci_sayisi': 6,
          },
        ],
      };

  static const _sectionMeta = <String, _SectionInfo>{
    'mesleki_ilgi': _SectionInfo(
      title: 'Mesleki Ilgi Envanterleri',
      icon: Icons.psychology,
      color: AppColors.primary,
    ),
    'universite_rehberi': _SectionInfo(
      title: 'Universite Rehberi',
      icon: Icons.school,
      color: AppColors.info,
    ),
    'staj_programlari': _SectionInfo(
      title: 'Staj Programlari',
      icon: Icons.work_outline,
      color: AppColors.success,
    ),
    'kariyer_gunleri': _SectionInfo(
      title: 'Kariyer Gunleri',
      icon: Icons.event,
      color: AppColors.warning,
    ),
  };

  void _showSectionItems(String key, List<Map<String, dynamic>> items) {
    final meta = _sectionMeta[key];
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        maxChildSize: 0.9,
        minChildSize: 0.3,
        expand: false,
        builder: (_, scrollCtrl) => Column(
          children: [
            const SizedBox(height: 12),
            Container(
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Row(
                children: [
                  Icon(meta?.icon ?? Icons.list,
                      color: meta?.color ?? AppColors.primary),
                  const SizedBox(width: 10),
                  Text(
                    meta?.title ?? key,
                    style: const TextStyle(
                        fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 8),
            const Divider(),
            Expanded(
              child: ListView.builder(
                controller: scrollCtrl,
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                itemCount: items.length,
                itemBuilder: (_, i) {
                  final item = items[i];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 8),
                    child: Padding(
                      padding: const EdgeInsets.all(14),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            item['baslik'] as String? ?? '-',
                            style: const TextStyle(
                                fontSize: 15, fontWeight: FontWeight.w600),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            item['aciklama'] as String? ?? '',
                            style: const TextStyle(
                                fontSize: 13,
                                color: AppColors.textSecondaryDark),
                          ),
                          const SizedBox(height: 8),
                          Wrap(
                            spacing: 12,
                            children: [
                              if (item.containsKey('katilimci_sayisi'))
                                _InfoChip(
                                  icon: Icons.people,
                                  label:
                                      '${item['katilimci_sayisi']} katilimci',
                                ),
                              if (item.containsKey('kontenjan'))
                                _InfoChip(
                                  icon: Icons.group_add,
                                  label: '${item['kontenjan']} kontenjan',
                                ),
                              if (item.containsKey('konusmaci_sayisi'))
                                _InfoChip(
                                  icon: Icons.mic,
                                  label:
                                      '${item['konusmaci_sayisi']} konusmaci',
                                ),
                              if (item.containsKey('tarih'))
                                _InfoChip(
                                  icon: Icons.calendar_today,
                                  label: item['tarih'] as String,
                                ),
                              if (item.containsKey('son_basvuru'))
                                _InfoChip(
                                  icon: Icons.timer,
                                  label:
                                      'Son: ${item['son_basvuru'] as String}',
                                ),
                              if (item.containsKey('guncelleme'))
                                _InfoChip(
                                  icon: Icons.update,
                                  label: item['guncelleme'] as String,
                                ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Search filtering
    final filteredSections = <String, List<Map<String, dynamic>>>{};
    for (final entry in _sections.entries) {
      if (_searchQuery.isEmpty) {
        filteredSections[entry.key] = entry.value;
      } else {
        final q = _searchQuery.toLowerCase();
        final filtered = entry.value.where((item) {
          final baslik =
              (item['baslik'] as String? ?? '').toLowerCase();
          final aciklama =
              (item['aciklama'] as String? ?? '').toLowerCase();
          return baslik.contains(q) || aciklama.contains(q);
        }).toList();
        if (filtered.isNotEmpty) {
          filteredSections[entry.key] = filtered;
        }
      }
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Kariyer Rehberligi'),
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
                  // -- Arama cubugu --
                  TextField(
                    decoration: InputDecoration(
                      hintText: 'Ara...',
                      prefixIcon: const Icon(Icons.search),
                      filled: true,
                      fillColor: Theme.of(context).cardColor,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                          vertical: 0, horizontal: 16),
                    ),
                    onChanged: (v) => setState(() => _searchQuery = v),
                  ),
                  const SizedBox(height: 16),

                  // -- Bolum kartlari --
                  if (filteredSections.isEmpty)
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Center(
                        child: Text('Sonuc bulunamadi',
                            style:
                                TextStyle(color: AppColors.textSecondaryDark)),
                      ),
                    )
                  else
                    ...filteredSections.entries.map((entry) {
                      final key = entry.key;
                      final items = entry.value;
                      final meta = _sectionMeta[key];
                      return _SectionCard(
                        title: meta?.title ?? key,
                        icon: meta?.icon ?? Icons.list,
                        color: meta?.color ?? AppColors.primary,
                        itemCount: items.length,
                        onTap: () => _showSectionItems(key, items),
                      );
                    }),
                ],
              ),
            ),
    );
  }
}

// ---------------------------------------------------------------------------
// Section metadata
// ---------------------------------------------------------------------------
class _SectionInfo {
  final String title;
  final IconData icon;
  final Color color;

  const _SectionInfo({
    required this.title,
    required this.icon,
    required this.color,
  });
}

// ---------------------------------------------------------------------------
// Section Card
// ---------------------------------------------------------------------------
class _SectionCard extends StatelessWidget {
  final String title;
  final IconData icon;
  final Color color;
  final int itemCount;
  final VoidCallback onTap;

  const _SectionCard({
    required this.title,
    required this.icon,
    required this.color,
    required this.itemCount,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Row(
            children: [
              Container(
                width: 52,
                height: 52,
                decoration: BoxDecoration(
                  color: color.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                          fontSize: 16, fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '$itemCount kayit',
                      style: const TextStyle(
                          fontSize: 13, color: AppColors.textSecondaryDark),
                    ),
                  ],
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  '$itemCount',
                  style: TextStyle(
                      color: color,
                      fontWeight: FontWeight.bold,
                      fontSize: 15),
                ),
              ),
              const SizedBox(width: 4),
              Icon(Icons.chevron_right, color: color.withOpacity(0.6)),
            ],
          ),
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Info Chip
// ---------------------------------------------------------------------------
class _InfoChip extends StatelessWidget {
  final IconData icon;
  final String label;

  const _InfoChip({required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 13, color: AppColors.textSecondaryDark),
        const SizedBox(width: 4),
        Text(label,
            style: const TextStyle(
                fontSize: 12, color: AppColors.textSecondaryDark)),
      ],
    );
  }
}
