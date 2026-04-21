import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// BEP (Bireysellestirilmis Egitim Plani) sayfasi - Rehber ogretmen gorunumu.
/// Ozel egitim planlari: ogrenci, engel turu, hedefler, durum.
class BepPage extends ConsumerStatefulWidget {
  const BepPage({super.key});

  @override
  ConsumerState<BepPage> createState() => _BepPageState();
}

class _BepPageState extends ConsumerState<BepPage> {
  List<Map<String, dynamic>> _plans = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/bep-planlari');
      final data = resp.data;
      if (data is List) {
        _plans = List<Map<String, dynamic>>.from(
          data.map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _plans = _staticData();
      }
    } catch (_) {
      _plans = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  List<Map<String, dynamic>> _staticData() => [
        {
          'id': 'bep_001',
          'ogrenci_adi': 'Kerem Aksoy',
          'sinif': '6-A',
          'engel_turu': 'Ogrenim Guclugu (Disleksi)',
          'plan_tarihi': '2026-03-01',
          'durum': 'aktif',
          'hedefler': [
            {
              'baslik': 'Okuma hizini artirma',
              'aciklama':
                  'Dakikada 60 kelime okuma hedefi (mevcut: 35 kelime)',
              'tamamlanma': 40,
            },
            {
              'baslik': 'Yazma becerisi gelistirme',
              'aciklama': 'Duzgun cumle yapisi ile 5 cumlelik paragraf yazma',
              'tamamlanma': 55,
            },
            {
              'baslik': 'Matematik problem cozme',
              'aciklama':
                  'Sozel problemleri anlama ve dogru islem secimi yapma',
              'tamamlanma': 30,
            },
            {
              'baslik': 'Oz-duzenleme becerisi',
              'aciklama': 'Ders sirasinda 20 dk odaklanma suresi',
              'tamamlanma': 60,
            },
          ],
        },
        {
          'id': 'bep_002',
          'ogrenci_adi': 'Sude Yildiz',
          'sinif': '4-B',
          'engel_turu': 'Dikkat Eksikligi (DEHB)',
          'plan_tarihi': '2026-02-15',
          'durum': 'revize',
          'hedefler': [
            {
              'baslik': 'Dikkat suresi uzatma',
              'aciklama': 'Ders icinde 15 dk kesintisiz odaklanma',
              'tamamlanma': 50,
            },
            {
              'baslik': 'Gorev tamamlama',
              'aciklama':
                  'Verilen odevlerin %80 ini zamaninda teslim etme',
              'tamamlanma': 35,
            },
            {
              'baslik': 'Sosyal etkilesim',
              'aciklama': 'Grup calismalarina aktif katilim',
              'tamamlanma': 70,
            },
          ],
        },
        {
          'id': 'bep_003',
          'ogrenci_adi': 'Emre Korkmaz',
          'sinif': '8-C',
          'engel_turu': 'Otizm Spektrum Bozuklugu',
          'plan_tarihi': '2025-09-10',
          'durum': 'tamamlandi',
          'hedefler': [
            {
              'baslik': 'Iletisim becerisi',
              'aciklama': 'Gunluk 10 sosyal etkilesim baslatma',
              'tamamlanma': 100,
            },
            {
              'baslik': 'Rutin degisikliklerine uyum',
              'aciklama': 'Program degisikliklerinde sakin kalma',
              'tamamlanma': 90,
            },
            {
              'baslik': 'Akademik ilerleme',
              'aciklama': 'Matematik ve Turkce derslerinde sinif seviyesi',
              'tamamlanma': 85,
            },
          ],
        },
      ];

  Color _durumColor(String durum) {
    switch (durum) {
      case 'aktif':
        return AppColors.success;
      case 'revize':
        return AppColors.warning;
      case 'tamamlandi':
        return AppColors.info;
      default:
        return Colors.grey;
    }
  }

  String _durumLabel(String durum) {
    switch (durum) {
      case 'aktif':
        return 'Aktif';
      case 'revize':
        return 'Revize';
      case 'tamamlandi':
        return 'Tamamlandi';
      default:
        return durum;
    }
  }

  IconData _durumIcon(String durum) {
    switch (durum) {
      case 'aktif':
        return Icons.play_circle_outline;
      case 'revize':
        return Icons.edit_note;
      case 'tamamlandi':
        return Icons.check_circle_outline;
      default:
        return Icons.info_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    // Ozet sayilari
    final aktifCount = _plans.where((p) => p['durum'] == 'aktif').length;
    final revizeCount = _plans.where((p) => p['durum'] == 'revize').length;
    final tamamCount =
        _plans.where((p) => p['durum'] == 'tamamlandi').length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('BEP Planlari'),
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
                      _StatusBadge(
                        label: 'Aktif',
                        count: aktifCount,
                        color: AppColors.success,
                        icon: Icons.play_circle_outline,
                      ),
                      const SizedBox(width: 8),
                      _StatusBadge(
                        label: 'Revize',
                        count: revizeCount,
                        color: AppColors.warning,
                        icon: Icons.edit_note,
                      ),
                      const SizedBox(width: 8),
                      _StatusBadge(
                        label: 'Tamamlandi',
                        count: tamamCount,
                        color: AppColors.info,
                        icon: Icons.check_circle_outline,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // -- Plan listesi --
                  if (_plans.isEmpty)
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Center(
                        child: Text('BEP plani bulunamadi',
                            style: TextStyle(
                                color: AppColors.textSecondaryDark)),
                      ),
                    )
                  else
                    ..._plans.map((p) => _BepPlanCard(
                          plan: p,
                          durumColor: _durumColor(p['durum'] as String),
                          durumLabel: _durumLabel(p['durum'] as String),
                          durumIcon: _durumIcon(p['durum'] as String),
                        )),
                ],
              ),
            ),
    );
  }
}

// ---------------------------------------------------------------------------
// Status Badge
// ---------------------------------------------------------------------------
class _StatusBadge extends StatelessWidget {
  final String label;
  final int count;
  final Color color;
  final IconData icon;

  const _StatusBadge({
    required this.label,
    required this.count,
    required this.color,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 4),
            Text(
              '$count',
              style: TextStyle(
                  fontSize: 22, fontWeight: FontWeight.bold, color: color),
            ),
            const SizedBox(height: 2),
            Text(label,
                style: TextStyle(
                    fontSize: 11, color: color.withOpacity(0.8))),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// BEP Plan Card (ExpansionTile ile hedefler)
// ---------------------------------------------------------------------------
class _BepPlanCard extends StatelessWidget {
  final Map<String, dynamic> plan;
  final Color durumColor;
  final String durumLabel;
  final IconData durumIcon;

  const _BepPlanCard({
    required this.plan,
    required this.durumColor,
    required this.durumLabel,
    required this.durumIcon,
  });

  @override
  Widget build(BuildContext context) {
    final hedefler = List<Map<String, dynamic>>.from(
      (plan['hedefler'] as List? ?? [])
          .map((e) => Map<String, dynamic>.from(e as Map)),
    );
    final hedefSayisi = hedefler.length;
    final tamamlananOrt = hedefler.isEmpty
        ? 0.0
        : hedefler.fold<double>(
                0.0,
                (sum, h) =>
                    sum + ((h['tamamlanma'] as num?)?.toDouble() ?? 0.0)) /
            hedefler.length;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          // Renkli ust serit
          Container(height: 4, color: durumColor),
          ExpansionTile(
            tilePadding:
                const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
            childrenPadding:
                const EdgeInsets.only(left: 14, right: 14, bottom: 14),
            leading: CircleAvatar(
              radius: 20,
              backgroundColor: durumColor.withOpacity(0.12),
              child: Icon(durumIcon, color: durumColor, size: 22),
            ),
            title: Text(
              plan['ogrenci_adi'] as String? ?? '-',
              style:
                  const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 4),
                Text(
                  '${plan['sinif']} - ${plan['engel_turu']}',
                  style: const TextStyle(
                      fontSize: 12, color: AppColors.textSecondaryDark),
                ),
                const SizedBox(height: 6),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: durumColor.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        durumLabel,
                        style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: durumColor),
                      ),
                    ),
                    const SizedBox(width: 8),
                    const Icon(Icons.flag_outlined,
                        size: 13, color: AppColors.textSecondaryDark),
                    const SizedBox(width: 3),
                    Text(
                      '$hedefSayisi hedef',
                      style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textSecondaryDark),
                    ),
                    const SizedBox(width: 8),
                    const Icon(Icons.calendar_today,
                        size: 13, color: AppColors.textSecondaryDark),
                    const SizedBox(width: 3),
                    Text(
                      plan['plan_tarihi'] as String? ?? '-',
                      style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textSecondaryDark),
                    ),
                  ],
                ),
                const SizedBox(height: 6),
                // Genel ilerleme bar
                Row(
                  children: [
                    Expanded(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(4),
                        child: LinearProgressIndicator(
                          value: tamamlananOrt / 100.0,
                          minHeight: 6,
                          backgroundColor: durumColor.withOpacity(0.15),
                          valueColor:
                              AlwaysStoppedAnimation<Color>(durumColor),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      '%${tamamlananOrt.toStringAsFixed(0)}',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: durumColor,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            children: [
              const Divider(),
              const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Hedefler',
                  style: TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w600),
                ),
              ),
              const SizedBox(height: 8),
              ...hedefler.map((h) {
                final tamamlanma =
                    (h['tamamlanma'] as num?)?.toInt() ?? 0;
                Color progColor;
                if (tamamlanma >= 80) {
                  progColor = AppColors.success;
                } else if (tamamlanma >= 50) {
                  progColor = AppColors.warning;
                } else {
                  progColor = AppColors.danger;
                }
                return Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Theme.of(context)
                        .scaffoldBackgroundColor
                        .withOpacity(0.5),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                        color: Colors.grey.withOpacity(0.2)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        h['baslik'] as String? ?? '-',
                        style: const TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        h['aciklama'] as String? ?? '',
                        style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.textSecondaryDark),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Expanded(
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(3),
                              child: LinearProgressIndicator(
                                value: tamamlanma / 100.0,
                                minHeight: 5,
                                backgroundColor:
                                    progColor.withOpacity(0.15),
                                valueColor:
                                    AlwaysStoppedAnimation<Color>(
                                        progColor),
                              ),
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text(
                            '%$tamamlanma',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: progColor,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              }),
            ],
          ),
        ],
      ),
    );
  }
}
