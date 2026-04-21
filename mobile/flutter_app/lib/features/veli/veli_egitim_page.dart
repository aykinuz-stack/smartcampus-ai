import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class VeliEgitimPage extends ConsumerStatefulWidget {
  const VeliEgitimPage({super.key});

  @override
  ConsumerState<VeliEgitimPage> createState() => _VeliEgitimPageState();
}

class _VeliEgitimPageState extends ConsumerState<VeliEgitimPage> {
  List<Map<String, dynamic>>? _categories;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final r = await ref.read(apiClientProvider).get('/veli/egitim-icerikleri');
      final data = r.data;
      if (data is Map && data['kategoriler'] != null) {
        _categories =
            List<Map<String, dynamic>>.from(data['kategoriler'] as List);
      } else if (data is List) {
        _categories = List<Map<String, dynamic>>.from(data);
      } else {
        _categories = _staticData();
      }
    } catch (_) {
      _categories = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  static List<Map<String, dynamic>> _staticData() {
    return [
      {
        'kategori': 'Cocuk Gelisimi',
        'icon': 'child',
        'color': 'success',
        'makaleler': [
          {
            'baslik': 'Yas Donemlerine Gore Gelisim Ozellikleri',
            'sure': '8 dk',
            'icerik':
                'Her cocuk kendine ozgu bir gelisim surecinden gecer. Ancak genel gelisim '
                    'asamalari bilindiginde, veliler cocuklarinin ihtiyaclarini daha iyi '
                    'anlayabilir. 0-6 yas doneminde temel guven duygusu olusur. Cocuk '
                    'cevresini kesfeder, dil becerileri gelisir. 6-12 yas doneminde akademik '
                    'beceriler one cikar. Cocuk okuma-yazma ogrenir, sosyal iliskiler kurar. '
                    'Bu donemde basari ve yetkinlik duygusu onemlidir. Velilerin her donemde '
                    'cocuklarini desteklemesi, onlarin saglikli bireyler olarak yetismesine '
                    'buyuk katki saglar.',
          },
          {
            'baslik': 'Cocugunuzun Duygusal Zekasini Gelistirme',
            'sure': '6 dk',
            'icerik':
                'Duygusal zeka, bireyin kendi duygularini tanimasi, yonetmesi ve baskalarinin '
                    'duygularini anlamasi becerisidir. Cocuklarda duygusal zekayi gelistirmek '
                    'icin oncelikle duyguların adini koymak onemlidir. "Uzgun gorunuyorsun" gibi '
                    'ifadeler kullanarak cocugunuza duygulari tanimasi ogretilir. Empati kurma '
                    'becerisi de duygusal zekanin temel taslarindan biridir. Cocugunuzla birlikte '
                    'hikayeler okuyarak karakterlerin duygularini konusabilirsiniz.',
          },
          {
            'baslik': 'Beslenme ve Fiziksel Gelisim',
            'sure': '5 dk',
            'icerik':
                'Dengeli beslenme, cocugun fiziksel ve zihinsel gelisimi icin kritik oneme '
                    'sahiptir. Kahvaltiyi atlamamak, gunluk meyve-sebze tuketimini saglamak ve '
                    'yeterli su icmek temel kurallardandir. Fiziksel aktivite de en az beslenme '
                    'kadar onemlidir. Gunde en az 60 dakika hareket etmek, cocuklarin kemik ve '
                    'kas gelisimine destek olur. Ekran basinda gecirilen sureyi sinirlandirmak '
                    've bunun yerine acik hava etkinliklerini tesvik etmek faydali olacaktir.',
          },
        ],
      },
      {
        'kategori': 'Dijital Guvenlik',
        'icon': 'security',
        'color': 'info',
        'makaleler': [
          {
            'baslik': 'Internette Guvenli Cocuk',
            'sure': '7 dk',
            'icerik':
                'Cocuklarin internet kullaniminda guvenlik en onemli konulardan biridir. '
                    'Ebeveyn kontrol yazilimlari kullanmak, cocugun hangi siteleri ziyaret '
                    'ettigini takip etmek ve acik iletisim kurmak temel adimlardir. Sosyal '
                    'medya hesaplari icin yas sinirlarina dikkat edilmeli, kisisel bilgilerin '
                    'paylasilmamasi gerektigini cocugunuza ogretmelisiniz. Online oyunlarda da '
                    'yabanci kisilerle iletisimin riskleri hakkinda konusulmalidir.',
          },
          {
            'baslik': 'Ekran Suresi Yonetimi',
            'sure': '5 dk',
            'icerik':
                'Dunya Saglik Orgutu, 5 yas alti cocuklar icin gunluk ekran suresinin 1 saati '
                    'gecmemesini onerir. Okul cagi cocuklari icin ise 2 saat makul bir sinirdir. '
                    'Ekran suresini yonetmek icin aile kurallari olusturmak, ekransiz bolgeler '
                    'belirlemek (yemek masasi, yatak odasi) ve alternatif etkinlikler sunmak '
                    'etkili yontemlerdir. Cocugunuzla birlikte bir "ekran suresi sozlesmesi" '
                    'hazirlayabilirsiniz.',
          },
          {
            'baslik': 'Siber Zorbalik ve Korunma Yollari',
            'sure': '6 dk',
            'icerik':
                'Siber zorbalik, dijital platformlar uzerinden gerceklesen, tekrarlayan '
                    'olumsuz davranislardir. Cocugunuzun siber zorbaliga maruz kalip kalmadigini '
                    'anlamak icin davranis degisikliklerine dikkat edin. Aniden icine kapanma, '
                    'cihaz kullanmaktan kacinma veya okula gitmek istememe gibi belirtiler '
                    'goruldugunde konuyu arastirmak onemlidir. Cocugunuza ekran goruntusu '
                    'almasini, size ya da bir yetisine haber vermesini ogretin.',
          },
          {
            'baslik': 'Yararli Egitim Uygulamalari',
            'sure': '4 dk',
            'icerik':
                'Teknolojiyi yasaklamak yerine dogru yonlendirmek daha etkili bir yaklasimdir. '
                    'Egitici uygulamalar ve oyunlar, cocugunuzun hem eglenmesini hem ogrenmeyi '
                    'saglar. Matematik, kodlama, yabanci dil ve bilim konularinda pek cok kaliteli '
                    'uygulama bulunmaktadir. Uygulamalari cocugunuzla birlikte secin ve deneyin.',
          },
        ],
      },
      {
        'kategori': 'Etkili Iletisim',
        'icon': 'chat',
        'color': 'gold',
        'makaleler': [
          {
            'baslik': 'Cocugunuzla Etkili Iletisim Kurma',
            'sure': '7 dk',
            'icerik':
                'Etkili iletisimin temeli aktif dinlemedir. Cocugunuz konusurken goz temasi '
                    'kurun, telefonunuzu birakin ve ona tam dikkatinizi verin. "Seni anliyorum" '
                    'gibi dogrulayici ifadeler kullanin. Elestiri yerine "Ben dili" kullanmak '
                    'iletisimi guclendirir. "Sen hic ders calismiyorsun" yerine "Ders calisma '
                    'planin konusunda endiseleniyorum" demek daha etkilidir. Gunluk rutinlerinize '
                    'sohbet zamanlari ekleyin: yemek saati, araba yolculugu, yatmadan once.',
          },
          {
            'baslik': 'Sinir Koyma Sanati',
            'sure': '6 dk',
            'icerik':
                'Cocuklara sinir koymak, onlari sevmedigimiz anlamina gelmez; aksine guvenli '
                    'bir ortam saglar. Tutarli olmak sinir koymanin en onemli kuralidir. Kurallar '
                    'net, anlasilir ve uygulanabilir olmalidir. Cocugunuzla birlikte kurallar '
                    'belirleyerek onun da surece katilimini saglayin. Kurallara uyulmadiginda '
                    'ise dogal sonuclari uygulayin; ceza yerine ders cikarma yaklasimini benimseyin.',
          },
          {
            'baslik': 'Ogretmenlerle Isbirligi',
            'sure': '5 dk',
            'icerik':
                'Cocugunuzun egitim surecinde ogretmenlerle isbirligi yapmak buyuk onem tasir. '
                    'Veli toplantilarini kacirmayin, ogretmenle duzenli gorusmeler talep edin. '
                    'Sorunlari erken tespit etmek icin ogretmenin geri bildirimlerini dikkate '
                    'alin. Ev ile okul arasinda tutarli mesajlar vermek cocugunuzun uyumunu '
                    'kolaylastirir. Ogretmene destek olmak, cocugunuzun basarisina dogrudan '
                    'katkida bulunur.',
          },
        ],
      },
      {
        'kategori': 'Sinav Donem Destegi',
        'icon': 'exam',
        'color': 'warning',
        'makaleler': [
          {
            'baslik': 'Sinav Oncesi Hazirlik Stratejileri',
            'sure': '8 dk',
            'icerik':
                'Sinav donemi hem ogrenciler hem veliler icin stresli bir surec olabilir. '
                    'Cocugunuzun duzensiz calisma yerine bir plan dahilinde hazirlanmasini '
                    'saglayin. Haftalik calisma programi olusturmak, konulari kucuk parcalara '
                    'bolmek ve duzenli tekrar yapmak basariyi artiran yontemlerdir. Calisma '
                    'ortamini sessiz ve duzenli hale getirin. Yeterli uyku ve beslenmenin de '
                    'sinav basarisinda kritik rolu vardir.',
          },
          {
            'baslik': 'Sinav Kaygisiyla Basa Cikma',
            'sure': '6 dk',
            'icerik':
                'Sinav kaygisi, ogrencilerin performansini olumsuz etkileyen yaygin bir '
                    'sorundur. Cocugunuzda sinav oncesi uyku bozuklugu, istahsizlik veya asiri '
                    'gerginlik goruluyor olabilir. Baskiyi azaltmak icin "Sonuc ne olursa olsun '
                    'seni seviyorum" mesajini verin. Nefes egzersizleri ve gevsetme teknikleri '
                    'ogretmek de faydali olabilir. Gerekirse okul rehberlik servisinden destek '
                    'alinmalidir.',
          },
          {
            'baslik': 'Motivasyonu Yuksek Tutma',
            'sure': '5 dk',
            'icerik':
                'Uzun bir sinav doneminde motivasyonun dusmesi normaldir. Kisa vadeli hedefler '
                    'koymak, her basariyi kutlamak ve kucuk odullerle tesvik etmek etkili '
                    'yontemlerdir. Cocugunuzu baskalariyla kiyaslamaktan kacinin, kendi '
                    'gelisimine odaklanmasini saglayin. "Dun 20 soru cozuyordun, bugun 25 '
                    'cozuyorsun, harika ilerliyorsun" gibi somut geri bildirimler verin.',
          },
          {
            'baslik': 'Sinav Sonrasi Degerlendirme',
            'sure': '4 dk',
            'icerik':
                'Sinav sonuclari aciklandiginda, not ne olursa olsun sakin kalmayi hedefleyin. '
                    'Sonuc iyi ise basariyi kutlayin, yetersiz ise hatalardan ders cikarma firsati '
                    'olarak degerlendirin. "Hangi konularda zorlandin?" ve "Bir dahaki sefere ne '
                    'yapalim?" gibi sorularla yapici bir konusma baslatin. Cocugunuzun ozguvenini '
                    'sarsmadan gelisim alanlarini birlikte belirleyin.',
          },
        ],
      },
    ];
  }

  Color _colorFromKey(String key) {
    switch (key) {
      case 'primary':
        return AppColors.primary;
      case 'info':
        return AppColors.info;
      case 'success':
        return AppColors.success;
      case 'warning':
        return AppColors.warning;
      case 'danger':
        return AppColors.danger;
      case 'gold':
        return AppColors.gold;
      default:
        return AppColors.primary;
    }
  }

  IconData _iconFromKey(String key) {
    switch (key) {
      case 'child':
        return Icons.child_care;
      case 'security':
        return Icons.security;
      case 'chat':
        return Icons.chat;
      case 'exam':
        return Icons.assignment;
      default:
        return Icons.article;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Veli Egitim Icerikleri')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  // Hero
                  _buildHeroHeader(),
                  const SizedBox(height: 16),

                  // Category expansion tiles
                  ...(_categories ?? []).map((cat) => _buildCategoryTile(cat)),

                  const SizedBox(height: 24),
                ],
              ),
            ),
    );
  }

  Widget _buildHeroHeader() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.primaryDark, AppColors.primary],
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
            child: const Icon(Icons.auto_stories,
                color: Colors.white, size: 28),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Veli Egitim Kosesi',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w700)),
                const SizedBox(height: 4),
                Text(
                  '${_totalArticleCount()} makale ile cocugunuza destek olun',
                  style:
                      const TextStyle(color: Colors.white70, fontSize: 13),
                ),
              ],
            ),
          ),
          const Icon(Icons.school, color: Colors.white38, size: 32),
        ],
      ),
    );
  }

  int _totalArticleCount() {
    int count = 0;
    for (final cat in _categories ?? []) {
      final makaleler = cat['makaleler'] as List?;
      count += makaleler?.length ?? 0;
    }
    return count;
  }

  Widget _buildCategoryTile(Map<String, dynamic> cat) {
    final kategori = cat['kategori'] as String? ?? '';
    final iconKey = cat['icon'] as String? ?? '';
    final colorKey = cat['color'] as String? ?? 'primary';
    final makaleler = (cat['makaleler'] as List?) ?? [];

    final color = _colorFromKey(colorKey);
    final icon = _iconFromKey(iconKey);

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: BoxDecoration(
          border: Border(left: BorderSide(color: color, width: 4)),
        ),
        child: Theme(
          data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
          child: ExpansionTile(
            leading: Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            title: Text(kategori,
                style: TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    color: color)),
            subtitle: Text('${makaleler.length} makale',
                style:
                    TextStyle(fontSize: 12, color: Colors.grey[500])),
            children: makaleler.map<Widget>((m) {
              final makale = m as Map;
              return _buildArticleItem(makale, color);
            }).toList(),
          ),
        ),
      ),
    );
  }

  Widget _buildArticleItem(Map makale, Color categoryColor) {
    final baslik = makale['baslik'] as String? ?? '';
    final sure = makale['sure'] as String? ?? '';
    final icerik = makale['icerik'] as String? ?? '';

    return InkWell(
      onTap: () => _showArticleSheet(baslik, icerik, sure, categoryColor),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: categoryColor.withOpacity(0.08),
                borderRadius: BorderRadius.circular(6),
              ),
              child:
                  Icon(Icons.article, size: 18, color: categoryColor),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(baslik,
                      style: const TextStyle(
                          fontSize: 13, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 2),
                  Row(
                    children: [
                      Icon(Icons.access_time,
                          size: 12, color: Colors.grey[500]),
                      const SizedBox(width: 4),
                      Text(sure,
                          style: TextStyle(
                              fontSize: 11, color: Colors.grey[500])),
                    ],
                  ),
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

  void _showArticleSheet(
      String baslik, String icerik, String sure, Color color) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return DraggableScrollableSheet(
          initialChildSize: 0.7,
          minChildSize: 0.4,
          maxChildSize: 0.9,
          expand: false,
          builder: (_, scrollCtrl) {
            return Column(
              children: [
                // Drag handle
                Padding(
                  padding: const EdgeInsets.only(top: 12, bottom: 4),
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),

                // Header
                Container(
                  width: double.infinity,
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [color, color.withOpacity(0.7)],
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(baslik,
                          style: const TextStyle(
                              color: Colors.white,
                              fontSize: 17,
                              fontWeight: FontWeight.w700)),
                      const SizedBox(height: 6),
                      Row(
                        children: [
                          const Icon(Icons.access_time,
                              size: 14, color: Colors.white70),
                          const SizedBox(width: 4),
                          Text('Okuma suresi: $sure',
                              style: const TextStyle(
                                  color: Colors.white70, fontSize: 12)),
                        ],
                      ),
                    ],
                  ),
                ),

                // Content
                Expanded(
                  child: ListView(
                    controller: scrollCtrl,
                    padding: const EdgeInsets.all(20),
                    children: [
                      Text(
                        icerik,
                        style: const TextStyle(
                          fontSize: 15,
                          height: 1.7,
                          color: AppColors.textPrimaryLight,
                        ),
                      ),
                      const SizedBox(height: 20),
                      const Divider(),
                      const SizedBox(height: 10),
                      Row(
                        children: [
                          Icon(Icons.info_outline,
                              size: 16, color: Colors.grey[500]),
                          const SizedBox(width: 6),
                          Expanded(
                            child: Text(
                              'Bu icerik SmartCampus egitim ekibi tarafindan hazirlanmistir.',
                              style: TextStyle(
                                  fontSize: 12, color: Colors.grey[500]),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            );
          },
        );
      },
    );
  }
}
