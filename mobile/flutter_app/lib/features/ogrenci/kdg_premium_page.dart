import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// KDG Premium — CEFR bazli Ingilizce + Almanca
class KdgPremiumPage extends ConsumerStatefulWidget {
  const KdgPremiumPage({super.key});
  @override
  ConsumerState<KdgPremiumPage> createState() => _KdgPremiumPageState();
}

class _KdgPremiumPageState extends ConsumerState<KdgPremiumPage> {
  String _dil = 'ingilizce';
  Map<String, dynamic>? _data;
  bool _loading = true;

  static const _dilInfo = {
    'ingilizce': {'bayrak': '🇬🇧', 'ad': 'KDG İngilizce Premium', 'renk': Color(0xFF2563EB)},
    'almanca': {'bayrak': '🇩🇪', 'ad': 'KDG Almanca Premium', 'renk': Color(0xFFDC2626)},
  };

  @override
  void initState() { super.initState(); _yukle(); }

  Future<void> _yukle() async {
    setState(() => _loading = true);
    try {
      final r = await ref.read(apiClientProvider).get('/kdg/$_dil');
      setState(() { _data = Map<String, dynamic>.from(r.data); _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final info = _dilInfo[_dil]!;
    final renk = info['renk'] as Color;
    final seviyeler = (_data?['seviyeler'] as List?) ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text(info['ad'] as String),
        actions: [
          TextButton.icon(
            icon: Text(_dil == 'ingilizce' ? '🇩🇪' : '🇬🇧', style: const TextStyle(fontSize: 20)),
            label: Text(_dil == 'ingilizce' ? 'Almanca' : 'İngilizce',
                style: const TextStyle(fontSize: 12)),
            onPressed: () { setState(() => _dil = _dil == 'ingilizce' ? 'almanca' : 'ingilizce'); _yukle(); },
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
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
                    Text(info['bayrak'] as String, style: const TextStyle(fontSize: 48)),
                    const SizedBox(width: 16),
                    Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text('KDG Premium', style: const TextStyle(color: Colors.white70, fontSize: 11, letterSpacing: 2)),
                      Text(info['ad'] as String,
                          style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                      const Text('CEFR A1 → C1', style: TextStyle(color: Colors.white70, fontSize: 12)),
                    ])),
                  ]),
                ),
                const SizedBox(height: 16),

                // CEFR seviyeleri
                const Text('CEFR Seviyeleri', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                const SizedBox(height: 10),
                ...seviyeler.map((s) {
                  final ss = s as Map;
                  final level = ss['seviye'] as String? ?? '';
                  Color c;
                  switch (level) {
                    case 'A1': c = AppColors.success; break;
                    case 'A2': c = AppColors.info; break;
                    case 'B1': c = AppColors.warning; break;
                    case 'B2': c = AppColors.gold; break;
                    case 'C1': c = AppColors.danger; break;
                    default: c = AppColors.primary;
                  }
                  return Card(
                    margin: const EdgeInsets.only(bottom: 10),
                    child: ListTile(
                      onTap: () => Navigator.push(context, MaterialPageRoute(
                        builder: (_) => _KdgSeviyeDetayPage(dil: _dil, seviye: level, renk: c))),
                      leading: Container(
                        width: 50, height: 50,
                        decoration: BoxDecoration(
                          gradient: LinearGradient(colors: [c, c.withOpacity(0.7)]),
                          borderRadius: BorderRadius.circular(12)),
                        child: Center(child: Text(level,
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16))),
                      ),
                      title: Text('$level — ${ss['aciklama'] ?? ''}',
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      subtitle: Row(children: [
                        _Tag('${ss['kelime_sayisi'] ?? 0} kelime', c),
                        const SizedBox(width: 4),
                        _Tag('${ss['kategori_sayisi'] ?? 0} kategori', AppColors.info),
                        const SizedBox(width: 4),
                        _Tag('${ss['gramer_sayisi'] ?? 0} gramer', AppColors.success),
                      ]),
                      trailing: Icon(Icons.arrow_forward_ios, size: 14, color: c),
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
// SEVIYE DETAY — Kategoriler + Kelimeler + Gramer
// ═══════════════════════════════════════════════════════════

class _KdgSeviyeDetayPage extends ConsumerStatefulWidget {
  final String dil, seviye;
  final Color renk;
  const _KdgSeviyeDetayPage({required this.dil, required this.seviye, required this.renk});
  @override
  ConsumerState<_KdgSeviyeDetayPage> createState() => _KdgSeviyeDetayPageState();
}

class _KdgSeviyeDetayPageState extends ConsumerState<_KdgSeviyeDetayPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Map<String, dynamic>? _data;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _yukle();
  }

  Future<void> _yukle() async {
    setState(() => _loading = true);
    try {
      final r = await ref.read(apiClientProvider).get('/kdg/${widget.dil}/${widget.seviye}');
      setState(() { _data = Map<String, dynamic>.from(r.data); _loading = false; });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  void dispose() { _tabCtrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    final kategoriler = (_data?['kategoriler'] as List?) ?? [];
    final gramer = (_data?['gramer'] as List?) ?? [];

    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.seviye} — ${widget.dil == "ingilizce" ? "🇬🇧" : "🇩🇪"}'),
        bottom: TabBar(controller: _tabCtrl, tabs: const [
          Tab(icon: Icon(Icons.translate, size: 18), text: 'Kelimeler'),
          Tab(icon: Icon(Icons.school, size: 18), text: 'Gramer'),
        ]),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(controller: _tabCtrl, children: [
              // KELIMELER — kategori bazli
              ListView(padding: const EdgeInsets.all(16), children: [
                Text('${_data?['aciklama'] ?? ''} · ${widget.seviye}',
                    style: TextStyle(color: widget.renk, fontSize: 13, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                if (kategoriler.isEmpty)
                  const Center(child: Text('Kelime verisi yok'))
                else
                  ...kategoriler.map((kat) {
                    final k = kat as Map;
                    final kelimeler = (k['kelimeler'] as List?) ?? [];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 10),
                      child: ExpansionTile(
                        leading: Container(
                          width: 40, height: 40,
                          decoration: BoxDecoration(
                            color: widget.renk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                          child: Center(child: Text('${kelimeler.length}',
                              style: TextStyle(color: widget.renk, fontWeight: FontWeight.bold))),
                        ),
                        title: Text(k['kategori'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                        subtitle: Text('${kelimeler.length} kelime', style: const TextStyle(fontSize: 11)),
                        children: [
                          Padding(padding: const EdgeInsets.all(12), child: Column(
                            children: kelimeler.map((w) {
                              final ww = w as Map;
                              return Padding(
                                padding: const EdgeInsets.symmetric(vertical: 4),
                                child: Row(children: [
                                  Expanded(
                                    child: Text(ww['word'] ?? '',
                                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: widget.renk)),
                                  ),
                                  if ((ww['pron'] as String? ?? '').isNotEmpty)
                                    Text('/${ww['pron']}/ ', style: const TextStyle(fontSize: 10, color: AppColors.info, fontStyle: FontStyle.italic)),
                                  Expanded(child: Text(ww['tr'] ?? '', textAlign: TextAlign.right,
                                      style: const TextStyle(fontSize: 14))),
                                ]),
                              );
                            }).toList(),
                          )),
                        ],
                      ),
                    );
                  }),
              ]),

              // GRAMER
              ListView(padding: const EdgeInsets.all(16), children: [
                if (gramer.isEmpty)
                  const Center(child: Text('Gramer verisi yok'))
                else
                  ...gramer.asMap().entries.map((e) {
                    final i = e.key;
                    final g = e.value;
                    if (g is Map) {
                      return Card(margin: const EdgeInsets.only(bottom: 8), child: ExpansionTile(
                        leading: Container(
                          width: 30, height: 30,
                          decoration: BoxDecoration(color: AppColors.success.withOpacity(0.15), shape: BoxShape.circle),
                          child: Center(child: Text('${i + 1}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold))),
                        ),
                        title: Text(g['topic'] ?? g['konu'] ?? 'Konu ${i + 1}',
                            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                        subtitle: Text(g['explanation'] ?? g['aciklama'] ?? '',
                            maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(fontSize: 12)),
                        children: [
                          if (g['examples'] != null || g['ornekler'] != null)
                            Padding(padding: const EdgeInsets.all(12), child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: ((g['examples'] ?? g['ornekler'] ?? []) as List).map((ex) => Container(
                                margin: const EdgeInsets.only(bottom: 6), padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: AppColors.success.withOpacity(0.08), borderRadius: BorderRadius.circular(6),
                                  border: const Border(left: BorderSide(color: AppColors.success, width: 3))),
                                child: Text(ex.toString(), style: const TextStyle(fontSize: 13)),
                              )).toList(),
                            )),
                        ],
                      ));
                    }
                    return ListTile(dense: true, title: Text(g.toString(), style: const TextStyle(fontSize: 13)));
                  }),
              ]),
            ]),
    );
  }
}
