import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/api_client.dart';
import '../../core/api/ogrenci_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/premium_widgets.dart';

// =============================================================================
// OGRENCI HOME PAGE — Ultra Premium World-Class Dashboard
// =============================================================================

class OgrenciHomePage extends ConsumerStatefulWidget {
  const OgrenciHomePage({super.key});

  @override
  ConsumerState<OgrenciHomePage> createState() => _OgrenciHomePageState();
}

class _OgrenciHomePageState extends ConsumerState<OgrenciHomePage>
    with TickerProviderStateMixin {
  // API futures
  Future<Map<String, dynamic>>? _dashFuture;
  Future<Map<String, dynamic>>? _moodFuture;
  Future<Map<String, dynamic>>? _bildirimFuture;

  // Auto-scroll carousel for Son Notlar
  late final PageController _pageCtrl;
  Timer? _autoTimer;
  int _currentPage = 0;

  // Animated page indicator
  late final AnimationController _dotPulse;

  @override
  void initState() {
    super.initState();
    _pageCtrl = PageController(viewportFraction: 0.92);
    _dotPulse = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    )..repeat(reverse: true);
    _loadAll();
  }

  @override
  void dispose() {
    _autoTimer?.cancel();
    _pageCtrl.dispose();
    _dotPulse.dispose();
    super.dispose();
  }

  void _loadAll() {
    final api = ref.read(apiClientProvider);
    setState(() {
      _dashFuture = api
          .get('/ogrenci/dashboard')
          .then((r) => Map<String, dynamic>.from(r.data));
      _moodFuture = api
          .get('/mood/summary')
          .then((r) => Map<String, dynamic>.from(r.data));
      _bildirimFuture = api
          .get('/bildirim/liste', params: {'limit': 5})
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  void _startAutoScroll(int pageCount) {
    _autoTimer?.cancel();
    if (pageCount <= 1) return;
    _autoTimer = Timer.periodic(const Duration(seconds: 4), (_) {
      _currentPage = (_currentPage + 1) % pageCount;
      if (_pageCtrl.hasClients) {
        _pageCtrl.animateToPage(
          _currentPage,
          duration: const Duration(milliseconds: 500),
          curve: Curves.easeInOutCubic,
        );
      }
    });
  }

  // ---------------------------------------------------------------------------
  // BUILD
  // ---------------------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    final userAsync = ref.watch(currentUserProvider);

    return userAsync.when(
      data: (user) => _buildPage(context, user),
      loading: () => Scaffold(
        backgroundColor: Theme.of(context).scaffoldBackgroundColor,
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              SizedBox(
                width: 48,
                height: 48,
                child: CircularProgressIndicator(
                  strokeWidth: 3,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Yukleniyor...',
                style: TextStyle(
                  color: AppColors.textSecondaryLight,
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),
      ),
      error: (e, _) => Scaffold(
        body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.error_outline_rounded,
                  size: 48, color: AppColors.danger),
              const SizedBox(height: 12),
              Text('Bir hata olustu',
                  style: TextStyle(
                      fontSize: 16, fontWeight: FontWeight.w600)),
              const SizedBox(height: 4),
              Text('$e',
                  style: TextStyle(
                      fontSize: 12, color: AppColors.textSecondaryLight)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPage(BuildContext context, AuthUser? user) {
    if (user == null) {
      WidgetsBinding.instance
          .addPostFrameCallback((_) => context.go('/login'));
      return const SizedBox.shrink();
    }

    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      // -- APP BAR --
      appBar: AppBar(
        title: Text(
          'Merhaba, ${user.adSoyad.split(' ').first}',
          style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 20),
        ),
        actions: [
          // Notification bell with badge
          FutureBuilder<Map<String, dynamic>>(
            future: _bildirimFuture,
            builder: (_, snap) {
              final okunmamis = (snap.data?['okunmamis'] as int?) ?? 0;
              return Padding(
                padding: const EdgeInsets.only(right: 4),
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    IconButton(
                      icon: Icon(
                        okunmamis > 0
                            ? Icons.notifications_active_rounded
                            : Icons.notifications_none_rounded,
                        size: 24,
                      ),
                      onPressed: () => context.push('/bildirimler'),
                      tooltip: 'Bildirimler',
                    ),
                    if (okunmamis > 0)
                      Positioned(
                        right: 8,
                        top: 8,
                        child: Container(
                          width: 18,
                          height: 18,
                          decoration: BoxDecoration(
                            color: AppColors.danger,
                            shape: BoxShape.circle,
                            border: Border.all(
                              color:
                                  isDark ? AppColors.surfaceDark : Colors.white,
                              width: 2,
                            ),
                            boxShadow: AppShadows.glow(AppColors.danger),
                          ),
                          child: Center(
                            child: Text(
                              okunmamis > 9 ? '9+' : '$okunmamis',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 9,
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                          ),
                        ),
                      ),
                  ],
                ),
              );
            },
          ),
          // Settings
          IconButton(
            icon: const Icon(Icons.settings_outlined, size: 22),
            onPressed: () => context.push('/ayarlar'),
            tooltip: 'Ayarlar',
          ),
          // Logout
          IconButton(
            icon: const Icon(Icons.logout_rounded, size: 22),
            onPressed: () async {
              await ref.read(authServiceProvider).logout();
              if (context.mounted) context.go('/login');
            },
            tooltip: 'Cikis Yap',
          ),
          const SizedBox(width: 4),
        ],
      ),

      // -- BODY --
      body: RefreshIndicator(
        color: AppColors.primary,
        strokeWidth: 2.5,
        onRefresh: () async => _loadAll(),
        child: FutureBuilder<Map<String, dynamic>>(
          future: _dashFuture,
          builder: (ctx, snap) {
            if (snap.connectionState == ConnectionState.waiting) {
              return Center(
                child: CircularProgressIndicator(
                  strokeWidth: 3,
                  color: AppColors.primary,
                ),
              );
            }
            final dash = snap.data ?? {};
            return SingleChildScrollView(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.lg,
                vertical: AppSpacing.md,
              ),
              physics: const AlwaysScrollableScrollPhysics(
                parent: BouncingScrollPhysics(),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 1. HERO BANNER
                  _buildHeroBanner(user),
                  const SizedBox(height: AppSpacing.xl),

                  // 2. KPI ROW
                  _buildKPIRow(dash),
                  const SizedBox(height: AppSpacing.xxl),

                  // 3. YAKLASAN SINAVLAR
                  _buildYaklasanSinavlar(dash),

                  // 4. ODEV GERI SAYIM
                  _buildOdevCountdown(dash),

                  // 5. SON NOTLAR CAROUSEL
                  _buildNotlarCarousel(dash),

                  // 6. BUGUN DERSLER
                  _buildBugunDersler(dash),

                  // 7. MOOD CHECK-IN BANNER
                  _buildMoodBanner(),
                  const SizedBox(height: AppSpacing.xxl),

                  // 8. HIZLI ERISIM
                  SectionHeader(
                    title: 'Hizli Erisim',
                    icon: Icons.grid_view_rounded,
                  ),
                  _buildFeatureGrid(),
                  const SizedBox(height: AppSpacing.xxxl),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  // ===========================================================================
  // 1. HERO BANNER
  // ===========================================================================

  Widget _buildHeroBanner(AuthUser user) {
    // Initials for avatar
    final parts = user.adSoyad.split(' ');
    final initials = parts.length >= 2
        ? '${parts[0][0]}${parts[1][0]}'.toUpperCase()
        : (user.adSoyad.isNotEmpty ? user.adSoyad[0].toUpperCase() : '?');

    return HeroBanner(
      title: user.adSoyad,
      subtitle: 'SmartCampus AI',
      badge: user.role.toUpperCase(),
      gradient: AppGradients.primary,
      trailing: Container(
        width: 56,
        height: 56,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white.withOpacity(0.15),
          border: Border.all(color: AppColors.gold, width: 2.5),
          boxShadow: [
            BoxShadow(
              color: AppColors.gold.withOpacity(0.25),
              blurRadius: 12,
              spreadRadius: 1,
            ),
          ],
        ),
        child: Center(
          child: Text(
            initials,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.w800,
              letterSpacing: 0.5,
            ),
          ),
        ),
      ),
    );
  }

  // ===========================================================================
  // 2. KPI ROW — 4 cards
  // ===========================================================================

  Widget _buildKPIRow(Map<String, dynamic> dash) {
    final ort = (dash['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
    final dev = (dash['devamsizlik_ozursuz'] as num?)?.toInt() ?? 0;
    final odev = (dash['bekleyen_odev_sayisi'] as num?)?.toInt() ?? 0;

    return Row(
      children: [
        Expanded(
          child: KPICard(
            icon: Icons.grade_rounded,
            label: 'Ortalama',
            value: ort.toStringAsFixed(1),
            color: ort >= 70 ? AppColors.success : AppColors.warning,
            onTap: () => context.push('/notes'),
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: KPICard(
            icon: Icons.event_busy_rounded,
            label: 'Devamsiz',
            value: '$dev',
            color: dev > 5 ? AppColors.danger : AppColors.success,
            onTap: () => context.push('/attendance'),
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: KPICard(
            icon: Icons.assignment_late_rounded,
            label: 'Odev',
            value: '$odev',
            color: odev > 3 ? AppColors.warning : AppColors.info,
            onTap: () => context.push('/homework'),
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: FutureBuilder<Map<String, dynamic>>(
            future: _moodFuture,
            builder: (_, snap) {
              final moodOrt =
                  (snap.data?['ortalama_seviye'] as num?)?.toDouble() ?? 0.0;
              final emoji = moodOrt >= 4
                  ? '\u{1F604}'
                  : moodOrt >= 3
                      ? '\u{1F642}'
                      : moodOrt > 0
                          ? '\u{1F61F}'
                          : '\u{2753}';
              return KPICard(
                icon: Icons.mood_rounded,
                label: 'Mood',
                value: emoji,
                color: moodOrt >= 4
                    ? AppColors.success
                    : moodOrt >= 3
                        ? AppColors.warning
                        : AppColors.danger,
                onTap: () => context.push('/mood'),
                isEmoji: true,
              );
            },
          ),
        ),
      ],
    );
  }

  // ===========================================================================
  // 3. YAKLASAN SINAVLAR — horizontal scrolling cards
  // ===========================================================================

  Widget _buildYaklasanSinavlar(Map<String, dynamic> dash) {
    final sinavlar = (dash['yaklasan_sinavlar'] as List?) ?? [];
    if (sinavlar.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SectionHeader(
          title: 'Yaklasan Sinavlar',
          icon: Icons.quiz_rounded,
          trailing: '${sinavlar.length} sinav',
        ),
        SizedBox(
          height: 128,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            itemCount: sinavlar.length,
            itemBuilder: (_, i) {
              final s = Map<String, dynamic>.from(sinavlar[i] as Map);
              return _buildSinavCard(s);
            },
          ),
        ),
        const SizedBox(height: AppSpacing.xxl),
      ],
    );
  }

  Widget _buildSinavCard(Map<String, dynamic> sinav) {
    final tarih = sinav['tarih'] as String? ?? '';
    final ders = sinav['ders'] as String? ?? '';
    final baslik = sinav['baslik'] as String? ?? ders;
    final konu = sinav['konu'] as String? ?? '';
    final isDark = Theme.of(context).brightness == Brightness.dark;

    DateTime? sinavTarih;
    try {
      sinavTarih = DateTime.parse(tarih);
    } catch (_) {}
    final kalanGun =
        sinavTarih != null ? sinavTarih.difference(DateTime.now()).inDays : 0;

    Color urgencyColor;
    Gradient urgencyGradient;
    if (kalanGun <= 3) {
      urgencyColor = AppColors.danger;
      urgencyGradient = AppGradients.danger;
    } else if (kalanGun <= 7) {
      urgencyColor = AppColors.warning;
      urgencyGradient = AppGradients.gold;
    } else {
      urgencyColor = AppColors.info;
      urgencyGradient = AppGradients.primary;
    }

    return Container(
      width: 172,
      margin: const EdgeInsets.only(right: AppSpacing.md),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            urgencyColor.withOpacity(isDark ? 0.20 : 0.10),
            urgencyColor.withOpacity(isDark ? 0.08 : 0.03),
          ],
        ),
        borderRadius: AppRadius.bLg,
        border: Border.all(color: urgencyColor.withOpacity(0.25)),
        boxShadow: AppShadows.soft,
      ),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Countdown badge
            Row(
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    gradient: urgencyGradient,
                    borderRadius: AppRadius.bFull,
                    boxShadow: AppShadows.glow(urgencyColor),
                  ),
                  child: Text(
                    kalanGun <= 0 ? 'BUGUN' : '$kalanGun gun',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 11,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 0.3,
                    ),
                  ),
                ),
                const Spacer(),
                Icon(Icons.quiz_rounded,
                    size: 16, color: urgencyColor.withOpacity(0.6)),
              ],
            ),
            const Spacer(),
            // Ders name
            Text(
              baslik,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w700,
                letterSpacing: -0.2,
              ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            if (konu.isNotEmpty) ...[
              const SizedBox(height: 2),
              Text(
                konu,
                style: TextStyle(
                  fontSize: 11,
                  color: isDark
                      ? AppColors.textTertiaryDark
                      : AppColors.textSecondaryLight,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ],
            const SizedBox(height: 4),
            Text(
              tarih,
              style: TextStyle(
                fontSize: 11,
                color: urgencyColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ===========================================================================
  // 4. ODEV GERI SAYIM
  // ===========================================================================

  Widget _buildOdevCountdown(Map<String, dynamic> dash) {
    final odevler = (dash['bekleyen_odevler'] as List?) ?? [];
    if (odevler.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SectionHeader(
          title: 'Odev Geri Sayim',
          icon: Icons.timer_rounded,
          trailing: '${odevler.length} odev',
        ),
        ...odevler.take(4).map((o) {
          final m = Map<String, dynamic>.from(o as Map);
          return _buildOdevTile(m);
        }),
        const SizedBox(height: AppSpacing.xxl),
      ],
    );
  }

  Widget _buildOdevTile(Map<String, dynamic> odev) {
    final baslik = odev['baslik'] as String? ?? '';
    final ders = odev['ders'] as String? ?? '';
    final teslim = odev['teslim_tarihi'] as String? ?? '';
    final isDark = Theme.of(context).brightness == Brightness.dark;

    DateTime? teslimTarih;
    try {
      teslimTarih = DateTime.parse(teslim);
    } catch (_) {}
    final kalanGun = teslimTarih != null
        ? teslimTarih.difference(DateTime.now()).inDays
        : 99;
    final kalanSaat = teslimTarih != null
        ? teslimTarih.difference(DateTime.now()).inHours % 24
        : 0;

    Color borderColor;
    if (kalanGun <= 1) {
      borderColor = AppColors.danger;
    } else if (kalanGun <= 3) {
      borderColor = AppColors.warning;
    } else {
      borderColor = AppColors.info;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: AppSpacing.sm),
      decoration: BoxDecoration(
        color: isDark
            ? borderColor.withOpacity(0.06)
            : borderColor.withOpacity(0.04),
        borderRadius: AppRadius.bMd,
        border: Border(
          left: BorderSide(color: borderColor, width: 4),
        ),
        boxShadow: AppShadows.soft,
      ),
      child: Padding(
        padding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            // Icon
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: borderColor.withOpacity(0.10),
                borderRadius: AppRadius.bSm,
              ),
              child: Icon(Icons.assignment_rounded,
                  size: 18, color: borderColor),
            ),
            const SizedBox(width: 12),
            // Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    baslik.isNotEmpty ? baslik : ders,
                    style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 2),
                  Text(
                    ders,
                    style: TextStyle(
                      fontSize: 11,
                      color: isDark
                          ? AppColors.textTertiaryDark
                          : AppColors.textSecondaryLight,
                    ),
                  ),
                ],
              ),
            ),
            // Countdown badge
            Container(
              padding:
                  const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: borderColor.withOpacity(0.12),
                borderRadius: AppRadius.bFull,
                border: Border.all(color: borderColor.withOpacity(0.2)),
              ),
              child: Text(
                kalanGun <= 0
                    ? 'BUGUN'
                    : kalanGun == 1
                        ? '${kalanSaat}s kaldi'
                        : '$kalanGun gun',
                style: TextStyle(
                  color: borderColor,
                  fontSize: 11,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ===========================================================================
  // 5. SON NOTLAR — Auto-scrolling PageView (3 notes per page)
  // ===========================================================================

  Widget _buildNotlarCarousel(Map<String, dynamic> dash) {
    final notlar = (dash['son_notlar'] as List?) ?? [];
    if (notlar.isEmpty) return const SizedBox.shrink();

    // Group notes, 3 per page
    final pages = <List<Map<String, dynamic>>>[];
    for (var i = 0; i < notlar.length; i += 3) {
      pages.add(notlar
          .skip(i)
          .take(3)
          .map((e) => Map<String, dynamic>.from(e as Map))
          .toList());
    }

    WidgetsBinding.instance
        .addPostFrameCallback((_) => _startAutoScroll(pages.length));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SectionHeader(
          title: 'Son Notlar',
          icon: Icons.analytics_rounded,
          trailing: '${notlar.length} not',
        ),
        SizedBox(
          height: 116,
          child: PageView.builder(
            controller: _pageCtrl,
            itemCount: pages.length,
            onPageChanged: (i) => setState(() => _currentPage = i),
            itemBuilder: (_, pageIdx) {
              final group = pages[pageIdx];
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 2),
                child: Row(
                  children: group.map((n) {
                    final puan =
                        (n['puan'] as num?)?.toDouble() ?? 0.0;
                    Color c;
                    IconData scoreIcon;
                    if (puan >= 85) {
                      c = AppColors.success;
                      scoreIcon = Icons.trending_up_rounded;
                    } else if (puan >= 70) {
                      c = AppColors.info;
                      scoreIcon = Icons.trending_flat_rounded;
                    } else if (puan >= 50) {
                      c = AppColors.warning;
                      scoreIcon = Icons.trending_down_rounded;
                    } else {
                      c = AppColors.danger;
                      scoreIcon = Icons.trending_down_rounded;
                    }
                    final isDark =
                        Theme.of(context).brightness == Brightness.dark;

                    return Expanded(
                      child: GlassCard(
                        margin: const EdgeInsets.symmetric(
                            horizontal: 4),
                        padding: const EdgeInsets.all(12),
                        borderRadius: AppRadius.md,
                        child: Column(
                          mainAxisAlignment:
                              MainAxisAlignment.center,
                          children: [
                            // Score
                            Row(
                              mainAxisAlignment:
                                  MainAxisAlignment.center,
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  puan.toStringAsFixed(0),
                                  style: TextStyle(
                                    fontSize: 26,
                                    fontWeight: FontWeight.w900,
                                    color: c,
                                    letterSpacing: -1,
                                  ),
                                ),
                                const SizedBox(width: 4),
                                Icon(scoreIcon,
                                    size: 16, color: c),
                              ],
                            ),
                            const SizedBox(height: 6),
                            // Ders
                            Text(
                              n['ders'] ?? '',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                                color: isDark
                                    ? AppColors.textPrimaryDark
                                    : AppColors.textPrimaryLight,
                              ),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 2),
                            // Not turu
                            Text(
                              n['not_turu'] ?? '',
                              style: TextStyle(
                                fontSize: 9,
                                fontWeight: FontWeight.w500,
                                color: c,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                ),
              );
            },
          ),
        ),
        // Animated page dots
        if (pages.length > 1)
          Padding(
            padding: const EdgeInsets.only(top: 10),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                pages.length,
                (i) => AnimatedContainer(
                  duration: const Duration(milliseconds: 350),
                  curve: Curves.easeInOutCubic,
                  width: _currentPage == i ? 22 : 6,
                  height: 6,
                  margin:
                      const EdgeInsets.symmetric(horizontal: 3),
                  decoration: BoxDecoration(
                    gradient: _currentPage == i
                        ? AppGradients.primary
                        : null,
                    color: _currentPage == i
                        ? null
                        : AppColors.primary.withOpacity(0.15),
                    borderRadius: AppRadius.bFull,
                    boxShadow: _currentPage == i
                        ? AppShadows.glow(AppColors.primary)
                        : AppShadows.none,
                  ),
                ),
              ),
            ),
          ),
        const SizedBox(height: AppSpacing.xxl),
      ],
    );
  }

  // ===========================================================================
  // 6. BUGUN DERSLER — horizontal chips
  // ===========================================================================

  Widget _buildBugunDersler(Map<String, dynamic> dash) {
    final dersler = (dash['bugun_dersler'] as List?) ?? [];
    if (dersler.isEmpty) return const SizedBox.shrink();

    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SectionHeader(
          title: 'Bugunku Dersler',
          icon: Icons.today_rounded,
          trailing: '${dersler.length} ders',
        ),
        SizedBox(
          height: 52,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            physics: const BouncingScrollPhysics(),
            itemCount: dersler.length,
            itemBuilder: (_, i) {
              final d = dersler[i] as Map;
              final colors = [
                AppColors.primary,
                AppColors.info,
                AppColors.success,
                AppColors.gold,
                AppColors.danger,
                const Color(0xFF8B5CF6),
                const Color(0xFFEC4899),
              ];
              final chipColor = colors[i % colors.length];

              return Container(
                margin: const EdgeInsets.only(right: AppSpacing.sm),
                padding: const EdgeInsets.symmetric(
                    horizontal: 16, vertical: 10),
                decoration: BoxDecoration(
                  color: chipColor.withOpacity(isDark ? 0.12 : 0.08),
                  borderRadius: AppRadius.bFull,
                  border: Border.all(
                      color: chipColor.withOpacity(0.20)),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 24,
                      height: 24,
                      decoration: BoxDecoration(
                        color: chipColor.withOpacity(0.15),
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: Text(
                          '${d['saat']}',
                          style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w800,
                            color: chipColor,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      '${d['ders']}',
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: isDark
                            ? AppColors.textPrimaryDark
                            : AppColors.textPrimaryLight,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
        const SizedBox(height: AppSpacing.xxl),
      ],
    );
  }

  // ===========================================================================
  // 7. MOOD CHECK-IN BANNER
  // ===========================================================================

  Widget _buildMoodBanner() {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: () => context.push('/mood'),
      child: Container(
        padding: const EdgeInsets.all(18),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppColors.mood5.withOpacity(isDark ? 0.15 : 0.10),
              AppColors.mood3.withOpacity(isDark ? 0.10 : 0.06),
              AppColors.mood4.withOpacity(isDark ? 0.08 : 0.04),
            ],
          ),
          borderRadius: AppRadius.bLg,
          border: Border.all(
              color: AppColors.mood5.withOpacity(isDark ? 0.25 : 0.20)),
          boxShadow: AppShadows.soft,
        ),
        child: Row(
          children: [
            // Emoji with glow
            Container(
              width: 52,
              height: 52,
              decoration: BoxDecoration(
                color: AppColors.mood5.withOpacity(0.12),
                shape: BoxShape.circle,
                boxShadow: AppShadows.glow(AppColors.mood5),
              ),
              child: const Center(
                child: Text('\u{1F60A}', style: TextStyle(fontSize: 28)),
              ),
            ),
            const SizedBox(width: 14),
            // Text
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Bugun nasil hissediyorsun?',
                    style: TextStyle(
                      fontWeight: FontWeight.w700,
                      fontSize: 15,
                      letterSpacing: -0.2,
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    '5 saniyede isaretle \u2014 gizli, sadece rehber gorur',
                    style: TextStyle(
                      fontSize: 11,
                      color: isDark
                          ? AppColors.textTertiaryDark
                          : AppColors.textSecondaryLight,
                    ),
                  ),
                ],
              ),
            ),
            // Arrow
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppColors.mood5.withOpacity(0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.arrow_forward_ios_rounded,
                size: 14,
                color: AppColors.mood5,
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ===========================================================================
  // 8. HIZLI ERISIM — Feature Grid
  // ===========================================================================

  Widget _buildFeatureGrid() {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      crossAxisSpacing: AppSpacing.md,
      mainAxisSpacing: AppSpacing.md,
      childAspectRatio: 1.4,
      children: [
        FeatureTile(
          icon: Icons.assignment_late_rounded,
          title: 'Gunluk Isler',
          subtitle: 'Bugun devamsizlar',
          color: const Color(0xFFDC2626),
          onTap: () => context.push('/gunluk-isler'),
        ),
        FeatureTile(
          icon: Icons.grade_rounded,
          title: 'Notlarim',
          subtitle: 'Ders ortalamalari',
          color: AppColors.primary,
          onTap: () => context.push('/notes'),
        ),
        FeatureTile(
          icon: Icons.assignment_rounded,
          title: 'Odevlerim',
          subtitle: 'Bekleyen + teslim',
          color: AppColors.gold,
          onTap: () => context.push('/homework'),
        ),
        FeatureTile(
          icon: Icons.calendar_today_rounded,
          title: 'Devamsizlik',
          subtitle: 'Bu donem',
          color: AppColors.warning,
          onTap: () => context.push('/attendance'),
        ),
        FeatureTile(
          icon: Icons.chat_rounded,
          title: 'Mesajlar',
          subtitle: 'Gelen / Giden',
          color: AppColors.info,
          onTap: () => context.push('/messages'),
        ),
        FeatureTile(
          icon: Icons.translate_rounded,
          title: 'Dil Gelisimi',
          subtitle: '5 dil - 104+ ders',
          color: AppColors.info,
          onTap: () => context.push('/dil-gelisimi'),
        ),
        FeatureTile(
          icon: Icons.workspace_premium_rounded,
          title: 'KDG Premium',
          subtitle: 'CEFR Ing + Alm',
          color: const Color(0xFF7C3AED),
          onTap: () => context.push('/kdg-premium'),
        ),
        FeatureTile(
          icon: Icons.shield_rounded,
          title: 'Ihbar Hatti',
          subtitle: 'Anonim bildirim',
          color: AppColors.danger,
          onTap: () => context.push('/ihbar'),
        ),
        FeatureTile(
          icon: Icons.calendar_month_rounded,
          title: 'Takvim',
          subtitle: 'Etkinlik + sinav',
          color: AppColors.gold,
          onTap: () => context.push('/takvim'),
        ),
        FeatureTile(
          icon: Icons.menu_book_rounded,
          title: 'Ders Programi',
          subtitle: 'Sinif/gun bazli',
          color: AppColors.info,
          onTap: () => context.push('/yonetici/ders-programi'),
        ),
        FeatureTile(
          icon: Icons.access_time_rounded,
          title: 'Zaman Cizelgesi',
          subtitle: 'Ders/teneffus',
          color: AppColors.warning,
          onTap: () => context.push('/yonetici/zaman-cizelgesi'),
        ),
        FeatureTile(
          icon: Icons.campaign_rounded,
          title: 'Duyuru & Yemek',
          subtitle: 'Okul duyurulari',
          color: AppColors.success,
          onTap: () => context.push('/duyuru-yemek'),
        ),
        FeatureTile(
          icon: Icons.lightbulb_rounded,
          title: 'Gunun Bilgisi',
          subtitle: 'Her gun yeni bilgi',
          color: AppColors.gold,
          onTap: () => context.push('/gunun-bilgisi'),
        ),
        FeatureTile(
          icon: Icons.extension_rounded,
          title: 'Zeka Oyunlari',
          subtitle: 'Hafiza + Sudoku',
          color: const Color(0xFFEC4899),
          onTap: () => context.push('/zeka-oyunlari'),
        ),
        FeatureTile(
          icon: Icons.local_library_rounded,
          title: 'Dijital Kutuphane',
          subtitle: 'YouTube + Lab + Muze',
          color: const Color(0xFF5D4037),
          onTap: () => context.push('/dijital-kutuphane'),
        ),
        FeatureTile(
          icon: Icons.emoji_events_rounded,
          title: 'Bilgi Yarismasi',
          subtitle: '4 tur - 3700+ soru',
          color: const Color(0xFF7C3AED),
          onTap: () => context.push('/bilgi-yarismasi-koleksiyon'),
        ),
        FeatureTile(
          icon: Icons.calculate_rounded,
          title: 'Matematik Koyu',
          subtitle: '6 oyun - formuller',
          color: const Color(0xFF6366F1),
          onTap: () => context.push('/matematik-koyu'),
        ),
        FeatureTile(
          icon: Icons.train_rounded,
          title: 'AI Treni',
          subtitle: '12 vagon - quiz',
          color: const Color(0xFF8B5CF6),
          onTap: () => context.push('/ai-treni'),
        ),
        FeatureTile(
          icon: Icons.quiz_rounded,
          title: 'Online Sinav',
          subtitle: 'Mobilde coz',
          color: AppColors.warning,
          onTap: () => context.push('/online-sinav'),
        ),
        FeatureTile(
          icon: Icons.emoji_events_rounded,
          title: 'Kocluk',
          subtitle: 'Hedef + gelisim',
          color: AppColors.gold,
          onTap: () => context.push('/kocluk'),
        ),
        FeatureTile(
          icon: Icons.smart_toy_rounded,
          title: 'Smarti AI',
          subtitle: 'Asistan',
          color: AppColors.primary,
          onTap: () => context.push('/smarti'),
        ),
        FeatureTile(
          icon: Icons.analytics_rounded,
          title: 'Sinav Sonuclari',
          subtitle: 'Yazili + deneme',
          color: const Color(0xFF8B5CF6),
          onTap: () => context.push('/ogrenci/sinav-sonuclari'),
        ),
        FeatureTile(
          icon: Icons.warning_amber_rounded,
          title: 'Kazanim Borclari',
          subtitle: 'Eksik kazanimlar',
          color: const Color(0xFFF97316),
          onTap: () => context.push('/ogrenci/kazanim-borclari'),
        ),
        FeatureTile(
          icon: Icons.replay_rounded,
          title: 'Telafi Gorevleri',
          subtitle: 'Quiz + pekistirme',
          color: const Color(0xFFEF4444),
          onTap: () => context.push('/ogrenci/telafi'),
        ),
        FeatureTile(
          icon: Icons.book_rounded,
          title: 'Defterim',
          subtitle: 'Kisisel notlar',
          color: const Color(0xFF14B8A6),
          onTap: () => context.push('/ogrenci/defterim'),
        ),
        FeatureTile(
          icon: Icons.gps_fixed_rounded,
          title: 'KYT Sorulari',
          subtitle: 'Kazanim pekistir',
          color: const Color(0xFF0EA5E9),
          onTap: () => context.push('/bilgi-yarismasi-koleksiyon'),
        ),
        FeatureTile(
          icon: Icons.palette_rounded,
          title: 'Sanat Sokagi',
          subtitle: 'Gorsel sanatlar',
          color: const Color(0xFFEC4899),
          onTap: () => context.push('/ogrenci/sanat-sokagi'),
        ),
        FeatureTile(
          icon: Icons.computer_rounded,
          title: 'Bilisim Vadisi',
          subtitle: 'Kodlama + dijital',
          color: const Color(0xFF6366F1),
          onTap: () => context.push('/ogrenci/bilisim-vadisi'),
        ),
      ],
    );
  }
}
