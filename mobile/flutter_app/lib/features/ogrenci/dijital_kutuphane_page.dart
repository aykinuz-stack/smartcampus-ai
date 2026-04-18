import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class DijitalKutuphanePage extends ConsumerStatefulWidget {
  const DijitalKutuphanePage({super.key});
  @override
  ConsumerState<DijitalKutuphanePage> createState() => _DijitalKutuphanePageState();
}

class _DijitalKutuphanePageState extends ConsumerState<DijitalKutuphanePage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/dijital-kutuphane/icerik').then((r) => Map<String, dynamic>.from(r.data)));
  }

  Future<void> _acUrl(String url) async {
    final uri = Uri.parse(url);
    try {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } catch (_) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Açılamadı: $url'), backgroundColor: AppColors.danger));
      }
    }
  }

  Color _hexToColor(String hex) {
    hex = hex.replaceAll('#', '');
    if (hex.length == 6) hex = 'FF$hex';
    return Color(int.parse(hex, radix: 16));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📚 Dijital Kütüphane')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final kategoriler = (d['kategoriler'] as List?) ?? [];

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Hero
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [Color(0xFF3E2723), Color(0xFF5D4037)]),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('📚', style: TextStyle(fontSize: 36)),
                  const SizedBox(height: 8),
                  const Text('Dijital Kütüphane',
                      style: TextStyle(color: Color(0xFFE8D48B), fontSize: 22, fontWeight: FontWeight.bold)),
                  Text('${kategoriler.length} kategori · 200+ kaynak',
                      style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 12)),
                ]),
              ),
              const SizedBox(height: 16),

              // Bilgi Yarismasi ozel kart
              Card(
                margin: const EdgeInsets.only(bottom: 12),
                color: AppColors.gold.withOpacity(0.08),
                child: ListTile(
                  leading: Container(
                    width: 50, height: 50,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(colors: [AppColors.gold, Color(0xFFD97706)]),
                      borderRadius: BorderRadius.circular(12)),
                    child: const Center(child: Text('🏆', style: TextStyle(fontSize: 26))),
                  ),
                  title: const Text('Bilgi Yarışması', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  subtitle: const Text('1500 soru · İlkokul / Ortaokul / Lise', style: TextStyle(fontSize: 12)),
                  trailing: const Icon(Icons.play_circle, color: AppColors.gold, size: 32),
                  onTap: () => Navigator.push(context, MaterialPageRoute(
                    builder: (_) => const _BilgiYarismasiPage())),
                ),
              ),
              const SizedBox(height: 4),

              // Kategori kartlari
              ...kategoriler.map((kat) {
                final k = kat as Map;
                final renk = _hexToColor(k['renk'] as String? ?? '#6366F1');
                final icerikler = (k['icerikler'] as List?) ?? [];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ExpansionTile(
                    leading: Container(
                      width: 44, height: 44,
                      decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                      child: Center(child: Text(k['ikon'] ?? '📚', style: const TextStyle(fontSize: 22))),
                    ),
                    title: Text(k['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                    subtitle: Row(children: [
                      Text(k['aciklama'] ?? '', style: const TextStyle(fontSize: 11)),
                      const Spacer(),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                        decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(4)),
                        child: Text('${icerikler.length}', style: TextStyle(fontSize: 10, color: renk, fontWeight: FontWeight.bold)),
                      ),
                    ]),
                    children: [
                      Padding(padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
                        child: Column(children: icerikler.map((ic) {
                          final i = ic as Map;
                          final tur = (i['tur'] ?? '').toString();
                          IconData turIkon;
                          switch (tur) {
                            case 'video': turIkon = Icons.play_circle; break;
                            case 'platform': turIkon = Icons.language; break;
                            case 'lab': turIkon = Icons.science; break;
                            case 'kodlama': turIkon = Icons.code; break;
                            case 'radyo': turIkon = Icons.radio; break;
                            case 'muze': turIkon = Icons.museum; break;
                            case 'bilim': turIkon = Icons.rocket_launch; break;
                            case 'ses': turIkon = Icons.headphones; break;
                            case 'sozluk': turIkon = Icons.book; break;
                            default: turIkon = Icons.open_in_new;
                          }
                          return ListTile(
                            dense: true,
                            contentPadding: EdgeInsets.zero,
                            leading: Icon(turIkon, color: renk, size: 20),
                            title: Text(i['ad'] ?? '', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
                            trailing: Icon(Icons.open_in_new, size: 16, color: renk),
                            onTap: () => _acUrl(i['url'] ?? ''),
                          );
                        }).toList()),
                      ),
                    ],
                  ),
                );
              }),
            ]),
          );
        },
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// BİLGİ YARIŞMASI
// ═══════════════════════════════════════════════════════════

class _BilgiYarismasiPage extends ConsumerStatefulWidget {
  const _BilgiYarismasiPage();
  @override
  ConsumerState<_BilgiYarismasiPage> createState() => _BilgiYarismasiPageState();
}

class _BilgiYarismasiPageState extends ConsumerState<_BilgiYarismasiPage> {
  String _level = 'ilkokul';
  Future<Map<String, dynamic>>? _future;
  int _current = 0;
  int _dogru = 0;
  int? _secilen;
  bool _cevaplandi = false;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() {
      _current = 0; _dogru = 0; _secilen = null; _cevaplandi = false;
      _future = ref.read(apiClientProvider)
          .get('/bilgi-yarismasi/$_level')
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🏆 Bilgi Yarışması'),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.school),
            onSelected: (v) { setState(() => _level = v); _load(); },
            itemBuilder: (_) => const [
              PopupMenuItem(value: 'ilkokul', child: Text('İlkokul (500 soru)')),
              PopupMenuItem(value: 'ortaokul', child: Text('Ortaokul (500 soru)')),
              PopupMenuItem(value: 'lise', child: Text('Lise (500 soru)')),
            ],
          ),
        ],
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final sorular = (snap.data?['sorular'] as List?) ?? [];
          if (sorular.isEmpty) return const Center(child: Text('Soru yüklenemedi'));

          if (_current >= sorular.length) {
            final oran = _dogru / sorular.length * 100;
            return Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
              Text(oran >= 70 ? '🎉' : oran >= 50 ? '👍' : '💪', style: const TextStyle(fontSize: 60)),
              const SizedBox(height: 16),
              Text('$_dogru / ${sorular.length}', style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              Text('${_level[0].toUpperCase()}${_level.substring(1)} Seviyesi', style: const TextStyle(fontSize: 14)),
              const SizedBox(height: 8),
              Text('%${oran.toStringAsFixed(0)}',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold,
                      color: oran >= 70 ? AppColors.success : oran >= 50 ? AppColors.warning : AppColors.danger)),
              const SizedBox(height: 24),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                ElevatedButton.icon(icon: const Icon(Icons.refresh), label: const Text('Tekrar'),
                    onPressed: _load),
                const SizedBox(width: 12),
                OutlinedButton.icon(icon: const Icon(Icons.school), label: const Text('Seviye Değiştir'),
                    onPressed: () {
                      final next = _level == 'ilkokul' ? 'ortaokul' : _level == 'ortaokul' ? 'lise' : 'ilkokul';
                      setState(() => _level = next); _load();
                    }),
              ]),
            ]));
          }

          final soru = sorular[_current] as Map;
          final secenekler = (soru['secenekler'] as List?) ?? [];
          final dogruIdx = (soru['dogru'] as num?)?.toInt() ?? 0;

          return Padding(
            padding: const EdgeInsets.all(20),
            child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
              // Progress + level
              Row(children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                  child: Text('${_level[0].toUpperCase()}${_level.substring(1)}',
                      style: const TextStyle(fontSize: 10, color: AppColors.gold, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(width: 8),
                Expanded(child: LinearProgressIndicator(
                  value: (_current + 1) / sorular.length, minHeight: 6,
                  backgroundColor: AppColors.gold.withOpacity(0.1),
                  valueColor: const AlwaysStoppedAnimation(AppColors.gold),
                )),
                const SizedBox(width: 8),
                Text('${_current + 1}/${sorular.length}', style: const TextStyle(fontSize: 12)),
              ]),
              if ((soru['kategori'] as String? ?? '').isNotEmpty) ...[
                const SizedBox(height: 6),
                Text(soru['kategori'], style: const TextStyle(fontSize: 11, color: AppColors.gold)),
              ],
              const SizedBox(height: 20),
              Text(soru['soru'] ?? '', style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w600, height: 1.4)),
              const SizedBox(height: 16),

              ...secenekler.asMap().entries.map((e) {
                final idx = e.key; final text = e.value.toString();
                Color? bg, border;
                if (_cevaplandi) {
                  if (idx == dogruIdx) { bg = AppColors.success.withOpacity(0.15); border = AppColors.success; }
                  else if (idx == _secilen) { bg = AppColors.danger.withOpacity(0.15); border = AppColors.danger; }
                }
                final secili = _secilen == idx && !_cevaplandi;
                return GestureDetector(
                  onTap: _cevaplandi ? null : () => setState(() => _secilen = idx),
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 8), padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: bg ?? (secili ? AppColors.gold.withOpacity(0.1) : null),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: border ?? (secili ? AppColors.gold : Colors.grey.withOpacity(0.3)),
                          width: (secili || _cevaplandi) ? 2 : 1)),
                    child: Row(children: [
                      Container(width: 28, height: 28,
                        decoration: BoxDecoration(shape: BoxShape.circle,
                            color: (border ?? (secili ? AppColors.gold : Colors.grey)).withOpacity(0.15)),
                        child: Center(child: Text(String.fromCharCode(65 + idx),
                            style: TextStyle(fontWeight: FontWeight.bold,
                                color: border ?? (secili ? AppColors.gold : Colors.grey))))),
                      const SizedBox(width: 12),
                      Expanded(child: Text(text, style: const TextStyle(fontSize: 14))),
                      if (_cevaplandi && idx == dogruIdx) const Icon(Icons.check_circle, color: AppColors.success),
                      if (_cevaplandi && idx == _secilen && idx != dogruIdx) const Icon(Icons.cancel, color: AppColors.danger),
                    ]),
                  ),
                );
              }),

              // Aciklama
              if (_cevaplandi && (soru['aciklama'] as String? ?? '').isNotEmpty) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.info.withOpacity(0.08), borderRadius: BorderRadius.circular(8),
                    border: const Border(left: BorderSide(color: AppColors.info, width: 3))),
                  child: Text(soru['aciklama'], style: const TextStyle(fontSize: 12)),
                ),
              ],

              const Spacer(),
              if (!_cevaplandi)
                SizedBox(height: 50, child: ElevatedButton(
                  onPressed: _secilen == null ? null : () {
                    setState(() { _cevaplandi = true; if (_secilen == dogruIdx) _dogru++; });
                  },
                  style: ElevatedButton.styleFrom(backgroundColor: AppColors.gold),
                  child: const Text('CEVAPLA')))
              else
                SizedBox(height: 50, child: ElevatedButton(
                  onPressed: () => setState(() { _current++; _secilen = null; _cevaplandi = false; }),
                  style: ElevatedButton.styleFrom(backgroundColor: AppColors.success),
                  child: Text(_current + 1 >= sorular.length ? 'SONUÇ' : 'SONRAKİ →'))),
            ]),
          );
        },
      ),
    );
  }
}
