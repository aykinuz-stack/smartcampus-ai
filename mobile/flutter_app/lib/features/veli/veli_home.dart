import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/veli_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


class VeliHomePage extends ConsumerStatefulWidget {
  const VeliHomePage({super.key});

  @override
  ConsumerState<VeliHomePage> createState() => _VeliHomePageState();
}

class _VeliHomePageState extends ConsumerState<VeliHomePage> {
  Future<List<Map<String, dynamic>>>? _cocuklarimFuture;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _cocuklarimFuture = ref.read(veliApiProvider).cocuklarim());
  }

  @override
  Widget build(BuildContext context) {
    final userAsync = ref.watch(currentUserProvider);
    return userAsync.when(
      data: (user) => _build(context, user),
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(body: Center(child: Text('Hata: $e'))),
    );
  }

  Widget _build(BuildContext context, AuthUser? user) {
    if (user == null) {
      WidgetsBinding.instance.addPostFrameCallback((_) => context.go('/login'));
      return const SizedBox();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Hoşgeldin, ${user.adSoyad.split(' ').first}'),
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
      body: RefreshIndicator(
        onRefresh: () async => _load(),
        child: SingleChildScrollView(
          physics: const AlwaysScrollableScrollPhysics(),
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Hero
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.primaryDark, AppColors.primary],
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.family_restroom, color: Colors.white, size: 26),
                        SizedBox(width: 10),
                        Text('Veli Paneli',
                            style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(user.adSoyad,
                        style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Cocuklarim
              const Text('Çocuklarım',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              FutureBuilder<List<Map<String, dynamic>>>(
                future: _cocuklarimFuture,
                builder: (ctx, snap) {
                  if (snap.connectionState == ConnectionState.waiting) {
                    return const Padding(
                      padding: EdgeInsets.all(32),
                      child: Center(child: CircularProgressIndicator()),
                    );
                  }
                  final cocuklar = snap.data ?? [];
                  if (cocuklar.isEmpty) {
                    return const Padding(
                      padding: EdgeInsets.all(24),
                      child: Center(
                        child: Text('Kayıtlı çocuk yok. Okul yönetimiyle iletişime geç.'),
                      ),
                    );
                  }
                  return Column(
                    children: cocuklar.map((c) => _CocukKart(cocuk: c)).toList(),
                  );
                },
              ),

              const SizedBox(height: 20),
              const Text('Hızlı Erişim',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),

              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.4,
                children: [
                  _QuickCard(
                    icon: Icons.auto_awesome,
                    title: 'Günlük Kapsül',
                    subtitle: '18:00 AI özet',
                    color: AppColors.primary,
                    onTap: () => context.push('/veli/kapsul'),
                  ),
                  _QuickCard(
                    icon: Icons.calendar_month,
                    title: 'Randevular',
                    subtitle: 'Öğretmenle randevu',
                    color: AppColors.info,
                    onTap: () => context.push('/veli/randevu'),
                  ),
                  _QuickCard(
                    icon: Icons.description,
                    title: 'Belge Talebi',
                    subtitle: 'Öğrenci belgesi vb.',
                    color: AppColors.warning,
                    onTap: () => context.push('/veli/belge'),
                  ),
                  _QuickCard(
                    icon: Icons.quiz,
                    title: 'Sınav Sonuçları',
                    subtitle: 'Yazılı / deneme',
                    color: Color(0xFF8B5CF6),
                    onTap: () {
                      final children = user?.childrenIds ?? [];
                      if (children.isNotEmpty) {
                        context.push('/veli/cocuk-detay',
                          extra: {'studentId': children.first, 'studentName': 'Çocuğum'});
                      }
                    },
                  ),
                  _QuickCard(
                    icon: Icons.menu_book,
                    title: 'Ders Programı',
                    subtitle: 'Sınıf/gün bazlı',
                    color: AppColors.info,
                    onTap: () => context.push('/yonetici/ders-programi'),
                  ),
                  _QuickCard(
                    icon: Icons.access_time,
                    title: 'Zaman Çizelgesi',
                    subtitle: 'Ders/teneffüs',
                    color: AppColors.warning,
                    onTap: () => context.push('/yonetici/zaman-cizelgesi'),
                  ),
                  _QuickCard(
                    icon: Icons.wb_sunny,
                    title: 'Günlük Rapor',
                    subtitle: 'Bugün okulda ne oldu',
                    color: AppColors.gold,
                    onTap: () => context.push('/veli/kapsul'),
                  ),
                  _QuickCard(
                    icon: Icons.assignment,
                    title: 'Ödevler',
                    subtitle: 'Bekleyen + teslim',
                    color: AppColors.warning,
                    onTap: () {
                      final children = user?.childrenIds ?? [];
                      if (children.isNotEmpty) {
                        context.push('/veli/cocuk-detay',
                          extra: {'studentId': children.first, 'studentName': 'Çocuğum'});
                      }
                    },
                  ),
                  _QuickCard(
                    icon: Icons.campaign,
                    title: 'Duyuru & Yemek',
                    subtitle: 'Okul duyuruları',
                    color: AppColors.success,
                    onTap: () => context.push('/duyuru-yemek'),
                  ),
                  _QuickCard(
                    icon: Icons.chat,
                    title: 'Mesajlar',
                    subtitle: 'Öğretmenle iletişim',
                    color: AppColors.primary,
                    onTap: () => context.push('/messages'),
                  ),
                  _QuickCard(
                    icon: Icons.smart_toy,
                    title: 'Smarti AI',
                    subtitle: 'Asistan',
                    color: Color(0xFF6366F1),
                    onTap: () => context.push('/smarti'),
                  ),
                  _QuickCard(
                    icon: Icons.local_library,
                    title: 'Dijital Kütüphane',
                    subtitle: 'YouTube + Lab + Müze',
                    color: Color(0xFF5D4037),
                    onTap: () => context.push('/dijital-kutuphane'),
                  ),
                  _QuickCard(
                    icon: Icons.emoji_events,
                    title: 'Bilgi Yarışmaları',
                    subtitle: '4 tür · 3700+ soru',
                    color: Color(0xFF7C3AED),
                    onTap: () => context.push('/bilgi-yarismasi-koleksiyon'),
                  ),
                  _QuickCard(
                    icon: Icons.calculate,
                    title: 'Matematik Köyü',
                    subtitle: '6 oyun · formüller',
                    color: Color(0xFF6366F1),
                    onTap: () => context.push('/matematik-koyu'),
                  ),
                  _QuickCard(
                    icon: Icons.extension,
                    title: 'Zeka Oyunları',
                    subtitle: '7 oyun · Sudoku +',
                    color: Color(0xFFEC4899),
                    onTap: () => context.push('/zeka-oyunlari'),
                  ),
                  _QuickCard(
                    icon: Icons.lightbulb,
                    title: 'Günün Bilgisi',
                    subtitle: '230 gün · 8 kategori',
                    color: Color(0xFFEAB308),
                    onTap: () => context.push('/gunun-bilgisi'),
                  ),
                  _QuickCard(
                    icon: Icons.translate,
                    title: 'Dil Gelişimi',
                    subtitle: '5 dil · 104+ ders',
                    color: AppColors.info,
                    onTap: () => context.push('/dil-gelisimi'),
                  ),
                  _QuickCard(
                    icon: Icons.workspace_premium,
                    title: 'KDG Premium',
                    subtitle: 'CEFR İng + Alm',
                    color: Color(0xFF7C3AED),
                    onTap: () => context.push('/kdg-premium'),
                  ),
                  _QuickCard(
                    icon: Icons.train,
                    title: 'AI Treni',
                    subtitle: '12 vagon · quiz',
                    color: Color(0xFF8B5CF6),
                    onTap: () => context.push('/ai-treni'),
                  ),
                  _QuickCard(
                    icon: Icons.shield,
                    title: 'İhbar Hattı',
                    subtitle: 'Anonim bildirim',
                    color: AppColors.danger,
                    onTap: () => context.push('/ihbar'),
                  ),
                  _QuickCard(
                    icon: Icons.description,
                    title: 'Belge Talebi',
                    subtitle: 'Öğrenci belgesi',
                    color: AppColors.warning,
                    onTap: () => context.push('/veli/belge'),
                  ),
                  _QuickCard(
                    icon: Icons.feedback,
                    title: 'Geri Bildirim',
                    subtitle: 'Memnuniyet / öneri',
                    color: AppColors.gold,
                    onTap: () => context.push('/veli/geri-bildirim'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}


class _CocukKart extends ConsumerWidget {
  final Map<String, dynamic> cocuk;
  const _CocukKart({required this.cocuk});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notOrt = (cocuk['not_ortalamasi'] as num?)?.toDouble() ?? 0.0;
    final devam = (cocuk['devamsizlik_sayisi'] as num?)?.toInt() ?? 0;
    final bekleyen = (cocuk['bekleyen_odev'] as num?)?.toInt() ?? 0;
    final geciken = (cocuk['geciken_odev'] as num?)?.toInt() ?? 0;
    final moodOrt = (cocuk['bu_ay_mood_ortalamasi'] as num?)?.toDouble() ?? 0.0;
    final riskVar = cocuk['risk_var'] as bool? ?? false;
    final riskSeviye = cocuk['risk_seviyesi'] as String? ?? '';

    return InkWell(
      onTap: () {
        context.push('/veli/cocuk-detay',
          extra: {'studentId': cocuk['student_id'], 'studentName': cocuk['ad_soyad']});
      },
      child: Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  radius: 24,
                  backgroundColor: AppColors.primary.withOpacity(0.2),
                  child: Text(
                    (cocuk['ad_soyad'] as String? ?? '?')[0],
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(cocuk['ad_soyad'] ?? '',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      Text('${cocuk['sinif']}/${cocuk['sube']} · No: ${cocuk['numara']}',
                          style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
                    ],
                  ),
                ),
                if (riskVar)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.warning.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      '⚠️ $riskSeviye',
                      style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold,
                          color: AppColors.warning),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 14),
            Row(
              children: [
                _StatItem(
                  label: 'Ortalama',
                  value: notOrt.toStringAsFixed(1),
                  color: notOrt >= 70 ? AppColors.success : AppColors.warning,
                ),
                _StatItem(
                  label: 'Devamsız',
                  value: '$devam',
                  color: devam > 5 ? AppColors.danger : AppColors.info,
                ),
                _StatItem(
                  label: 'Ödev',
                  value: '${bekleyen + geciken}',
                  color: geciken > 0 ? AppColors.danger : AppColors.success,
                ),
                _StatItem(
                  label: 'Mood',
                  value: moodOrt > 0 ? moodOrt.toStringAsFixed(1) : '-',
                  color: moodOrt >= 3.5 ? AppColors.success : (moodOrt > 0 ? AppColors.warning : Colors.grey),
                ),
              ],
            ),
          ],
        ),
      ),
    ),  // InkWell kapanisi
    );
  }
}


class _StatItem extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _StatItem({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: [
          Text(value,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
          Text(label, style: const TextStyle(fontSize: 11)),
        ],
      ),
    );
  }
}


class _QuickCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  const _QuickCard({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(12),
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
              child: Icon(icon, color: color, size: 22),
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
