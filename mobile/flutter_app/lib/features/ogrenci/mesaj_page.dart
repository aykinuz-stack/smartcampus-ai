import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';

class MesajPage extends ConsumerStatefulWidget {
  const MesajPage({super.key});

  @override
  ConsumerState<MesajPage> createState() => _MesajPageState();
}

class _MesajPageState extends ConsumerState<MesajPage> {
  Future<Map<String, dynamic>>? _future;
  final _mesajCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(mesajApiProvider).getListe());
  }

  Future<void> _gonder() async {
    final text = _mesajCtrl.text.trim();
    if (text.isEmpty) return;
    try {
      final user = await ref.read(authServiceProvider).getCurrentUser();
      await ref.read(mesajApiProvider).gonder(
        aliciRol: user?.isOgrenci == true ? 'ogretmen' : 'ogretmen',
        aliciId: 'default_ogretmen',  // Son sürümde öğretmen seçici olacak
        mesaj: text,
      );
      _mesajCtrl.clear();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Mesaj gönderildi'), backgroundColor: AppColors.success),
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
  void dispose() {
    _mesajCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mesajlarım')),
      body: Column(
        children: [
          Expanded(
            child: FutureBuilder<Map<String, dynamic>>(
              future: _future,
              builder: (ctx, snap) {
                if (snap.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }
                if (snap.hasError) return Center(child: Text('Hata: ${snap.error}'));
                final data = snap.data ?? {};
                final mesajlar = (data['mesajlar'] as List?) ?? [];

                if (mesajlar.isEmpty) {
                  return const Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.chat_bubble_outline, size: 64, color: AppColors.textSecondaryDark),
                        SizedBox(height: 12),
                        Text('Mesaj yok'),
                      ],
                    ),
                  );
                }

                return RefreshIndicator(
                  onRefresh: () async => _load(),
                  child: ListView.builder(
                    reverse: true,
                    padding: const EdgeInsets.all(12),
                    itemCount: mesajlar.length,
                    itemBuilder: (_, i) {
                      final m = mesajlar[i];
                      final yon = (m['yon'] as String? ?? '').toLowerCase();
                      final gelen = yon.contains('to_ogrenci') || yon.contains('to_veli');
                      final ad = gelen ? m['ogretmen_adi'] : (m['veli_adi'] ?? 'Ben');

                      return Align(
                        alignment: gelen ? Alignment.centerLeft : Alignment.centerRight,
                        child: Container(
                          margin: const EdgeInsets.symmetric(vertical: 4),
                          padding: const EdgeInsets.all(12),
                          constraints: BoxConstraints(
                            maxWidth: MediaQuery.of(context).size.width * 0.75,
                          ),
                          decoration: BoxDecoration(
                            color: gelen
                                ? AppColors.cardDark
                                : AppColors.primary.withOpacity(0.2),
                            borderRadius: BorderRadius.only(
                              topLeft: const Radius.circular(14),
                              topRight: const Radius.circular(14),
                              bottomLeft: Radius.circular(gelen ? 2 : 14),
                              bottomRight: Radius.circular(gelen ? 14 : 2),
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: gelen
                                ? CrossAxisAlignment.start
                                : CrossAxisAlignment.end,
                            children: [
                              Text(
                                ad ?? '',
                                style: const TextStyle(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w600,
                                  color: AppColors.gold,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(m['mesaj'] ?? '',
                                  style: const TextStyle(fontSize: 14)),
                              const SizedBox(height: 4),
                              Text(
                                (m['tarih'] ?? '').toString().substring(0, 16),
                                style: const TextStyle(
                                  fontSize: 10,
                                  color: AppColors.textSecondaryDark,
                                ),
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
          ),

          // Mesaj yazma kutusu
          SafeArea(
            top: false,
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Theme.of(context).cardColor,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 4,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _mesajCtrl,
                      decoration: const InputDecoration(
                        hintText: 'Mesajını yaz...',
                        border: InputBorder.none,
                      ),
                      maxLines: null,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send, color: AppColors.primary),
                    onPressed: _gonder,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
