import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';


class OnaylarPage extends ConsumerStatefulWidget {
  const OnaylarPage({super.key});

  @override
  ConsumerState<OnaylarPage> createState() => _OnaylarPageState();
}

class _OnaylarPageState extends ConsumerState<OnaylarPage> {
  Future<List<dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(yoneticiApiProvider).onaylar());
  }

  Future<void> _aksiyon(String id, String aksiyon) async {
    try {
      await ref.read(yoneticiApiProvider).onayAksiyon(id, aksiyon);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(aksiyon == 'onayla' ? '✓ Onaylandı' : '✗ Reddedildi'),
          backgroundColor: aksiyon == 'onayla' ? AppColors.success : AppColors.danger,
        ),
      );
      _load();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Onaylar')),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final list = snap.data ?? [];
          if (list.isEmpty) {
            return const Center(child: Text('✓ Onay bekleyen yok'));
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: list.length,
              itemBuilder: (_, i) {
                final o = list[i];
                final tur = o['tur'] as String? ?? '';
                IconData icon;
                Color c;
                switch (tur) {
                  case 'randevu': icon = Icons.calendar_month; c = AppColors.info; break;
                  case 'belge': icon = Icons.description; c = AppColors.warning; break;
                  case 'izin': icon = Icons.beach_access; c = AppColors.success; break;
                  default: icon = Icons.inbox; c = Colors.grey;
                }

                return Card(
                  margin: const EdgeInsets.only(bottom: 10),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              backgroundColor: c.withOpacity(0.15),
                              child: Icon(icon, color: c),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(o['baslik'] ?? '',
                                      style: const TextStyle(fontWeight: FontWeight.w600)),
                                  Text(o['aciklama'] ?? '',
                                      style: const TextStyle(fontSize: 12)),
                                  const SizedBox(height: 4),
                                  Text('${o['talep_eden']} · ${o['tarih']}',
                                      style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.end,
                          children: [
                            TextButton.icon(
                              onPressed: () => _aksiyon(o['id'] as String, 'reddet'),
                              icon: const Icon(Icons.close, color: AppColors.danger),
                              label: const Text('Reddet', style: TextStyle(color: AppColors.danger)),
                            ),
                            const SizedBox(width: 8),
                            ElevatedButton.icon(
                              onPressed: () => _aksiyon(o['id'] as String, 'onayla'),
                              icon: const Icon(Icons.check),
                              label: const Text('Onayla'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppColors.success,
                                foregroundColor: Colors.white,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
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
