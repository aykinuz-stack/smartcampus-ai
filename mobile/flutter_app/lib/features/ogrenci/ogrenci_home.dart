import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';

class OgrenciHomePage extends ConsumerWidget {
  const OgrenciHomePage({super.key});

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

    final features = [
      _HomeFeature('😊 Mood Check-in', 'Bugünkü ruh halin', Icons.mood, AppColors.mood5, '/mood'),
      _HomeFeature('📝 Notlarım', 'Sınav/yazılı notları', Icons.grade, AppColors.primary, '/notes'),
      _HomeFeature('📚 Ödevlerim', 'Bekleyen + teslim', Icons.assignment, AppColors.gold, '/homework'),
      _HomeFeature('📅 Devamsızlık', 'Bu dönem', Icons.calendar_today, AppColors.warning, '/attendance'),
      _HomeFeature('💬 Mesajlar', 'Öğretmen / veli', Icons.chat, AppColors.info, '/messages'),
      _HomeFeature('🚨 İhbar Hattı', 'Anonim bildirim', Icons.shield, AppColors.danger, '/ihbar'),
      _HomeFeature('🤖 Smarti AI', 'Asistan', Icons.smart_toy, AppColors.primary, '/smarti'),
      _HomeFeature('📊 Profilim', 'Tam Öğrenci 360', Icons.person, AppColors.success, '/profile'),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('Merhaba, ${user.adSoyad.split(' ').first}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
          ),
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
            // Hero card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [AppColors.primary, AppColors.primaryDark],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.school, color: Colors.white, size: 28),
                      SizedBox(width: 10),
                      Text('SmartCampus AI', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    user.adSoyad,
                    style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    user.role.toUpperCase(),
                    style: const TextStyle(color: AppColors.gold, fontSize: 13, letterSpacing: 1.2),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            const Text('Hızlı Erişim',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
            const SizedBox(height: 12),

            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.3,
              ),
              itemCount: features.length,
              itemBuilder: (ctx, i) {
                final f = features[i];
                return _FeatureCard(feature: f, onTap: () => context.push(f.route));
              },
            ),
          ],
        ),
      ),
    );
  }
}


class _HomeFeature {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final String route;
  const _HomeFeature(this.title, this.subtitle, this.icon, this.color, this.route);
}


class _FeatureCard extends StatelessWidget {
  final _HomeFeature feature;
  final VoidCallback onTap;
  const _FeatureCard({required this.feature, required this.onTap});

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
          border: Border.all(color: feature.color.withOpacity(0.3), width: 1),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: feature.color.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(feature.icon, color: feature.color, size: 24),
            ),
            const Spacer(),
            Text(feature.title,
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            Text(feature.subtitle,
                style: TextStyle(fontSize: 11, color: Theme.of(context).textTheme.bodySmall?.color)),
          ],
        ),
      ),
    );
  }
}
