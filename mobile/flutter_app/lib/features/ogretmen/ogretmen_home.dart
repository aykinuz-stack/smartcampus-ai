import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


class OgretmenHomePage extends ConsumerStatefulWidget {
  const OgretmenHomePage({super.key});

  @override
  ConsumerState<OgretmenHomePage> createState() => _OgretmenHomePageState();
}

class _OgretmenHomePageState extends ConsumerState<OgretmenHomePage> {
  Future<List<Map<String, dynamic>>>? _siniflarFuture;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _siniflarFuture = ref.read(ogretmenApiProvider).siniflarim());
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
        title: Text('Merhaba, ${user.adSoyad.split(' ').first}'),
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
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [AppColors.success, Color(0xFF10B981)],
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(children: [
                      Icon(Icons.person_pin, color: Colors.white, size: 26),
                      SizedBox(width: 10),
                      Text('Öğretmen Paneli',
                          style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                    ]),
                    const SizedBox(height: 12),
                    Text(user.adSoyad,
                        style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              const Text('Sınıflarım',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              FutureBuilder<List<Map<String, dynamic>>>(
                future: _siniflarFuture,
                builder: (ctx, snap) {
                  if (snap.connectionState == ConnectionState.waiting) {
                    return const Padding(
                      padding: EdgeInsets.all(32),
                      child: Center(child: CircularProgressIndicator()),
                    );
                  }
                  final siniflar = snap.data ?? [];
                  if (siniflar.isEmpty) {
                    return const Padding(
                      padding: EdgeInsets.all(16),
                      child: Text('Atanmış sınıf yok'),
                    );
                  }
                  return Wrap(
                    spacing: 8, runSpacing: 8,
                    children: siniflar.map((s) => _SinifChip(data: s)).toList(),
                  );
                },
              ),

              const SizedBox(height: 24),
              const Text('Hızlı İşlemler',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: 1.2,
                children: [
                  _QuickCard(
                    icon: Icons.how_to_reg,
                    title: 'Yoklama',
                    subtitle: 'Manuel liste',
                    color: AppColors.success,
                    onTap: () => context.push('/ogretmen/yoklama'),
                  ),
                  _QuickCard(
                    icon: Icons.qr_code_scanner,
                    title: 'QR Yoklama',
                    subtitle: 'Kamera ile hızlı',
                    color: AppColors.primary,
                    onTap: () => context.push('/ogretmen/qr-yoklama'),
                  ),
                  _QuickCard(
                    icon: Icons.analytics,
                    title: 'Sınav Sonuçları',
                    subtitle: 'Sınıf/ders analiz',
                    color: AppColors.gold,
                    onTap: () => context.push('/ogretmen/sinav-sonuclari'),
                  ),
                  _QuickCard(
                    icon: Icons.grade,
                    title: 'Not Girişi',
                    subtitle: 'Toplu not gir',
                    color: AppColors.primary,
                    onTap: () => context.push('/ogretmen/not'),
                  ),
                  _QuickCard(
                    icon: Icons.menu_book,
                    title: 'Ders Defteri',
                    subtitle: 'Konu + kazanım',
                    color: AppColors.info,
                    onTap: () => context.push('/ogretmen/ders-defteri'),
                  ),
                  _QuickCard(
                    icon: Icons.assignment_add,
                    title: 'Ödev Ver',
                    subtitle: 'Sınıfa ödev ata',
                    color: AppColors.gold,
                    onTap: () => context.push('/ogretmen/odev-ata'),
                  ),
                  _QuickCard(
                    icon: Icons.chat,
                    title: 'Mesajlar',
                    subtitle: 'Veli iletişim',
                    color: AppColors.warning,
                    onTap: () => context.push('/messages'),
                  ),
                  _QuickCard(
                    icon: Icons.local_library,
                    title: 'Dijital Kütüphane',
                    subtitle: 'YouTube + Lab + Müze',
                    color: Color(0xFF5D4037),
                    onTap: () => context.push('/dijital-kutuphane'),
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
                    icon: Icons.smart_toy,
                    title: 'Ders Planı AI',
                    subtitle: 'Smarti ile planla',
                    color: AppColors.primary,
                    onTap: () => context.push('/smarti'),
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


class _SinifChip extends StatelessWidget {
  final Map<String, dynamic> data;
  const _SinifChip({required this.data});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        color: AppColors.success.withOpacity(0.1),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: AppColors.success.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.class_, color: AppColors.success, size: 18),
          const SizedBox(width: 6),
          Text('${data['sinif']}/${data['sube']}',
              style: const TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(width: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: AppColors.success,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text('${data['ogrenci_sayisi']}',
                style: const TextStyle(color: Colors.white, fontSize: 11,
                    fontWeight: FontWeight.bold)),
          ),
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
    required this.icon, required this.title,
    required this.subtitle, required this.color, required this.onTap,
  });

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
