import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../core/theme/app_theme.dart';


/// Bilisim Vadisi — kodlama, dijital okuryazarlik, STEM
class BilisimVadisiPage extends ConsumerWidget {
  const BilisimVadisiPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bilisim Vadisi')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Hero
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF6366F1), Color(0xFF0EA5E9)],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Column(
                children: [
                  Icon(Icons.computer, size: 48, color: Colors.white),
                  SizedBox(height: 8),
                  Text('Bilisim Vadisi',
                      style: TextStyle(color: Colors.white, fontSize: 22,
                          fontWeight: FontWeight.bold)),
                  SizedBox(height: 4),
                  Text('Kodlama · Dijital Okuryazarlik · STEM',
                      style: TextStyle(color: Colors.white70, fontSize: 13)),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Seviye secimi
            const Text('Kodlama Patikasi',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),

            // Baslangic
            _SeviyeSection(
              seviye: 'Baslangic',
              renk: AppColors.success,
              ikon: Icons.play_circle,
              konular: const [
                _Konu('Algoritma Nedir?', 'Adim adim dusunme, akis semasi',
                    Icons.account_tree),
                _Konu('Scratch ile Kodlama', 'Blok tabanli gorsel programlama',
                    Icons.extension),
                _Konu('HTML & CSS Temelleri', 'Web sayfasi yapisi ve tasarimi',
                    Icons.web),
                _Konu('Dijital Vatandaslik', 'Internet guvenligi, siber zorbalik',
                    Icons.security),
              ],
            ),
            const SizedBox(height: 16),

            // Orta
            _SeviyeSection(
              seviye: 'Orta Seviye',
              renk: AppColors.warning,
              ikon: Icons.trending_up,
              konular: const [
                _Konu('Python ile Kodlama', 'Degiskenler, donguler, fonksiyonlar',
                    Icons.code),
                _Konu('Mobil Uygulama', 'App Inventor ile mobil gelistirme',
                    Icons.phone_android),
                _Konu('Veritabani Temelleri', 'Veri saklama, SQL giris',
                    Icons.storage),
                _Konu('Robotik Kodlama', 'Arduino, sensor, motor kontrolu',
                    Icons.smart_toy),
              ],
            ),
            const SizedBox(height: 16),

            // Ileri
            _SeviyeSection(
              seviye: 'Ileri Seviye',
              renk: AppColors.danger,
              ikon: Icons.rocket_launch,
              konular: const [
                _Konu('Yapay Zeka Giris', 'Makine ogrenmesi temelleri',
                    Icons.psychology),
                _Konu('Web Gelistirme', 'JavaScript, React, API kullanimi',
                    Icons.language),
                _Konu('Siber Guvenlik', 'Sifreleme, guvenlik duvari, etik hack',
                    Icons.shield),
                _Konu('Veri Bilimi', 'Pandas, gorsellestirme, analiz',
                    Icons.bar_chart),
              ],
            ),

            const SizedBox(height: 24),
            const Text('Dijital Okuryazarlik',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            ..._dijitalOkur.map((d) => _DijitalKart(data: d)),

            const SizedBox(height: 24),
            const Text('Yararli Kaynaklar',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            ..._kaynaklar.map((k) => _KaynakTile(kaynak: k)),
          ],
        ),
      ),
    );
  }
}


class _Konu {
  final String baslik;
  final String aciklama;
  final IconData ikon;
  const _Konu(this.baslik, this.aciklama, this.ikon);
}


class _SeviyeSection extends StatelessWidget {
  final String seviye;
  final Color renk;
  final IconData ikon;
  final List<_Konu> konular;
  const _SeviyeSection({
    required this.seviye, required this.renk,
    required this.ikon, required this.konular,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(ikon, color: renk, size: 20),
            const SizedBox(width: 6),
            Text(seviye, style: TextStyle(fontSize: 15,
                fontWeight: FontWeight.w600, color: renk)),
          ],
        ),
        const SizedBox(height: 8),
        ...konular.map((k) => Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: renk.withOpacity(0.06),
            borderRadius: BorderRadius.circular(10),
            border: Border(left: BorderSide(color: renk, width: 3)),
          ),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: renk.withOpacity(0.12),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(k.ikon, size: 18, color: renk),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(k.baslik, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
                    Text(k.aciklama, style: TextStyle(fontSize: 11, color: Colors.grey[600])),
                  ],
                ),
              ),
              Icon(Icons.chevron_right, size: 18, color: Colors.grey[400]),
            ],
          ),
        )),
      ],
    );
  }
}


const _dijitalOkur = [
  {'baslik': 'Guvenli Sifre Olusturma', 'ikon': 0xe59e, 'renk': 0xFF059669},
  {'baslik': 'Sosyal Medya Bilinclendirme', 'ikon': 0xe894, 'renk': 0xFF0284C7},
  {'baslik': 'Kisisel Veri Koruma (KVKK)', 'ikon': 0xea18, 'renk': 0xFF7C3AED},
  {'baslik': 'Sahte Haber / Dogrulama', 'ikon': 0xe629, 'renk': 0xFFD97706},
];

const _kaynaklar = [
  {'baslik': 'Code.org', 'aciklama': 'Ucretsiz kodlama dersleri', 'url': 'https://code.org'},
  {'baslik': 'Scratch', 'aciklama': 'MIT blok tabanli kodlama', 'url': 'https://scratch.mit.edu'},
  {'baslik': 'Khan Academy', 'aciklama': 'Bilgisayar bilimi dersleri', 'url': 'https://khanacademy.org'},
];


class _DijitalKart extends StatelessWidget {
  final Map<String, dynamic> data;
  const _DijitalKart({required this.data});

  @override
  Widget build(BuildContext context) {
    final c = Color(data['renk'] as int);
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color: c.withOpacity(0.08),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: c.withOpacity(0.2)),
      ),
      child: Row(
        children: [
          Icon(IconData(data['ikon'] as int, fontFamily: 'MaterialIcons'),
              color: c, size: 22),
          const SizedBox(width: 12),
          Expanded(
            child: Text(data['baslik'] as String,
                style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
          ),
          Icon(Icons.chevron_right, size: 18, color: Colors.grey[400]),
        ],
      ),
    );
  }
}


class _KaynakTile extends StatelessWidget {
  final Map<String, String> kaynak;
  const _KaynakTile({required this.kaynak});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppColors.primary.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: const Icon(Icons.open_in_new, color: AppColors.primary, size: 20),
        ),
        title: Text(kaynak['baslik']!, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(kaynak['aciklama']!, style: const TextStyle(fontSize: 12)),
        trailing: const Icon(Icons.chevron_right),
        onTap: () async {
          final url = kaynak['url']!;
          if (await canLaunchUrl(Uri.parse(url))) {
            await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
          }
        },
      ),
    );
  }
}
