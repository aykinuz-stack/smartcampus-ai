import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


class RehberHomePage extends ConsumerWidget {
  const RehberHomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(currentUserProvider);
    return userAsync.when(
      data: (user) => _build(context, ref, user),
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(body: Center(child: Text('Hata: $e'))),
    );
  }

  Widget _build(BuildContext context, WidgetRef ref, AuthUser? user) {
    if (user == null) {
      WidgetsBinding.instance.addPostFrameCallback((_) => context.go('/login'));
      return const SizedBox();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Rehber, ${user.adSoyad.split(' ').first}'),
        actions: [
          IconButton(icon: const Icon(Icons.notifications_outlined), onPressed: () {}),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await ref.read(authServiceProvider).logout();
              if (context.mounted) context.go('/login');
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppColors.danger, Color(0xFFF43F5E)],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(children: [
                    Icon(Icons.psychology, color: Colors.white, size: 26),
                    SizedBox(width: 10),
                    Text('Rehberlik Paneli',
                        style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                  ]),
                  const SizedBox(height: 12),
                  Text(user.adSoyad,
                      style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const Text('İşlemler',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              crossAxisSpacing: 12, mainAxisSpacing: 12,
              childAspectRatio: 1.2,
              children: [
                _QCard(
                  icon: Icons.folder_open, title: 'Vakalar',
                  subtitle: 'Açık / Kapalı', color: AppColors.primary,
                  onTap: () => context.push('/rehber/vakalar'),
                ),
                _QCard(
                  icon: Icons.record_voice_over, title: 'Görüşme',
                  subtitle: 'Kayıt + not', color: AppColors.info,
                  onTap: () => context.push('/rehber/gorusme'),
                ),
                _QCard(
                  icon: Icons.family_restroom, title: 'Aile Formu',
                  subtitle: 'Bilgi formu', color: AppColors.gold,
                  onTap: () => context.push('/rehber/aile-form'),
                ),
                _QCard(
                  icon: Icons.mood, title: 'Mood Paneli',
                  subtitle: 'Riskli öğrenciler', color: AppColors.warning,
                  onTap: () => context.push('/rehber/mood'),
                ),
                _QCard(
                  icon: Icons.shield, title: 'İhbarlar',
                  subtitle: 'Anonim bildirimler', color: AppColors.danger,
                  onTap: () => context.push('/rehber/ihbar'),
                ),
                _QCard(
                  icon: Icons.chat, title: 'Mesajlar',
                  subtitle: 'İletişim', color: AppColors.success,
                  onTap: () => context.push('/messages'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}


class _QCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  const _QCard({required this.icon, required this.title,
                required this.subtitle, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const Spacer(),
            Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            Text(subtitle, style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
          ],
        ),
      ),
    );
  }
}
