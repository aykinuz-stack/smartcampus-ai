import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'core/auth/auth_service.dart';
import 'core/theme/app_theme.dart';
import 'core/theme/theme_provider.dart';
import 'features/auth/login_page.dart';
import 'features/ogrenci/mood_checkin_page.dart';
import 'features/ogrenci/ogrenci_home.dart';
import 'features/ogrenci/notlar_page.dart';
import 'features/ogrenci/devamsizlik_page.dart';
import 'features/ogrenci/odev_page.dart';
import 'features/ogrenci/mesaj_page.dart';
import 'features/ogrenci/ihbar_page.dart';
import 'features/ogrenci/dil_gelisimi_page.dart';
import 'features/ogrenci/smarti_chat_page.dart';
import 'features/ogrenci/akademik_takvim_page.dart';
import 'features/ogrenci/duyuru_yemek_page.dart';
import 'features/ogrenci/ai_treni_page.dart';
import 'features/ogrenci/online_sinav_page.dart';
import 'features/ogrenci/kocluk_page.dart';
import 'features/ogrenci/dijital_kutuphane_page.dart';
import 'features/shared/bilgi_yarismasi_koleksiyon_page.dart';
import 'features/shared/matematik_koyu_page.dart';
import 'features/shared/gunluk_isler_page.dart';
import 'features/shared/bildirim_page.dart';
import 'features/ogrenci/gunun_bilgisi_page.dart';
import 'features/ogrenci/zeka_oyunlari_page.dart';
import 'features/ogrenci/kdg_premium_page.dart';
import 'features/ogrenci/sinav_sonuclari_page.dart';
import 'features/ogrenci/kazanim_borclari_page.dart';
import 'features/ogrenci/telafi_page.dart';
import 'features/ogrenci/defterim_page.dart';
import 'features/ogrenci/sanat_sokagi_page.dart';
import 'features/ogrenci/bilisim_vadisi_page.dart';
import 'features/shared/profil_page.dart';
import 'features/veli/veli_home.dart';
import 'features/veli/kapsul_page.dart';
import 'features/veli/randevu_page.dart';
import 'features/veli/belge_page.dart';
import 'features/veli/geri_bildirim_page.dart';
import 'features/veli/servis_takip_page.dart';
import 'features/veli/gunluk_bulten_page.dart';
import 'features/veli/basari_duvari_page.dart';
import 'features/veli/yemek_menusu_page.dart';
import 'features/veli/anket_page.dart';
import 'features/veli/saglik_rehberlik_page.dart';
import 'features/veli/veli_egitim_page.dart';
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
import 'features/rehber/risk_degerlendirme_page.dart';
import 'features/rehber/gelisim_dosyasi_page.dart';
import 'features/rehber/yonlendirme_page.dart';
import 'features/rehber/kriz_mudahale_page.dart';
import 'features/rehber/kariyer_rehberligi_page.dart';
import 'features/rehber/sosyo_duygusal_page.dart';
import 'features/rehber/bep_page.dart';
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
import 'features/yonetici/destek_hizmetleri_page.dart';
import 'features/yonetici/revir_page.dart';
import 'features/yonetici/kutuphane_page.dart';
import 'features/yonetici/sosyal_etkinlik_page.dart';
import 'features/yonetici/veli_talepleri_page.dart';
import 'features/yonetici/servis_hizmetleri_page.dart';
import 'features/yonetici/toplanti_kurullar_page.dart';


class SmartCampusApp extends ConsumerWidget {
  const SmartCampusApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    final router = _createRouter(ref);
    return MaterialApp.router(
      title: 'SmartCampus AI',
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: themeMode,
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
        // ORTAK
        GoRoute(path: '/bildirimler', builder: (_, __) => const BildirimPage()),
        GoRoute(path: '/ayarlar', builder: (_, __) => const _AyarlarPage()),
        // OGRENCI
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
        GoRoute(path: '/ogrenci/sinav-sonuclari', builder: (_, __) => const SinavSonuclariPage()),
        GoRoute(path: '/ogrenci/kazanim-borclari', builder: (_, __) => const KazanimBorclariPage()),
        GoRoute(path: '/ogrenci/telafi', builder: (_, __) => const TelafiPage()),
        GoRoute(path: '/ogrenci/defterim', builder: (_, __) => const DefterimPage()),
        GoRoute(path: '/ogrenci/sanat-sokagi', builder: (_, __) => const SanatSokagiPage()),
        GoRoute(path: '/ogrenci/bilisim-vadisi', builder: (_, __) => const BilisimVadisiPage()),
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
          builder: (_, __) => const SmartiChatPage(),
        ),
        GoRoute(path: '/dil-gelisimi', builder: (_, __) => const DilGelisimiPage()),
        GoRoute(path: '/takvim', builder: (_, __) => const AkademikTakvimPage()),
        GoRoute(path: '/duyuru-yemek', builder: (_, __) => const DuyuruYemekPage()),
        GoRoute(path: '/ai-treni', builder: (_, __) => const AiTreniPage()),
        GoRoute(path: '/online-sinav', builder: (_, __) => const OnlineSinavPage()),
        GoRoute(path: '/kocluk', builder: (_, __) => const KoclukPage()),
        GoRoute(path: '/dijital-kutuphane', builder: (_, __) => const DijitalKutuphanePage()),
        GoRoute(path: '/bilgi-yarismasi-koleksiyon', builder: (_, __) => const BilgiYarismasiKoleksiyonPage()),
        GoRoute(path: '/matematik-koyu', builder: (_, __) => const MatematikKoyuPage()),
        GoRoute(path: '/gunluk-isler', builder: (_, __) => const GunlukIslerPage()),
        GoRoute(path: '/gunun-bilgisi', builder: (_, __) => const GununBilgisiPage()),
        GoRoute(path: '/zeka-oyunlari', builder: (_, __) => const ZekaOyunlariPage()),
        GoRoute(path: '/kdg-premium', builder: (_, __) => const KdgPremiumPage()),
        GoRoute(
          path: '/profile',
          builder: (_, __) => const ProfilPage(),
        ),
        // VELI rotaları
        GoRoute(path: '/veli', builder: (_, __) => const VeliHomePage()),
        GoRoute(path: '/veli/kapsul', builder: (_, __) => const KapsulPage()),
        GoRoute(path: '/veli/randevu', builder: (_, __) => const RandevuPage()),
        GoRoute(path: '/veli/belge', builder: (_, __) => const BelgePage()),
        GoRoute(path: '/veli/geri-bildirim', builder: (_, __) => const GeriBildirimPage()),
        GoRoute(path: '/veli/servis', builder: (_, __) => const ServisTakipPage()),
        GoRoute(path: '/veli/yemek-menusu', builder: (_, __) => const YemekMenusuPage()),
        GoRoute(path: '/veli/anket', builder: (_, __) => const AnketPage()),
        GoRoute(path: '/veli/basari-duvari', builder: (_, __) => const BasariDuvariPage()),
        GoRoute(path: '/veli/saglik-rehberlik', builder: (_, __) => const SaglikRehberlikPage()),
        GoRoute(path: '/veli/veli-egitim', builder: (_, __) => const VeliEgitimPage()),
        GoRoute(path: '/veli/bulten', builder: (_, __) => const GunlukBultenPage()),
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
        GoRoute(path: '/rehber/yonlendirme', builder: (_, __) => const YonlendirmePage()),
        GoRoute(path: '/rehber/kriz', builder: (_, __) => const KrizMudahalePage()),
        GoRoute(path: '/rehber/risk', builder: (_, __) => const RiskDegerlendirmePage()),
        GoRoute(path: '/rehber/gelisim-dosyasi', builder: (_, __) => const GelisimDosyasiPage()),
        GoRoute(path: '/rehber/kariyer', builder: (_, __) => const KariyerRehberligiPage()),
        GoRoute(path: '/rehber/sosyo-duygusal', builder: (_, __) => const SosyoDuygusalPage()),
        GoRoute(path: '/rehber/bep', builder: (_, __) => const BepPage()),
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
        GoRoute(path: '/yonetici/destek-hizmetleri', builder: (_, __) => const DestekHizmetleriPage()),
        GoRoute(path: '/yonetici/revir', builder: (_, __) => const RevirPage()),
        GoRoute(path: '/yonetici/kutuphane', builder: (_, __) => const KutuphanePage()),
        GoRoute(path: '/yonetici/sosyal-etkinlik', builder: (_, __) => const SosyalEtkinlikPage()),
        GoRoute(path: '/yonetici/toplanti-kurullar', builder: (_, __) => const ToplantiKurullarPage()),
        GoRoute(path: '/yonetici/servis-hizmetleri', builder: (_, __) => const ServisHizmetleriPage()),
        GoRoute(path: '/yonetici/veli-talepleri', builder: (_, __) => const VeliTalepleriPage()),
        // Fallback
        GoRoute(path: '/home', builder: (_, __) => const _PlaceholderPage(title: 'Ana Sayfa')),
      ],
    );
  }
}


/// Splash -- Ultra Premium token kontrol + yonlendir.
class _SplashPage extends ConsumerStatefulWidget {
  const _SplashPage();

  @override
  ConsumerState<_SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends ConsumerState<_SplashPage>
    with TickerProviderStateMixin {
  late final AnimationController _logoCtrl;
  late final Animation<double> _logoScale;
  late final AnimationController _fadeCtrl;
  late final Animation<double> _fadeAnim;
  late final AnimationController _pulseCtrl;
  late final Animation<double> _pulseAnim;

  @override
  void initState() {
    super.initState();

    // Logo elastic animation
    _logoCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    );
    _logoScale = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _logoCtrl, curve: Curves.elasticOut),
    );

    // Fade-in for text
    _fadeCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _fadeAnim = CurvedAnimation(parent: _fadeCtrl, curve: Curves.easeOut);

    // Pulsing loader
    _pulseCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
    _pulseAnim = Tween<double>(begin: 0.6, end: 1.0).animate(
      CurvedAnimation(parent: _pulseCtrl, curve: Curves.easeInOut),
    );

    // Start animations in sequence
    _logoCtrl.forward();
    Future.delayed(const Duration(milliseconds: 400), () {
      if (mounted) _fadeCtrl.forward();
    });

    _check();
  }

  @override
  void dispose() {
    _logoCtrl.dispose();
    _fadeCtrl.dispose();
    _pulseCtrl.dispose();
    super.dispose();
  }

  Future<void> _check() async {
    await Future.delayed(const Duration(milliseconds: 1800));
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
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              AppColors.surfaceDarker,
              Color(0xFF1E1B4B),
              AppColors.surfaceDark,
            ],
            stops: [0.0, 0.5, 1.0],
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(flex: 3),

              // ---- Animated Logo ----
              ScaleTransition(
                scale: _logoScale,
                child: Container(
                  width: 120,
                  height: 120,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                      colors: [AppColors.primary, Color(0xFF8B5CF6), AppColors.gold],
                      stops: [0.0, 0.5, 1.0],
                    ),
                    borderRadius: BorderRadius.circular(32),
                    boxShadow: [
                      BoxShadow(
                        color: AppColors.primary.withOpacity(0.5),
                        blurRadius: 40,
                        spreadRadius: 4,
                      ),
                      BoxShadow(
                        color: AppColors.gold.withOpacity(0.25),
                        blurRadius: 60,
                        spreadRadius: 2,
                        offset: const Offset(0, 16),
                      ),
                    ],
                  ),
                  child: const Icon(
                    Icons.school_rounded,
                    size: 64,
                    color: Colors.white,
                  ),
                ),
              ),

              const SizedBox(height: 36),

              // ---- Title with fade-in ----
              FadeTransition(
                opacity: _fadeAnim,
                child: Column(
                  children: [
                    const Text(
                      'SmartCampus AI',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 1.5,
                      ),
                    ),
                    const SizedBox(height: 10),
                    const Text(
                      'Egitimin Gelecegi',
                      style: TextStyle(
                        color: AppColors.gold,
                        fontSize: 14,
                        fontStyle: FontStyle.italic,
                        fontWeight: FontWeight.w500,
                        letterSpacing: 0.8,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 48),

              // ---- Pulsing loading indicator ----
              FadeTransition(
                opacity: _pulseAnim,
                child: const SizedBox(
                  width: 30,
                  height: 30,
                  child: CircularProgressIndicator(
                    strokeWidth: 2.0,
                    color: AppColors.gold,
                  ),
                ),
              ),

              const SizedBox(height: 14),

              FadeTransition(
                opacity: _fadeAnim,
                child: Text(
                  'Yukleniyor...',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.4),
                    fontSize: 12,
                    letterSpacing: 0.5,
                  ),
                ),
              ),

              const Spacer(flex: 2),

              // ---- Version text at bottom ----
              Padding(
                padding: const EdgeInsets.only(bottom: 40),
                child: Text(
                  'v25',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.25),
                    fontSize: 11,
                    letterSpacing: 1.0,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}


/// Ayarlar Sayfası — tema toggle + profil
class _AyarlarPage extends ConsumerWidget {
  const _AyarlarPage();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);

    String temaAdi;
    IconData temaIcon;
    switch (themeMode) {
      case ThemeMode.light:
        temaAdi = 'Aydınlık';
        temaIcon = Icons.light_mode;
        break;
      case ThemeMode.dark:
        temaAdi = 'Karanlık';
        temaIcon = Icons.dark_mode;
        break;
      case ThemeMode.system:
        temaAdi = 'Sistem';
        temaIcon = Icons.brightness_auto;
        break;
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Ayarlar')),
      body: ListView(
        children: [
          // Tema
          ListTile(
            leading: Icon(temaIcon, color: AppColors.primary),
            title: const Text('Tema'),
            subtitle: Text(temaAdi),
            trailing: SegmentedButton<ThemeMode>(
              segments: const [
                ButtonSegment(value: ThemeMode.light,
                    icon: Icon(Icons.light_mode, size: 18)),
                ButtonSegment(value: ThemeMode.system,
                    icon: Icon(Icons.brightness_auto, size: 18)),
                ButtonSegment(value: ThemeMode.dark,
                    icon: Icon(Icons.dark_mode, size: 18)),
              ],
              selected: {themeMode},
              onSelectionChanged: (s) =>
                  ref.read(themeModeProvider.notifier).setTheme(s.first),
            ),
          ),
          const Divider(),
          // Bildirimler
          ListTile(
            leading: const Icon(Icons.notifications, color: AppColors.gold),
            title: const Text('Bildirimler'),
            subtitle: const Text('Push bildirim ayarları'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {},
          ),
          const Divider(),
          // Uygulama hakkında
          ListTile(
            leading: const Icon(Icons.info_outline, color: AppColors.info),
            title: const Text('Hakkında'),
            subtitle: const Text('SmartCampus AI v22'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              showAboutDialog(
                context: context,
                applicationName: 'SmartCampus AI',
                applicationVersion: 'v22',
                applicationLegalese: '2026 SmartCampus',
                applicationIcon: Container(
                  width: 48, height: 48,
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primary, AppColors.gold]),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(Icons.school, color: Colors.white, size: 28),
                ),
              );
            },
          ),
          const Divider(),
          // Cikis
          ListTile(
            leading: const Icon(Icons.logout, color: AppColors.danger),
            title: const Text('Çıkış Yap'),
            onTap: () async {
              await ref.read(authServiceProvider).logout();
              if (context.mounted) {
                GoRouter.of(context).go('/login');
              }
            },
          ),
        ],
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
            Text('Sprint takvimi icin MIMARI.md\'ye bak',
                style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ],
        ),
      ),
    );
  }
}
