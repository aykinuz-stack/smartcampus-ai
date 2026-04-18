import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Kisisel Dil Gelisimi — 5 dil × 104 ders
/// Her ders: Kelimeler + Gramer + Alistirma
class DilGelisimiPage extends ConsumerStatefulWidget {
  const DilGelisimiPage({super.key});
  @override
  ConsumerState<DilGelisimiPage> createState() => _DilGelisimiPageState();
}

class _DilGelisimiPageState extends ConsumerState<DilGelisimiPage> {
  String _dil = 'ingilizce';
  Map<String, dynamic>? _data;
  bool _yukleniyor = true;
  String? _hata;

  static const _dilBilgi = {
    'ingilizce': {'bayrak': '🇬🇧', 'ad': 'İngilizce', 'renk': Color(0xFF2563EB)},
    'almanca':   {'bayrak': '🇩🇪', 'ad': 'Almanca',   'renk': Color(0xFFDC2626)},
    'fransizca': {'bayrak': '🇫🇷', 'ad': 'Fransızca', 'renk': Color(0xFF0891B2)},
    'italyanca': {'bayrak': '🇮🇹', 'ad': 'İtalyanca', 'renk': Color(0xFF059669)},
    'ispanyolca':{'bayrak': '🇪🇸', 'ad': 'İspanyolca','renk': Color(0xFFD97706)},
  };

  @override
  void initState() { super.initState(); _yukle(); }

  Future<void> _yukle() async {
    setState(() { _yukleniyor = true; _hata = null; });
    try {
      final r = await ref.read(apiClientProvider).get('/dil/dersler', params: {'dil': _dil});
      setState(() { _data = Map<String, dynamic>.from(r.data); _yukleniyor = false; });
    } on DioException catch (e) {
      setState(() { _hata = 'Bağlantı hatası: ${e.message}'; _yukleniyor = false; });
    } catch (e) {
      setState(() { _hata = 'Hata: $e'; _yukleniyor = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    final bilgi = _dilBilgi[_dil]!;
    final renk = bilgi['renk'] as Color;
    final diller = (_data?['diller'] as List?)?.cast<String>() ?? _dilBilgi.keys.toList();
    final dersler = (_data?['dersler'] as List?) ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text('🌍 ${bilgi['ad']}'),
        actions: [
          PopupMenuButton<String>(
            icon: Text(bilgi['bayrak'] as String, style: const TextStyle(fontSize: 24)),
            onSelected: (v) { setState(() => _dil = v); _yukle(); },
            itemBuilder: (_) => diller.map((d) => PopupMenuItem(
              value: d,
              child: Row(children: [
                Text(_dilBilgi[d]?['bayrak'] as String? ?? '🌐', style: const TextStyle(fontSize: 20)),
                const SizedBox(width: 10),
                Text(_dilBilgi[d]?['ad'] as String? ?? d),
                if (d == _dil) ...[const Spacer(), const Icon(Icons.check, color: AppColors.success)],
              ]),
            )).toList(),
          ),
        ],
      ),
      body: _yukleniyor
          ? const Center(child: CircularProgressIndicator())
          : _hata != null
              ? Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                  const Icon(Icons.error_outline, size: 48, color: AppColors.danger),
                  const SizedBox(height: 12),
                  Text(_hata!, textAlign: TextAlign.center),
                  const SizedBox(height: 12),
                  ElevatedButton(onPressed: _yukle, child: const Text('Tekrar Dene')),
                ]))
              : RefreshIndicator(
                  onRefresh: _yukle,
                  child: ListView(padding: const EdgeInsets.all(16), children: [
                    // Hero
                    Container(
                      padding: const EdgeInsets.all(20),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(colors: [renk, renk.withOpacity(0.7)]),
                        borderRadius: BorderRadius.circular(16)),
                      child: Row(children: [
                        Text(bilgi['bayrak'] as String, style: const TextStyle(fontSize: 48)),
                        const SizedBox(width: 16),
                        Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                          Text(bilgi['ad'] as String,
                              style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                          Text('${_data?['toplam_ders'] ?? 0} ders',
                              style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 14)),
                        ])),
                      ]),
                    ),
                    const SizedBox(height: 12),

                    // Dil secici yatay
                    SizedBox(
                      height: 60,
                      child: ListView(scrollDirection: Axis.horizontal, children: diller.map((d) {
                        final info = _dilBilgi[d];
                        final secili = _dil == d;
                        final c = info?['renk'] as Color? ?? AppColors.primary;
                        return GestureDetector(
                          onTap: () { setState(() => _dil = d); _yukle(); },
                          child: Container(
                            width: 70, margin: const EdgeInsets.only(right: 8),
                            decoration: BoxDecoration(
                              color: secili ? c.withOpacity(0.2) : null,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: secili ? c : Colors.grey.withOpacity(0.3), width: secili ? 2.5 : 1)),
                            child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                              Text(info?['bayrak'] as String? ?? '🌐', style: const TextStyle(fontSize: 24)),
                              Text((info?['ad'] as String? ?? d).substring(0, 3),
                                  style: TextStyle(fontSize: 9, fontWeight: secili ? FontWeight.bold : FontWeight.normal, color: secili ? c : null)),
                            ]),
                          ),
                        );
                      }).toList()),
                    ),
                    const SizedBox(height: 16),

                    // Ders listesi
                    Text('${dersler.length} Ders', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 10),
                    if (dersler.isEmpty)
                      const Padding(padding: EdgeInsets.all(32), child: Center(child: Text('Ders bulunamadı')))
                    else
                      ...dersler.map((ders) {
                        final d = ders as Map;
                        return Card(
                          margin: const EdgeInsets.only(bottom: 6),
                          child: ListTile(
                            onTap: () => Navigator.push(context, MaterialPageRoute(
                              builder: (_) => _DersDetayPage(
                                dersNo: (d['no'] as num?)?.toInt() ?? 1,
                                dil: _dil,
                                baslik: d['title'] as String? ?? 'Ders',
                                renk: renk,
                              ),
                            )),
                            leading: Container(
                              width: 40, height: 40,
                              decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                              child: Center(child: Text('${d['no']}',
                                  style: TextStyle(color: renk, fontWeight: FontWeight.bold, fontSize: 14))),
                            ),
                            title: Text(d['title'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                            subtitle: Row(children: [
                              _Tag('${d['kelime_sayisi'] ?? 0} kelime', renk),
                              const SizedBox(width: 4),
                              _Tag('${d['gramer_sayisi'] ?? 0} gramer', AppColors.success),
                              const SizedBox(width: 4),
                              _Tag('${d['alistirma_sayisi'] ?? 0} alıştırma', AppColors.gold),
                            ]),
                            trailing: Icon(Icons.arrow_forward_ios, size: 14, color: renk),
                          ),
                        );
                      }),
                  ]),
                ),
    );
  }
}


class _Tag extends StatelessWidget {
  final String text; final Color color;
  const _Tag(this.text, this.color);
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 1),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(4)),
      child: Text(text, style: TextStyle(fontSize: 8, color: color, fontWeight: FontWeight.bold)),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// DERS DETAY — Kelimeler + Gramer + Alistirma
// ═══════════════════════════════════════════════════════════

class _DersDetayPage extends ConsumerStatefulWidget {
  final int dersNo;
  final String dil;
  final String baslik;
  final Color renk;
  const _DersDetayPage({required this.dersNo, required this.dil, required this.baslik, required this.renk});
  @override
  ConsumerState<_DersDetayPage> createState() => _DersDetayPageState();
}

class _DersDetayPageState extends ConsumerState<_DersDetayPage> with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Map<String, dynamic>? _data;
  bool _yukleniyor = true;
  String? _hata;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
    _yukle();
  }

  Future<void> _yukle() async {
    setState(() { _yukleniyor = true; _hata = null; });
    try {
      final r = await ref.read(apiClientProvider).get(
        '/dil/ders/${widget.dersNo}', params: {'dil': widget.dil});
      setState(() { _data = Map<String, dynamic>.from(r.data); _yukleniyor = false; });
    } catch (e) {
      setState(() { _hata = 'Hata: $e'; _yukleniyor = false; });
    }
  }

  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Ders ${widget.dersNo}'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(icon: Icon(Icons.translate, size: 18), text: 'Kelimeler'),
          Tab(icon: Icon(Icons.school, size: 18), text: 'Gramer'),
          Tab(icon: Icon(Icons.quiz, size: 18), text: 'Alıştırma'),
        ]),
      ),
      body: _yukleniyor
          ? const Center(child: CircularProgressIndicator())
          : _hata != null
              ? Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
                  Text(_hata!), const SizedBox(height: 12),
                  ElevatedButton(onPressed: _yukle, child: const Text('Tekrar Dene')),
                ]))
              : TabBarView(controller: _tabCtrl, children: [
                  _KelimelerTab(data: _data!, renk: widget.renk, baslik: widget.baslik),
                  _GramerTab(data: _data!),
                  _AlistirmaTab(data: _data!, renk: widget.renk),
                ]),
    );
  }
}


class _KelimelerTab extends StatelessWidget {
  final Map<String, dynamic> data;
  final Color renk;
  final String baslik;
  const _KelimelerTab({required this.data, required this.renk, required this.baslik});

  @override
  Widget build(BuildContext context) {
    final vocab = (data['vocabulary'] as List?) ?? [];
    return ListView(padding: const EdgeInsets.all(16), children: [
      Text(baslik, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      const SizedBox(height: 4),
      Text('${vocab.length} kelime', style: TextStyle(fontSize: 12, color: renk)),
      const SizedBox(height: 16),
      if (vocab.isEmpty)
        const Center(child: Text('Bu derste kelime yok'))
      else
        ...vocab.map((v) {
          final vv = v as Map;
          return Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(
            leading: Container(
              width: 44, height: 44,
              decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
              child: const Center(child: Icon(Icons.translate, size: 20)),
            ),
            title: Text(vv['word'] ?? '', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 17, color: renk)),
            subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              if ((vv['pron'] as String? ?? '').isNotEmpty)
                Text('/${vv['pron']}/', style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: AppColors.info)),
              Text(vv['tr'] ?? '', style: const TextStyle(fontSize: 14)),
            ]),
          ));
        }),
    ]);
  }
}


class _GramerTab extends StatelessWidget {
  final Map<String, dynamic> data;
  const _GramerTab({required this.data});

  @override
  Widget build(BuildContext context) {
    final topics = (data['grammar_topics'] as List?) ?? [];
    final examples = (data['grammar_examples'] as List?) ?? [];
    final reading = data['reading'] as String? ?? '';

    return ListView(padding: const EdgeInsets.all(16), children: [
      if (topics.isNotEmpty) ...[
        const Text('📚 Gramer Konuları', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        ...topics.map((g) => Card(child: ListTile(
          dense: true,
          leading: const Icon(Icons.school, color: AppColors.success, size: 18),
          title: Text(g.toString(), style: const TextStyle(fontSize: 14)),
        ))),
      ],
      if (examples.isNotEmpty) ...[
        const SizedBox(height: 16),
        const Text('💬 Örnekler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        ...examples.map((e) => Container(
          margin: const EdgeInsets.only(bottom: 6), padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.success.withOpacity(0.08), borderRadius: BorderRadius.circular(8),
            border: const Border(left: BorderSide(color: AppColors.success, width: 3))),
          child: Text(e.toString(), style: const TextStyle(fontSize: 13, height: 1.5)),
        )),
      ],
      if (reading.isNotEmpty) ...[
        const SizedBox(height: 16),
        const Text('📖 Okuma Parçası', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(color: AppColors.info.withOpacity(0.08), borderRadius: BorderRadius.circular(10)),
          child: Text(reading, style: const TextStyle(fontSize: 14, height: 1.6)),
        ),
      ],
      if (topics.isEmpty && examples.isEmpty && reading.isEmpty)
        const Padding(padding: EdgeInsets.all(32), child: Center(child: Text('Bu derste gramer içeriği yok'))),
    ]);
  }
}


class _AlistirmaTab extends StatelessWidget {
  final Map<String, dynamic> data;
  final Color renk;
  const _AlistirmaTab({required this.data, required this.renk});

  @override
  Widget build(BuildContext context) {
    final exercises = (data['exercises'] as List?) ?? [];
    if (exercises.isEmpty) {
      return const Center(child: Text('Bu derste alıştırma yok'));
    }
    return ListView(padding: const EdgeInsets.all(16), children: [
      Text('${exercises.length} Alıştırma', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
      const SizedBox(height: 12),
      ...exercises.asMap().entries.map((e) {
        final i = e.key;
        final ex = e.value;
        if (ex is Map) {
          final soru = ex['question'] ?? ex['soru'] ?? ex.toString();
          final options = (ex['options'] as List?) ?? [];
          return Card(margin: const EdgeInsets.only(bottom: 10), child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text('Soru ${i + 1}', style: TextStyle(fontWeight: FontWeight.bold, color: renk, fontSize: 12)),
              const SizedBox(height: 6),
              Text(soru.toString(), style: const TextStyle(fontSize: 15)),
              if (options.isNotEmpty) ...[
                const SizedBox(height: 8),
                ...options.map((opt) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 3),
                  child: Row(children: [
                    Icon(Icons.radio_button_off, size: 16, color: renk),
                    const SizedBox(width: 8),
                    Expanded(child: Text(opt.toString(), style: const TextStyle(fontSize: 13))),
                  ]),
                )),
              ],
            ]),
          ));
        }
        return Card(child: ListTile(
          dense: true,
          leading: Text('${i + 1}', style: TextStyle(fontWeight: FontWeight.bold, color: renk)),
          title: Text(ex.toString(), style: const TextStyle(fontSize: 13)),
        ));
      }),
    ]);
  }
}
