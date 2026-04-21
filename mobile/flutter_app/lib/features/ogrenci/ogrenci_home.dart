import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/api_client.dart';
import '../../core/api/ogrenci_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


/// Ultra Premium Öğrenci Home — Dashboard API, yaklaşan sınav, ödev countdown, karusel
class OgrenciHomePage extends ConsumerStatefulWidget {
  const OgrenciHomePage({super.key});

  @override
  ConsumerState<OgrenciHomePage> createState() => _OgrenciHomePageState();
}

class _OgrenciHomePageState extends ConsumerState<OgrenciHomePage>
    with TickerProviderStateMixin {
  Future<Map<String, dynamic>>? _dashFuture;
  Future<Map<String, dynamic>>? _moodFuture;
  Future<Map<String, dynamic>>? _bildirimFuture;

  // Karusel auto-scroll
  late final PageController _pageCtrl;
  Timer? _autoTimer;
  int _currentPage = 0;

  @override
  void initState() {
    super.initState();
    _pageCtrl = PageController(viewportFraction: 0.85);
    _loadAll();
  }

  @override
  void dispose() {
    _autoTimer?.cancel();
    _pageCtrl.dispose();
    super.dispose();
  }

  void _loadAll() {
    final api = ref.read(apiClientProvider);
    setState(() {
      _dashFuture = api.get('/ogrenci/dashboard').then((r) =>
          Map<String, dynamic>.from(r.data));
      _moodFuture = api.get('/mood/summary').then((r) =>
          Map<String, dynamic>.from(r.data));
      _bildirimFuture = api.get('/bildirim/liste', params: {'limit': 5}).then(
          (r) => Map<String, dynamic>.from(r.data));
    });
  }

  void _startAutoScroll(int pageCount) {
    _autoTimer?.cancel();
    if (pageCount <= 1) return;
    _autoTimer = Timer.periodic(const Duration(seconds: 4), (_) {
      _currentPage = (_currentPage + 1) % pageCount;
      if (_pageCtrl.hasClients) {
        _pageCtrl.animateToPage(_currentPage,
            duration: const Duration(milliseconds: 400),
            curve: Curves.easeInOut);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final userAsync = ref.watch(currentUserProvider);

    return userAsync.when(
      data: (user) => _buildPage(context, user),
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(body: Center(child: Text('Hata: $e'))),
    );
  }

  Widget _buildPage(BuildContext context, AuthUser? user) {
    if (user == null) {
      WidgetsBinding.instance.addPostFrameCallback((_) => context.go('/login'));
      return const SizedBox();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Merhaba, ${user.adSoyad.split(' ').first}'),
        actions: [
          // Bildirim badge
          FutureBuilder<Map<String, dynamic>>(
            future: _bildirimFuture,
            builder: (_, snap) {
              final okunmamis = (snap.data?['okunmamis'] as int?) ?? 0;
              return Stack(
                children: [
                  IconButton(
                    icon: const Icon(Icons.notifications_outlined),
                    onPressed: () => context.push('/bildirimler'),
                  ),
                  if (okunmamis > 0)
                    Positioned(
                      right: 6, top: 6,
                      child: Container(
                        padding: const EdgeInsets.all(4),
                        decoration: const BoxDecoration(
                          color: AppColors.danger,
                          shape: BoxShape.circle,
                        ),
                        child: Text('$okunmamis',
                            style: const TextStyle(color: Colors.white,
                                fontSize: 10, fontWeight: FontWeight.bold)),
                      ),
                    ),
                ],
              );
            },
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
      body: RefreshIndicator(
        onRefresh: () async => _loadAll(),
        child: FutureBuilder<Map<String, dynamic>>(
          future: _dashFuture,
          builder: (ctx, snap) {
            if (snap.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            final dash = snap.data ?? {};
            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              physics: const AlwaysScrollableScrollPhysics(),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // === HERO CARD ===
                  _HeroCard(user: user),
                  const SizedBox(height: 16),

                  // === 4 KPI KART ===
                  _buildKPIRow(dash),
                  const SizedBox(height: 20),

                  // === YAKLASAN SINAVLAR ===
                  _buildYaklasanSinavlar(dash),

                  // === ODEV COUNTDOWN ===
                  _buildOdevCountdown(dash),

                  // === SON NOTLAR KARUSEL ===
                  _buildNotlarKarusel(dash),
                  const SizedBox(height: 20),

                  // === BUGUN DERSLER ===
                  _buildBugunDersler(dash),

                  // === MOOD CHECK-IN BANNER ===
                  _buildMoodBanner(),
                  const SizedBox(height: 20),

                  // === HIZLI ERISIM GRID ===
                  const Text('Hızlı Erişim',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 12),
                  _buildFeatureGrid(),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  // ─── KPI ROW ───
  Widget _buildKPIRow(Map<String, dynamic> dash) {
    final ort = (dash['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
    final dev = (dash['devamsizlik_ozursuz'] as num?)?.toInt() ?? 0;
    final odev = (dash['bekleyen_odev_sayisi'] as num?)?.toInt() ?? 0;

    return Row(children: [
      Expanded(child: _KPICard(
        icon: Icons.grade, label: 'Ortalama',
        value: ort.toStringAsFixed(1),
        color: ort >= 70 ? AppColors.success : AppColors.warning,
        onTap: () => context.push('/notes'),
      )),
      const SizedBox(width: 8),
      Expanded(child: _KPICard(
        icon: Icons.event_busy, label: 'Devamsız',
        value: '$dev',
        color: dev > 5 ? AppColors.danger : AppColors.success,
        onTap: () => context.push('/attendance'),
      )),
      const SizedBox(width: 8),
      Expanded(child: _KPICard(
        icon: Icons.assignment_late, label: 'Ödev',
        value: '$odev',
        color: odev > 3 ? AppColors.warning : AppColors.info,
        onTap: () => context.push('/homework'),
      )),
      const SizedBox(width: 8),
      Expanded(child: FutureBuilder<Map<String, dynamic>>(
        future: _moodFuture,
        builder: (_, snap) {
          final ort = (snap.data?['ortalama_seviye'] as num?)?.toDouble() ?? 0.0;
          final emoji = ort >= 4 ? '😄' : ort >= 3 ? '🙂' : ort > 0 ? '😟' : '❓';
          return _KPICard(
            icon: Icons.mood, label: 'Mood',
            value: emoji,
            color: ort >= 4 ? AppColors.success : ort >= 3 ? AppColors.warning : AppColors.danger,
            onTap: () => context.push('/mood'),
            isEmoji: true,
          );
        },
      )),
    ]);
  }

  // ─── YAKLASAN SINAVLAR ───
  Widget _buildYaklasanSinavlar(Map<String, dynamic> dash) {
    final sinavlar = (dash['yaklasan_sinavlar'] as List?) ?? [];
    if (sinavlar.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.quiz, size: 20, color: AppColors.danger),
            const SizedBox(width: 6),
            const Text('Yaklaşan Sınavlar',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const Spacer(),
            Text('${sinavlar.length} sınav',
                style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ],
        ),
        const SizedBox(height: 10),
        SizedBox(
          height: 110,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: sinavlar.length,
            itemBuilder: (_, i) {
              final s = sinavlar[i] as Map;
              return _SinavCard(sinav: Map<String, dynamic>.from(s));
            },
          ),
        ),
        const SizedBox(height: 20),
      ],
    );
  }

  // ─── ODEV COUNTDOWN ───
  Widget _buildOdevCountdown(Map<String, dynamic> dash) {
    final odevler = (dash['bekleyen_odevler'] as List?) ?? [];
    if (odevler.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.timer, size: 20, color: AppColors.warning),
            const SizedBox(width: 6),
            const Text('Ödev Geri Sayım',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
          ],
        ),
        const SizedBox(height: 10),
        ...odevler.take(3).map((o) {
          final m = Map<String, dynamic>.from(o as Map);
          return _OdevCountdownTile(odev: m);
        }),
        const SizedBox(height: 20),
      ],
    );
  }

  // ─── SON NOTLAR KARUSEL (PageView) ───
  Widget _buildNotlarKarusel(Map<String, dynamic> dash) {
    final notlar = (dash['son_notlar'] as List?) ?? [];
    if (notlar.isEmpty) return const SizedBox.shrink();

    // 3'lü gruplar halinde PageView
    final pages = <List<Map>>[];
    for (var i = 0; i < notlar.length; i += 3) {
      pages.add(notlar.skip(i).take(3).map((e) =>
          Map<String, dynamic>.from(e as Map)).toList());
    }

    WidgetsBinding.instance.addPostFrameCallback((_) => _startAutoScroll(pages.length));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Son Notlar',
            style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
        const SizedBox(height: 10),
        SizedBox(
          height: 100,
          child: PageView.builder(
            controller: _pageCtrl,
            itemCount: pages.length,
            onPageChanged: (i) => _currentPage = i,
            itemBuilder: (_, pageIdx) {
              final group = pages[pageIdx];
              return Row(
                children: group.map((n) {
                  final puan = (n['puan'] as num?)?.toDouble() ?? 0.0;
                  Color c = puan >= 85
                      ? AppColors.success
                      : puan >= 70
                          ? AppColors.info
                          : puan >= 50
                              ? AppColors.warning
                              : AppColors.danger;
                  return Expanded(
                    child: Container(
                      margin: const EdgeInsets.symmetric(horizontal: 4),
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: c.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: c.withOpacity(0.3)),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(puan.toStringAsFixed(0),
                              style: TextStyle(fontSize: 24,
                                  fontWeight: FontWeight.bold, color: c)),
                          const SizedBox(height: 4),
                          Text(n['ders'] ?? '', textAlign: TextAlign.center,
                              style: const TextStyle(fontSize: 10),
                              maxLines: 2, overflow: TextOverflow.ellipsis),
                          Text(n['not_turu'] ?? '',
                              style: TextStyle(fontSize: 9, color: c)),
                        ],
                      ),
                    ),
                  );
                }).toList(),
              );
            },
          ),
        ),
        if (pages.length > 1)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(pages.length, (i) =>
                  AnimatedContainer(
                    duration: const Duration(milliseconds: 300),
                    width: _currentPage == i ? 18 : 6,
                    height: 6,
                    margin: const EdgeInsets.symmetric(horizontal: 3),
                    decoration: BoxDecoration(
                      color: _currentPage == i
                          ? AppColors.primary
                          : AppColors.primary.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(3),
                    ),
                  ),
              ),
            ),
          ),
      ],
    );
  }

  // ─── BUGUN DERSLER ───
  Widget _buildBugunDersler(Map<String, dynamic> dash) {
    final dersler = (dash['bugun_dersler'] as List?) ?? [];
    if (dersler.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.today, size: 20, color: AppColors.primary),
            const SizedBox(width: 6),
            const Text('Bugünkü Dersler',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const Spacer(),
            Text('${dersler.length} ders',
                style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ],
        ),
        const SizedBox(height: 10),
        SizedBox(
          height: 60,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: dersler.length,
            itemBuilder: (_, i) {
              final d = dersler[i] as Map;
              return Container(
                width: 110,
                margin: const EdgeInsets.only(right: 8),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.08),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppColors.primary.withOpacity(0.2)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('${d['saat']}. ders',
                        style: const TextStyle(fontSize: 10,
                            fontWeight: FontWeight.bold, color: AppColors.primary)),
                    Text('${d['ders']}',
                        style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                        maxLines: 1, overflow: TextOverflow.ellipsis),
                  ],
                ),
              );
            },
          ),
        ),
        const SizedBox(height: 20),
      ],
    );
  }

  // ─── MOOD BANNER ─��─
  Widget _buildMoodBanner() {
    return InkWell(
      onTap: () => context.push('/mood'),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [
            AppColors.mood5.withOpacity(0.15),
            AppColors.mood3.withOpacity(0.1),
          ]),
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.mood5.withOpacity(0.3)),
        ),
        child: Row(children: [
          const Text('😊', style: TextStyle(fontSize: 32)),
          const SizedBox(width: 12),
          Expanded(child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Bugün nasıl hissediyorsun?',
                  style: TextStyle(fontWeight: FontWeight.w600, fontSize: 15)),
              Text('5 saniyede işaretle — gizli, sadece rehber görür',
                  style: TextStyle(fontSize: 11, color: Colors.grey[600])),
            ],
          )),
          const Icon(Icons.arrow_forward_ios, size: 16,
              color: AppColors.textSecondaryDark),
        ]),
      ),
    );
  }

  // ─── FEATURE GRID ───
  Widget _buildFeatureGrid() {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      crossAxisSpacing: 12, mainAxisSpacing: 12,
      childAspectRatio: 1.4,
      children: [
        _FeatureCard(icon: Icons.assignment_late, title: 'Günlük İşler',
            subtitle: 'Bugün devamsızlar', color: const Color(0xFFDC2626),
            onTap: () => context.push('/gunluk-isler')),
        _FeatureCard(icon: Icons.grade, title: 'Notlarım',
            subtitle: 'Ders ortalamaları', color: AppColors.primary,
            onTap: () => context.push('/notes')),
        _FeatureCard(icon: Icons.assignment, title: 'Ödevlerim',
            subtitle: 'Bekleyen + teslim', color: AppColors.gold,
            onTap: () => context.push('/homework')),
        _FeatureCard(icon: Icons.calendar_today, title: 'Devamsızlık',
            subtitle: 'Bu dönem', color: AppColors.warning,
            onTap: () => context.push('/attendance')),
        _FeatureCard(icon: Icons.chat, title: 'Mesajlar',
            subtitle: 'Gelen / Giden', color: AppColors.info,
            onTap: () => context.push('/messages')),
        _FeatureCard(icon: Icons.translate, title: 'Dil Gelişimi',
            subtitle: '5 dil · 104+ ders', color: AppColors.info,
            onTap: () => context.push('/dil-gelisimi')),
        _FeatureCard(icon: Icons.workspace_premium, title: 'KDG Premium',
            subtitle: 'CEFR İng + Alm', color: const Color(0xFF7C3AED),
            onTap: () => context.push('/kdg-premium')),
        _FeatureCard(icon: Icons.shield, title: 'İhbar Hattı',
            subtitle: 'Anonim bildirim', color: AppColors.danger,
            onTap: () => context.push('/ihbar')),
        _FeatureCard(icon: Icons.calendar_month, title: 'Takvim',
            subtitle: 'Etkinlik + sınav', color: AppColors.gold,
            onTap: () => context.push('/takvim')),
        _FeatureCard(icon: Icons.menu_book, title: 'Ders Programı',
            subtitle: 'Sınıf/gün bazlı', color: AppColors.info,
            onTap: () => context.push('/yonetici/ders-programi')),
        _FeatureCard(icon: Icons.access_time, title: 'Zaman Çizelgesi',
            subtitle: 'Ders/teneffüs', color: AppColors.warning,
            onTap: () => context.push('/yonetici/zaman-cizelgesi')),
        _FeatureCard(icon: Icons.campaign, title: 'Duyuru & Yemek',
            subtitle: 'Okul duyuruları', color: AppColors.success,
            onTap: () => context.push('/duyuru-yemek')),
        _FeatureCard(icon: Icons.lightbulb, title: 'Günün Bilgisi',
            subtitle: 'Her gün yeni bilgi', color: AppColors.gold,
            onTap: () => context.push('/gunun-bilgisi')),
        _FeatureCard(icon: Icons.extension, title: 'Zeka Oyunları',
            subtitle: 'Hafıza + Sudoku', color: const Color(0xFFEC4899),
            onTap: () => context.push('/zeka-oyunlari')),
        _FeatureCard(icon: Icons.local_library, title: 'Dijital Kütüphane',
            subtitle: 'YouTube + Lab + Müze', color: const Color(0xFF5D4037),
            onTap: () => context.push('/dijital-kutuphane')),
        _FeatureCard(icon: Icons.emoji_events, title: 'Bilgi Yarışmaları',
            subtitle: '4 tür · 3700+ soru', color: const Color(0xFF7C3AED),
            onTap: () => context.push('/bilgi-yarismasi-koleksiyon')),
        _FeatureCard(icon: Icons.calculate, title: 'Matematik Köyü',
            subtitle: '6 oyun · formüller', color: const Color(0xFF6366F1),
            onTap: () => context.push('/matematik-koyu')),
        _FeatureCard(icon: Icons.train, title: 'AI Treni',
            subtitle: '12 vagon · quiz', color: const Color(0xFF8B5CF6),
            onTap: () => context.push('/ai-treni')),
        _FeatureCard(icon: Icons.quiz, title: 'Online Sınav',
            subtitle: 'Mobilde çöz', color: AppColors.warning,
            onTap: () => context.push('/online-sinav')),
        _FeatureCard(icon: Icons.emoji_events, title: 'Koçluk',
            subtitle: 'Hedef + gelişim', color: AppColors.gold,
            onTap: () => context.push('/kocluk')),
        _FeatureCard(icon: Icons.smart_toy, title: 'Smarti AI',
            subtitle: 'Asistan', color: AppColors.primary,
            onTap: () => context.push('/smarti')),
        _FeatureCard(icon: Icons.analytics, title: 'Sınav Sonuçlarım',
            subtitle: 'Yazılı + deneme', color: const Color(0xFF8B5CF6),
            onTap: () => context.push('/ogrenci/sinav-sonuclari')),
        _FeatureCard(icon: Icons.warning_amber, title: 'Kazanım Borçlarım',
            subtitle: 'Eksik kazanımlar', color: const Color(0xFFF97316),
            onTap: () => context.push('/ogrenci/kazanim-borclari')),
        _FeatureCard(icon: Icons.replay, title: 'Telafi Görevleri',
            subtitle: 'Quiz + pekiştirme', color: const Color(0xFFEF4444),
            onTap: () => context.push('/ogrenci/telafi')),
        _FeatureCard(icon: Icons.book, title: 'Öğrenci Defterim',
            subtitle: 'Kişisel notlar', color: const Color(0xFF14B8A6),
            onTap: () => context.push('/ogrenci/defterim')),
        _FeatureCard(icon: Icons.gps_fixed, title: 'KYT Soruları',
            subtitle: 'Kazanım pekiştir', color: const Color(0xFF0EA5E9),
            onTap: () => context.push('/bilgi-yarismasi-koleksiyon')),
        _FeatureCard(icon: Icons.palette, title: 'Sanat Sokağı',
            subtitle: 'Görsel sanatlar', color: const Color(0xFFEC4899),
            onTap: () => context.push('/ogrenci/sanat-sokagi')),
        _FeatureCard(icon: Icons.computer, title: 'Bilişim Vadisi',
            subtitle: 'Kodlama + dijital', color: const Color(0xFF6366F1),
            onTap: () => context.push('/ogrenci/bilisim-vadisi')),
      ],
    );
  }
}


// ═══════════════════════════════════════════════════════════
// HERO CARD
// ═══════════════════════════════════════════════════════════

class _HeroCard extends StatelessWidget {
  final AuthUser user;
  const _HeroCard({required this.user});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft, end: Alignment.bottomRight,
          colors: [AppColors.primary, AppColors.primaryDark],
        ),
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(color: AppColors.primary.withOpacity(0.3),
              blurRadius: 16, offset: const Offset(0, 6)),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(children: [
            const Icon(Icons.school, color: Colors.white, size: 28),
            const SizedBox(width: 10),
            const Text('SmartCampus AI',
                style: TextStyle(color: Colors.white, fontSize: 16,
                    fontWeight: FontWeight.w600)),
            const Spacer(),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: AppColors.gold.withOpacity(0.3),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(user.role.toUpperCase(),
                  style: const TextStyle(color: AppColors.gold, fontSize: 10,
                      fontWeight: FontWeight.bold, letterSpacing: 1.2)),
            ),
          ]),
          const SizedBox(height: 12),
          Text(user.adSoyad,
              style: const TextStyle(color: Colors.white, fontSize: 22,
                  fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}


// ════════════════════════════��══════════════════════════════
// SINAV CARD (Countdown)
// ═════���═══════════════════���═════════════════════════��═══════

class _SinavCard extends StatelessWidget {
  final Map<String, dynamic> sinav;
  const _SinavCard({required this.sinav});

  @override
  Widget build(BuildContext context) {
    final tarih = sinav['tarih'] as String? ?? '';
    final ders = sinav['ders'] as String? ?? '';
    final baslik = sinav['baslik'] as String? ?? ders;
    final konu = sinav['konu'] as String? ?? '';

    // Geri sayım
    DateTime? sinavTarih;
    try { sinavTarih = DateTime.parse(tarih); } catch (_) {}
    final kalanGun = sinavTarih != null
        ? sinavTarih.difference(DateTime.now()).inDays
        : 0;

    Color acil = kalanGun <= 3
        ? AppColors.danger
        : kalanGun <= 7
            ? AppColors.warning
            : AppColors.info;

    return Container(
      width: 160,
      margin: const EdgeInsets.only(right: 10),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft, end: Alignment.bottomRight,
          colors: [acil.withOpacity(0.15), acil.withOpacity(0.05)],
        ),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: acil.withOpacity(0.4)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: acil.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  kalanGun <= 0 ? 'BUGÜN!' : '$kalanGun gün',
                  style: TextStyle(color: acil, fontSize: 11,
                      fontWeight: FontWeight.bold),
                ),
              ),
              const Spacer(),
              Icon(Icons.quiz, size: 16, color: acil),
            ],
          ),
          const Spacer(),
          Text(baslik, style: const TextStyle(fontSize: 13,
              fontWeight: FontWeight.w600),
              maxLines: 1, overflow: TextOverflow.ellipsis),
          if (konu.isNotEmpty)
            Text(konu, style: TextStyle(fontSize: 10,
                color: Colors.grey[600]),
                maxLines: 1, overflow: TextOverflow.ellipsis),
          Text(tarih, style: TextStyle(fontSize: 10, color: acil,
              fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }
}


// ═══════════════════════════���═══════════════════════════════
// ODEV COUNTDOWN TILE
// ═══════════════════════════════════════════════════════════

class _OdevCountdownTile extends StatelessWidget {
  final Map<String, dynamic> odev;
  const _OdevCountdownTile({required this.odev});

  @override
  Widget build(BuildContext context) {
    final baslik = odev['baslik'] as String? ?? '';
    final ders = odev['ders'] as String? ?? '';
    final teslim = odev['teslim_tarihi'] as String? ?? '';

    DateTime? teslimTarih;
    try { teslimTarih = DateTime.parse(teslim); } catch (_) {}
    final kalanGun = teslimTarih != null
        ? teslimTarih.difference(DateTime.now()).inDays
        : 99;
    final kalanSaat = teslimTarih != null
        ? teslimTarih.difference(DateTime.now()).inHours % 24
        : 0;

    Color c = kalanGun <= 1
        ? AppColors.danger
        : kalanGun <= 3
            ? AppColors.warning
            : AppColors.info;

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        color: c.withOpacity(0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border(left: BorderSide(color: c, width: 4)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(baslik.isNotEmpty ? baslik : ders,
                    style: const TextStyle(fontSize: 13,
                        fontWeight: FontWeight.w600),
                    maxLines: 1, overflow: TextOverflow.ellipsis),
                Text(ders, style: TextStyle(fontSize: 11,
                    color: Colors.grey[600])),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: c.withOpacity(0.15),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              kalanGun <= 0
                  ? 'BUGÜN!'
                  : kalanGun == 1
                      ? '${kalanSaat}s kaldı'
                      : '$kalanGun gün',
              style: TextStyle(color: c, fontSize: 12,
                  fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// YARDIMCI WIDGET'LAR
// ═══════���══════════════════════════════════════════���════════

class _KPICard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;
  final VoidCallback onTap;
  final bool isEmoji;
  const _KPICard({required this.icon, required this.label, required this.value,
                  required this.color, required this.onTap, this.isEmoji = false});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 8),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (isEmoji)
              Text(value, style: const TextStyle(fontSize: 22))
            else
              Text(value, style: TextStyle(fontSize: 22,
                  fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 10),
                textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}


class _FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  const _FeatureCard({required this.icon, required this.title,
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
              child: Icon(icon, color: color, size: 22),
            ),
            const Spacer(),
            Text(title, style: const TextStyle(fontSize: 13,
                fontWeight: FontWeight.w600)),
            Text(subtitle, style: TextStyle(fontSize: 11,
                color: Theme.of(context).textTheme.bodySmall?.color)),
          ],
        ),
      ),
    );
  }
}
