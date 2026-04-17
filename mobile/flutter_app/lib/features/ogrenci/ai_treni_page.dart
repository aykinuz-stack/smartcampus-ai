import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class AiTreniPage extends ConsumerStatefulWidget {
  const AiTreniPage({super.key});
  @override
  ConsumerState<AiTreniPage> createState() => _AiTreniPageState();
}

class _AiTreniPageState extends ConsumerState<AiTreniPage> {
  Future<Map<String, dynamic>>? _configFuture;
  int? _selectedSinif;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _configFuture = ref.read(apiClientProvider)
        .get('/ai-treni/config').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🚂 AI Treni')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _configFuture,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final siniflar = (d['siniflar'] as List?) ?? [];
          final kompartimanlar = (d['kompartimanlar'] as List?) ?? [];

          return ListView(padding: const EdgeInsets.all(16), children: [
            // Hero
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF6366F1), Color(0xFF8B5CF6), Color(0xFFEC4899)],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
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

            // Sinif secici (vagon)
            const Text('🚃 Vagonunu Seç (Sınıf)', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            GridView.builder(
              shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4, crossAxisSpacing: 8, mainAxisSpacing: 8, childAspectRatio: 1.2),
              itemCount: siniflar.length,
              itemBuilder: (_, i) {
                final s = siniflar[i] as Map;
                final no = (s['no'] as num?)?.toInt() ?? i + 1;
                final renk = _hexToColor(s['renk'] as String? ?? '#6366F1');
                final secili = _selectedSinif == no;
                return GestureDetector(
                  onTap: () => setState(() => _selectedSinif = no),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    decoration: BoxDecoration(
                      color: secili ? renk.withOpacity(0.2) : Colors.transparent,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: secili ? renk : Colors.grey.withOpacity(0.3), width: secili ? 2.5 : 1),
                    ),
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
              Builder(builder: (_) {
                final s = siniflar.firstWhere((x) => (x as Map)['no'] == _selectedSinif,
                    orElse: () => {}) as Map;
                return Text(s['tema'] ?? '', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark),
                    textAlign: TextAlign.center);
              }),
            ],

            const SizedBox(height: 20),

            // Kompartımanlar
            if (_selectedSinif != null) ...[
              const Text('🎯 Kompartıman Seç', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              ...kompartimanlar.asMap().entries.map((e) {
                final i = e.key;
                final k = e.value as Map;
                final colors = [AppColors.primary, AppColors.success, AppColors.info, AppColors.gold,
                    AppColors.danger, AppColors.warning, Color(0xFF8B5CF6), Color(0xFF06B6D4),
                    Color(0xFFEC4899), AppColors.primary];
                final c = colors[i % colors.length];

                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    onTap: () {
                      if (k['baslik'] == 'Bilgi Yarışması') {
                        Navigator.push(context, MaterialPageRoute(
                          builder: (_) => _QuizPage(sinif: _selectedSinif!),
                        ));
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                          content: Text('${k['baslik']} — yakında aktif'),
                          backgroundColor: c,
                        ));
                      }
                    },
                    leading: Container(
                      width: 44, height: 44,
                      decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                      child: Center(child: Text(k['ikon'] ?? '📚', style: const TextStyle(fontSize: 22))),
                    ),
                    title: Text(k['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                    subtitle: Text(k['aciklama'] ?? '', style: const TextStyle(fontSize: 11)),
                    trailing: Icon(Icons.arrow_forward_ios, size: 14, color: c),
                  ),
                );
              }),
            ] else
              Container(
                padding: const EdgeInsets.all(32),
                child: const Center(child: Text('Yukarıdan sınıfını seç, kompartımanlar açılsın',
                    style: TextStyle(color: AppColors.textSecondaryDark))),
              ),
          ]);
        },
      ),
    );
  }

  Color _hexToColor(String hex) {
    hex = hex.replaceAll('#', '');
    if (hex.length == 6) hex = 'FF$hex';
    return Color(int.parse(hex, radix: 16));
  }
}


// ═══════════════════════════════════════════════════════════
// QUIZ SAYFASI
// ═══════════════════════════════════════════════════════════

class _QuizPage extends ConsumerStatefulWidget {
  final int sinif;
  const _QuizPage({required this.sinif});
  @override
  ConsumerState<_QuizPage> createState() => _QuizPageState();
}

class _QuizPageState extends ConsumerState<_QuizPage> {
  Future<Map<String, dynamic>>? _future;
  int _current = 0;
  int _dogru = 0;
  int? _secilen;
  bool _cevaplandi = false;

  @override
  void initState() {
    super.initState();
    _future = ref.read(apiClientProvider)
        .get('/ai-treni/quiz/${widget.sinif}')
        .then((r) => Map<String, dynamic>.from(r.data));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('❓ Quiz — ${widget.sinif}. Sınıf')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final sorular = (snap.data?['sorular'] as List?) ?? [];
          if (sorular.isEmpty)
            return const Center(child: Text('Soru bulunamadı'));

          if (_current >= sorular.length) {
            // Sonuc ekrani
            final oran = _dogru / sorular.length * 100;
            return Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
              Text(oran >= 70 ? '🎉' : oran >= 50 ? '👍' : '💪', style: const TextStyle(fontSize: 60)),
              const SizedBox(height: 16),
              Text('$_dogru / ${sorular.length}', style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              Text('Doğru Cevap', style: const TextStyle(fontSize: 14)),
              const SizedBox(height: 8),
              Text('%${oran.toStringAsFixed(0)} Başarı',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold,
                      color: oran >= 70 ? AppColors.success : oran >= 50 ? AppColors.warning : AppColors.danger)),
              const SizedBox(height: 24),
              ElevatedButton.icon(
                icon: const Icon(Icons.refresh),
                label: const Text('Tekrar Dene'),
                onPressed: () => setState(() { _current = 0; _dogru = 0; _secilen = null; _cevaplandi = false; }),
              ),
            ]));
          }

          final soru = sorular[_current] as Map;
          final secenekler = (soru['secenekler'] as List?) ?? [];
          final dogruIdx = (soru['dogru'] as num?)?.toInt() ?? 0;

          return Padding(
            padding: const EdgeInsets.all(20),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              // Progress
              LinearProgressIndicator(
                value: (_current + 1) / sorular.length,
                minHeight: 6,
                backgroundColor: AppColors.primary.withOpacity(0.1),
                valueColor: const AlwaysStoppedAnimation(AppColors.primary),
              ),
              const SizedBox(height: 6),
              Text('Soru ${_current + 1} / ${sorular.length}',
                  style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
              if (soru['kategori'] != null)
                Text(soru['kategori'], style: const TextStyle(fontSize: 11, color: AppColors.gold)),
              const SizedBox(height: 20),

              // Soru
              Text(soru['soru'] ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600, height: 1.4)),
              const SizedBox(height: 20),

              // Secenekler
              ...secenekler.asMap().entries.map((e) {
                final idx = e.key;
                final text = e.value.toString();
                Color? bg;
                Color? border;
                if (_cevaplandi) {
                  if (idx == dogruIdx) { bg = AppColors.success.withOpacity(0.15); border = AppColors.success; }
                  else if (idx == _secilen) { bg = AppColors.danger.withOpacity(0.15); border = AppColors.danger; }
                }
                final secili = _secilen == idx && !_cevaplandi;
                return GestureDetector(
                  onTap: _cevaplandi ? null : () => setState(() => _secilen = idx),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 10),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: bg ?? (secili ? AppColors.primary.withOpacity(0.1) : null),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: border ?? (secili ? AppColors.primary : Colors.grey.withOpacity(0.3)),
                        width: (secili || _cevaplandi) ? 2 : 1),
                    ),
                    child: Row(children: [
                      Container(
                        width: 28, height: 28,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: (border ?? (secili ? AppColors.primary : Colors.grey)).withOpacity(0.15)),
                        child: Center(child: Text(String.fromCharCode(65 + idx),
                            style: TextStyle(fontWeight: FontWeight.bold,
                                color: border ?? (secili ? AppColors.primary : Colors.grey)))),
                      ),
                      const SizedBox(width: 12),
                      Expanded(child: Text(text, style: const TextStyle(fontSize: 15))),
                      if (_cevaplandi && idx == dogruIdx) const Icon(Icons.check_circle, color: AppColors.success),
                      if (_cevaplandi && idx == _secilen && idx != dogruIdx) const Icon(Icons.cancel, color: AppColors.danger),
                    ]),
                  ),
                );
              }),

              const Spacer(),

              // Butonlar
              if (!_cevaplandi)
                SizedBox(height: 52, child: ElevatedButton(
                  onPressed: _secilen == null ? null : () {
                    setState(() {
                      _cevaplandi = true;
                      if (_secilen == dogruIdx) _dogru++;
                    });
                  },
                  child: const Text('CEVAPLA', style: TextStyle(letterSpacing: 1.2)),
                ))
              else
                SizedBox(height: 52, child: ElevatedButton(
                  onPressed: () => setState(() {
                    _current++;
                    _secilen = null;
                    _cevaplandi = false;
                  }),
                  style: ElevatedButton.styleFrom(backgroundColor: AppColors.success),
                  child: Text(_current + 1 >= (sorular.length) ? 'SONUÇ' : 'SONRAKİ SORU →',
                      style: const TextStyle(letterSpacing: 1.2)),
                )),
            ]),
          );
        },
      ),
    );
  }
}
