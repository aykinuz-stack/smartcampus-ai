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
