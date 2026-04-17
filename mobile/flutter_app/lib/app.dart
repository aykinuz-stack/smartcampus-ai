import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'core/auth/auth_service.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/login_page.dart';
import 'features/ogrenci/mood_checkin_page.dart';
import 'features/ogrenci/ogrenci_home.dart';
import 'features/ogrenci/notlar_page.dart';
import 'features/ogrenci/devamsizlik_page.dart';
import 'features/ogrenci/odev_page.dart';
import 'features/ogrenci/mesaj_page.dart';
import 'features/ogrenci/ihbar_page.dart';
import 'features/veli/veli_home.dart';
import 'features/veli/kapsul_page.dart';
import 'features/veli/randevu_page.dart';
import 'features/veli/belge_page.dart';
import 'features/veli/geri_bildirim_page.dart';
import 'features/veli/cocuk_detay_page.dart';
import 'features/ogretmen/ogretmen_home.dart';
import 'features/ogretmen/yoklama_page.dart';
import 'features/ogretmen/qr_yoklama_page.dart';
import 'features/ogretmen/sinav_sonuc_page.dart';
import 'features/ogretmen/not_giris_page.dart';
import 'features/ogretmen/ders_defteri_page.dart';
import 'features/ogretmen/odev_ata_page.dart';
import 'features/rehber/rehber_home.dart';
import 'features/rehber/vakalar_page.dart';
import 'features/rehber/gorusme_page.dart';
import 'features/rehber/aile_form_page.dart';
import 'features/rehber/mood_panel_page.dart';
import 'features/rehber/ihbar_inceleme_page.dart';
import 'features/yonetici/yonetici_home.dart';
import 'features/yonetici/erken_uyari_page.dart';
import 'features/yonetici/onaylar_page.dart';
import 'features/yonetici/bugun_okulda_page.dart';
import 'features/yonetici/butce_page.dart';
import 'features/yonetici/randevular_page.dart';
import 'features/yonetici/gun_raporu_page.dart';
import 'features/yonetici/kayit_ozet_page.dart';
import 'features/yonetici/ders_programi_page.dart';
import 'features/yonetici/nobet_page.dart';
import 'features/yonetici/zaman_cizelgesi_page.dart';
import 'features/yonetici/calisanlar_page.dart';
import 'features/yonetici/sinif_listeleri_page.dart';
import 'features/yonetici/tuketim_demirbas_page.dart';


class SmartCampusApp extends ConsumerWidget {
  const SmartCampusApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = _createRouter(ref);
    return MaterialApp.router(
      title: 'SmartCampus AI',
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: ThemeMode.system,
      debugShowCheckedModeBanner: false,
      routerConfig: router,
    );
  }

  GoRouter _createRouter(WidgetRef ref) {
    return GoRouter(
      initialLocation: '/splash',
      routes: [
        GoRoute(
          path: '/splash',
          builder: (_, __) => const _SplashPage(),
        ),
        GoRoute(
          path: '/login',
          builder: (_, __) => const LoginPage(),
        ),
        GoRoute(
          path: '/ogrenci',
          builder: (_, __) => const OgrenciHomePage(),
        ),
        GoRoute(
          path: '/mood',
          builder: (_, __) => const MoodCheckinPage(),
        ),
        GoRoute(
          path: '/notes',
          builder: (_, __) => const NotlarPage(),
        ),
        GoRoute(
          path: '/homework',
          builder: (_, __) => const OdevPage(),
        ),
        GoRoute(
          path: '/attendance',
          builder: (_, __) => const DevamsizlikPage(),
        ),
        GoRoute(
          path: '/messages',
          builder: (_, __) => const MesajPage(),
        ),
        GoRoute(
          path: '/ihbar',
          builder: (_, __) => const IhbarPage(),
        ),
        GoRoute(
          path: '/smarti',
          builder: (_, __) => const _PlaceholderPage(title: 'Smarti AI'),
        ),
        GoRoute(
          path: '/profile',
          builder: (_, __) => const _PlaceholderPage(title: 'Profilim'),
        ),
        // VELI rotaları
        GoRoute(path: '/veli', builder: (_, __) => const VeliHomePage()),
        GoRoute(path: '/veli/kapsul', builder: (_, __) => const KapsulPage()),
        GoRoute(path: '/veli/randevu', builder: (_, __) => const RandevuPage()),
        GoRoute(path: '/veli/belge', builder: (_, __) => const BelgePage()),
        GoRoute(path: '/veli/geri-bildirim', builder: (_, __) => const GeriBildirimPage()),
        GoRoute(
          path: '/veli/cocuk-detay',
          builder: (ctx, state) {
            final extra = state.extra as Map<String, dynamic>? ?? {};
            return CocukDetayPage(
              studentId: extra['studentId'] ?? '',
              studentName: extra['studentName'] ?? 'Öğrenci',
            );
          },
        ),
        // OGRETMEN rotaları
        GoRoute(path: '/ogretmen', builder: (_, __) => const OgretmenHomePage()),
        GoRoute(path: '/ogretmen/yoklama', builder: (_, __) => const YoklamaPage()),
        GoRoute(path: '/ogretmen/qr-yoklama', builder: (_, __) => const QRYoklamaPage()),
        GoRoute(path: '/ogretmen/not', builder: (_, __) => const NotGirisPage()),
        GoRoute(path: '/ogretmen/ders-defteri', builder: (_, __) => const DersDefteriPage()),
        GoRoute(path: '/ogretmen/odev-ata', builder: (_, __) => const OdevAtaPage()),
        GoRoute(path: '/ogretmen/sinav-sonuclari', builder: (_, __) => const SinavSonucPage()),
        // REHBER rotaları
        GoRoute(path: '/rehber', builder: (_, __) => const RehberHomePage()),
        GoRoute(path: '/rehber/vakalar', builder: (_, __) => const VakalarPage()),
        GoRoute(path: '/rehber/gorusme', builder: (_, __) => const GorusmePage()),
        GoRoute(path: '/rehber/aile-form', builder: (_, __) => const AileFormPage()),
        GoRoute(path: '/rehber/mood', builder: (_, __) => const MoodPanelPage()),
        GoRoute(path: '/rehber/ihbar', builder: (_, __) => const IhbarIncelemePage()),
        // YONETICI rotaları
        GoRoute(path: '/yonetici', builder: (_, __) => const YoneticiHomePage()),
        GoRoute(path: '/yonetici/erken-uyari', builder: (_, __) => const ErkenUyariPage()),
        GoRoute(path: '/yonetici/onaylar', builder: (_, __) => const OnaylarPage()),
        GoRoute(path: '/yonetici/bugun-okulda', builder: (_, __) => const BugunOkuldaPage()),
        GoRoute(path: '/yonetici/butce', builder: (_, __) => const ButcePage()),
        GoRoute(path: '/yonetici/randevular', builder: (_, __) => const YoneticiRandevularPage()),
        GoRoute(path: '/yonetici/gun-raporu', builder: (_, __) => const GunRaporuPage()),
        GoRoute(path: '/yonetici/kayit-ozet', builder: (_, __) => const KayitOzetPage()),
        GoRoute(path: '/yonetici/ders-programi', builder: (_, __) => const DersProgramiPage()),
        GoRoute(path: '/yonetici/nobet', builder: (_, __) => const NobetPage()),
        GoRoute(path: '/yonetici/zaman-cizelgesi', builder: (_, __) => const ZamanCizelgesiPage()),
        GoRoute(path: '/yonetici/calisanlar', builder: (_, __) => const CalisanlarPage()),
        GoRoute(path: '/yonetici/sinif-listeleri', builder: (_, __) => const SinifListeleriPage()),
        GoRoute(path: '/yonetici/tuketim-demirbas', builder: (_, __) => const TuketimDemirbasPage()),
        // Fallback
        GoRoute(path: '/home', builder: (_, __) => const _PlaceholderPage(title: 'Ana Sayfa')),
      ],
    );
  }
}


/// Splash — token kontrol + yönlendir.
class _SplashPage extends ConsumerStatefulWidget {
  const _SplashPage();

  @override
  ConsumerState<_SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends ConsumerState<_SplashPage> {
  @override
  void initState() {
    super.initState();
    _check();
  }

  Future<void> _check() async {
    await Future.delayed(const Duration(milliseconds: 600));
    final user = await ref.read(authServiceProvider).getCurrentUser();
    if (!mounted) return;
    if (user == null) {
      context.go('/login');
    } else if (user.isOgrenci) {
      context.go('/ogrenci');
    } else if (user.isVeli) {
      context.go('/veli');
    } else if (user.isOgretmen) {
      context.go('/ogretmen');
    } else if (user.isRehber) {
      context.go('/rehber');
    } else if (user.isYonetici) {
      context.go('/yonetici');
    } else {
      context.go('/home');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surfaceDarker,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 96,
              height: 96,
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [AppColors.primary, AppColors.gold]),
                borderRadius: BorderRadius.circular(24),
              ),
              child: const Icon(Icons.school_rounded, size: 56, color: Colors.white),
            ),
            const SizedBox(height: 24),
            const Text('SmartCampus AI',
                style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 24),
            const CircularProgressIndicator(color: AppColors.gold),
          ],
        ),
      ),
    );
  }
}


/// Geçici placeholder — modül daha yazılmamış.
class _PlaceholderPage extends StatelessWidget {
  final String title;
  const _PlaceholderPage({required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.construction, size: 64, color: AppColors.warning),
            SizedBox(height: 16),
            Text('Yakında aktif olacak', style: TextStyle(fontSize: 16)),
            SizedBox(height: 8),
            Text('Sprint takvimi için MIMARI.md\'ye bak',
                style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ],
        ),
      ),
    );
  }
}
