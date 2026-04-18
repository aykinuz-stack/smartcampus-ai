import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/api_client.dart';
import '../../core/api/ogrenci_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


/// Ultra Premium Ogrenci Home — KPI + karusel + hizli erisim
class OgrenciHomePage extends ConsumerStatefulWidget {
  const OgrenciHomePage({super.key});

  @override
  ConsumerState<OgrenciHomePage> createState() => _OgrenciHomePageState();
}

class _OgrenciHomePageState extends ConsumerState<OgrenciHomePage> {
  Future<Map<String, dynamic>>? _notlarFuture;
  Future<Map<String, dynamic>>? _devamFuture;
  Future<Map<String, dynamic>>? _odevFuture;
  Future<Map<String, dynamic>>? _moodFuture;

  @override
  void initState() {
    super.initState();
    _loadAll();
  }

  void _loadAll() {
    final api = ref.read(apiClientProvider);
    setState(() {
      _notlarFuture = ref.read(ogrenciApiProvider).getNotlar();
      _devamFuture = ref.read(ogrenciApiProvider).getDevamsizlik();
      _odevFuture = ref.read(ogrenciApiProvider).getOdevler();
      _moodFuture = api.get('/mood/summary').then((r) =>
          Map<String, dynamic>.from(r.data));
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
        onRefresh: () async => _loadAll(),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          physics: const AlwaysScrollableScrollPhysics(),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ═══ HERO CARD ═══
              Container(
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
                          style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
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
                        style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // ═══ 4 KPI KART ═══
              Row(children: [
                Expanded(child: _KPIBuilder(
                  future: _notlarFuture,
                  builder: (d) {
                    final ort = (d['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
                    return _KPICard(
                      icon: Icons.grade, label: 'Ortalama',
                      value: ort.toStringAsFixed(1),
                      color: ort >= 70 ? AppColors.success : AppColors.warning,
                      onTap: () => context.push('/notes'),
                    );
                  },
                )),
                const SizedBox(width: 8),
                Expanded(child: _KPIBuilder(
                  future: _devamFuture,
                  builder: (d) {
                    final oz = (d['ozursuz'] as num?)?.toInt() ?? 0;
                    return _KPICard(
                      icon: Icons.event_busy, label: 'Devamsız',
                      value: '$oz',
                      color: oz > 5 ? AppColors.danger : AppColors.success,
                      onTap: () => context.push('/attendance'),
                    );
                  },
                )),
                const SizedBox(width: 8),
                Expanded(child: _KPIBuilder(
                  future: _odevFuture,
                  builder: (d) {
                    final bek = ((d['bekleyen'] as List?)?.length ?? 0) +
                                ((d['geciken'] as List?)?.length ?? 0);
                    return _KPICard(
                      icon: Icons.assignment_late, label: 'Ödev',
                      value: '$bek',
                      color: bek > 3 ? AppColors.warning : AppColors.info,
                      onTap: () => context.push('/homework'),
                    );
                  },
                )),
                const SizedBox(width: 8),
                Expanded(child: _KPIBuilder(
                  future: _moodFuture,
                  builder: (d) {
                    final ort = (d['ortalama_seviye'] as num?)?.toDouble() ?? 0.0;
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
              ]),
              const SizedBox(height: 20),

              // ═══ SON NOTLAR KARUSEL ═══
              const Text('Son Notlar',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              SizedBox(
                height: 100,
                child: _KPIBuilder(
                  future: _notlarFuture,
                  builder: (d) {
                    final notlar = (d['notlar'] as List?) ?? [];
                    if (notlar.isEmpty) {
                      return const Center(child: Text('Henüz not yok',
                          style: TextStyle(color: AppColors.textSecondaryDark)));
                    }
                    return ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: notlar.length > 10 ? 10 : notlar.length,
                      itemBuilder: (_, i) {
                        final n = notlar[i] as Map;
                        final puan = (n['puan'] as num?)?.toDouble() ?? 0.0;
                        Color c = puan >= 85 ? AppColors.success : puan >= 70 ? AppColors.info :
                                  puan >= 50 ? AppColors.warning : AppColors.danger;
                        return Container(
                          width: 100,
                          margin: const EdgeInsets.only(right: 10),
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
                                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: c)),
                              const SizedBox(height: 4),
                              Text(n['ders'] ?? '', textAlign: TextAlign.center,
                                  style: const TextStyle(fontSize: 10), maxLines: 2, overflow: TextOverflow.ellipsis),
                              Text(n['not_turu'] ?? '', style: TextStyle(fontSize: 9, color: c)),
                            ],
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
              const SizedBox(height: 20),

              // ═══ MOOD CHECK-IN BANNER ═══
              InkWell(
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
                    const Icon(Icons.arrow_forward_ios, size: 16, color: AppColors.textSecondaryDark),
                  ]),
                ),
              ),
              const SizedBox(height: 20),

              // ═══ HIZLI ERİŞİM GRID ═══
              const Text('Hızlı Erişim',
                  style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
              const SizedBox(height: 12),
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                crossAxisSpacing: 12, mainAxisSpacing: 12,
                childAspectRatio: 1.4,
                children: [
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
                      subtitle: 'CEFR İng + Alm', color: Color(0xFF7C3AED),
                      onTap: () => context.push('/kdg-premium')),
                  _FeatureCard(icon: Icons.shield, title: 'İhbar Hattı',
                      subtitle: 'Anonim bildirim', color: AppColors.danger,
                      onTap: () => context.push('/ihbar')),
                  _FeatureCard(icon: Icons.calendar_month, title: 'Takvim',
                      subtitle: 'Etkinlik + sınav', color: AppColors.gold,
                      onTap: () => context.push('/takvim')),
                  _FeatureCard(icon: Icons.campaign, title: 'Duyuru & Yemek',
                      subtitle: 'Okul duyuruları', color: AppColors.success,
                      onTap: () => context.push('/duyuru-yemek')),
                  _FeatureCard(icon: Icons.lightbulb, title: 'Günün Bilgisi',
                      subtitle: 'Her gün yeni bilgi', color: AppColors.gold,
                      onTap: () => context.push('/gunun-bilgisi')),
                  _FeatureCard(icon: Icons.extension, title: 'Zeka Oyunları',
                      subtitle: 'Hafıza + Sudoku', color: Color(0xFFEC4899),
                      onTap: () => context.push('/zeka-oyunlari')),
                  _FeatureCard(icon: Icons.local_library, title: 'Dijital Kütüphane',
                      subtitle: 'YouTube + Lab + Müze', color: Color(0xFF5D4037),
                      onTap: () => context.push('/dijital-kutuphane')),
                  _FeatureCard(icon: Icons.emoji_events, title: 'Bilgi Yarışmaları',
                      subtitle: '4 tür · 3700+ soru', color: Color(0xFF7C3AED),
                      onTap: () => context.push('/bilgi-yarismasi-koleksiyon')),
                  _FeatureCard(icon: Icons.train, title: 'AI Treni',
                      subtitle: '12 vagon · quiz', color: Color(0xFF8B5CF6),
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
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// YARDIMCI WIDGET'LAR
// ═══════════════════════════════════════════════════════════

class _KPIBuilder extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  final Widget Function(Map<String, dynamic>) builder;
  const _KPIBuilder({required this.future, required this.builder});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: SizedBox(width: 16, height: 16,
              child: CircularProgressIndicator(strokeWidth: 2)));
        }
        if (snap.hasError || snap.data == null) {
          return const Center(child: Text('-', style: TextStyle(fontSize: 20)));
        }
        return builder(snap.data!);
      },
    );
  }
}


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
              Text(value, style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 10), textAlign: TextAlign.center),
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
            Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
            Text(subtitle, style: TextStyle(fontSize: 11,
                color: Theme.of(context).textTheme.bodySmall?.color)),
          ],
        ),
      ),
    );
  }
}
