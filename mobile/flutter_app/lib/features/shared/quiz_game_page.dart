import 'dart:async';
import 'package:flutter/material.dart';

import '../../core/theme/app_theme.dart';

/// Genel quiz oyun sayfası — tüm yarışma türleri için kullanılır.
class QuizGamePage extends StatefulWidget {
  final String baslik;
  final List<Map<String, dynamic>> sorular;
  final Color renk;
  final int? timerSaniye;

  const QuizGamePage({
    super.key,
    required this.baslik,
    required this.sorular,
    required this.renk,
    this.timerSaniye,
  });

  @override
  State<QuizGamePage> createState() => _QuizGamePageState();
}

class _QuizGamePageState extends State<QuizGamePage> {
  int _current = 0;
  int _dogru = 0;
  int _yanlis = 0;
  int? _secilen;
  bool _cevaplandi = false;
  bool _bitti = false;
  Timer? _timer;
  int _kalan = 0;

  @override
  void initState() {
    super.initState();
    if (widget.timerSaniye != null) {
      _kalan = widget.timerSaniye!;
      _startTimer();
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startTimer() {
    _timer?.cancel();
    _kalan = widget.timerSaniye!;
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_kalan <= 0) {
        t.cancel();
        _sureDoldu();
      } else {
        setState(() => _kalan--);
      }
    });
  }

  void _sureDoldu() {
    if (_cevaplandi) return;
    setState(() {
      _cevaplandi = true;
      _yanlis++;
    });
    Future.delayed(const Duration(seconds: 2), _sonraki);
  }

  void _cevapla(int idx) {
    if (_cevaplandi) return;
    _timer?.cancel();
    final soru = widget.sorular[_current];
    final dogru = soru['d'] as int;

    setState(() {
      _secilen = idx;
      _cevaplandi = true;
      if (idx == dogru) {
        _dogru++;
      } else {
        _yanlis++;
      }
    });

    Future.delayed(const Duration(milliseconds: 1500), _sonraki);
  }

  void _sonraki() {
    if (_current + 1 >= widget.sorular.length) {
      setState(() => _bitti = true);
      return;
    }
    setState(() {
      _current++;
      _secilen = null;
      _cevaplandi = false;
    });
    if (widget.timerSaniye != null) _startTimer();
  }

  @override
  Widget build(BuildContext context) {
    if (_bitti) return _buildSonuc();
    if (widget.sorular.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.baslik)),
        body: const Center(child: Text('Soru bulunamadı')),
      );
    }

    final soru = widget.sorular[_current];
    final soruMetni = soru['s'] as String? ?? soru['q'] as String? ?? '';
    final secenekler = List<String>.from(soru['o'] as List? ?? []);
    final dogruIdx = soru['d'] as int;
    final aciklama = soru['a'] as String? ?? '';
    final kategori = soru['k'] as String? ?? '';

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.baslik),
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.only(right: 14),
              child: Text('${_current + 1}/${widget.sorular.length}',
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Progress bar
          LinearProgressIndicator(
            value: (_current + 1) / widget.sorular.length,
            backgroundColor: Colors.grey.withOpacity(0.2),
            valueColor: AlwaysStoppedAnimation(widget.renk),
            minHeight: 4,
          ),

          // Timer + skor bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            color: widget.renk.withOpacity(0.08),
            child: Row(
              children: [
                _MiniStat(icon: Icons.check_circle, value: '$_dogru', color: AppColors.success),
                const SizedBox(width: 12),
                _MiniStat(icon: Icons.cancel, value: '$_yanlis', color: AppColors.danger),
                const Spacer(),
                if (kategori.isNotEmpty)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                    decoration: BoxDecoration(
                      color: widget.renk.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(kategori, style: TextStyle(fontSize: 11,
                        fontWeight: FontWeight.bold, color: widget.renk)),
                  ),
                if (widget.timerSaniye != null) ...[
                  const SizedBox(width: 10),
                  Icon(Icons.timer, size: 16,
                      color: _kalan <= 10 ? AppColors.danger : Colors.grey),
                  const SizedBox(width: 4),
                  Text('$_kalan s',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13,
                          color: _kalan <= 10 ? AppColors.danger : Colors.grey)),
                ],
              ],
            ),
          ),

          // Soru
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [widget.renk.withOpacity(0.08), widget.renk.withOpacity(0.03)],
                      ),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: widget.renk.withOpacity(0.2)),
                    ),
                    child: Text(
                      soruMetni,
                      style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600, height: 1.5),
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Seçenekler
                  ...List.generate(secenekler.length, (i) {
                    Color bg = Theme.of(context).cardColor;
                    Color border = Colors.grey.withOpacity(0.3);
                    Color textColor = Theme.of(context).textTheme.bodyLarge?.color ?? Colors.white;

                    if (_cevaplandi) {
                      if (i == dogruIdx) {
                        bg = AppColors.success.withOpacity(0.2);
                        border = AppColors.success;
                      } else if (i == _secilen && i != dogruIdx) {
                        bg = AppColors.danger.withOpacity(0.2);
                        border = AppColors.danger;
                      }
                    } else if (i == _secilen) {
                      bg = widget.renk.withOpacity(0.15);
                      border = widget.renk;
                    }

                    final harf = String.fromCharCode(65 + i); // A, B, C, D

                    return Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: InkWell(
                        onTap: _cevaplandi ? null : () => _cevapla(i),
                        borderRadius: BorderRadius.circular(12),
                        child: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
                          decoration: BoxDecoration(
                            color: bg,
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: border, width: 1.5),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 30, height: 30,
                                alignment: Alignment.center,
                                decoration: BoxDecoration(
                                  color: _cevaplandi && i == dogruIdx
                                      ? AppColors.success
                                      : (_cevaplandi && i == _secilen && i != dogruIdx
                                          ? AppColors.danger
                                          : widget.renk.withOpacity(0.15)),
                                  shape: BoxShape.circle,
                                ),
                                child: Text(harf,
                                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14,
                                        color: _cevaplandi && (i == dogruIdx || i == _secilen)
                                            ? Colors.white : widget.renk)),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Text(secenekler[i],
                                    style: TextStyle(fontSize: 15, color: textColor)),
                              ),
                              if (_cevaplandi && i == dogruIdx)
                                const Icon(Icons.check_circle, color: AppColors.success, size: 22),
                              if (_cevaplandi && i == _secilen && i != dogruIdx)
                                const Icon(Icons.cancel, color: AppColors.danger, size: 22),
                            ],
                          ),
                        ),
                      ),
                    );
                  }),

                  // Açıklama
                  if (_cevaplandi && aciklama.isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.info.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: AppColors.info.withOpacity(0.3)),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Icon(Icons.lightbulb, color: AppColors.info, size: 18),
                          const SizedBox(width: 8),
                          Expanded(child: Text(aciklama,
                              style: const TextStyle(fontSize: 13, height: 1.4))),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSonuc() {
    final toplam = widget.sorular.length;
    final yuzde = toplam > 0 ? (_dogru / toplam * 100).round() : 0;
    Color skorRenk = yuzde >= 80 ? AppColors.success
        : (yuzde >= 50 ? AppColors.warning : AppColors.danger);
    String emoji = yuzde >= 80 ? '🏆' : (yuzde >= 50 ? '👍' : '💪');
    String mesaj = yuzde >= 80 ? 'Mükemmel!'
        : (yuzde >= 50 ? 'İyi!' : 'Tekrar dene!');

    // Kategori dağılımı
    final katSkor = <String, List<int>>{};
    for (int i = 0; i < widget.sorular.length; i++) {
      final k = widget.sorular[i]['k'] as String? ?? 'Genel';
      katSkor.putIfAbsent(k, () => [0, 0]);
      katSkor[k]![1]++;
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Sonuç')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const SizedBox(height: 20),
            Text(emoji, style: const TextStyle(fontSize: 60)),
            const SizedBox(height: 10),
            Text(mesaj, style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: skorRenk)),
            const SizedBox(height: 20),

            // Skor dairesi
            Container(
              width: 140, height: 140,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: skorRenk, width: 6),
              ),
              child: Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text('%$yuzde', style: TextStyle(fontSize: 36,
                        fontWeight: FontWeight.bold, color: skorRenk)),
                    Text('$_dogru/$toplam', style: const TextStyle(fontSize: 14)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // İstatistik satırı
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _SonucStat(label: 'Doğru', value: '$_dogru', color: AppColors.success),
                _SonucStat(label: 'Yanlış', value: '$_yanlis', color: AppColors.danger),
                _SonucStat(label: 'Toplam', value: '$toplam', color: widget.renk),
              ],
            ),
            const SizedBox(height: 24),

            // Tekrar oyna
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => Navigator.pop(context),
                icon: const Icon(Icons.arrow_back),
                label: const Text('Yarışmalara Dön'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: widget.renk,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}


class _MiniStat extends StatelessWidget {
  final IconData icon;
  final String value;
  final Color color;
  const _MiniStat({required this.icon, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: color, size: 16),
        const SizedBox(width: 4),
        Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: color)),
      ],
    );
  }
}


class _SonucStat extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _SonucStat({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(value, style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
