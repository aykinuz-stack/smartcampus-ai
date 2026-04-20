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
                  icon: Icons.assignment_late, title: 'Günlük İşler',
                  subtitle: 'Bugün devamsızlar', color: Color(0xFFDC2626),
                  onTap: () => context.push('/gunluk-isler'),
                ),
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
                  icon: Icons.send, title: 'Yönlendirme',
                  subtitle: 'RAM / Kurum sevk', color: Color(0xFF0EA5E9),
                  onTap: () => context.push('/rehber/yonlendirme'),
                ),
                _QCard(
                  icon: Icons.emergency, title: 'Kriz Müdahale',
                  subtitle: 'Acil müdahale', color: Color(0xFFDC2626),
                  onTap: () => context.push('/rehber/kriz'),
                ),
                _QCard(
                  icon: Icons.assessment, title: 'Risk Değerlendirme',
                  subtitle: 'Öğrenci risk skoru', color: Color(0xFFF97316),
                  onTap: () => context.push('/rehber/risk'),
                ),
                _QCard(
                  icon: Icons.folder_shared, title: 'Gelişim Dosyası',
                  subtitle: 'Öğrenci dosyası', color: Color(0xFF8B5CF6),
                  onTap: () => context.push('/rehber/gelisim-dosyasi'),
                ),
                _QCard(
                  icon: Icons.work, title: 'Kariyer Rehberliği',
                  subtitle: 'Meslek yönlendirme', color: Color(0xFF14B8A6),
                  onTap: () => context.push('/rehber/kariyer'),
                ),
                _QCard(
                  icon: Icons.favorite, title: 'Sosyo-Duygusal',
                  subtitle: 'Duygu takibi', color: Color(0xFFEC4899),
                  onTap: () => context.push('/rehber/sosyo-duygusal'),
                ),
                _QCard(
                  icon: Icons.accessibility_new, title: 'BEP',
                  subtitle: 'Özel eğitim planı', color: Color(0xFF6366F1),
                  onTap: () => context.push('/rehber/bep'),
                ),
                _QCard(
                  icon: Icons.chat, title: 'Mesajlar',
                  subtitle: 'İletişim', color: AppColors.success,
                  onTap: () => context.push('/messages'),
                ),
                _QCard(
                  icon: Icons.warning_amber, title: 'Erken Uyarı',
                  subtitle: 'Bütüncül Risk', color: AppColors.danger,
                  onTap: () => context.push('/yonetici/erken-uyari'),
                ),
                _QCard(
                  icon: Icons.calendar_month, title: 'Takvim',
                  subtitle: 'Etkinlik + sınav', color: AppColors.gold,
                  onTap: () => context.push('/takvim'),
                ),
                _QCard(
                  icon: Icons.menu_book, title: 'Ders Programı',
                  subtitle: 'Sınıf/gün bazlı', color: AppColors.info,
                  onTap: () => context.push('/yonetici/ders-programi'),
                ),
                _QCard(
                  icon: Icons.access_time, title: 'Zaman Çizelgesi',
                  subtitle: 'Ders/teneffüs', color: AppColors.warning,
                  onTap: () => context.push('/yonetici/zaman-cizelgesi'),
                ),
                _QCard(
                  icon: Icons.campaign, title: 'Duyuru & Yemek',
                  subtitle: 'Okul duyuruları', color: AppColors.success,
                  onTap: () => context.push('/duyuru-yemek'),
                ),
                _QCard(
                  icon: Icons.train, title: 'AI Treni',
                  subtitle: '12 vagon · quiz', color: Color(0xFF8B5CF6),
                  onTap: () => context.push('/ai-treni'),
                ),
                _QCard(
                  icon: Icons.local_library, title: 'Dijital Kütüphane',
                  subtitle: 'YouTube + Lab + Müze', color: Color(0xFF5D4037),
                  onTap: () => context.push('/dijital-kutuphane'),
                ),
                _QCard(
                  icon: Icons.emoji_events, title: 'Bilgi Yarışmaları',
                  subtitle: '4 tür · 3700+ soru', color: Color(0xFF7C3AED),
                  onTap: () => context.push('/bilgi-yarismasi-koleksiyon'),
                ),
                _QCard(
                  icon: Icons.calculate, title: 'Matematik Köyü',
                  subtitle: '6 oyun · formüller', color: Color(0xFF6366F1),
                  onTap: () => context.push('/matematik-koyu'),
                ),
                _QCard(
                  icon: Icons.extension, title: 'Zeka Oyunları',
                  subtitle: '7 oyun · Sudoku +', color: Color(0xFFEC4899),
                  onTap: () => context.push('/zeka-oyunlari'),
                ),
                _QCard(
                  icon: Icons.lightbulb, title: 'Günün Bilgisi',
                  subtitle: '230 gün · 8 kategori', color: Color(0xFFEAB308),
                  onTap: () => context.push('/gunun-bilgisi'),
                ),
                _QCard(
                  icon: Icons.translate, title: 'Dil Gelişimi',
                  subtitle: '5 dil · 104+ ders', color: AppColors.info,
                  onTap: () => context.push('/dil-gelisimi'),
                ),
                _QCard(
                  icon: Icons.workspace_premium, title: 'KDG Premium',
                  subtitle: 'CEFR İng + Alm', color: Color(0xFF7C3AED),
                  onTap: () => context.push('/kdg-premium'),
                ),
                _QCard(
                  icon: Icons.smart_toy, title: 'Smarti AI',
                  subtitle: 'Asistan', color: AppColors.primary,
                  onTap: () => context.push('/smarti'),
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
