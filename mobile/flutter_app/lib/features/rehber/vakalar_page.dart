import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';


class VakalarPage extends ConsumerStatefulWidget {
  const VakalarPage({super.key});

  @override
  ConsumerState<VakalarPage> createState() => _VakalarPageState();
}

class _VakalarPageState extends ConsumerState<VakalarPage> {
  Future<List<dynamic>>? _future;
  String? _durumFiltre;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(rehberApiProvider).vakalar(durum: _durumFiltre));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Vakalar'),
        actions: [
          PopupMenuButton<String?>(
            icon: const Icon(Icons.filter_list),
            onSelected: (v) { setState(() => _durumFiltre = v); _load(); },
            itemBuilder: (_) => const [
              PopupMenuItem(value: null, child: Text('Hepsi')),
              PopupMenuItem(value: 'acik', child: Text('Açık')),
              PopupMenuItem(value: 'devam', child: Text('Devam Eden')),
              PopupMenuItem(value: 'cozuldu', child: Text('Çözülen')),
            ],
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final list = snap.data ?? [];
          if (list.isEmpty) return const Center(child: Text('Vaka yok'));

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: list.length,
              itemBuilder: (_, i) {
                final v = list[i];
                final durum = v['durum'] as String? ?? '';
                final oncelik = v['oncelik'] as String? ?? '';
                Color c;
                switch (durum) {
                  case 'acik': c = AppColors.danger; break;
                  case 'devam': c = AppColors.warning; break;
                  case 'cozuldu': c = AppColors.success; break;
                  default: c = Colors.grey;
                }

                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: c.withOpacity(0.15),
                      child: Icon(Icons.folder, color: c),
                    ),
                    title: Text('${v['konu']} — ${v['ogrenci_adi']}',
                        style: const TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: Text(
                        '${v['sinif']}/${v['sube']} · Öncelik: $oncelik · ${(v['acilis_tarihi'] ?? '').toString().substring(0, 10)}'),
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: c.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(durum.toUpperCase(),
                          style: TextStyle(color: c, fontSize: 11, fontWeight: FontWeight.bold)),
                    ),
                    onTap: () async {
                      if (durum != 'cozuldu') {
                        final ok = await showDialog<bool>(
                          context: context,
                          builder: (_) => AlertDialog(
                            title: const Text('Vakayı Kapat'),
                            content: Text('"${v['konu']}" vakası kapatılsın mı?'),
                            actions: [
                              TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Vazgeç')),
                              TextButton(
                                onPressed: () => Navigator.pop(context, true),
                                child: const Text('Kapat'),
                              ),
                            ],
                          ),
                        );
                        if (ok == true) {
                          await ref.read(rehberApiProvider).vakaKapat(v['id'] as String);
                          _load();
                        }
                      }
                    },
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}
