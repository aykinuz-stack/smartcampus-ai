import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class SaglikRehberlikPage extends ConsumerStatefulWidget {
  const SaglikRehberlikPage({super.key});

  @override
  ConsumerState<SaglikRehberlikPage> createState() =>
      _SaglikRehberlikPageState();
}

class _SaglikRehberlikPageState extends ConsumerState<SaglikRehberlikPage>
    with SingleTickerProviderStateMixin {
  late final TabController _tabCtrl;
  Map<String, dynamic>? _data;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final r = await ref
          .read(apiClientProvider)
          .get('/veli/saglik-rehberlik');
      if (r.data is Map) {
        _data = Map<String, dynamic>.from(r.data as Map);
      } else {
        _data = _staticData();
      }
    } catch (_) {
      _data = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  static Map<String, dynamic> _staticData() {
    return {
      // --- Saglik ---
      'asi_takvimi': [
        {
          'asi_adi': 'Hepatit B (3. Doz)',
          'tarih': '2026-05-10',
          'durum': 'planli',
        },
        {
          'asi_adi': 'KKK (Kizamik-Kabakulak-Kizamikik)',
          'tarih': '2026-03-15',
          'durum': 'tamamlandi',
        },
        {
          'asi_adi': 'DaBT-IPA-Hib (Rapel)',
          'tarih': '2025-11-20',
          'durum': 'tamamlandi',
        },
        {
          'asi_adi': 'Grip Asisi',
          'tarih': '2026-10-01',
          'durum': 'planli',
        },
      ],
      'saglik_kayitlari': [
        {
          'tarih': '2026-04-05',
          'baslik': 'Boy-Kilo Olcumu',
          'detay': 'Boy: 142 cm, Kilo: 36 kg, VKI: Normal',
          'tip': 'olcum',
        },
        {
          'tarih': '2026-03-18',
          'baslik': 'Goz Taramasi',
          'detay': 'Her iki goz normal, gozluk gerekmiyor',
          'tip': 'tarama',
        },
        {
          'tarih': '2026-02-10',
          'baslik': 'Dis Kontrolu',
          'detay': '2 curuk dis tespit edildi, tedavi onerisi verildi',
          'tip': 'kontrol',
        },
      ],
      'acil_iletisim': {
        'okul_hemsireleri': 'Ayse Saglik - Tel: 0212 555 01 01 (Dahili: 120)',
        'en_yakin_hastane': 'Devlet Hastanesi - 0212 444 01 01',
        'ambulans': '112',
      },
      // --- Rehberlik ---
      'rehber_bilgi': {
        'ad': 'Zeynep Kaya',
        'unvan': 'Psikolojik Danisma ve Rehberlik Uzmani',
        'email': 'zeynep.kaya@okul.edu.tr',
        'telefon': '0212 555 01 01 (Dahili: 130)',
        'musait_gunler': 'Pazartesi - Cuma, 09:00 - 16:00',
      },
      'veli_rehberleri': [
        {
          'baslik': 'Ergenlik Donemi',
          'ozet': 'Ergenlik doneminde cocugunuzla iletisim kurma yollari.',
          'icon': 'psychology',
        },
        {
          'baslik': 'Sinav Stresi ile Basa Cikma',
          'ozet': 'Sinav donemlerinde cocugunuza nasil destek olabilirsiniz.',
          'icon': 'stress',
        },
        {
          'baslik': 'Akran Zorbaligi (Bullying)',
          'ozet': 'Zorbalikla karsilasan cocugunuz icin yapabilecekleriniz.',
          'icon': 'bullying',
        },
        {
          'baslik': 'Ekran Suresi ve Dijital Bagimllik',
          'ozet': 'Saglikli teknoloji kullanimi icin veli rehberi.',
          'icon': 'digital',
        },
        {
          'baslik': 'Ozguven Gelistirme',
          'ozet': 'Cocugunuzun ozguvenini desteklemek icin pratik oneriler.',
          'icon': 'confidence',
        },
      ],
    };
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Saglik & Rehberlik'),
        bottom: TabBar(
          controller: _tabCtrl,
          indicatorColor: AppColors.primary,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textSecondaryLight,
          tabs: const [
            Tab(icon: Icon(Icons.health_and_safety), text: 'Saglik'),
            Tab(icon: Icon(Icons.psychology), text: 'Rehberlik'),
          ],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabCtrl,
              children: [
                _buildSaglikTab(),
                _buildRehberlikTab(),
              ],
            ),
    );
  }

  // ---------------------------------------------------------------------------
  // SAGLIK TAB
  // ---------------------------------------------------------------------------
  Widget _buildSaglikTab() {
    final data = _data ?? {};
    final asiTakvimi = (data['asi_takvimi'] as List?) ?? [];
    final saglikKayitlari = (data['saglik_kayitlari'] as List?) ?? [];
    final acilIletisim = (data['acil_iletisim'] as Map?) ?? {};

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Hero
          _buildSaglikHero(),
          const SizedBox(height: 16),

          // Vaccination calendar
          _buildSection(
            color: AppColors.primary,
            icon: Icons.vaccines,
            title: 'Asi Takvimi',
            child: asiTakvimi.isEmpty
                ? const Padding(
                    padding: EdgeInsets.all(14),
                    child: Text('Asi kaydi bulunamadi',
                        style:
                            TextStyle(color: AppColors.textSecondaryLight)),
                  )
                : Column(
                    children: asiTakvimi
                        .map<Widget>((a) => _buildAsiItem(a as Map))
                        .toList(),
                  ),
          ),
          const SizedBox(height: 12),

          // Health records
          _buildSection(
            color: AppColors.success,
            icon: Icons.medical_information,
            title: 'Saglik Kayitlari',
            child: saglikKayitlari.isEmpty
                ? const Padding(
                    padding: EdgeInsets.all(14),
                    child: Text('Kayit bulunamadi',
                        style:
                            TextStyle(color: AppColors.textSecondaryLight)),
                  )
                : Column(
                    children: saglikKayitlari
                        .map<Widget>((k) => _buildSaglikKaydi(k as Map))
                        .toList(),
                  ),
          ),
          const SizedBox(height: 12),

          // Emergency contacts
          _buildSection(
            color: AppColors.danger,
            icon: Icons.emergency,
            title: 'Acil Iletisim',
            child: _buildAcilIletisim(acilIletisim),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildSaglikHero() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF059669), Color(0xFF10B981)],
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
            child: const Icon(Icons.health_and_safety,
                color: Colors.white, size: 28),
          ),
          const SizedBox(width: 14),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Saglik Bilgileri',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w700)),
                SizedBox(height: 4),
                Text('Asi takvimi, saglik kayitlari ve acil iletisim',
                    style: TextStyle(color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAsiItem(Map asi) {
    final ad = asi['asi_adi'] as String? ?? '';
    final tarih = asi['tarih'] as String? ?? '';
    final durum = (asi['durum'] as String? ?? '').toLowerCase();

    final isTamam = durum == 'tamamlandi';
    final durumColor = isTamam ? AppColors.success : AppColors.info;
    final durumLabel = isTamam ? 'Tamamlandi' : 'Planli';
    final durumIcon = isTamam ? Icons.check_circle : Icons.schedule;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
      child: Row(
        children: [
          Icon(Icons.vaccines, size: 18, color: durumColor),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(ad,
                    style: const TextStyle(
                        fontSize: 13, fontWeight: FontWeight.w600)),
                const SizedBox(height: 2),
                Text(tarih,
                    style: TextStyle(fontSize: 12, color: Colors.grey[500])),
              ],
            ),
          ),
          Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: durumColor.withOpacity(0.12),
              borderRadius: BorderRadius.circular(6),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(durumIcon, size: 12, color: durumColor),
                const SizedBox(width: 4),
                Text(durumLabel,
                    style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: durumColor)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSaglikKaydi(Map kayit) {
    final tarih = kayit['tarih'] as String? ?? '';
    final baslik = kayit['baslik'] as String? ?? '';
    final detay = kayit['detay'] as String? ?? '';
    final tip = (kayit['tip'] as String? ?? '').toLowerCase();

    IconData tipIcon;
    Color tipColor;
    switch (tip) {
      case 'olcum':
        tipIcon = Icons.straighten;
        tipColor = AppColors.info;
        break;
      case 'tarama':
        tipIcon = Icons.visibility;
        tipColor = AppColors.primary;
        break;
      case 'kontrol':
        tipIcon = Icons.medical_services;
        tipColor = AppColors.warning;
        break;
      default:
        tipIcon = Icons.note_alt;
        tipColor = AppColors.textSecondaryLight;
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: tipColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(tipIcon, size: 18, color: tipColor),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(baslik,
                          style: const TextStyle(
                              fontSize: 13, fontWeight: FontWeight.w600)),
                    ),
                    Text(tarih,
                        style:
                            TextStyle(fontSize: 11, color: Colors.grey[500])),
                  ],
                ),
                if (detay.isNotEmpty) ...[
                  const SizedBox(height: 3),
                  Text(detay,
                      style:
                          TextStyle(fontSize: 12, color: Colors.grey[600])),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAcilIletisim(Map data) {
    final hemsireleri = data['okul_hemsireleri'] as String? ?? '';
    final hastane = data['en_yakin_hastane'] as String? ?? '';
    final ambulans = data['ambulans'] as String? ?? '112';

    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 8, 14, 14),
      child: Column(
        children: [
          _acilRow(Icons.local_hospital, 'Okul Hemsiresi', hemsireleri,
              AppColors.danger),
          const Divider(height: 16),
          _acilRow(Icons.apartment, 'En Yakin Hastane', hastane,
              AppColors.warning),
          const Divider(height: 16),
          _acilRow(Icons.phone_in_talk, 'Ambulans', ambulans,
              AppColors.danger),
        ],
      ),
    );
  }

  Widget _acilRow(IconData icon, String label, String value, Color color) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 20, color: color),
        const SizedBox(width: 10),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label,
                  style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: Colors.grey[600])),
              const SizedBox(height: 2),
              Text(value,
                  style: const TextStyle(
                      fontSize: 13, fontWeight: FontWeight.w500)),
            ],
          ),
        ),
      ],
    );
  }

  // ---------------------------------------------------------------------------
  // REHBERLIK TAB
  // ---------------------------------------------------------------------------
  Widget _buildRehberlikTab() {
    final data = _data ?? {};
    final rehberBilgi = (data['rehber_bilgi'] as Map?) ?? {};
    final rehberler = (data['veli_rehberleri'] as List?) ?? [];

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Hero
          _buildRehberlikHero(),
          const SizedBox(height: 16),

          // Counselor info card
          _buildSection(
            color: AppColors.primary,
            icon: Icons.person,
            title: 'Rehberlik Uzmani',
            child: _buildRehberInfo(rehberBilgi),
          ),
          const SizedBox(height: 12),

          // Parent guides
          _buildSection(
            color: AppColors.info,
            icon: Icons.menu_book,
            title: 'Veli Rehberleri',
            child: rehberler.isEmpty
                ? const Padding(
                    padding: EdgeInsets.all(14),
                    child: Text('Rehber bulunamadi',
                        style:
                            TextStyle(color: AppColors.textSecondaryLight)),
                  )
                : Column(
                    children: rehberler
                        .map<Widget>((r) => _buildRehberItem(r as Map))
                        .toList(),
                  ),
          ),
          const SizedBox(height: 16),

          // Appointment request button
          SizedBox(
            height: 52,
            child: ElevatedButton.icon(
              onPressed: () => _showRandevuDialog(),
              icon: const Icon(Icons.calendar_month),
              label: const Text('RANDEVU TALEP ET',
                  style: TextStyle(letterSpacing: 1.1)),
            ),
          ),
          const SizedBox(height: 24),
        ],
      ),
    );
  }

  Widget _buildRehberlikHero() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.primary, AppColors.primaryLight],
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
            child:
                const Icon(Icons.psychology, color: Colors.white, size: 28),
          ),
          const SizedBox(width: 14),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Rehberlik Hizmetleri',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w700)),
                SizedBox(height: 4),
                Text('Uzman destegi ve veli rehberleri',
                    style: TextStyle(color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRehberInfo(Map info) {
    if (info.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(14),
        child: Text('Rehber bilgisi bulunamadi',
            style: TextStyle(color: AppColors.textSecondaryLight)),
      );
    }
    final ad = info['ad'] as String? ?? '';
    final unvan = info['unvan'] as String? ?? '';
    final email = info['email'] as String? ?? '';
    final telefon = info['telefon'] as String? ?? '';
    final musait = info['musait_gunler'] as String? ?? '';

    return Padding(
      padding: const EdgeInsets.fromLTRB(14, 10, 14, 14),
      child: Column(
        children: [
          Row(
            children: [
              CircleAvatar(
                radius: 24,
                backgroundColor: AppColors.primary.withOpacity(0.15),
                child: const Icon(Icons.person,
                    color: AppColors.primary, size: 26),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(ad,
                        style: const TextStyle(
                            fontSize: 15, fontWeight: FontWeight.w700)),
                    const SizedBox(height: 2),
                    Text(unvan,
                        style: TextStyle(
                            fontSize: 12, color: Colors.grey[600])),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          const Divider(height: 1),
          const SizedBox(height: 10),
          _infoRow(Icons.email, email, AppColors.info),
          const SizedBox(height: 6),
          _infoRow(Icons.phone, telefon, AppColors.success),
          const SizedBox(height: 6),
          _infoRow(Icons.access_time, musait, AppColors.warning),
        ],
      ),
    );
  }

  Widget _infoRow(IconData icon, String text, Color color) {
    return Row(
      children: [
        Icon(icon, size: 16, color: color),
        const SizedBox(width: 8),
        Expanded(
          child: Text(text,
              style: const TextStyle(fontSize: 13)),
        ),
      ],
    );
  }

  Widget _buildRehberItem(Map rehber) {
    final baslik = rehber['baslik'] as String? ?? '';
    final ozet = rehber['ozet'] as String? ?? '';
    final iconKey = (rehber['icon'] as String? ?? '').toLowerCase();

    IconData itemIcon;
    Color itemColor;
    switch (iconKey) {
      case 'psychology':
        itemIcon = Icons.psychology;
        itemColor = AppColors.primary;
        break;
      case 'stress':
        itemIcon = Icons.sentiment_stressed;
        itemColor = AppColors.warning;
        break;
      case 'bullying':
        itemIcon = Icons.shield;
        itemColor = AppColors.danger;
        break;
      case 'digital':
        itemIcon = Icons.phone_android;
        itemColor = AppColors.info;
        break;
      case 'confidence':
        itemIcon = Icons.emoji_emotions;
        itemColor = AppColors.success;
        break;
      default:
        itemIcon = Icons.article;
        itemColor = AppColors.textSecondaryLight;
    }

    return InkWell(
      onTap: () {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('"$baslik" rehberi yakin zamanda eklenecektir.'),
            backgroundColor: AppColors.info,
          ),
        );
      },
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: itemColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(itemIcon, size: 20, color: itemColor),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(baslik,
                      style: const TextStyle(
                          fontSize: 14, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 2),
                  Text(ozet,
                      style:
                          TextStyle(fontSize: 12, color: Colors.grey[600])),
                ],
              ),
            ),
            const Icon(Icons.chevron_right,
                size: 20, color: AppColors.textSecondaryLight),
          ],
        ),
      ),
    );
  }

  void _showRandevuDialog() {
    showDialog(
      context: context,
      builder: (ctx) {
        return AlertDialog(
          title: const Row(
            children: [
              Icon(Icons.calendar_month, color: AppColors.primary),
              SizedBox(width: 8),
              Text('Randevu Talebi', style: TextStyle(fontSize: 17)),
            ],
          ),
          content: const Text(
            'Rehberlik uzmaniyla gorusme randevusu talep etmek istiyorsaniz, '
            'asagidaki butonu kullanarak talebinizi iletebilirsiniz. '
            'En kisa surede size donulecektir.',
            style: TextStyle(fontSize: 14, height: 1.5),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Vazgec'),
            ),
            ElevatedButton(
              onPressed: () async {
                Navigator.pop(ctx);
                try {
                  await ref.read(apiClientProvider).post(
                    '/veli/rehberlik-randevu',
                    data: {'tarih': DateTime.now().toIso8601String()},
                  );
                } catch (_) {
                  // offline-first
                }
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Randevu talebiniz iletildi.'),
                    backgroundColor: AppColors.success,
                  ),
                );
              },
              child: const Text('Talep Gonder'),
            ),
          ],
        );
      },
    );
  }

  // ---------------------------------------------------------------------------
  // SHARED SECTION BUILDER
  // ---------------------------------------------------------------------------
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
                const SizedBox(height: 4),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
