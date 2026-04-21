import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../core/theme/app_theme.dart';


/// Sanat Sokagi — gorsel sanatlar + muzik + yaratici icerikler
class SanatSokagiPage extends ConsumerWidget {
  const SanatSokagiPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sanat Sokagi')),
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
                  colors: [Color(0xFFEC4899), Color(0xFF8B5CF6)],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Column(
                children: [
                  Icon(Icons.palette, size: 48, color: Colors.white),
                  SizedBox(height: 8),
                  Text('Sanat Sokagi',
                      style: TextStyle(color: Colors.white, fontSize: 22,
                          fontWeight: FontWeight.bold)),
                  SizedBox(height: 4),
                  Text('Gorsel Sanatlar · Muzik · Yaraticilik',
                      style: TextStyle(color: Colors.white70, fontSize: 13)),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Kategoriler
            const Text('Atolyeler',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 12, mainAxisSpacing: 12,
              childAspectRatio: 1.2,
              children: [
                _AtolyeCard(
                  icon: Icons.brush,
                  title: 'Resim Atolyesi',
                  subtitle: 'Renk teorisi, cizim teknikleri',
                  color: const Color(0xFFEF4444),
                  icerikler: _resimIcerikler,
                ),
                _AtolyeCard(
                  icon: Icons.music_note,
                  title: 'Muzik Atolyesi',
                  subtitle: 'Ritim, nota, enstrumanlar',
                  color: const Color(0xFF8B5CF6),
                  icerikler: _muzikIcerikler,
                ),
                _AtolyeCard(
                  icon: Icons.camera_alt,
                  title: 'Fotograf',
                  subtitle: 'Kadraj, isik, kompozisyon',
                  color: const Color(0xFF0EA5E9),
                  icerikler: _fotografIcerikler,
                ),
                _AtolyeCard(
                  icon: Icons.theater_comedy,
                  title: 'Drama & Tiyatro',
                  subtitle: 'Rol, sahne, donaklasma',
                  color: const Color(0xFFF97316),
                  icerikler: _dramaIcerikler,
                ),
                _AtolyeCard(
                  icon: Icons.architecture,
                  title: 'El Sanatlari',
                  subtitle: 'Seramik, origami, kolaj',
                  color: const Color(0xFF14B8A6),
                  icerikler: _elSanatlariIcerikler,
                ),
                _AtolyeCard(
                  icon: Icons.auto_awesome,
                  title: 'Dijital Sanat',
                  subtitle: 'Pixel art, animasyon',
                  color: const Color(0xFF6366F1),
                  icerikler: _dijitalSanatIcerikler,
                ),
              ],
            ),

            const SizedBox(height: 24),
            const Text('Ilham Kosesi',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),
            ..._ilhamlar.map((i) => _IlhamKart(ilham: i)),
          ],
        ),
      ),
    );
  }
}


// ── Icerik verileri ──

const _resimIcerikler = [
  {'baslik': 'Renk Carki', 'aciklama': 'Ana, ara ve tamamlayici renkler'},
  {'baslik': 'Perspektif Cizim', 'aciklama': '1-2-3 kacan noktali perspektif'},
  {'baslik': 'Portre Cizimi', 'aciklama': 'Yuz oranlari ve golgeler'},
  {'baslik': 'Suluboya Teknikleri', 'aciklama': 'Islak-islak, kuru firca'},
];

const _muzikIcerikler = [
  {'baslik': 'Nota Okuma', 'aciklama': 'Sol anahtari, nota degerleri'},
  {'baslik': 'Ritim Kaliplari', 'aciklama': '2/4, 3/4, 4/4 olcu'},
  {'baslik': 'Enstruman Tanima', 'aciklama': 'Yayli, uflemeli, vurmali'},
  {'baslik': 'Turk Muzigi Makam', 'aciklama': 'Rast, Huseyni, Hicaz'},
];

const _fotografIcerikler = [
  {'baslik': 'Ucler Kurali', 'aciklama': 'Kompozisyonda altin oran'},
  {'baslik': 'Isik & Golge', 'aciklama': 'Dogal isik, kontrast'},
  {'baslik': 'Makro Fotograf', 'aciklama': 'Yakin cekim teknikleri'},
];

const _dramaIcerikler = [
  {'baslik': 'Donaklasma Oyunlari', 'aciklama': 'Isindirma ve guvem kurma'},
  {'baslik': 'Kukla Tiyatrosu', 'aciklama': 'Parmak kukla, golge tiyatrosu'},
  {'baslik': 'Sahne Kurallari', 'aciklama': 'Giris, doruk, cozum'},
];

const _elSanatlariIcerikler = [
  {'baslik': 'Origami', 'aciklama': 'Kagit katlama sanati'},
  {'baslik': 'Seramik', 'aciklama': 'Kil sekillendirme teknikleri'},
  {'baslik': 'Kolaj', 'aciklama': 'Karma malzeme kompozisyonu'},
];

const _dijitalSanatIcerikler = [
  {'baslik': 'Pixel Art', 'aciklama': 'Piksel piksel cizim'},
  {'baslik': 'Animasyon Temelleri', 'aciklama': '12 animasyon ilkesi'},
  {'baslik': 'Dijital Illustrasyon', 'aciklama': 'Tablet ile cizim'},
];

const _ilhamlar = [
  {
    'sanatci': 'Leonardo da Vinci',
    'eser': 'Mona Lisa',
    'soz': 'Basitlik, sonun inceligidir.',
    'renk': 0xFFC5962E,
  },
  {
    'sanatci': 'Frida Kahlo',
    'eser': 'Otoportreler',
    'soz': 'Hayali boyadigimi saniyorlardi ama ben gercegimi boyuyordum.',
    'renk': 0xFFEC4899,
  },
  {
    'sanatci': 'Osman Hamdi Bey',
    'eser': 'Kaplumbaga Terbiyecisi',
    'soz': 'Sanat, toplumun aynasidir.',
    'renk': 0xFF4F46E5,
  },
];


class _AtolyeCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final List<Map<String, String>> icerikler;

  const _AtolyeCard({
    required this.icon, required this.title, required this.subtitle,
    required this.color, required this.icerikler,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => _showIcerikler(context),
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: color.withOpacity(0.08),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            const Spacer(),
            Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
            Text(subtitle, style: TextStyle(fontSize: 10, color: Colors.grey[600]),
                maxLines: 1, overflow: TextOverflow.ellipsis),
          ],
        ),
      ),
    );
  }

  void _showIcerikler(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color),
                const SizedBox(width: 8),
                Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 16),
            ...icerikler.map((i) => Container(
              margin: const EdgeInsets.only(bottom: 8),
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withOpacity(0.06),
                borderRadius: BorderRadius.circular(10),
                border: Border(left: BorderSide(color: color, width: 3)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(i['baslik']!, style: const TextStyle(fontWeight: FontWeight.w600)),
                  Text(i['aciklama']!, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
                ],
              ),
            )),
          ],
        ),
      ),
    );
  }
}


class _IlhamKart extends StatelessWidget {
  final Map<String, dynamic> ilham;
  const _IlhamKart({required this.ilham});

  @override
  Widget build(BuildContext context) {
    final c = Color(ilham['renk'] as int);
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(color: c, width: 4)),
        ),
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('"${ilham['soz']}"',
                style: const TextStyle(fontSize: 14, fontStyle: FontStyle.italic, height: 1.4)),
            const SizedBox(height: 8),
            Row(
              children: [
                Text('— ${ilham['sanatci']}',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: c)),
                const Spacer(),
                Text(ilham['eser'] as String,
                    style: TextStyle(fontSize: 11, color: Colors.grey[500])),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
