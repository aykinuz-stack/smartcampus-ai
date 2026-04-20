import 'dart:math';
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class AiTreniPage extends StatefulWidget {
  const AiTreniPage({super.key});
  @override
  State<AiTreniPage> createState() => _AiTreniPageState();
}

class _AiTreniPageState extends State<AiTreniPage> {
  int? _selectedSinif;

  static const _siniflar = [
    {'no': 1, 'tema': 'Keşif Vagonu', 'renk': '#EF4444'},
    {'no': 2, 'tema': 'Merak Vagonu', 'renk': '#F59E0B'},
    {'no': 3, 'tema': 'Bilgi Vagonu', 'renk': '#10B981'},
    {'no': 4, 'tema': 'Macera Vagonu', 'renk': '#3B82F6'},
    {'no': 5, 'tema': 'Düşünce Vagonu', 'renk': '#8B5CF6'},
    {'no': 6, 'tema': 'Araştırma Vagonu', 'renk': '#EC4899'},
    {'no': 7, 'tema': 'Analiz Vagonu', 'renk': '#06B6D4'},
    {'no': 8, 'tema': 'Sentez Vagonu', 'renk': '#F97316'},
    {'no': 9, 'tema': 'Strateji Vagonu', 'renk': '#6366F1'},
    {'no': 10, 'tema': 'Uzmanlık Vagonu', 'renk': '#14B8A6'},
    {'no': 11, 'tema': 'Vizyon Vagonu', 'renk': '#A855F7'},
    {'no': 12, 'tema': 'Liderlik Vagonu', 'renk': '#EAB308'},
  ];

  static const _kompartimanlar = [
    {'ikon': '📚', 'baslik': 'Konu Anlatımı', 'aciklama': 'Ders notları + özet'},
    {'ikon': '🎯', 'baslik': 'Kazanım Takibi', 'aciklama': 'Hedef kazanımlar'},
    {'ikon': '❓', 'baslik': 'Bilgi Yarışması', 'aciklama': '10 soruluk quiz', 'aktif': true},
    {'ikon': '🧩', 'baslik': 'Bulmaca', 'aciklama': 'Eğlenceli sorular'},
    {'ikon': '📝', 'baslik': 'Mini Test', 'aciklama': 'Kısa değerlendirme'},
    {'ikon': '🔬', 'baslik': 'Deney Lab', 'aciklama': 'Sanal deneyler'},
    {'ikon': '🎮', 'baslik': 'Oyun Alanı', 'aciklama': 'Eğitici oyunlar'},
    {'ikon': '📊', 'baslik': 'İlerleme', 'aciklama': 'Gelişim takibi'},
    {'ikon': '🏆', 'baslik': 'Başarılar', 'aciklama': 'Rozetler + ödüller'},
    {'ikon': '🤖', 'baslik': 'AI Asistan', 'aciklama': 'Kişisel rehber'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Treni')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        // Hero
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFF6366F1), Color(0xFF8B5CF6), Color(0xFFEC4899)]),
            borderRadius: BorderRadius.circular(16)),
          child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('🚂', style: TextStyle(fontSize: 40)),
            SizedBox(height: 8),
            Text('AI Eğitim Treni', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
            SizedBox(height: 4),
            Text('12 vagon • 10 kompartıman • Sınıfını seç, vagona bin!',
                style: TextStyle(color: Colors.white70, fontSize: 13)),
          ]),
        ),
        const SizedBox(height: 20),

        const Text('🚃 Vagonunu Seç (Sınıf)', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        GridView.builder(
          shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 4, crossAxisSpacing: 8, mainAxisSpacing: 8, childAspectRatio: 1.2),
          itemCount: _siniflar.length,
          itemBuilder: (_, i) {
            final s = _siniflar[i];
            final no = s['no'] as int;
            final renk = _hexToColor(s['renk'] as String);
            final secili = _selectedSinif == no;
            return GestureDetector(
              onTap: () => setState(() => _selectedSinif = no),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                decoration: BoxDecoration(
                  color: secili ? renk.withOpacity(0.2) : Colors.transparent,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: secili ? renk : Colors.grey.withOpacity(0.3), width: secili ? 2.5 : 1)),
                child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Text('🚃', style: TextStyle(fontSize: secili ? 24 : 18)),
                  Text('$no', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: secili ? renk : null)),
                ]),
              ),
            );
          },
        ),

        if (_selectedSinif != null) ...[
          const SizedBox(height: 8),
          Text(_siniflar.firstWhere((s) => s['no'] == _selectedSinif)['tema'] as String,
              style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark), textAlign: TextAlign.center),
          const SizedBox(height: 20),
          const Text('🎯 Kompartıman Seç', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          ..._kompartimanlar.asMap().entries.map((e) {
            final i = e.key;
            final k = e.value;
            final colors = [AppColors.primary, AppColors.success, AppColors.info, AppColors.gold,
                AppColors.danger, AppColors.warning, Color(0xFF8B5CF6), Color(0xFF06B6D4),
                Color(0xFFEC4899), AppColors.primary];
            final c = colors[i % colors.length];
            final aktif = k['aktif'] == true;

            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                onTap: () {
                  if (aktif) {
                    Navigator.push(context, MaterialPageRoute(
                      builder: (_) => _QuizPage(sinif: _selectedSinif!)));
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                      content: Text('${k['baslik']} — yakında aktif'), backgroundColor: c));
                  }
                },
                leading: Container(
                  width: 44, height: 44,
                  decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                  child: Center(child: Text(k['ikon'] as String, style: const TextStyle(fontSize: 22))),
                ),
                title: Text(k['baslik'] as String, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                subtitle: Text(k['aciklama'] as String, style: const TextStyle(fontSize: 11)),
                trailing: Icon(aktif ? Icons.play_circle : Icons.lock, size: 20, color: aktif ? c : Colors.grey),
              ),
            );
          }),
        ] else
          Container(
            padding: const EdgeInsets.all(32),
            child: const Center(child: Text('Yukarıdan sınıfını seç, kompartımanlar açılsın',
                style: TextStyle(color: AppColors.textSecondaryDark))),
          ),
      ]),
    );
  }

  Color _hexToColor(String hex) {
    hex = hex.replaceAll('#', '');
    if (hex.length == 6) hex = 'FF$hex';
    return Color(int.parse(hex, radix: 16));
  }
}


// ═══════════════════════════════════════════════════════════
// QUIZ — Gömülü sorularla çalışır (backend gerektirmez)
// ═══════════════════════════════════════════════════════════

class _QuizPage extends StatefulWidget {
  final int sinif;
  const _QuizPage({required this.sinif});
  @override
  State<_QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends State<_QuizPage> {
  late List<Map<String, dynamic>> _sorular;
  int _current = 0, _dogru = 0;
  int? _secilen;
  bool _cevaplandi = false;

  static const _tumSorular = <int, List<Map<String, dynamic>>>{
    1: [
      {'soru':'2 + 3 = ?','secenekler':['4','5','6','7'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Hangi hayvan "miyav" der?','secenekler':['Köpek','Kedi','Kuş','Balık'],'dogru':1,'kategori':'Hayat Bilgisi'},
      {'soru':'Gökkuşağında kaç renk var?','secenekler':['5','6','7','8'],'dogru':2,'kategori':'Fen'},
      {'soru':'Haftanın kaç günü var?','secenekler':['5','6','7','8'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Güneş hangi yönden doğar?','secenekler':['Batı','Kuzey','Güney','Doğu'],'dogru':3,'kategori':'Hayat Bilgisi'},
    ],
    2: [
      {'soru':'15 + 27 = ?','secenekler':['41','42','43','44'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Suyun kaynama sıcaklığı?','secenekler':['50°C','80°C','100°C','120°C'],'dogru':2,'kategori':'Fen'},
      {'soru':'Türkiye\'nin başkenti?','secenekler':['İstanbul','Ankara','İzmir','Bursa'],'dogru':1,'kategori':'Sosyal'},
      {'soru':'Bir yılda kaç ay var?','secenekler':['10','11','12','13'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Hangisi sebzedir?','secenekler':['Elma','Havuç','Üzüm','Muz'],'dogru':1,'kategori':'Hayat Bilgisi'},
    ],
    3: [
      {'soru':'144 ÷ 12 = ?','secenekler':['10','11','12','13'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Atatürk nerede doğdu?','secenekler':['Ankara','İstanbul','Selanik','İzmir'],'dogru':2,'kategori':'Sosyal'},
      {'soru':'Bitkiler fotosentez için ne kullanır?','secenekler':['Su','Güneş ışığı','İkisi de','Toprak'],'dogru':2,'kategori':'Fen'},
      {'soru':'1 km kaç metre?','secenekler':['100','500','1000','10000'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Hangisi iç organ değil?','secenekler':['Kalp','Beyin','Karaciğer','Dirsek'],'dogru':3,'kategori':'Fen'},
    ],
    4: [
      {'soru':'3/4 + 1/4 = ?','secenekler':['1/2','3/4','1','4/4'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Dünya\'nın uydusu?','secenekler':['Güneş','Ay','Mars','Yıldız'],'dogru':1,'kategori':'Fen'},
      {'soru':'Cumhuriyet ne zaman ilan edildi?','secenekler':['1920','1922','1923','1938'],'dogru':2,'kategori':'Sosyal'},
      {'soru':'250 × 4 = ?','secenekler':['800','900','1000','1100'],'dogru':2,'kategori':'Matematik'},
      {'soru':'En büyük okyanus?','secenekler':['Atlas','Hint','Kuzey Buz','Büyük'],'dogru':3,'kategori':'Coğrafya'},
    ],
    5: [
      {'soru':'%25\'i 80 olan sayı?','secenekler':['20','200','320','400'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Fotosentez sonucu?','secenekler':['CO2','O2','N2','H2'],'dogru':1,'kategori':'Fen'},
      {'soru':'Malazgirt Savaşı yılı?','secenekler':['1071','1176','1243','1453'],'dogru':0,'kategori':'Tarih'},
      {'soru':'1.5 kg kaç gram?','secenekler':['150','1050','1500','15000'],'dogru':2,'kategori':'Matematik'},
      {'soru':'İstanbul Boğazı hangi kıtaları ayırır?','secenekler':['Avrupa-Afrika','Avrupa-Asya','Asya-Afrika','Amerika-Avrupa'],'dogru':1,'kategori':'Coğrafya'},
    ],
    6: [
      {'soru':'-5 + 8 = ?','secenekler':['3','-3','13','-13'],'dogru':0,'kategori':'Matematik'},
      {'soru':'Hücrenin enerji merkezi?','secenekler':['Çekirdek','Mitokondri','Ribozom','Golgi'],'dogru':1,'kategori':'Fen'},
      {'soru':'TBMM ne zaman açıldı?','secenekler':['23 Nisan 1920','29 Ekim 1923','19 Mayıs 1919','30 Ağustos 1922'],'dogru':0,'kategori':'Tarih'},
      {'soru':'x + 7 = 15 ise x = ?','secenekler':['6','7','8','9'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Ses boşlukta yayılır mı?','secenekler':['Evet','Hayır','Bazen','Sadece gece'],'dogru':1,'kategori':'Fen'},
    ],
    7: [
      {'soru':'2³ = ?','secenekler':['6','8','9','12'],'dogru':1,'kategori':'Matematik'},
      {'soru':'pH 7 ne demek?','secenekler':['Asit','Baz','Nötr','Tuz'],'dogru':2,'kategori':'Fen'},
      {'soru':'Osmanlı kurucusu?','secenekler':['Fatih','Osman Bey','Kanuni','Yavuz'],'dogru':1,'kategori':'Tarih'},
      {'soru':'√144 = ?','secenekler':['10','11','12','14'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Kuvvet birimi?','secenekler':['Joule','Watt','Newton','Pascal'],'dogru':2,'kategori':'Fizik'},
    ],
    8: [
      {'soru':'(x+3)(x-3) = ?','secenekler':['x²-9','x²+9','x²-6','x²+6'],'dogru':0,'kategori':'Matematik'},
      {'soru':'DNA\'nın yapı taşı?','secenekler':['Amino asit','Nükleotid','Yağ asidi','Glikoz'],'dogru':1,'kategori':'Biyoloji'},
      {'soru':'LGS hangi sınıfta?','secenekler':['7','8','9','10'],'dogru':1,'kategori':'Genel'},
      {'soru':'Pisagor: 3²+4²=?','secenekler':['20','24','25','30'],'dogru':2,'kategori':'Geometri'},
      {'soru':'Işık hızı yaklaşık?','secenekler':['300 km/s','3000 km/s','300.000 km/s','3.000.000 km/s'],'dogru':2,'kategori':'Fizik'},
    ],
    9: [
      {'soru':'log₁₀(1000) = ?','secenekler':['2','3','4','10'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Atom numarası neyi belirtir?','secenekler':['Nötron','Proton','Elektron','Kütle'],'dogru':1,'kategori':'Kimya'},
      {'soru':'F = m × a hangi yasa?','secenekler':['Newton 1','Newton 2','Newton 3','Kepler'],'dogru':1,'kategori':'Fizik'},
      {'soru':'sin 30° = ?','secenekler':['0','1/2','√2/2','√3/2'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Mitoz sonucu kaç hücre?','secenekler':['1','2','4','8'],'dogru':1,'kategori':'Biyoloji'},
    ],
    10: [
      {'soru':'lim(x→0) sin(x)/x = ?','secenekler':['0','1','∞','tanımsız'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Avogadro sayısı?','secenekler':['6.02×10²³','3.14×10⁸','9.81','1.38×10⁻²³'],'dogru':0,'kategori':'Kimya'},
      {'soru':'Ohm yasası: V = ?','secenekler':['I/R','I×R','R/I','I+R'],'dogru':1,'kategori':'Fizik'},
      {'soru':'∫2x dx = ?','secenekler':['x²','x²+C','2x²','2x²+C'],'dogru':1,'kategori':'Matematik'},
      {'soru':'Krebs döngüsü nerede?','secenekler':['Çekirdek','Sitoplazma','Mitokondri','Ribozom'],'dogru':2,'kategori':'Biyoloji'},
    ],
    11: [
      {'soru':'Türev: f(x)=x³ → f\'(x)=?','secenekler':['x²','2x²','3x²','3x'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Entropi neyi ölçer?','secenekler':['Enerji','Düzensizlik','Kütle','Hız'],'dogru':1,'kategori':'Fizik'},
      {'soru':'Organik kimyanın temel elementi?','secenekler':['Oksijen','Azot','Karbon','Hidrojen'],'dogru':2,'kategori':'Kimya'},
      {'soru':'Permütasyon P(5,3) = ?','secenekler':['15','30','60','120'],'dogru':2,'kategori':'Matematik'},
      {'soru':'Felsefede "Düşünüyorum, o halde varım" kime ait?','secenekler':['Sokrates','Platon','Descartes','Kant'],'dogru':2,'kategori':'Felsefe'},
    ],
    12: [
      {'soru':'∫₀¹ x² dx = ?','secenekler':['1/2','1/3','1/4','1'],'dogru':1,'kategori':'Matematik'},
      {'soru':'E=mc² kime ait?','secenekler':['Newton','Bohr','Einstein','Planck'],'dogru':2,'kategori':'Fizik'},
      {'soru':'Euler formülü: e^(iπ)+1=?','secenekler':['-1','0','1','π'],'dogru':1,'kategori':'Matematik'},
      {'soru':'GDP neyi ölçer?','secenekler':['Nüfus','Milli gelir','İhracat','Enflasyon'],'dogru':1,'kategori':'Ekonomi'},
      {'soru':'Fibonacci: 1,1,2,3,5,8,?','secenekler':['10','11','12','13'],'dogru':3,'kategori':'Matematik'},
    ],
  };

  @override
  void initState() {
    super.initState();
    final pool = _tumSorular[widget.sinif] ?? _tumSorular[5]!;
    _sorular = List<Map<String, dynamic>>.from(pool)..shuffle(Random());
  }

  @override
  Widget build(BuildContext context) {
    if (_current >= _sorular.length) return _sonucEkrani();

    final soru = _sorular[_current];
    final secenekler = List<String>.from(soru['secenekler']);
    final dogruIdx = soru['dogru'] as int;

    return Scaffold(
      appBar: AppBar(title: Text('Quiz — ${widget.sinif}. Sınıf')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
          LinearProgressIndicator(
            value: (_current + 1) / _sorular.length, minHeight: 6,
            backgroundColor: AppColors.primary.withOpacity(0.1),
            valueColor: const AlwaysStoppedAnimation(AppColors.primary)),
          const SizedBox(height: 6),
          Row(children: [
            Text('Soru ${_current + 1}/${_sorular.length}', style: const TextStyle(fontSize: 12)),
            const Spacer(),
            if (soru['kategori'] != null)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                child: Text(soru['kategori'], style: const TextStyle(fontSize: 10, color: AppColors.gold, fontWeight: FontWeight.bold)),
              ),
          ]),
          const SizedBox(height: 20),
          Text(soru['soru'] as String, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600, height: 1.4)),
          const SizedBox(height: 20),
          ...secenekler.asMap().entries.map((e) {
            final idx = e.key;
            Color? bg, border;
            if (_cevaplandi) {
              if (idx == dogruIdx) { bg = AppColors.success.withOpacity(0.15); border = AppColors.success; }
              else if (idx == _secilen) { bg = AppColors.danger.withOpacity(0.15); border = AppColors.danger; }
            }
            final secili = _secilen == idx && !_cevaplandi;
            return GestureDetector(
              onTap: _cevaplandi ? null : () => setState(() => _secilen = idx),
              child: Container(
                margin: const EdgeInsets.only(bottom: 10), padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: bg ?? (secili ? AppColors.primary.withOpacity(0.1) : null),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: border ?? (secili ? AppColors.primary : Colors.grey.withOpacity(0.3)), width: secili || _cevaplandi ? 2 : 1)),
                child: Row(children: [
                  CircleAvatar(radius: 14, backgroundColor: (border ?? (secili ? AppColors.primary : Colors.grey)).withOpacity(0.15),
                    child: Text(String.fromCharCode(65 + idx), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13,
                        color: border ?? (secili ? AppColors.primary : Colors.grey)))),
                  const SizedBox(width: 12),
                  Expanded(child: Text(e.value, style: const TextStyle(fontSize: 15))),
                  if (_cevaplandi && idx == dogruIdx) const Icon(Icons.check_circle, color: AppColors.success, size: 20),
                  if (_cevaplandi && idx == _secilen && idx != dogruIdx) const Icon(Icons.cancel, color: AppColors.danger, size: 20),
                ]),
              ),
            );
          }),
          const Spacer(),
          SizedBox(height: 52, child: ElevatedButton(
            onPressed: !_cevaplandi
              ? (_secilen == null ? null : () => setState(() { _cevaplandi = true; if (_secilen == dogruIdx) _dogru++; }))
              : () => setState(() { _current++; _secilen = null; _cevaplandi = false; }),
            style: ElevatedButton.styleFrom(backgroundColor: _cevaplandi ? AppColors.success : null),
            child: Text(_cevaplandi ? (_current + 1 >= _sorular.length ? 'SONUÇ' : 'SONRAKİ →') : 'CEVAPLA'),
          )),
        ]),
      ),
    );
  }

  Widget _sonucEkrani() {
    final oran = _dogru / _sorular.length * 100;
    return Scaffold(
      appBar: AppBar(title: const Text('Sonuç')),
      body: Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
        Text(oran >= 70 ? '🎉' : oran >= 50 ? '👍' : '💪', style: const TextStyle(fontSize: 60)),
        const SizedBox(height: 16),
        Text('$_dogru / ${_sorular.length}', style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Text('%${oran.toStringAsFixed(0)} Başarı',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold,
                color: oran >= 70 ? AppColors.success : oran >= 50 ? AppColors.warning : AppColors.danger)),
        const SizedBox(height: 24),
        ElevatedButton.icon(icon: const Icon(Icons.refresh), label: const Text('Tekrar'),
          onPressed: () => setState(() { _sorular.shuffle(Random()); _current = 0; _dogru = 0; _secilen = null; _cevaplandi = false; })),
        const SizedBox(height: 10),
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Trene Dön')),
      ])),
    );
  }
}
