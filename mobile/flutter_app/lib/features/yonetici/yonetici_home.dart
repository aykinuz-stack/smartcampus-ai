import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


class YoneticiHomePage extends ConsumerStatefulWidget {
  const YoneticiHomePage({super.key});

  @override
  ConsumerState<YoneticiHomePage> createState() => _YoneticiHomePageState();
}

class _YoneticiHomePageState extends ConsumerState<YoneticiHomePage> {
  Future<Map<String, dynamic>>? _dashboardFuture;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() =>
        _dashboardFuture = ref.read(yoneticiApiProvider).dashboard());
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
        title: Text('Yönetim · ${user.adSoyad.split(' ').first}'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
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
        child: FutureBuilder<Map<String, dynamic>>(
          future: _dashboardFuture,
          builder: (ctx, snap) {
            if (snap.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            final d = snap.data ?? {};
            return SingleChildScrollView(
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
                        colors: [AppColors.surfaceDarker, AppColors.primaryDark],
                      ),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(children: [
                          Icon(Icons.dashboard, color: AppColors.gold, size: 26),
                          SizedBox(width: 10),
                          Text('Yönetici Dashboard',
                              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                        ]),
                        const SizedBox(height: 12),
                        Text(user.adSoyad,
                            style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  const SizedBox(height: 20),

                  // KPI grid
                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 2,
                    crossAxisSpacing: 10,
                    mainAxisSpacing: 10,
                    childAspectRatio: 1.4,
                    children: [
                      _Kpi(label: 'Öğrenci', value: '${d['toplam_ogrenci'] ?? '-'}',
                          icon: Icons.school, color: AppColors.primary),
                      _Kpi(label: 'Öğretmen', value: '${d['toplam_ogretmen'] ?? '-'}',
                          icon: Icons.person, color: AppColors.success),
                      _Kpi(label: 'Bugün Devamsız', value: '${d['bugun_devamsiz'] ?? 0}',
                          icon: Icons.person_off, color: AppColors.danger),
                      _Kpi(label: 'Açık Vaka', value: '${d['acik_vaka'] ?? 0}',
                          icon: Icons.folder_open, color: AppColors.warning),
                      _Kpi(label: 'Kritik Risk', value: '${d['kritik_risk_ogrenci'] ?? 0}',
                          icon: Icons.warning, color: AppColors.danger),
                      _Kpi(label: 'Yeni İhbar', value: '${d['bekleyen_ihbar'] ?? 0}',
                          icon: Icons.shield, color: AppColors.warning),
                    ],
                  ),
                  const SizedBox(height: 18),

                  // Onay bekleyen bandı
                  if ((d['bekleyen_onay'] as num? ?? 0) > 0) ...[
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: AppColors.warning.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: AppColors.warning),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.approval, color: AppColors.warning),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              '${d['bekleyen_onay']} onay bekliyor',
                              style: const TextStyle(fontWeight: FontWeight.bold),
                            ),
                          ),
                          TextButton(
                            onPressed: () => context.push('/yonetici/onaylar'),
                            child: const Text('İncele'),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 14),
                  ],

                  const Text('İşlemler',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),

                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 2,
                    crossAxisSpacing: 12, mainAxisSpacing: 12,
                    childAspectRatio: 1.3,
                    children: [
                      _QCard(
                        icon: Icons.wb_sunny, title: 'Gün Raporu',
                        subtitle: 'Başı + sonu', color: AppColors.gold,
                        onTap: () => context.push('/yonetici/gun-raporu'),
                      ),
                      _QCard(
                        icon: Icons.today, title: 'Bugün Okulda',
                        subtitle: 'Ders + etkinlik', color: AppColors.info,
                        onTap: () => context.push('/yonetici/bugun-okulda'),
                      ),
                      _QCard(
                        icon: Icons.app_registration, title: 'Kayıt Özeti',
                        subtitle: 'Pipeline + bugün', color: AppColors.primary,
                        onTap: () => context.push('/yonetici/kayit-ozet'),
                      ),
                      _QCard(
                        icon: Icons.account_balance_wallet, title: 'Bütçe',
                        subtitle: 'Gelir/gider akışı', color: AppColors.success,
                        onTap: () => context.push('/yonetici/butce'),
                      ),
                      _QCard(
                        icon: Icons.calendar_month, title: 'Randevular',
                        subtitle: 'Bugün + yaklaşan', color: AppColors.gold,
                        onTap: () => context.push('/yonetici/randevular'),
                      ),
                      _QCard(
                        icon: Icons.people, title: 'Çalışanlar',
                        subtitle: 'Aktif personel', color: AppColors.primary,
                        onTap: () => context.push('/yonetici/calisanlar'),
                      ),
                      _QCard(
                        icon: Icons.class_, title: 'Sınıf Listeleri',
                        subtitle: 'Öğrenci listeleri', color: AppColors.info,
                        onTap: () => context.push('/yonetici/sinif-listeleri'),
                      ),
                      _QCard(
                        icon: Icons.warning_amber, title: 'Erken Uyarı',
                        subtitle: 'Bütüncül Risk', color: AppColors.danger,
                        onTap: () => context.push('/yonetici/erken-uyari'),
                      ),
                      _QCard(
                        icon: Icons.inventory, title: 'Tüketim/Demirbaş',
                        subtitle: 'Stok + günlük', color: AppColors.gold,
                        onTap: () => context.push('/yonetici/tuketim-demirbas'),
                      ),
                      _QCard(
                        icon: Icons.build, title: 'Destek Hizmetleri',
                        subtitle: 'Ticket + SLA', color: AppColors.warning,
                        onTap: () => context.push('/yonetici/destek-hizmetleri'),
                      ),
                      _QCard(
                        icon: Icons.checklist, title: 'Onaylar',
                        subtitle: 'Randevu + belge', color: AppColors.warning,
                        onTap: () => context.push('/yonetici/onaylar'),
                      ),
                      _QCard(
                        icon: Icons.menu_book, title: 'Ders Programı',
                        subtitle: 'Sınıf/gün bazlı', color: AppColors.info,
                        onTap: () => context.push('/yonetici/ders-programi'),
                      ),
                      _QCard(
                        icon: Icons.shield, title: 'Nöbet',
                        subtitle: 'Bugün + haftalık', color: AppColors.success,
                        onTap: () => context.push('/yonetici/nobet'),
                      ),
                      _QCard(
                        icon: Icons.access_time, title: 'Zaman Çizelgesi',
                        subtitle: 'Ders/teneffüs', color: AppColors.warning,
                        onTap: () => context.push('/yonetici/zaman-cizelgesi'),
                      ),
                      _QCard(
                        icon: Icons.local_hospital, title: 'Revir',
                        subtitle: 'Ziyaret + şüpheli', color: AppColors.danger,
                        onTap: () => context.push('/yonetici/revir'),
                      ),
                      _QCard(
                        icon: Icons.menu_book, title: 'Kütüphane',
                        subtitle: 'Ödünç + geciken', color: AppColors.info,
                        onTap: () => context.push('/yonetici/kutuphane'),
                      ),
                      _QCard(
                        icon: Icons.theater_comedy, title: 'Sosyal Etkinlik',
                        subtitle: 'Kulüp + etkinlik', color: AppColors.success,
                        onTap: () => context.push('/yonetici/sosyal-etkinlik'),
                      ),
                      _QCard(
                        icon: Icons.chat, title: 'Mesajlar',
                        subtitle: 'Gelen/Giden/Yeni', color: AppColors.primary,
                        onTap: () => context.push('/messages'),
                      ),
                    ],
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}


class _Kpi extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  const _Kpi({required this.label, required this.value,
              required this.icon, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const Spacer(),
              Text(value,
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
            ],
          ),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
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
