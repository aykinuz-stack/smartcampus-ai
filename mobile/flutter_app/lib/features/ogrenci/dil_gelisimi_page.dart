import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class DilGelisimiPage extends ConsumerStatefulWidget {
  const DilGelisimiPage({super.key});
  @override
  ConsumerState<DilGelisimiPage> createState() => _DilGelisimiPageState();
}

class _DilGelisimiPageState extends ConsumerState<DilGelisimiPage> {
  String _dil = 'ingilizce';
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/dil-gelisimi', params: {'dil': _dil})
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  static const _dilIkon = {
    'ingilizce': '🇬🇧', 'almanca': '🇩🇪', 'fransizca': '🇫🇷',
    'italyanca': '🇮🇹', 'ispanyolca': '🇪🇸',
  };
  static const _dilRenk = {
    'ingilizce': AppColors.primary, 'almanca': AppColors.danger,
    'fransizca': AppColors.info, 'italyanca': AppColors.success,
    'ispanyolca': AppColors.gold,
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🌍 Kişisel Dil Gelişimi')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final diller = List<String>.from((d['diller'] as List?) ?? []);
          final dersler = (d['dersler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Dil secici
              const Text('Dil Seç', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              SizedBox(
                height: 80,
                child: ListView(scrollDirection: Axis.horizontal, children: diller.map((dil) {
                  final secili = _dil == dil;
                  final renk = _dilRenk[dil] ?? AppColors.primary;
                  return GestureDetector(
                    onTap: () { setState(() => _dil = dil); _load(); },
                    child: Container(
                      width: 90, margin: const EdgeInsets.only(right: 10),
                      decoration: BoxDecoration(
                        color: secili ? renk.withOpacity(0.2) : Colors.transparent,
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: secili ? renk : Colors.grey.withOpacity(0.3), width: secili ? 2.5 : 1),
                      ),
                      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text(_dilIkon[dil] ?? '🌐', style: const TextStyle(fontSize: 28)),
                        const SizedBox(height: 4),
                        Text(dil[0].toUpperCase() + dil.substring(1),
                            style: TextStyle(fontSize: 11, fontWeight: secili ? FontWeight.bold : FontWeight.normal,
                                color: secili ? renk : null)),
                      ]),
                    ),
                  );
                }).toList()),
              ),
              const SizedBox(height: 16),

              // Ozet
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: LinearGradient(colors: [
                    (_dilRenk[_dil] ?? AppColors.primary),
                    (_dilRenk[_dil] ?? AppColors.primary).withOpacity(0.7),
                  ]),
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Row(children: [
                  Text(_dilIkon[_dil] ?? '🌐', style: const TextStyle(fontSize: 40)),
                  const SizedBox(width: 14),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('${_dil[0].toUpperCase()}${_dil.substring(1)}',
                        style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                    Text('${d['toplam_ders'] ?? 0} ders',
                        style: TextStyle(color: Colors.white.withOpacity(0.8))),
                  ]),
                ]),
              ),
              const SizedBox(height: 16),

              // Ders listesi
              const Text('Dersler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              ...dersler.map((ders) {
                final dd = ders as Map;
                final renk = _dilRenk[_dil] ?? AppColors.primary;
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    onTap: () => _derseGit(dd['no'] as int? ?? 1),
                    leading: Container(
                      width: 40, height: 40,
                      decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                      child: Center(child: Text('${dd['no']}',
                          style: TextStyle(color: renk, fontWeight: FontWeight.bold))),
                    ),
                    title: Text(dd['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                    subtitle: Row(children: [
                      _Tag('${dd['kelime_sayisi']} kelime', AppColors.info),
                      const SizedBox(width: 4),
                      _Tag('${dd['gramer_sayisi']} gramer', AppColors.success),
                      const SizedBox(width: 4),
                      _Tag('${dd['alistirma_sayisi']} alıştırma', AppColors.gold),
                    ]),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 14),
                  ),
                );
              }),
            ]),
          );
        },
      ),
    );
  }

  void _derseGit(int dersNo) {
    Navigator.push(context, MaterialPageRoute(
      builder: (_) => _DersDetayPage(dersNo: dersNo, dil: _dil),
    ));
  }
}


class _Tag extends StatelessWidget {
  final String text; final Color color;
  const _Tag(this.text, this.color);
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(4)),
      child: Text(text, style: TextStyle(fontSize: 9, color: color, fontWeight: FontWeight.bold)),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// DERS DETAY
// ═══════════════════════════════════════════════════════════

class _DersDetayPage extends ConsumerStatefulWidget {
  final int dersNo;
  final String dil;
  const _DersDetayPage({required this.dersNo, required this.dil});
  @override
  ConsumerState<_DersDetayPage> createState() => _DersDetayPageState();
}

class _DersDetayPageState extends ConsumerState<_DersDetayPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
    _future = ref.read(apiClientProvider)
        .get('/yonetici/dil-gelisimi/ders/${widget.dersNo}', params: {'dil': widget.dil})
        .then((r) => Map<String, dynamic>.from(r.data));
  }

  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Ders ${widget.dersNo}'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(text: 'Kelimeler'),
          Tab(text: 'Gramer'),
          Tab(text: 'Alıştırma'),
        ]),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final vocab = (d['vocabulary'] as List?) ?? [];
          final grammar = (d['grammar_topics'] as List?) ?? [];
          final grammarEx = (d['grammar_examples'] as List?) ?? [];
          final exercises = (d['exercises'] as List?) ?? [];
          final reading = d['reading'] as String? ?? '';

          return TabBarView(controller: _tabCtrl, children: [
            // KELIMELER
            ListView(padding: const EdgeInsets.all(16), children: [
              Text(d['title'] ?? '', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              ...vocab.map((v) {
                final vv = v as Map;
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: Container(
                      width: 44, height: 44,
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                      child: const Center(child: Icon(Icons.translate, color: AppColors.primary, size: 20)),
                    ),
                    title: Text(vv['en'] ?? vv['word'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                    subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      if (vv['pron'] != null)
                        Text('/${vv['pron']}/', style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: AppColors.info)),
                      Text(vv['tr'] ?? vv['meaning'] ?? '', style: const TextStyle(fontSize: 14)),
                    ]),
                  ),
                );
              }),
            ]),

            // GRAMER
            ListView(padding: const EdgeInsets.all(16), children: [
              if (grammar.isNotEmpty) ...[
                const Text('Gramer Konuları', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...grammar.map((g) => ListTile(
                  dense: true, contentPadding: EdgeInsets.zero,
                  leading: const Icon(Icons.school, color: AppColors.success, size: 18),
                  title: Text(g.toString(), style: const TextStyle(fontSize: 14)),
                )),
              ],
              if (grammarEx.isNotEmpty) ...[
                const SizedBox(height: 12),
                const Text('Örnekler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                ...grammarEx.map((e) => Container(
                  margin: const EdgeInsets.only(bottom: 6),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.success.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(8),
                    border: Border(left: BorderSide(color: AppColors.success, width: 3)),
                  ),
                  child: Text(e.toString(), style: const TextStyle(fontSize: 13)),
                )),
              ],
              if (reading.isNotEmpty) ...[
                const SizedBox(height: 16),
                const Text('Okuma Parçası', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppColors.info.withOpacity(0.08), borderRadius: BorderRadius.circular(10)),
                  child: Text(reading, style: const TextStyle(fontSize: 14, height: 1.6)),
                ),
              ],
            ]),

            // ALIŞTIRMA
            ListView(padding: const EdgeInsets.all(16), children: [
              if (exercises.isEmpty)
                const Center(child: Padding(padding: EdgeInsets.all(32),
                    child: Text('Bu derste alıştırma yok')))
              else
                ...exercises.asMap().entries.map((e) {
                  final i = e.key;
                  final ex = e.value;
                  if (ex is Map) {
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: Padding(padding: const EdgeInsets.all(14), child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Soru ${i + 1}', style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.gold)),
                          const SizedBox(height: 6),
                          Text(ex['question'] ?? ex['soru'] ?? ex.toString(),
                              style: const TextStyle(fontSize: 14)),
                          if (ex['options'] != null) ...[
                            const SizedBox(height: 8),
                            ...((ex['options'] as List?) ?? []).map((opt) => Padding(
                              padding: const EdgeInsets.symmetric(vertical: 2),
                              child: Row(children: [
                                const Icon(Icons.radio_button_off, size: 16, color: AppColors.textSecondaryDark),
                                const SizedBox(width: 8),
                                Text(opt.toString(), style: const TextStyle(fontSize: 13)),
                              ]),
                            )),
                          ],
                        ],
                      )),
                    );
                  }
                  return ListTile(
                    dense: true,
                    leading: Text('${i + 1}', style: const TextStyle(fontWeight: FontWeight.bold)),
                    title: Text(ex.toString(), style: const TextStyle(fontSize: 13)),
                  );
                }),
            ]),
          ]);
        },
      ),
    );
  }
}
