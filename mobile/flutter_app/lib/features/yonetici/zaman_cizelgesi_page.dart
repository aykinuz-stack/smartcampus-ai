import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class ZamanCizelgesiPage extends ConsumerStatefulWidget {
  const ZamanCizelgesiPage({super.key});
  @override
  ConsumerState<ZamanCizelgesiPage> createState() => _ZamanCizelgesiPageState();
}

class _ZamanCizelgesiPageState extends ConsumerState<ZamanCizelgesiPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/zaman-cizelgesi')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('⏰ Zaman Çizelgesi')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final cizelge = (d['cizelge'] as List?) ?? [];
          final aktif = d['aktif_dilim'] as Map?;
          final simdi = d['simdi'] as String? ?? '';

          return ListView(padding: const EdgeInsets.all(16), children: [
            // Saat banner
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(children: [
                const Icon(Icons.access_time, color: Colors.white, size: 32),
                const SizedBox(width: 12),
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(simdi, style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
                  Text(
                    aktif != null
                        ? '${aktif['tur'] == 'ders' ? '${aktif['no']}. Ders' : aktif['tur'] == 'teneffus' ? 'Teneffüs' : aktif['tur'] == 'ogle' ? 'Öğle Arası' : 'Etüt'} devam ediyor'
                        : 'Ders saati dışında',
                    style: const TextStyle(color: Colors.white70, fontSize: 13),
                  ),
                ]),
              ]),
            ),
            const SizedBox(height: 20),

            // Cizelge listesi
            ...cizelge.map((c) {
              final cc = c as Map;
              final tur = cc['tur'] as String? ?? '';
              final no = cc['no'] as int? ?? 0;
              final saat = cc['saat'] ?? '';
              final bitis = cc['bitis'] ?? '';
              final sure = cc['sure'] ?? 0;
              final isAktif = aktif != null && aktif['saat'] == saat;

              Color renk;
              IconData ikon;
              String etiket;
              switch (tur) {
                case 'ders':
                  renk = AppColors.primary; ikon = Icons.menu_book; etiket = '$no. Ders'; break;
                case 'teneffus':
                  renk = AppColors.success; ikon = Icons.free_breakfast; etiket = 'Teneffüs'; break;
                case 'ogle':
                  renk = AppColors.gold; ikon = Icons.restaurant; etiket = 'Öğle Arası'; break;
                case 'etut':
                  renk = AppColors.info; ikon = Icons.auto_stories; etiket = 'Etüt'; break;
                default:
                  renk = Colors.grey; ikon = Icons.schedule; etiket = tur;
              }

              return Container(
                margin: const EdgeInsets.only(bottom: 6),
                decoration: BoxDecoration(
                  color: isAktif ? renk.withOpacity(0.15) : null,
                  borderRadius: BorderRadius.circular(10),
                  border: isAktif ? Border.all(color: renk, width: 2) : null,
                ),
                child: ListTile(
                  leading: Container(
                    width: 42, height: 42,
                    decoration: BoxDecoration(
                      color: renk.withOpacity(isAktif ? 0.3 : 0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Icon(ikon, color: renk, size: 20),
                  ),
                  title: Row(children: [
                    Text(etiket, style: TextStyle(fontWeight: FontWeight.w600, fontSize: 14,
                        color: isAktif ? renk : null)),
                    if (isAktif) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(color: renk, borderRadius: BorderRadius.circular(4)),
                        child: const Text('ŞU AN', style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ]),
                  subtitle: Text('$saat — $bitis ($sure dk)',
                      style: const TextStyle(fontSize: 12)),
                  trailing: tur == 'ders'
                      ? Text('$sure dk', style: TextStyle(color: renk, fontWeight: FontWeight.bold))
                      : null,
                ),
              );
            }),
          ]);
        },
      ),
    );
  }
}
