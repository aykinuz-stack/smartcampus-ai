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
          IconButton(icon: const Icon(Icons.notifications_outlined),
              onPressed: () => context.push('/bildirimler')),
          IconButton(icon: const Icon(Icons.settings_outlined),
              onPressed: () => context.push('/ayarlar')),
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

              FutureBuilder<List<Map<String, dynamic>>>(
                future: _siniflarFuture,
                builder: (ctx, snap) {
                  final siniflar = snap.data ?? [];
                  if (snap.connectionState == ConnectionState.waiting) {
                    return const SizedBox();
                  }
                  if (siniflar.isEmpty) return const SizedBox();
                  return ExpansionTile(
                    leading: const Icon(Icons.class_, color: AppColors.success, size: 22),
                    title: Text('Sınıflarım (${siniflar.length})',
                        style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                    initiallyExpanded: false,
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        child: Wrap(
                          spacing: 8, runSpacing: 8,
                          children: siniflar.map((s) => _SinifChip(data: s)).toList(),
                        ),
                      ),
                    ],
                  );
                },
              ),

              const SizedBox(height: 10),
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
                    icon: Icons.assignment_late,
                    title: 'Günlük İşler',
                    subtitle: 'Bugün devamsızlar',
                    color: Color(0xFFDC2626),
                    onTap: () => context.push('/gunluk-isler'),
                  ),
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
                    icon: Icons.smart_toy,
                    title: 'Ders Planı AI',
                    subtitle: 'Smarti ile planla',
                    color: AppColors.primary,
                    onTap: () => context.push('/smarti'),
                  ),
                  _QuickCard(
                    icon: Icons.class_,
                    title: 'Sınıf Listeleri',
                    subtitle: 'Öğrenci listeleri',
                    color: AppColors.info,
                    onTap: () => context.push('/yonetici/sinif-listeleri'),
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
                    icon: Icons.shield,
                    title: 'Nöbet',
                    subtitle: 'Bugün + haftalık',
                    color: AppColors.success,
                    onTap: () => context.push('/yonetici/nobet'),
                  ),
                  _QuickCard(
                    icon: Icons.local_hospital,
                    title: 'Revir',
                    subtitle: 'Ziyaret + şüpheli',
                    color: AppColors.danger,
                    onTap: () => context.push('/yonetici/revir'),
                  ),
                  _QuickCard(
                    icon: Icons.menu_book,
                    title: 'Kütüphane',
                    subtitle: 'Ödünç + geciken',
                    color: AppColors.info,
                    onTap: () => context.push('/yonetici/kutuphane'),
                  ),
                  _QuickCard(
                    icon: Icons.calendar_month,
                    title: 'Takvim',
                    subtitle: 'Etkinlik + sınav',
                    color: AppColors.gold,
                    onTap: () => context.push('/takvim'),
                  ),
                  _QuickCard(
                    icon: Icons.campaign,
                    title: 'Duyuru & Yemek',
                    subtitle: 'Okul duyuruları',
                    color: AppColors.success,
                    onTap: () => context.push('/duyuru-yemek'),
                  ),
                  _QuickCard(
                    icon: Icons.train,
                    title: 'AI Treni',
                    subtitle: '12 vagon · quiz',
                    color: Color(0xFF8B5CF6),
                    onTap: () => context.push('/ai-treni'),
                  ),
                  _QuickCard(
                    icon: Icons.warning_amber,
                    title: 'Erken Uyarı',
                    subtitle: 'Bütüncül Risk',
                    color: AppColors.danger,
                    onTap: () => context.push('/yonetici/erken-uyari'),
                  ),
                  _QuickCard(
                    icon: Icons.theater_comedy,
                    title: 'Sosyal Etkinlik',
                    subtitle: 'Kulüp + etkinlik',
                    color: AppColors.success,
                    onTap: () => context.push('/yonetici/sosyal-etkinlik'),
                  ),
                  _QuickCard(
                    icon: Icons.shield,
                    title: 'İhbar Hattı',
                    subtitle: 'Anonim bildirim',
                    color: AppColors.danger,
                    onTap: () => context.push('/ihbar'),
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
