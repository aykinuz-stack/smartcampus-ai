import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class GununBilgisiPage extends ConsumerStatefulWidget {
  const GununBilgisiPage({super.key});
  @override
  ConsumerState<GununBilgisiPage> createState() => _GununBilgisiPageState();
}

class _GununBilgisiPageState extends ConsumerState<GununBilgisiPage> {
  Future<Map<String, dynamic>>? _future;
  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/gunun-bilgisi').then((r) => Map<String, dynamic>.from(r.data)));
  }

  static const _katIkon = {'tarih': '📜', 'bilim': '🔬', 'doga': '🌿', 'uzay': '🚀',
    'teknoloji': '💻', 'sanat': '🎨', 'matematik': '🔢', 'insan': '👤'};
  static const _katRenk = {'tarih': AppColors.gold, 'bilim': AppColors.info, 'doga': AppColors.success,
    'uzay': Color(0xFF7C3AED), 'teknoloji': AppColors.primary, 'sanat': Color(0xFFEC4899),
    'matematik': AppColors.warning, 'insan': AppColors.danger};

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('💡 Günün Bilgisi')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final bugun = d['bugun'] as Map? ?? {};
          final gecmis = (d['gecmis'] as List?) ?? [];
          final kat = bugun['kategori'] as String? ?? '';
          final renk = _katRenk[kat] ?? AppColors.primary;

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Bugunun bilgisi hero
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: LinearGradient(colors: [renk, renk.withOpacity(0.7)]),
                  borderRadius: BorderRadius.circular(16)),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    Text(_katIkon[kat] ?? '💡', style: const TextStyle(fontSize: 36)),
                    const SizedBox(width: 12),
                    Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      const Text('BUGÜN', style: TextStyle(color: Colors.white70, fontSize: 11, letterSpacing: 2)),
                      Text(bugun['baslik'] ?? 'Yükleniyor...',
                          style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                    ])),
                  ]),
                  const SizedBox(height: 16),
                  Text(bugun['icerik'] ?? '', style: const TextStyle(color: Colors.white, fontSize: 15, height: 1.5)),
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(color: Colors.white.withOpacity(0.2), borderRadius: BorderRadius.circular(8)),
                    child: Text(kat.isNotEmpty ? '${kat[0].toUpperCase()}${kat.substring(1)}' : '',
                        style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
                  ),
                ]),
              ),
              const SizedBox(height: 20),

              // Gecmis
              const Text('📅 Geçmiş Bilgiler', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              ...gecmis.map((g) {
                final gg = g as Map;
                final gKat = gg['kategori'] as String? ?? '';
                final gRenk = _katRenk[gKat] ?? AppColors.primary;
                return Card(margin: const EdgeInsets.only(bottom: 8), child: ListTile(
                  leading: Container(
                    width: 40, height: 40,
                    decoration: BoxDecoration(color: gRenk.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                    child: Center(child: Text(_katIkon[gKat] ?? '💡', style: const TextStyle(fontSize: 20))),
                  ),
                  title: Text(gg['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                  subtitle: Text('${gg['tarih'] ?? ''} · ${gKat}', style: const TextStyle(fontSize: 11)),
                  onTap: () => showDialog(context: context, builder: (_) => AlertDialog(
                    title: Text(gg['baslik'] ?? ''),
                    content: Text(gg['icerik'] ?? ''),
                    actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text('Kapat'))],
                  )),
                ));
              }),
            ]),
          );
        },
      ),
    );
  }
}
