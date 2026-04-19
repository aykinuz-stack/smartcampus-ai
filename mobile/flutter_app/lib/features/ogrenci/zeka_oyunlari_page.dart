import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class ZekaOyunlariPage extends StatelessWidget {
  const ZekaOyunlariPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Zeka Oyunları')),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        // Hero
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            gradient: const LinearGradient(colors: [Color(0xFF6366F1), Color(0xFFEC4899)]),
            borderRadius: BorderRadius.circular(16)),
          child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('🧩', style: TextStyle(fontSize: 36)),
            SizedBox(height: 8),
            Text('Zeka Oyunları Koleksiyonu',
                style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
            Text('7 oyun · Diamond 3D Edition',
                style: TextStyle(color: Colors.white70, fontSize: 13)),
          ]),
        ),
        const SizedBox(height: 16),

        _OyunKart(
          ikon: '🔢', baslik: 'Sudoku', aciklama: '9×9 klasik bulmaca',
          renk: const Color(0xFF6366F1),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _SudokuPage())),
        ),
        _OyunKart(
          ikon: '🟦', baslik: 'Kare Bulmaca', aciklama: 'Sayı yerleştirme',
          renk: const Color(0xFF0EA5E9),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _KareBulmacaPage())),
        ),
        _OyunKart(
          ikon: '🧠', baslik: 'Hafıza Oyunu', aciklama: 'Eşleşen kartları bul',
          renk: const Color(0xFFEC4899),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _HafizaOyunuPage())),
        ),
        _OyunKart(
          ikon: '🔍', baslik: 'Kelime Avı', aciklama: 'Gizli kelimeleri bul',
          renk: const Color(0xFF10B981),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _KelimeAviPage())),
        ),
        _OyunKart(
          ikon: '🔢', baslik: 'Matematik', aciklama: 'Hızlı işlem çöz',
          renk: const Color(0xFFF59E0B),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _MatematikPage())),
        ),
        _OyunKart(
          ikon: '🏙️', baslik: 'Şehir-Hayvan', aciklama: 'İsim-Şehir oyunu',
          renk: const Color(0xFF8B5CF6),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _SehirHayvanPage())),
        ),
        _OyunKart(
          ikon: '🧠', baslik: 'Genel Yetenek', aciklama: 'Mantık + örüntü',
          renk: const Color(0xFFEF4444),
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const _GenelYetenekPage())),
        ),
      ]),
    );
  }
}

class _OyunKart extends StatelessWidget {
  final String ikon, baslik, aciklama;
  final Color renk;
  final VoidCallback onTap;
  const _OyunKart({required this.ikon, required this.baslik, required this.aciklama,
                    required this.renk, required this.onTap});
  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        leading: Container(
          width: 50, height: 50,
          decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(12)),
          child: Center(child: Text(ikon, style: const TextStyle(fontSize: 26))),
        ),
        title: Text(baslik, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(aciklama, style: const TextStyle(fontSize: 12)),
        trailing: Icon(Icons.play_circle, color: renk, size: 28),
        onTap: onTap,
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 1) SUDOKU
// ═══════════════════════════════════════════════════════════

class _SudokuPage extends StatefulWidget {
  const _SudokuPage();
  @override State<_SudokuPage> createState() => _SudokuPageState();
}

class _SudokuPageState extends State<_SudokuPage> {
  late List<List<int>> _board;
  late List<List<int>> _solution;
  late List<List<bool>> _fixed;
  int? _selR, _selC;
  int _hataSayisi = 0;

  @override void initState() { super.initState(); _yeniOyun(); }

  void _yeniOyun() {
    _solution = _generateSudoku();
    _board = _solution.map((r) => List<int>.from(r)).toList();
    _fixed = List.generate(9, (_) => List.filled(9, true));
    final rng = Random();
    int removed = 0;
    while (removed < 40) {
      final r = rng.nextInt(9), c = rng.nextInt(9);
      if (_board[r][c] != 0) { _board[r][c] = 0; _fixed[r][c] = false; removed++; }
    }
    _hataSayisi = 0; _selR = null; _selC = null;
    setState(() {});
  }

  List<List<int>> _generateSudoku() {
    final b = List.generate(9, (_) => List.filled(9, 0));
    _fillBoard(b);
    return b;
  }

  bool _fillBoard(List<List<int>> b) {
    for (int r = 0; r < 9; r++) {
      for (int c = 0; c < 9; c++) {
        if (b[r][c] == 0) {
          final nums = List.generate(9, (i) => i + 1)..shuffle();
          for (final n in nums) {
            if (_isValid(b, r, c, n)) {
              b[r][c] = n;
              if (_fillBoard(b)) return true;
              b[r][c] = 0;
            }
          }
          return false;
        }
      }
    }
    return true;
  }

  bool _isValid(List<List<int>> b, int r, int c, int n) {
    for (int i = 0; i < 9; i++) { if (b[r][i] == n || b[i][c] == n) return false; }
    final br = (r ~/ 3) * 3, bc = (c ~/ 3) * 3;
    for (int i = br; i < br + 3; i++) for (int j = bc; j < bc + 3; j++) if (b[i][j] == n) return false;
    return true;
  }

  void _numSec(int n) {
    if (_selR == null || _selC == null || _fixed[_selR!][_selC!]) return;
    setState(() {
      _board[_selR!][_selC!] = n;
      if (n != _solution[_selR!][_selC!]) _hataSayisi++;
    });
    // Kazandı mı?
    bool tamamlandi = true;
    for (int r = 0; r < 9; r++) for (int c = 0; c < 9; c++) if (_board[r][c] != _solution[r][c]) tamamlandi = false;
    if (tamamlandi) {
      showDialog(context: context, builder: (_) => AlertDialog(
        title: const Text('🎉 Tebrikler!'),
        content: Text('Sudoku tamamlandı! $_hataSayisi hata'),
        actions: [TextButton(onPressed: () { Navigator.pop(context); _yeniOyun(); }, child: const Text('Yeni Oyun'))],
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Sudoku · Hata: $_hataSayisi'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeniOyun)]),
      body: Column(children: [
        Expanded(child: Padding(
          padding: const EdgeInsets.all(8),
          child: AspectRatio(aspectRatio: 1, child: GridView.builder(
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 9),
            itemCount: 81,
            itemBuilder: (_, idx) {
              final r = idx ~/ 9, c = idx % 9;
              final val = _board[r][c];
              final selected = r == _selR && c == _selC;
              final isFixed = _fixed[r][c];
              final isWrong = val != 0 && !isFixed && val != _solution[r][c];
              return GestureDetector(
                onTap: () => setState(() { _selR = r; _selC = c; }),
                child: Container(
                  decoration: BoxDecoration(
                    color: selected ? AppColors.primary.withOpacity(0.2)
                        : isWrong ? AppColors.danger.withOpacity(0.15) : null,
                    border: Border(
                      top: BorderSide(width: r % 3 == 0 ? 2 : 0.5, color: r % 3 == 0 ? Colors.white : Colors.grey.withOpacity(0.3)),
                      left: BorderSide(width: c % 3 == 0 ? 2 : 0.5, color: c % 3 == 0 ? Colors.white : Colors.grey.withOpacity(0.3)),
                      right: BorderSide(width: c == 8 ? 2 : 0, color: Colors.white),
                      bottom: BorderSide(width: r == 8 ? 2 : 0, color: Colors.white),
                    ),
                  ),
                  child: Center(child: Text(
                    val == 0 ? '' : '$val',
                    style: TextStyle(
                      fontSize: 18, fontWeight: isFixed ? FontWeight.bold : FontWeight.normal,
                      color: isWrong ? AppColors.danger : (isFixed ? Colors.white : AppColors.primary)),
                  )),
                ),
              );
            },
          )),
        )),
        // Numpad
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: List.generate(9, (i) => InkWell(
              onTap: () => _numSec(i + 1),
              child: Container(
                width: 36, height: 44,
                decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                child: Center(child: Text('${i + 1}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold))),
              ),
            )),
          ),
        ),
        const SizedBox(height: 8),
      ]),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 2) KARE BULMACA — 4×4 grid, 1-4 yerleştir
// ═══════════════════════════════════════════════════════════

class _KareBulmacaPage extends StatefulWidget {
  const _KareBulmacaPage();
  @override State<_KareBulmacaPage> createState() => _KareBulmacaPageState();
}

class _KareBulmacaPageState extends State<_KareBulmacaPage> {
  late List<List<int>> _board, _solution;
  late List<List<bool>> _fixed;
  int? _selR, _selC;

  @override void initState() { super.initState(); _yeniOyun(); }

  void _yeniOyun() {
    // 4×4 Latin kare oluştur
    _solution = [
      [1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]
    ];
    // Satırları ve sütunları karıştır
    final rng = Random();
    for (int i = 0; i < 10; i++) {
      final a = rng.nextInt(2), b = a + 2;
      if (rng.nextBool()) {
        // Satır swap (aynı blok içinde)
        final r1 = rng.nextBool() ? 0 : 2;
        final tmp = _solution[r1]; _solution[r1] = _solution[r1+1]; _solution[r1+1] = tmp;
      }
    }
    _board = _solution.map((r) => List<int>.from(r)).toList();
    _fixed = List.generate(4, (_) => List.filled(4, true));
    int removed = 0;
    while (removed < 8) {
      final r = rng.nextInt(4), c = rng.nextInt(4);
      if (_board[r][c] != 0) { _board[r][c] = 0; _fixed[r][c] = false; removed++; }
    }
    _selR = null; _selC = null;
    setState(() {});
  }

  void _numSec(int n) {
    if (_selR == null || _selC == null || _fixed[_selR!][_selC!]) return;
    setState(() => _board[_selR!][_selC!] = n);
    bool ok = true;
    for (int r = 0; r < 4; r++) for (int c = 0; c < 4; c++) if (_board[r][c] != _solution[r][c]) ok = false;
    if (ok) {
      showDialog(context: context, builder: (_) => AlertDialog(
        title: const Text('🎉 Bravo!'), content: const Text('Kare bulmaca çözüldü!'),
        actions: [TextButton(onPressed: () { Navigator.pop(context); _yeniOyun(); }, child: const Text('Yeni'))],
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Kare Bulmaca 4×4'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeniOyun)]),
      body: Column(children: [
        const Padding(padding: EdgeInsets.all(16),
          child: Text('Her satır ve sütunda 1-4 arası sayılar birer kez bulunmalı.',
              style: TextStyle(fontSize: 13))),
        Expanded(child: Center(child: SizedBox(
          width: 280, height: 280,
          child: GridView.builder(
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 4, crossAxisSpacing: 4, mainAxisSpacing: 4),
            itemCount: 16,
            itemBuilder: (_, idx) {
              final r = idx ~/ 4, c = idx % 4;
              final val = _board[r][c];
              final sel = r == _selR && c == _selC;
              return GestureDetector(
                onTap: () => setState(() { _selR = r; _selC = c; }),
                child: Container(
                  decoration: BoxDecoration(
                    color: sel ? AppColors.primary.withOpacity(0.3) : AppColors.primary.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: sel ? AppColors.primary : Colors.grey.withOpacity(0.3), width: sel ? 2 : 1),
                  ),
                  child: Center(child: Text(val == 0 ? '' : '$val',
                      style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold,
                          color: _fixed[r][c] ? Colors.white : AppColors.info))),
                ),
              );
            },
          ),
        ))),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: List.generate(4, (i) => ElevatedButton(
              onPressed: () => _numSec(i + 1),
              style: ElevatedButton.styleFrom(fixedSize: const Size(56, 56)),
              child: Text('${i + 1}', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            )),
          ),
        ),
        const SizedBox(height: 16),
      ]),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 3) HAFIZA OYUNU
// ═══════════════════════════════════════════════════════════

class _HafizaOyunuPage extends StatefulWidget {
  const _HafizaOyunuPage();
  @override State<_HafizaOyunuPage> createState() => _HafizaOyunuPageState();
}

class _HafizaOyunuPageState extends State<_HafizaOyunuPage> {
  late List<String> _kartlar;
  late List<bool> _acik, _eslesti;
  int? _ilkSecim;
  int _hamle = 0, _eslesme = 0;
  bool _bekliyor = false;
  static const _emojiler = ['🐱','🐶','🌸','🌞','🦋','🐟','🍎','🌈'];

  @override void initState() { super.initState(); _yeniOyun(); }

  void _yeniOyun() {
    final c = [..._emojiler, ..._emojiler]..shuffle(Random());
    setState(() { _kartlar = c; _acik = List.filled(16, false); _eslesti = List.filled(16, false);
      _ilkSecim = null; _hamle = 0; _eslesme = 0; _bekliyor = false; });
  }

  void _kartTikla(int idx) {
    if (_bekliyor || _acik[idx] || _eslesti[idx]) return;
    setState(() => _acik[idx] = true);
    if (_ilkSecim == null) { _ilkSecim = idx; } else {
      _hamle++;
      if (_kartlar[_ilkSecim!] == _kartlar[idx]) {
        setState(() { _eslesti[_ilkSecim!] = true; _eslesti[idx] = true; _eslesme++; });
        _ilkSecim = null;
      } else {
        _bekliyor = true; final f = _ilkSecim!; _ilkSecim = null;
        Future.delayed(const Duration(milliseconds: 800), () {
          if (mounted) setState(() { _acik[f] = false; _acik[idx] = false; _bekliyor = false; });
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final bitti = _eslesme == 8;
    return Scaffold(
      appBar: AppBar(title: Text('Hafıza Oyunu · $_hamle hamle'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeniOyun)]),
      body: Column(children: [
        if (bitti) Container(
          padding: const EdgeInsets.all(20), margin: const EdgeInsets.all(16),
          decoration: BoxDecoration(color: AppColors.success.withOpacity(0.15), borderRadius: BorderRadius.circular(14)),
          child: Column(children: [
            const Text('🎉 Tebrikler!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text('$_hamle hamlede tamamladın!'),
            const SizedBox(height: 12),
            ElevatedButton.icon(icon: const Icon(Icons.refresh), label: const Text('Tekrar'), onPressed: _yeniOyun),
          ]),
        ),
        Expanded(child: GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 4, crossAxisSpacing: 8, mainAxisSpacing: 8),
          itemCount: 16,
          itemBuilder: (_, i) {
            final g = _acik[i] || _eslesti[i];
            return GestureDetector(onTap: () => _kartTikla(i), child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              decoration: BoxDecoration(
                color: _eslesti[i] ? AppColors.success.withOpacity(0.2) : g ? AppColors.primary.withOpacity(0.15) : AppColors.primary.withOpacity(0.08),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: _eslesti[i] ? AppColors.success : g ? AppColors.primary : Colors.grey.withOpacity(0.3), width: 2),
              ),
              child: Center(child: Text(g ? _kartlar[i] : '❓', style: TextStyle(fontSize: g ? 28 : 22))),
            ));
          },
        )),
      ]),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 4) KELİME AVI
// ═══════════════════════════════════════════════════════════

class _KelimeAviPage extends StatefulWidget {
  const _KelimeAviPage();
  @override State<_KelimeAviPage> createState() => _KelimeAviPageState();
}

class _KelimeAviPageState extends State<_KelimeAviPage> {
  static const _kelimeHavuzu = [
    ['OKUL','DERS','KİTAP','SINIF','ÖDEV'],
    ['DÜNYA','GÜNEŞ','YILDIZ','AY','BULUT'],
    ['ASLAN','KARTAL','BALIK','KEDİ','TAVŞAN'],
    ['ELMA','ARMUT','ÜZM','KİRAZ','MUZ'],
  ];
  late List<String> _hedefler;
  late List<List<String>> _grid;
  final Set<String> _bulunanlar = {};
  List<int> _secili = [];
  int _setIdx = 0;

  @override void initState() { super.initState(); _yeniOyun(); }

  void _yeniOyun() {
    _setIdx = Random().nextInt(_kelimeHavuzu.length);
    _hedefler = _kelimeHavuzu[_setIdx];
    _bulunanlar.clear(); _secili.clear();
    _grid = _generateGrid();
    setState(() {});
  }

  List<List<String>> _generateGrid() {
    const size = 8;
    final g = List.generate(size, (_) => List.generate(size, (_) => ''));
    final rng = Random();
    final harfler = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ';
    // Kelimeleri yatay yerleştir
    for (final k in _hedefler) {
      bool placed = false;
      for (int attempt = 0; attempt < 50 && !placed; attempt++) {
        final r = rng.nextInt(size);
        final c = rng.nextInt(size - k.length + 1);
        bool ok = true;
        for (int i = 0; i < k.length; i++) {
          if (g[r][c + i] != '' && g[r][c + i] != k[i]) { ok = false; break; }
        }
        if (ok) { for (int i = 0; i < k.length; i++) g[r][c + i] = k[i]; placed = true; }
      }
    }
    // Boşları rastgele doldur
    for (int r = 0; r < size; r++) for (int c = 0; c < size; c++) {
      if (g[r][c] == '') g[r][c] = harfler[rng.nextInt(harfler.length)];
    }
    return g;
  }

  void _hucreSec(int r, int c) {
    final idx = r * 8 + c;
    setState(() {
      if (_secili.contains(idx)) { _secili.remove(idx); } else { _secili.add(idx); }
    });
    // Seçili harflerden kelime oluştur
    final seciliHarfler = _secili.map((i) => _grid[i ~/ 8][i % 8]).join();
    for (final k in _hedefler) {
      if (seciliHarfler == k && !_bulunanlar.contains(k)) {
        setState(() { _bulunanlar.add(k); _secili.clear(); });
        if (_bulunanlar.length == _hedefler.length) {
          showDialog(context: context, builder: (_) => AlertDialog(
            title: const Text('🎉 Hepsini buldun!'),
            actions: [TextButton(onPressed: () { Navigator.pop(context); _yeniOyun(); }, child: const Text('Yeni'))],
          ));
        }
        return;
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Kelime Avı · ${_bulunanlar.length}/${_hedefler.length}'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeniOyun)]),
      body: Column(children: [
        // Hedef kelimeler
        Padding(padding: const EdgeInsets.all(12), child: Wrap(spacing: 8, runSpacing: 6,
          children: _hedefler.map((k) => Chip(
            label: Text(k, style: TextStyle(
              fontWeight: FontWeight.bold,
              decoration: _bulunanlar.contains(k) ? TextDecoration.lineThrough : null,
              color: _bulunanlar.contains(k) ? AppColors.success : null)),
            backgroundColor: _bulunanlar.contains(k) ? AppColors.success.withOpacity(0.15) : null,
          )).toList(),
        )),
        // Grid
        Expanded(child: Center(child: Padding(
          padding: const EdgeInsets.all(12),
          child: AspectRatio(aspectRatio: 1, child: GridView.builder(
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 8, crossAxisSpacing: 3, mainAxisSpacing: 3),
            itemCount: 64,
            itemBuilder: (_, idx) {
              final r = idx ~/ 8, c = idx % 8;
              final sel = _secili.contains(idx);
              return GestureDetector(
                onTap: () => _hucreSec(r, c),
                child: Container(
                  decoration: BoxDecoration(
                    color: sel ? AppColors.primary.withOpacity(0.3) : AppColors.primary.withOpacity(0.06),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: sel ? AppColors.primary : Colors.grey.withOpacity(0.2)),
                  ),
                  child: Center(child: Text(_grid[r][c],
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold,
                          color: sel ? AppColors.primary : Colors.white))),
                ),
              );
            },
          )),
        ))),
        Padding(padding: const EdgeInsets.all(12),
          child: TextButton.icon(icon: const Icon(Icons.clear), label: const Text('Seçimi Temizle'),
            onPressed: () => setState(() => _secili.clear()))),
      ]),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 5) MATEMATİK — Hızlı işlem
// ═══════════════════════════════════════════════════════════

class _MatematikPage extends StatefulWidget {
  const _MatematikPage();
  @override State<_MatematikPage> createState() => _MatematikPageState();
}

class _MatematikPageState extends State<_MatematikPage> {
  final _rng = Random();
  int _skor = 0, _soruNo = 0, _toplam = 10;
  late int _a, _b, _cevap;
  late String _op;
  List<int> _secenekler = [];
  bool? _sonuc;
  Timer? _timer;
  int _kalan = 15;

  @override void initState() { super.initState(); _yeniSoru(); }
  @override void dispose() { _timer?.cancel(); super.dispose(); }

  void _yeniSoru() {
    _soruNo++;
    _timer?.cancel();
    _kalan = 15;
    final ops = ['+', '-', '×'];
    _op = ops[_rng.nextInt(ops.length)];
    if (_op == '+') { _a = _rng.nextInt(50) + 1; _b = _rng.nextInt(50) + 1; _cevap = _a + _b; }
    else if (_op == '-') { _a = _rng.nextInt(50) + 20; _b = _rng.nextInt(_a); _cevap = _a - _b; }
    else { _a = _rng.nextInt(12) + 2; _b = _rng.nextInt(12) + 2; _cevap = _a * _b; }

    _secenekler = [_cevap];
    while (_secenekler.length < 4) {
      final y = _cevap + _rng.nextInt(20) - 10;
      if (y != _cevap && y > 0 && !_secenekler.contains(y)) _secenekler.add(y);
    }
    _secenekler.shuffle();
    _sonuc = null;
    setState(() {});
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_kalan <= 0) { t.cancel(); _cevapVer(-1); } else { setState(() => _kalan--); }
    });
  }

  void _cevapVer(int sec) {
    _timer?.cancel();
    setState(() { _sonuc = sec == _cevap; if (_sonuc!) _skor++; });
    Future.delayed(const Duration(seconds: 1), () {
      if (_soruNo >= _toplam) {
        showDialog(context: context, builder: (_) => AlertDialog(
          title: const Text('🎯 Sonuç'),
          content: Text('$_skor / $_toplam doğru!'),
          actions: [TextButton(onPressed: () { Navigator.pop(context);
            setState(() { _skor = 0; _soruNo = 0; }); _yeniSoru(); }, child: const Text('Tekrar'))],
        ));
      } else { _yeniSoru(); }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Matematik · $_soruNo/$_toplam · Skor: $_skor')),
      body: Center(child: Padding(padding: const EdgeInsets.all(24), child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          // Timer
          LinearProgressIndicator(value: _kalan / 15, backgroundColor: Colors.grey.withOpacity(0.2),
            valueColor: AlwaysStoppedAnimation(_kalan <= 5 ? AppColors.danger : AppColors.primary), minHeight: 6),
          const SizedBox(height: 30),
          Text('$_a $_op $_b = ?', style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold)),
          const SizedBox(height: 30),
          Wrap(spacing: 12, runSpacing: 12,
            children: _secenekler.map((s) => SizedBox(width: 140, height: 56,
              child: ElevatedButton(
                onPressed: _sonuc != null ? null : () => _cevapVer(s),
                style: ElevatedButton.styleFrom(
                  backgroundColor: _sonuc != null
                    ? (s == _cevap ? AppColors.success : AppColors.danger.withOpacity(0.3))
                    : AppColors.primary.withOpacity(0.15),
                ),
                child: Text('$s', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              ),
            )).toList(),
          ),
        ],
      ))),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 6) ŞEHİR-HAYVAN — İsim/Şehir/Hayvan/Bitki
// ═══════════════════════════════════════════════════════════

class _SehirHayvanPage extends StatefulWidget {
  const _SehirHayvanPage();
  @override State<_SehirHayvanPage> createState() => _SehirHayvanPageState();
}

class _SehirHayvanPageState extends State<_SehirHayvanPage> {
  static const _veriler = {
    'A': {'isim':'Ali','sehir':'Ankara','hayvan':'Aslan','bitki':'Akasya'},
    'B': {'isim':'Burak','sehir':'Bursa','hayvan':'Balık','bitki':'Begonya'},
    'C': {'isim':'Cem','sehir':'Cizre','hayvan':'Ceylan','bitki':'Ciğdem'},
    'D': {'isim':'Deniz','sehir':'Denizli','hayvan':'Deve','bitki':'Defne'},
    'E': {'isim':'Elif','sehir':'Edirne','hayvan':'Eşek','bitki':'Erik'},
    'F': {'isim':'Fatma','sehir':'Fethiye','hayvan':'Flamingo','bitki':'Fesleğen'},
    'G': {'isim':'Gül','sehir':'Giresun','hayvan':'Geyik','bitki':'Gül'},
    'H': {'isim':'Hakan','sehir':'Hatay','hayvan':'Hamsi','bitki':'Hanımeli'},
    'İ': {'isim':'İrem','sehir':'İstanbul','hayvan':'İnek','bitki':'Itır'},
    'K': {'isim':'Kerem','sehir':'Kayseri','hayvan':'Kedi','bitki':'Karanfil'},
    'L': {'isim':'Leyla','sehir':'Lüleburgaz','hayvan':'Leylek','bitki':'Lale'},
    'M': {'isim':'Mert','sehir':'Muğla','hayvan':'Maymun','bitki':'Manolya'},
    'N': {'isim':'Naz','sehir':'Nevşehir','hayvan':'Nar balığı','bitki':'Nergis'},
    'O': {'isim':'Onur','sehir':'Ordu','hayvan':'Ördek','bitki':'Orkide'},
    'P': {'isim':'Pınar','sehir':'Pendik','hayvan':'Penguen','bitki':'Papatya'},
    'S': {'isim':'Selin','sehir':'Samsun','hayvan':'Sincap','bitki':'Sardunya'},
    'T': {'isim':'Tolga','sehir':'Trabzon','hayvan':'Tavşan','bitki':'Turunç'},
    'Y': {'isim':'Yusuf','sehir':'Yozgat','hayvan':'Yılan','bitki':'Yasemin'},
    'Z': {'isim':'Zeynep','sehir':'Zonguldak','hayvan':'Zebra','bitki':'Zambak'},
  };
  final _harfler = 'ABCDEFGHİKLMNOPSTYZ'.split('');
  late String _harf;
  final _controllers = List.generate(4, (_) => TextEditingController());
  final _kategoriler = ['İsim', 'Şehir', 'Hayvan', 'Bitki'];
  final _keys = ['isim', 'sehir', 'hayvan', 'bitki'];
  List<bool?> _sonuclar = [null, null, null, null];
  bool _kontrol = false;
  int _puan = 0;
  Timer? _timer;
  int _kalan = 30;

  @override void initState() { super.initState(); _yeniTur(); }
  @override void dispose() { _timer?.cancel(); for (var c in _controllers) c.dispose(); super.dispose(); }

  void _yeniTur() {
    _harf = (_harfler..shuffle()).first;
    for (var c in _controllers) c.clear();
    _sonuclar = [null, null, null, null];
    _kontrol = false; _kalan = 30;
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_kalan <= 0) { t.cancel(); _kontrolEt(); } else { setState(() => _kalan--); }
    });
    setState(() {});
  }

  void _kontrolEt() {
    _timer?.cancel();
    final cevaplar = _veriler[_harf] ?? {};
    int p = 0;
    for (int i = 0; i < 4; i++) {
      final yanitTrim = _controllers[i].text.trim().toLowerCase();
      final dogru = (cevaplar[_keys[i]] ?? '').toLowerCase();
      _sonuclar[i] = yanitTrim.isNotEmpty && (yanitTrim == dogru || dogru.contains(yanitTrim));
      if (_sonuclar[i]!) p += 25;
    }
    setState(() { _kontrol = true; _puan += p; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Şehir-Hayvan · Puan: $_puan'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _yeniTur)]),
      body: SingleChildScrollView(padding: const EdgeInsets.all(16), child: Column(
        children: [
          // Harf
          Container(
            width: 80, height: 80,
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [Color(0xFF8B5CF6), Color(0xFFEC4899)]),
              borderRadius: BorderRadius.circular(20)),
            child: Center(child: Text(_harf, style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, color: Colors.white))),
          ),
          const SizedBox(height: 6),
          Text('Kalan: $_kalan sn', style: TextStyle(color: _kalan <= 10 ? AppColors.danger : Colors.grey)),
          const SizedBox(height: 16),
          ...List.generate(4, (i) => Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: TextField(
              controller: _controllers[i],
              enabled: !_kontrol,
              decoration: InputDecoration(
                labelText: _kategoriler[i],
                border: const OutlineInputBorder(),
                suffixIcon: _kontrol ? Icon(
                  _sonuclar[i] == true ? Icons.check_circle : Icons.cancel,
                  color: _sonuclar[i] == true ? AppColors.success : AppColors.danger,
                ) : null,
              ),
            ),
          )),
          if (_kontrol) ...[
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
              child: Column(children: [
                const Text('Doğru cevaplar:', style: TextStyle(fontWeight: FontWeight.bold)),
                ...List.generate(4, (i) => Text(
                  '${_kategoriler[i]}: ${_veriler[_harf]?[_keys[i]] ?? "-"}',
                  style: const TextStyle(fontSize: 13))),
              ]),
            ),
            const SizedBox(height: 12),
            ElevatedButton.icon(icon: const Icon(Icons.arrow_forward), label: const Text('Sonraki'),
              onPressed: _yeniTur),
          ] else
            SizedBox(width: double.infinity, child: ElevatedButton(
              onPressed: _kontrolEt,
              style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 14)),
              child: const Text('Kontrol Et', style: TextStyle(fontSize: 16)),
            )),
        ],
      )),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// 7) GENEL YETENEK — Mantık + Örüntü
// ═══════════════════════════════════════════════════════════

class _GenelYetenekPage extends StatefulWidget {
  const _GenelYetenekPage();
  @override State<_GenelYetenekPage> createState() => _GenelYetenekPageState();
}

class _GenelYetenekPageState extends State<_GenelYetenekPage> {
  static const _sorular = [
    {'s': '2, 4, 8, 16, ?', 'o': ['24', '30', '32', '36'], 'd': 2, 'a': 'Her sayı 2 ile çarpılıyor: 32'},
    {'s': '1, 1, 2, 3, 5, 8, ?', 'o': ['11', '13', '15', '10'], 'd': 1, 'a': 'Fibonacci: 5+8=13'},
    {'s': '3, 6, 12, 24, ?', 'o': ['36', '48', '32', '30'], 'd': 1, 'a': 'Her sayı 2 ile çarpılıyor: 48'},
    {'s': 'A=1, B=2, C=3 ise "DAD" = ?', 'o': ['7', '8', '9', '10'], 'd': 2, 'a': 'D(4)+A(1)+D(4)=9'},
    {'s': '100, 81, 64, 49, ?', 'o': ['25', '36', '30', '40'], 'd': 1, 'a': '10²,9²,8²,7²,6²=36'},
    {'s': 'ARABA kelimesinde kaç sesli harf var?', 'o': ['2', '3', '4', '1'], 'd': 1, 'a': 'A-A-A = 3 sesli'},
    {'s': '5, 10, 20, 40, ?', 'o': ['60', '70', '80', '100'], 'd': 2, 'a': 'Her sayı 2 katı: 80'},
    {'s': 'Bir üçgenin iç açıları toplamı kaç derecedir?', 'o': ['90', '180', '270', '360'], 'd': 1, 'a': '180°'},
    {'s': '1, 4, 9, 16, 25, ?', 'o': ['30', '35', '36', '49'], 'd': 2, 'a': 'Kareler: 6²=36'},
    {'s': 'Saat 3:15\'te akrep ile yelkovan arasındaki açı?', 'o': ['0°', '7.5°', '15°', '90°'], 'd': 1, 'a': 'Akrep 90°+7.5°=97.5°, yelkovan 90°. Fark=7.5°'},
    {'s': '7, 14, 28, 56, ?', 'o': ['84', '96', '112', '128'], 'd': 2, 'a': 'Her sayı 2 ile çarpılıyor: 112'},
    {'s': '"MASA" kelimesinin harflerini ters çevirin', 'o': ['ASAM', 'AMSA', 'AMAS', 'SAMA'], 'd': 0, 'a': 'M-A-S-A ters = A-S-A-M'},
    {'s': '2, 6, 18, 54, ?', 'o': ['108', '162', '72', '126'], 'd': 1, 'a': '3 ile çarpılıyor: 54×3=162'},
    {'s': 'Bir dikdörtgenin 4 köşesi var. 3 dikdörtgende kaç köşe var?', 'o': ['8', '10', '12', '16'], 'd': 2, 'a': '3×4=12'},
    {'s': 'Hangi sayı hem 3\'e hem 5\'e tam bölünür?', 'o': ['10', '12', '15', '20'], 'd': 2, 'a': '15÷3=5, 15÷5=3'},
    {'s': '11, 22, 33, 44, ?', 'o': ['50', '55', '66', '54'], 'd': 1, 'a': '11\'in katları: 55'},
    {'s': 'Bir yılda kaç hafta vardır?', 'o': ['48', '50', '52', '54'], 'd': 2, 'a': '365÷7≈52 hafta'},
    {'s': '1+2+3+...+10 = ?', 'o': ['45', '50', '55', '60'], 'd': 2, 'a': 'n(n+1)/2 = 10×11/2 = 55'},
    {'s': 'K, L, M, N, ?', 'o': ['O', 'P', 'R', 'S'], 'd': 0, 'a': 'Alfabetik sıra: O'},
    {'s': '1000 gramda kaç kilogram vardır?', 'o': ['0.1', '1', '10', '100'], 'd': 1, 'a': '1000g = 1kg'},
  ];

  int _current = 0, _dogru = 0;
  int? _secilen;
  bool _cevaplandi = false;
  late List<Map<String, dynamic>> _karisik;

  @override void initState() { super.initState(); _baslat(); }

  void _baslat() {
    _karisik = List<Map<String, dynamic>>.from(_sorular)..shuffle();
    _karisik = _karisik.take(10).toList();
    _current = 0; _dogru = 0; _secilen = null; _cevaplandi = false;
    setState(() {});
  }

  void _cevapla(int idx) {
    if (_cevaplandi) return;
    setState(() { _secilen = idx; _cevaplandi = true;
      if (idx == _karisik[_current]['d']) _dogru++; });
    Future.delayed(const Duration(milliseconds: 1500), () {
      if (_current + 1 >= _karisik.length) {
        showDialog(context: context, builder: (_) => AlertDialog(
          title: const Text('🧠 Sonuç'),
          content: Text('$_dogru / ${_karisik.length} doğru!'),
          actions: [TextButton(onPressed: () { Navigator.pop(context); _baslat(); }, child: const Text('Tekrar'))],
        ));
      } else {
        setState(() { _current++; _secilen = null; _cevaplandi = false; });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_karisik.isEmpty) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    final s = _karisik[_current];
    final opts = List<String>.from(s['o']);
    final dogru = s['d'] as int;

    return Scaffold(
      appBar: AppBar(title: Text('Genel Yetenek · ${_current + 1}/${_karisik.length}')),
      body: Padding(padding: const EdgeInsets.all(20), child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          LinearProgressIndicator(value: (_current + 1) / _karisik.length, minHeight: 4,
            backgroundColor: Colors.grey.withOpacity(0.2),
            valueColor: const AlwaysStoppedAnimation(Color(0xFFEF4444))),
          const SizedBox(height: 20),
          Container(
            width: double.infinity, padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: const Color(0xFFEF4444).withOpacity(0.08),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: const Color(0xFFEF4444).withOpacity(0.2))),
            child: Text(s['s'], style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, height: 1.5)),
          ),
          const SizedBox(height: 20),
          ...List.generate(opts.length, (i) {
            Color bg = Theme.of(context).cardColor;
            if (_cevaplandi && i == dogru) bg = AppColors.success.withOpacity(0.2);
            if (_cevaplandi && i == _secilen && i != dogru) bg = AppColors.danger.withOpacity(0.2);
            return Padding(padding: const EdgeInsets.only(bottom: 10), child: InkWell(
              onTap: _cevaplandi ? null : () => _cevapla(i),
              borderRadius: BorderRadius.circular(12),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: _cevaplandi && i == dogru ? AppColors.success
                    : (_cevaplandi && i == _secilen ? AppColors.danger : Colors.grey.withOpacity(0.3)))),
                child: Row(children: [
                  Text('${String.fromCharCode(65 + i)})', style: const TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(width: 12),
                  Expanded(child: Text(opts[i], style: const TextStyle(fontSize: 16))),
                ]),
              ),
            ));
          }),
          if (_cevaplandi && s['a'] != null) ...[
            const SizedBox(height: 8),
            Container(padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
              child: Row(children: [
                const Icon(Icons.lightbulb, color: AppColors.info, size: 18),
                const SizedBox(width: 8),
                Expanded(child: Text(s['a'], style: const TextStyle(fontSize: 13))),
              ]),
            ),
          ],
        ],
      )),
    );
  }
}
