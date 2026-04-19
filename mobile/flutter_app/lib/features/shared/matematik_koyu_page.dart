import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

/// Matematik Köyü (Math Village) — STEAM modülünden
class MatematikKoyuPage extends StatelessWidget {
  const MatematikKoyuPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Matematik Köyü')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        // Hero
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: const LinearGradient(colors: [Color(0xFF6366F1), Color(0xFF8B5CF6)]),
            borderRadius: BorderRadius.circular(18)),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const Text('🏘️', style: TextStyle(fontSize: 40)),
            const SizedBox(height: 8),
            const Text('Matematik Köyü',
                style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
            const Text('Olimpik düzeyde eğitim, interaktif oyunlar',
                style: TextStyle(color: Colors.white70, fontSize: 13)),
            const SizedBox(height: 12),
            // Günlük ipucu
            _GunlukIpucu(),
          ]),
        ),
        const SizedBox(height: 16),

        // Köy Meydanı
        const Text('🏠 Köy Meydanı', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        _MatematikciKart(),
        const SizedBox(height: 16),

        // Oyun Parkı
        const Text('🎮 Oyun Parkı', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        _OyunCard(ikon: '⚡', baslik: 'Hızlı Hesap', aciklama: '4 işlem yarışı', renk: const Color(0xFFF59E0B),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _HizliHesapPage()))),
        _OyunCard(ikon: '⚔️', baslik: 'Çarpım Savaşları', aciklama: 'Çarpım tablosu fethi', renk: const Color(0xFFEF4444),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _CarpimSavaslariPage()))),
        _OyunCard(ikon: '🔢', baslik: 'Sayı Gizemi', aciklama: 'İpuçlarıyla sayı bul', renk: const Color(0xFF10B981),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _SayiGizemiPage()))),
        _OyunCard(ikon: '🔺', baslik: 'Sayı Piramidi', aciklama: 'Toplama piramidi', renk: const Color(0xFF0EA5E9),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _SayiPiramidiPage()))),
        _OyunCard(ikon: '📐', baslik: 'Geometri Macerası', aciklama: 'Şekil + alan + çevre', renk: const Color(0xFF8B5CF6),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _GeometriPage()))),
        _OyunCard(ikon: '🎯', baslik: 'Tahmin Oyunu', aciklama: 'Sayı tahmin et', renk: const Color(0xFF6366F1),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _TahminOyunuPage()))),
        const SizedBox(height: 16),

        // Formül Kütüphanesi
        const Text('📖 Formül Kütüphanesi', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        _FormulKutuphanesi(),
        const SizedBox(height: 16),

        // Matematik Tarihi
        const Text('📜 Matematik Tarihi', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        _MatematikTarihi(),
      ]),
    );
  }
}

// ── Günlük İpucu ──
class _GunlukIpucu extends StatelessWidget {
  static const _ipuclari = [
    {'ikon': '🌻', 'baslik': 'Fibonacci Doğada', 'icerik': 'Ayçiçeği spiralleri 34 ve 55 — Fibonacci sayıları!'},
    {'ikon': '9️⃣', 'baslik': '9\'un Sihri', 'icerik': '9 ile çarpılan sayıların rakamları toplamı hep 9 yapar.'},
    {'ikon': '🔮', 'baslik': 'Euler Formülü', 'icerik': 'e^(iπ) + 1 = 0 — matematiğin en güzel denklemi.'},
    {'ikon': '📏', 'baslik': 'Pi Sayısı', 'icerik': 'π ilk 10 basamak: 3.1415926535 — sonsuz ve tekrarsız!'},
    {'ikon': '🎲', 'baslik': 'Olasılık', 'icerik': '2 zar atıldığında en olası toplam 7\'dir (6 farklı kombinasyon).'},
    {'ikon': '🔢', 'baslik': 'Kaprekar Sabiti', 'icerik': 'Herhangi 4 basamaklı sayı → 6174\'e ulaşır.'},
    {'ikon': '📐', 'baslik': 'Pisagor', 'icerik': 'a²+b²=c² — 4000 yıldır kullanılan en ünlü teorem.'},
  ];
  @override
  Widget build(BuildContext context) {
    final tip = _ipuclari[DateTime.now().day % _ipuclari.length];
    return Container(
      padding: const EdgeInsets.all(12), margin: const EdgeInsets.only(top: 8),
      decoration: BoxDecoration(color: Colors.white.withOpacity(0.12), borderRadius: BorderRadius.circular(12)),
      child: Row(children: [
        Text(tip['ikon']!, style: const TextStyle(fontSize: 24)),
        const SizedBox(width: 10),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(tip['baslik']!, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13)),
          Text(tip['icerik']!, style: const TextStyle(color: Colors.white70, fontSize: 11)),
        ])),
      ]),
    );
  }
}

// ── Matematikçi Kartı ──
class _MatematikciKart extends StatelessWidget {
  static const _matematikçiler = [
    {'ad': 'Carl Friedrich Gauss', 'yil': '1777-1855', 'alan': 'Sayılar Teorisi', 'ikon': '👑',
     'soz': 'Matematik bilimlerin kraliçesidir.', 'bilgi': 'Daha 10 yaşındayken 1\'den 100\'e kadar toplamı 5050 olarak buldu.'},
    {'ad': 'Leonhard Euler', 'yil': '1707-1783', 'alan': 'Analiz, Graf Teorisi', 'ikon': '∞',
     'soz': 'Hayatımın iki büyük tutkusu: matematik ve müzik.', 'bilgi': 'Kör olduktan sonra bile günde 1 makale yazdı.'},
    {'ad': 'Pisagor', 'yil': 'MÖ 570-495', 'alan': 'Geometri', 'ikon': '📐',
     'soz': 'Sayı evrenin özüdür.', 'bilgi': 'a²+b²=c² teoremi 4000 yıldır kullanılıyor.'},
    {'ad': 'Öklid', 'yil': 'MÖ 325-265', 'alan': 'Geometri', 'ikon': '📏',
     'soz': 'Geometriye kraliyet yolu yoktur.', 'bilgi': 'Elementler kitabı 2000+ yıl ders kitabı olarak kullanıldı.'},
    {'ad': 'Archimedes', 'yil': 'MÖ 287-212', 'alan': 'Fizik, Geometri', 'ikon': '⚙️',
     'soz': 'Eureka! Eureka!', 'bilgi': 'Pi sayısını ilk hesaplayan kişi.'},
    {'ad': 'Ramanujan', 'yil': '1887-1920', 'alan': 'Sayılar Teorisi', 'ikon': '🌟',
     'soz': 'Her sayı benim arkadaşımdır.', 'bilgi': '1729 = 12³+1³ = 10³+9³ "Hardy-Ramanujan sayısı".'},
  ];

  @override
  Widget build(BuildContext context) {
    final m = _matematikçiler[DateTime.now().day % _matematikçiler.length];
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor, borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFF6366F1).withOpacity(0.3))),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Text(m['ikon']!, style: const TextStyle(fontSize: 32)),
          const SizedBox(width: 12),
          Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(m['ad']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
            Text('${m['yil']} · ${m['alan']}', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ])),
        ]),
        const SizedBox(height: 10),
        Text('"${m['soz']}"', style: const TextStyle(fontStyle: FontStyle.italic, fontSize: 13)),
        const SizedBox(height: 6),
        Text('💡 ${m['bilgi']}', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
      ]),
    );
  }
}

// ── Oyun Kartı ──
class _OyunCard extends StatelessWidget {
  final String ikon, baslik, aciklama;
  final Color renk;
  final VoidCallback onTap;
  const _OyunCard({required this.ikon, required this.baslik, required this.aciklama,
                    required this.renk, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(
      leading: Container(width: 46, height: 46,
        decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(12)),
        child: Center(child: Text(ikon, style: const TextStyle(fontSize: 24)))),
      title: Text(baslik, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
      subtitle: Text(aciklama, style: const TextStyle(fontSize: 12)),
      trailing: Icon(Icons.play_circle, color: renk, size: 28),
      onTap: onTap,
    ));
  }
}

// ── Formül Kütüphanesi ──
class _FormulKutuphanesi extends StatelessWidget {
  static const _formuller = [
    {'kat': 'Temel', 'items': [
      {'ad': 'Alan (Dikdörtgen)', 'formul': 'A = a × b'},
      {'ad': 'Alan (Üçgen)', 'formul': 'A = (a × h) / 2'},
      {'ad': 'Alan (Daire)', 'formul': 'A = π × r²'},
      {'ad': 'Çevre (Daire)', 'formul': 'Ç = 2 × π × r'},
      {'ad': 'Pisagor', 'formul': 'a² + b² = c²'},
    ]},
    {'kat': 'Cebir', 'items': [
      {'ad': 'Kare farkı', 'formul': 'a²-b² = (a-b)(a+b)'},
      {'ad': 'Tam kare', 'formul': '(a+b)² = a²+2ab+b²'},
      {'ad': 'Diskriminant', 'formul': 'Δ = b²-4ac'},
      {'ad': 'Kökler', 'formul': 'x = (-b±√Δ) / 2a'},
    ]},
    {'kat': 'Oran/Yüzde', 'items': [
      {'ad': 'Yüzde', 'formul': '% = (Parça/Bütün)×100'},
      {'ad': 'Oran', 'formul': 'a/b = c/d → a×d = b×c'},
      {'ad': 'Bileşik Faiz', 'formul': 'A = P(1+r/n)^(nt)'},
    ]},
  ];

  @override
  Widget build(BuildContext context) {
    return Column(children: _formuller.map((k) => ExpansionTile(
      title: Text(k['kat'] as String, style: const TextStyle(fontWeight: FontWeight.bold)),
      children: (k['items'] as List).map((f) => ListTile(
        dense: true,
        title: Text(f['ad'], style: const TextStyle(fontSize: 14)),
        subtitle: Text(f['formul'], style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold,
            color: Color(0xFF6366F1))),
      )).toList(),
    )).toList());
  }
}

// ── Matematik Tarihi ──
class _MatematikTarihi extends StatelessWidget {
  static const _donemler = [
    {'ikon': '🏛️', 'donem': 'Antik Mısır & Babil', 'yil': 'MÖ 3000-500', 'olay': 'Sayı sistemleri, 60 tabanlı sistem'},
    {'ikon': '🏺', 'donem': 'Antik Yunan', 'yil': 'MÖ 600-300', 'olay': 'Öklid Elementler, Pisagor teoremi'},
    {'ikon': '🕌', 'donem': 'İslam Altın Çağı', 'yil': '800-1400', 'olay': 'Harezmi (cebir), Biruni, Ömer Hayyam'},
    {'ikon': '📈', 'donem': 'Kalkülüs Devrimi', 'yil': '1600-1700', 'olay': 'Newton & Leibniz — diferansiyel/integral'},
    {'ikon': '💻', 'donem': 'Modern Dönem', 'yil': '1900-günümüz', 'olay': 'Gödel, Turing, Wiles (Fermat ispatı)'},
  ];

  @override
  Widget build(BuildContext context) {
    return Column(children: _donemler.map((d) => Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor, borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey.withOpacity(0.2))),
      child: Row(children: [
        Text(d['ikon']!, style: const TextStyle(fontSize: 28)),
        const SizedBox(width: 12),
        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(d['donem']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
          Text(d['yil']!, style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
          Text(d['olay']!, style: const TextStyle(fontSize: 12)),
        ])),
      ]),
    )).toList());
  }
}


// ═══════════════════════════════════════════════════════════
// OYUNLAR
// ═══════════════════════════════════════════════════════════

// 1) HIZLI HESAP
class _HizliHesapPage extends StatefulWidget {
  const _HizliHesapPage();
  @override State<_HizliHesapPage> createState() => _HizliHesapState();
}
class _HizliHesapState extends State<_HizliHesapPage> {
  final _rng = Random();
  int _skor = 0, _soru = 0, _toplam = 15;
  late int _a, _b, _cevap; late String _op;
  List<int> _secenekler = [];
  bool? _sonuc; Timer? _timer; int _kalan = 10;

  @override void initState() { super.initState(); _yeni(); }
  @override void dispose() { _timer?.cancel(); super.dispose(); }

  void _yeni() {
    _soru++; _timer?.cancel(); _kalan = 10; _sonuc = null;
    final ops = ['+','-','×','÷'];
    _op = ops[_rng.nextInt(ops.length)];
    switch (_op) {
      case '+': _a = _rng.nextInt(50)+1; _b = _rng.nextInt(50)+1; _cevap = _a+_b;
      case '-': _a = _rng.nextInt(50)+20; _b = _rng.nextInt(_a); _cevap = _a-_b;
      case '×': _a = _rng.nextInt(12)+2; _b = _rng.nextInt(12)+2; _cevap = _a*_b;
      case '÷': _b = _rng.nextInt(10)+2; _cevap = _rng.nextInt(10)+1; _a = _b*_cevap;
    }
    _secenekler = [_cevap];
    while (_secenekler.length < 4) {
      final y = _cevap + _rng.nextInt(20)-10;
      if (y != _cevap && y >= 0 && !_secenekler.contains(y)) _secenekler.add(y);
    }
    _secenekler.shuffle();
    setState(() {});
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_kalan <= 0) { t.cancel(); _cevapla(-1); } else setState(() => _kalan--);
    });
  }

  void _cevapla(int s) {
    _timer?.cancel();
    setState(() { _sonuc = s == _cevap; if (_sonuc!) _skor++; });
    Future.delayed(const Duration(milliseconds: 800), () {
      if (_soru >= _toplam) {
        showDialog(context: context, builder: (_) => AlertDialog(
          title: const Text('⚡ Sonuç'), content: Text('$_skor/$_toplam doğru!'),
          actions: [TextButton(onPressed: () { Navigator.pop(context); setState(() { _skor=0; _soru=0; }); _yeni(); },
            child: const Text('Tekrar'))],
        ));
      } else _yeni();
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: Text('Hızlı Hesap · $_soru/$_toplam')),
    body: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(
      mainAxisAlignment: MainAxisAlignment.center, children: [
        LinearProgressIndicator(value: _kalan/10, minHeight: 6,
          valueColor: AlwaysStoppedAnimation(_kalan<=3 ? AppColors.danger : const Color(0xFFF59E0B))),
        const SizedBox(height: 30),
        Text('$_a $_op $_b = ?', style: const TextStyle(fontSize: 42, fontWeight: FontWeight.bold)),
        const SizedBox(height: 30),
        Wrap(spacing: 12, runSpacing: 12, children: _secenekler.map((s) => SizedBox(width: 130, height: 54,
          child: ElevatedButton(onPressed: _sonuc != null ? null : () => _cevapla(s),
            style: ElevatedButton.styleFrom(backgroundColor: _sonuc != null
              ? (s == _cevap ? AppColors.success : AppColors.danger.withOpacity(0.3))
              : const Color(0xFFF59E0B).withOpacity(0.15)),
            child: Text('$s', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold))),
        )).toList()),
        const SizedBox(height: 16),
        Text('Skor: $_skor', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      ],
    ))),
  );
}

// 2) ÇARPIM SAVAŞLARI
class _CarpimSavaslariPage extends StatefulWidget {
  const _CarpimSavaslariPage();
  @override State<_CarpimSavaslariPage> createState() => _CarpimSavaslariState();
}
class _CarpimSavaslariState extends State<_CarpimSavaslariPage> {
  final _rng = Random();
  int _a = 0, _b = 0, _skor = 0, _soru = 0;
  List<int> _opts = [];
  bool? _sonuc;

  @override void initState() { super.initState(); _yeni(); }

  void _yeni() {
    _soru++; _sonuc = null;
    _a = _rng.nextInt(10)+2; _b = _rng.nextInt(10)+2;
    final cevap = _a*_b;
    _opts = [cevap];
    while (_opts.length < 4) {
      final y = cevap + _rng.nextInt(20)-10;
      if (y != cevap && y > 0 && !_opts.contains(y)) _opts.add(y);
    }
    _opts.shuffle();
    setState(() {});
  }

  void _cevapla(int s) {
    setState(() { _sonuc = s == _a*_b; if (_sonuc!) _skor++; });
    Future.delayed(const Duration(milliseconds: 700), () {
      if (_soru >= 20) {
        showDialog(context: context, builder: (_) => AlertDialog(
          title: const Text('⚔️ Savaş Bitti'), content: Text('$_skor/20 doğru!'),
          actions: [TextButton(onPressed: () { Navigator.pop(context); setState(() { _skor=0; _soru=0; }); _yeni(); },
            child: const Text('Tekrar'))],
        ));
      } else _yeni();
    });
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: Text('Çarpım Savaşları · $_soru/20')),
    body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text('$_a × $_b = ?', style: const TextStyle(fontSize: 44, fontWeight: FontWeight.bold)),
      const SizedBox(height: 30),
      Wrap(spacing: 12, runSpacing: 12, children: _opts.map((s) => SizedBox(width: 130, height: 54,
        child: ElevatedButton(onPressed: _sonuc != null ? null : () => _cevapla(s),
          style: ElevatedButton.styleFrom(backgroundColor: _sonuc != null
            ? (s == _a*_b ? AppColors.success : AppColors.danger.withOpacity(0.3))
            : const Color(0xFFEF4444).withOpacity(0.15)),
          child: Text('$s', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold))),
      )).toList()),
      const SizedBox(height: 20),
      Text('Skor: $_skor', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
    ])),
  );
}

// 3) SAYI GİZEMİ
class _SayiGizemiPage extends StatefulWidget {
  const _SayiGizemiPage();
  @override State<_SayiGizemiPage> createState() => _SayiGizemiState();
}
class _SayiGizemiState extends State<_SayiGizemiPage> {
  late int _hedef;
  final _ctrl = TextEditingController();
  String _ipucu = '';
  int _tahmin = 0;
  bool _bitti = false;

  @override void initState() { super.initState(); _yeni(); }
  @override void dispose() { _ctrl.dispose(); super.dispose(); }

  void _yeni() {
    _hedef = Random().nextInt(100)+1; _ipucu = '1-100 arası bir sayı düşünüyorum.';
    _tahmin = 0; _bitti = false; _ctrl.clear();
    setState(() {});
  }

  void _tahminEt() {
    final t = int.tryParse(_ctrl.text);
    if (t == null) return;
    _tahmin++;
    if (t == _hedef) {
      setState(() { _ipucu = '🎉 $_tahmin tahminde buldun!'; _bitti = true; });
    } else if (t < _hedef) {
      setState(() => _ipucu = '⬆️ Daha büyük! (Tahmin: $_tahmin)');
    } else {
      setState(() => _ipucu = '⬇️ Daha küçük! (Tahmin: $_tahmin)');
    }
    _ctrl.clear();
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Sayı Gizemi'), actions: [
      IconButton(icon: const Icon(Icons.refresh), onPressed: _yeni)]),
    body: Center(child: Padding(padding: const EdgeInsets.all(32), child: Column(
      mainAxisAlignment: MainAxisAlignment.center, children: [
        const Text('🔢', style: TextStyle(fontSize: 60)),
        const SizedBox(height: 16),
        Text(_ipucu, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
        const SizedBox(height: 24),
        if (!_bitti) ...[
          SizedBox(width: 160, child: TextField(controller: _ctrl, keyboardType: TextInputType.number,
            textAlign: TextAlign.center, style: const TextStyle(fontSize: 28),
            decoration: const InputDecoration(border: OutlineInputBorder(), hintText: '?'))),
          const SizedBox(height: 16),
          ElevatedButton(onPressed: _tahminEt, child: const Text('Tahmin Et', style: TextStyle(fontSize: 18))),
        ] else
          ElevatedButton.icon(icon: const Icon(Icons.refresh), label: const Text('Yeni Oyun'), onPressed: _yeni),
      ],
    ))),
  );
}

// 4) SAYI PİRAMİDİ
class _SayiPiramidiPage extends StatefulWidget {
  const _SayiPiramidiPage();
  @override State<_SayiPiramidiPage> createState() => _SayiPiramidiState();
}
class _SayiPiramidiState extends State<_SayiPiramidiPage> {
  late List<List<int?>> _piramit;
  late List<List<int>> _cevap;
  late List<List<bool>> _fixed;
  int _seviye = 4;

  @override void initState() { super.initState(); _yeni(); }

  void _yeni() {
    final rng = Random();
    // Alt satır
    final alt = List.generate(_seviye, (_) => rng.nextInt(9)+1);
    _cevap = [alt];
    for (int i = _seviye-1; i >= 1; i--) {
      final ust = <int>[];
      for (int j = 0; j < i; j++) ust.add(_cevap.last[j] + _cevap.last[j+1]);
      _cevap.add(ust);
    }
    _cevap = _cevap.reversed.toList();
    _piramit = _cevap.map((r) => r.map<int?>((v) => v).toList()).toList();
    _fixed = _cevap.map((r) => List.filled(r.length, false)).toList();
    // Alt satırı göster + tepe
    for (int c = 0; c < _cevap.last.length; c++) { _fixed[_seviye-1][c] = true; }
    _fixed[0][0] = true;
    // Bazı ara değerleri gizle
    for (int r = 1; r < _seviye-1; r++) for (int c = 0; c < _cevap[r].length; c++) {
      if (rng.nextBool()) { _piramit[r][c] = null; } else { _fixed[r][c] = true; }
    }
    setState(() {});
  }

  void _kontrol() {
    bool ok = true;
    for (int r = 0; r < _seviye; r++) for (int c = 0; c < _cevap[r].length; c++) {
      if (_piramit[r][c] != _cevap[r][c]) ok = false;
    }
    showDialog(context: context, builder: (_) => AlertDialog(
      title: Text(ok ? '🎉 Doğru!' : '❌ Yanlış'),
      content: Text(ok ? 'Piramidi doğru tamamladın!' : 'Tekrar dene.'),
      actions: [TextButton(onPressed: () { Navigator.pop(context); if (ok) _yeni(); }, child: const Text('Tamam'))],
    ));
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Sayı Piramidi'),
      actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeni),
        IconButton(icon: const Icon(Icons.check), onPressed: _kontrol)]),
    body: Center(child: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(
      children: [
        const Text('Her hücre = altındaki iki sayının toplamı', style: TextStyle(fontSize: 13)),
        const SizedBox(height: 20),
        ...List.generate(_seviye, (r) => Padding(
          padding: const EdgeInsets.only(bottom: 6),
          child: Row(mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(_cevap[r].length, (c) => Container(
              width: 56, height: 48, margin: const EdgeInsets.symmetric(horizontal: 3),
              decoration: BoxDecoration(
                color: _fixed[r][c] ? const Color(0xFF6366F1).withOpacity(0.15) : Colors.transparent,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: const Color(0xFF6366F1).withOpacity(0.4))),
              child: Center(child: _fixed[r][c]
                ? Text('${_piramit[r][c] ?? ''}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold))
                : SizedBox(width: 40, child: TextField(
                    keyboardType: TextInputType.number, textAlign: TextAlign.center,
                    style: const TextStyle(fontSize: 16),
                    decoration: const InputDecoration(border: InputBorder.none, isDense: true),
                    onChanged: (v) => _piramit[r][c] = int.tryParse(v),
                  ))),
            ))),
        )),
      ],
    ))),
  );
}

// 5) GEOMETRİ MACERASI
class _GeometriPage extends StatefulWidget {
  const _GeometriPage();
  @override State<_GeometriPage> createState() => _GeometriState();
}
class _GeometriState extends State<_GeometriPage> {
  static const _sorular = [
    {'s':'Bir kenarı 5 cm olan karenin alanı?','o':['20','25','30','15'],'d':1,'a':'5²=25 cm²'},
    {'s':'Yarıçapı 7 cm olan dairenin çevresi? (π≈22/7)','o':['44','42','38','48'],'d':0,'a':'2×22/7×7=44 cm'},
    {'s':'Tabanı 10, yüksekliği 6 olan üçgenin alanı?','o':['60','30','40','20'],'d':1,'a':'10×6/2=30 cm²'},
    {'s':'Bir dikdörtgenin kenarları 8 ve 3 cm. Çevresi?','o':['22','24','11','16'],'d':0,'a':'2×(8+3)=22 cm'},
    {'s':'Bir küpün kenarı 4 cm. Hacmi?','o':['16','48','64','32'],'d':2,'a':'4³=64 cm³'},
    {'s':'İç açıları toplamı 540° olan çokgen kaç kenarlıdır?','o':['4','5','6','7'],'d':1,'a':'(n-2)×180=540→n=5'},
    {'s':'Yarıçapı 3 cm olan kürenin hacmi? (π≈3)','o':['108','36','113','81'],'d':0,'a':'4/3×3×27=108 cm³'},
    {'s':'30-60-90 üçgeninde hipotenüs 10 cm ise kısa kenar?','o':['5','6','7','8'],'d':0,'a':'Kısa kenar=hipotenüs/2=5'},
    {'s':'Bir silindir: r=5, h=10. Hacmi? (π≈3)','o':['750','500','250','1000'],'d':0,'a':'3×25×10=750'},
    {'s':'Bir eşkenar üçgenin her açısı kaç derecedir?','o':['45','60','90','120'],'d':1,'a':'180/3=60°'},
  ];
  int _cur = 0, _dogru = 0; int? _sec; bool _cev = false;

  void _cevapla(int i) {
    if (_cev) return;
    setState(() { _sec = i; _cev = true; if (i == _sorular[_cur]['d']) _dogru++; });
    Future.delayed(const Duration(milliseconds: 1200), () {
      if (_cur+1 >= _sorular.length) {
        showDialog(context: context, builder: (_) => AlertDialog(
          title: const Text('📐 Sonuç'), content: Text('$_dogru/${_sorular.length} doğru!'),
          actions: [TextButton(onPressed: () { Navigator.pop(context);
            setState(() { _cur=0; _dogru=0; _sec=null; _cev=false; }); }, child: const Text('Tekrar'))],
        ));
      } else setState(() { _cur++; _sec=null; _cev=false; });
    });
  }

  @override
  Widget build(BuildContext context) {
    final s = _sorular[_cur]; final opts = s['o'] as List; final d = s['d'] as int;
    return Scaffold(
      appBar: AppBar(title: Text('Geometri · ${_cur+1}/${_sorular.length}')),
      body: Padding(padding: const EdgeInsets.all(20), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Container(width: double.infinity, padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(color: const Color(0xFF8B5CF6).withOpacity(0.08), borderRadius: BorderRadius.circular(14)),
          child: Text(s['s'] as String, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600))),
        const SizedBox(height: 16),
        ...List.generate(opts.length, (i) => Padding(padding: const EdgeInsets.only(bottom: 8), child: InkWell(
          onTap: () => _cevapla(i), borderRadius: BorderRadius.circular(12),
          child: Container(padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(borderRadius: BorderRadius.circular(12),
              color: _cev && i == d ? AppColors.success.withOpacity(0.2) : (_cev && i == _sec ? AppColors.danger.withOpacity(0.2) : null),
              border: Border.all(color: _cev && i == d ? AppColors.success : Colors.grey.withOpacity(0.3))),
            child: Text('${String.fromCharCode(65+i)}) ${opts[i]}', style: const TextStyle(fontSize: 16)))))),
        if (_cev) Container(padding: const EdgeInsets.all(12), margin: const EdgeInsets.only(top: 8),
          decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
          child: Text('💡 ${s['a']}', style: const TextStyle(fontSize: 13))),
      ])),
    );
  }
}

// 6) TAHMİN OYUNU
class _TahminOyunuPage extends StatefulWidget {
  const _TahminOyunuPage();
  @override State<_TahminOyunuPage> createState() => _TahminOyunuState();
}
class _TahminOyunuState extends State<_TahminOyunuPage> {
  static const _sorular = [
    {'s':'İstanbul\'un nüfusu yaklaşık kaç milyon?','cevap':16,'birim':'milyon'},
    {'s':'Everest Dağı kaç metre yüksekliktedir?','cevap':8849,'birim':'metre'},
    {'s':'Türkiye\'nin yüzölçümü yaklaşık kaç km²?','cevap':783562,'birim':'km²'},
    {'s':'Bir yılda yaklaşık kaç saat var?','cevap':8760,'birim':'saat'},
    {'s':'İnsan vücudunda yaklaşık kaç kemik var?','cevap':206,'birim':'kemik'},
    {'s':'Dünya\'nın Güneş\'e uzaklığı kaç milyon km?','cevap':150,'birim':'milyon km'},
    {'s':'Bir maraton kaç km?','cevap':42,'birim':'km'},
    {'s':'Işık hızı saniyede yaklaşık kaç km?','cevap':300000,'birim':'km/s'},
  ];
  int _cur = 0, _puan = 0;
  final _ctrl = TextEditingController();
  String? _sonucText;

  void _tahmin() {
    final t = int.tryParse(_ctrl.text); if (t == null) return;
    final cevap = _sorular[_cur]['cevap'] as int;
    final fark = (t - cevap).abs();
    final yuzde = (fark / cevap * 100).round();
    int p = 0;
    if (yuzde <= 5) p = 100; else if (yuzde <= 10) p = 75; else if (yuzde <= 25) p = 50; else if (yuzde <= 50) p = 25;
    _puan += p;
    setState(() => _sonucText = 'Cevap: $cevap ${_sorular[_cur]['birim']}\nSenin tahminin: $t (fark: %$yuzde) → $p puan');
    _ctrl.clear();
  }

  void _sonraki() {
    if (_cur+1 >= _sorular.length) {
      showDialog(context: context, builder: (_) => AlertDialog(
        title: const Text('🎯 Sonuç'), content: Text('Toplam: $_puan puan'),
        actions: [TextButton(onPressed: () { Navigator.pop(context);
          setState(() { _cur=0; _puan=0; _sonucText=null; }); }, child: const Text('Tekrar'))],
      ));
    } else setState(() { _cur++; _sonucText = null; });
  }

  @override
  Widget build(BuildContext context) {
    final s = _sorular[_cur];
    return Scaffold(
      appBar: AppBar(title: Text('Tahmin · ${_cur+1}/${_sorular.length} · $_puan puan')),
      body: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(
        mainAxisAlignment: MainAxisAlignment.center, children: [
          const Text('🎯', style: TextStyle(fontSize: 50)),
          const SizedBox(height: 16),
          Text(s['s'] as String, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
          const SizedBox(height: 20),
          if (_sonucText == null) ...[
            SizedBox(width: 200, child: TextField(controller: _ctrl, keyboardType: TextInputType.number,
              textAlign: TextAlign.center, style: const TextStyle(fontSize: 24),
              decoration: InputDecoration(border: const OutlineInputBorder(), suffixText: s['birim'] as String?))),
            const SizedBox(height: 16),
            ElevatedButton(onPressed: _tahmin, child: const Text('Tahmin Et', style: TextStyle(fontSize: 16))),
          ] else ...[
            Container(padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
              child: Text(_sonucText!, style: const TextStyle(fontSize: 15), textAlign: TextAlign.center)),
            const SizedBox(height: 16),
            ElevatedButton(onPressed: _sonraki, child: const Text('Sonraki')),
          ],
        ],
      ))),
    );
  }
}
