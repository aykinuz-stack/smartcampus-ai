import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class GunlukBultenPage extends ConsumerStatefulWidget {
  const GunlukBultenPage({super.key});

  @override
  ConsumerState<GunlukBultenPage> createState() => _GunlukBultenPageState();
}

class _GunlukBultenPageState extends ConsumerState<GunlukBultenPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetchBulten());
  }

  Future<Map<String, dynamic>> _fetchBulten() async {
    try {
      final r = await ref.read(apiClientProvider).get('/veli/gunluk-bulten');
      return Map<String, dynamic>.from(r.data as Map);
    } catch (_) {
      return _staticData();
    }
  }

  static Map<String, dynamic> _staticData() {
    return {
      'tarih': DateTime.now().toString().substring(0, 10),
      'ozet': 'Bugun okulumuzda dersler normal programda devam etmektedir. '
          'Hava durumu nedeniyle beden egitimi dersleri spor salonunda yapilacaktir.',
      'duyurular': [
        {
          'baslik': 'Veli Toplantisi',
          'icerik': '25 Nisan Cuma gunu saat 14:00\'da veli toplantisi yapilacaktir.',
          'onem': 'yuksek',
        },
        {
          'baslik': 'Kitap Fuari',
          'icerik': 'Okul kitap fuari 28 Nisan - 2 Mayis tarihleri arasinda acik olacaktir.',
          'onem': 'normal',
        },
      ],
      'yemek_menusu': {
        'ana_yemek': 'Tavuk Sote',
        'yan_yemek': 'Bulgur Pilavi',
        'corba': 'Mercimek Corbasi',
        'tatli': 'Meyve',
      },
      'etkinlikler': [
        {
          'saat': '10:00',
          'baslik': '23 Nisan Provalari',
          'yer': 'Konferans Salonu',
        },
        {
          'saat': '14:00',
          'baslik': 'Bilim Kulubu Toplantisi',
          'yer': 'Laboratuvar',
        },
        {
          'saat': '15:30',
          'baslik': 'Futbol Antrenman',
          'yer': 'Spor Sahasi',
        },
      ],
    };
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gunluk Bulten')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snap.data ?? {};

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Date header
                _buildDateHeader(data['tarih'] as String? ?? ''),
                const SizedBox(height: 16),

                // Bugunun Ozeti
                _buildSection(
                  color: AppColors.primary,
                  icon: Icons.summarize,
                  title: 'Bugunun Ozeti',
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Text(
                      data['ozet'] as String? ?? 'Bilgi yok',
                      style: const TextStyle(fontSize: 14, height: 1.5),
                    ),
                  ),
                ),
                const SizedBox(height: 12),

                // Duyurular
                _buildSection(
                  color: AppColors.warning,
                  icon: Icons.campaign,
                  title: 'Duyurular',
                  child: _buildDuyurular(
                      (data['duyurular'] as List?) ?? []),
                ),
                const SizedBox(height: 12),

                // Yemek Menusu
                _buildSection(
                  color: AppColors.success,
                  icon: Icons.restaurant_menu,
                  title: 'Yemek Menusu',
                  child: _buildYemekMenusu(
                      (data['yemek_menusu'] as Map?) ?? {}),
                ),
                const SizedBox(height: 12),

                // Etkinlikler
                _buildSection(
                  color: AppColors.info,
                  icon: Icons.event,
                  title: 'Etkinlikler',
                  child: _buildEtkinlikler(
                      (data['etkinlikler'] as List?) ?? []),
                ),
                const SizedBox(height: 24),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildDateHeader(String tarih) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.primary, AppColors.primaryLight],
        ),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          const Icon(Icons.calendar_today, color: Colors.white, size: 18),
          const SizedBox(width: 10),
          Text(
            tarih.isNotEmpty ? tarih : 'Bugun',
            style: const TextStyle(
                color: Colors.white,
                fontSize: 15,
                fontWeight: FontWeight.w600),
          ),
          const Spacer(),
          const Icon(Icons.newspaper, color: Colors.white70, size: 20),
        ],
      ),
    );
  }

  Widget _buildSection({
    required Color color,
    required IconData icon,
    required String title,
    required Widget child,
  }) {
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Colored left border effect via container
          Container(
            decoration: BoxDecoration(
              border: Border(left: BorderSide(color: color, width: 4)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(12, 12, 14, 0),
                  child: Row(
                    children: [
                      Icon(icon, color: color, size: 20),
                      const SizedBox(width: 8),
                      Text(title,
                          style: TextStyle(
                              fontSize: 15,
                              fontWeight: FontWeight.w700,
                              color: color)),
                    ],
                  ),
                ),
                child,
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDuyurular(List duyurular) {
    if (duyurular.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(14),
        child: Text('Bugun icin duyuru yok',
            style: TextStyle(color: AppColors.textSecondaryLight)),
      );
    }
    return Column(
      children: duyurular.map<Widget>((d) {
        final onem = (d['onem'] as String? ?? '').toLowerCase();
        final onemColor = onem == 'yuksek' ? AppColors.danger : AppColors.textSecondaryLight;

        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(
                onem == 'yuksek'
                    ? Icons.priority_high
                    : Icons.circle,
                size: onem == 'yuksek' ? 18 : 8,
                color: onemColor,
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(d['baslik'] as String? ?? '',
                        style: const TextStyle(
                            fontWeight: FontWeight.w600, fontSize: 14)),
                    const SizedBox(height: 2),
                    Text(d['icerik'] as String? ?? '',
                        style: TextStyle(
                            fontSize: 13, color: Colors.grey[700])),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildYemekMenusu(Map menu) {
    if (menu.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(14),
        child: Text('Menu bilgisi yok',
            style: TextStyle(color: AppColors.textSecondaryLight)),
      );
    }

    final items = <MapEntry<String, IconData>>[
      MapEntry('corba', Icons.soup_kitchen),
      MapEntry('ana_yemek', Icons.dinner_dining),
      MapEntry('yan_yemek', Icons.rice_bowl),
      MapEntry('tatli', Icons.cake),
    ];

    final labels = {
      'corba': 'Corba',
      'ana_yemek': 'Ana Yemek',
      'yan_yemek': 'Yan Yemek',
      'tatli': 'Tatli/Meyve',
    };

    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 8, 14, 14),
      child: Column(
        children: items.where((e) => menu[e.key] != null).map((e) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Row(
              children: [
                Icon(e.value, size: 18, color: AppColors.success),
                const SizedBox(width: 10),
                SizedBox(
                  width: 90,
                  child: Text('${labels[e.key]}:',
                      style: TextStyle(
                          fontSize: 13, color: Colors.grey[600])),
                ),
                Expanded(
                  child: Text(menu[e.key] as String? ?? '',
                      style: const TextStyle(
                          fontSize: 13, fontWeight: FontWeight.w500)),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildEtkinlikler(List etkinlikler) {
    if (etkinlikler.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(14),
        child: Text('Bugun icin etkinlik yok',
            style: TextStyle(color: AppColors.textSecondaryLight)),
      );
    }
    return Column(
      children: etkinlikler.map<Widget>((e) {
        final saat = e['saat'] as String? ?? '';
        final baslik = e['baslik'] as String? ?? '';
        final yer = e['yer'] as String? ?? '';

        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.info.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(saat,
                    style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: AppColors.info)),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(baslik,
                        style: const TextStyle(
                            fontSize: 13, fontWeight: FontWeight.w600)),
                    if (yer.isNotEmpty)
                      Text(yer,
                          style: TextStyle(
                              fontSize: 12, color: Colors.grey[600])),
                  ],
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
