import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/premium_widgets.dart';

/// SmartCampus AI -- Ultra Premium Login Page
/// World-class dark glassmorphism design with animated logo and shimmer accents.

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage>
    with SingleTickerProviderStateMixin {
  final _usernameCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _tenantCtrl = TextEditingController(text: 'default');
  bool _loading = false;
  String? _error;
  bool _obscurePw = true;

  late final AnimationController _shimmerCtrl;

  @override
  void initState() {
    super.initState();
    _shimmerCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2400),
    )..repeat();

    // Set status bar to light icons on dark background
    SystemChrome.setSystemUIOverlayStyle(SystemUiOverlayStyle.light);
  }

  @override
  void dispose() {
    _usernameCtrl.dispose();
    _passwordCtrl.dispose();
    _tenantCtrl.dispose();
    _shimmerCtrl.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    final user = await ref.read(authServiceProvider).login(
          _usernameCtrl.text.trim(),
          _passwordCtrl.text,
          tenantId: _tenantCtrl.text.trim(),
        );
    setState(() => _loading = false);
    if (user != null) {
      if (user.isOgrenci) {
        if (mounted) context.go('/ogrenci');
      } else if (user.isVeli) {
        if (mounted) context.go('/veli');
      } else if (user.isOgretmen) {
        if (mounted) context.go('/ogretmen');
      } else if (user.isRehber) {
        if (mounted) context.go('/rehber');
      } else if (user.isYonetici) {
        if (mounted) context.go('/yonetici');
      } else {
        if (mounted) context.go('/home');
      }
    } else {
      setState(() => _error = 'Giris basarisiz. Kontrol et:\n'
          '- Kullanici adi ve sifre dogru mu?\n'
          '- Backend calisiyor mu?\n'
          '- Ayni Wi-Fi aginda misin?');
    }
  }

  InputDecoration _premiumInputDecoration({
    required String label,
    required IconData prefixIcon,
    Widget? suffixIcon,
  }) {
    return InputDecoration(
      labelText: label,
      labelStyle: TextStyle(
        color: AppColors.textSecondaryDark.withOpacity(0.8),
        fontSize: 14,
        fontWeight: FontWeight.w500,
      ),
      prefixIcon: ShaderMask(
        shaderCallback: (bounds) => const LinearGradient(
          colors: [AppColors.primaryLight, AppColors.gold],
        ).createShader(bounds),
        child: Icon(prefixIcon, size: 22, color: Colors.white),
      ),
      suffixIcon: suffixIcon,
      filled: true,
      fillColor: AppColors.surfaceDarker.withOpacity(0.6),
      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 18),
      border: OutlineInputBorder(
        borderRadius: AppRadius.bLg,
        borderSide: BorderSide(color: AppColors.glassBorder),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: AppRadius.bLg,
        borderSide: BorderSide(color: AppColors.glassBorder),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: AppRadius.bLg,
        borderSide: const BorderSide(color: AppColors.primaryLight, width: 2),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: AppRadius.bLg,
        borderSide: const BorderSide(color: AppColors.danger, width: 1.5),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenH = MediaQuery.of(context).size.height;
    final isCompact = screenH < 700;

    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(gradient: AppGradients.dark),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              physics: const BouncingScrollPhysics(),
              padding: EdgeInsets.symmetric(
                horizontal: 28,
                vertical: isCompact ? 16 : 32,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // ---- Animated Logo ----
                  TweenAnimationBuilder<double>(
                    tween: Tween(begin: 0.0, end: 1.0),
                    duration: const Duration(milliseconds: 900),
                    curve: Curves.elasticOut,
                    builder: (_, scale, child) =>
                        Transform.scale(scale: scale, child: child),
                    child: TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0.0, end: 1.0),
                      duration: const Duration(milliseconds: 700),
                      builder: (_, opacity, child) =>
                          Opacity(opacity: opacity, child: child),
                      child: Container(
                        width: 100,
                        height: 100,
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: [AppColors.primary, AppColors.gold],
                          ),
                          borderRadius: BorderRadius.circular(28),
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.primary.withOpacity(0.45),
                              blurRadius: 36,
                              spreadRadius: 4,
                            ),
                            BoxShadow(
                              color: AppColors.gold.withOpacity(0.2),
                              blurRadius: 48,
                              spreadRadius: 2,
                              offset: const Offset(0, 12),
                            ),
                          ],
                        ),
                        child: const Icon(
                          Icons.school_rounded,
                          size: 54,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),

                  SizedBox(height: isCompact ? 20 : 28),

                  // ---- Title ----
                  TweenAnimationBuilder<double>(
                    tween: Tween(begin: 0.0, end: 1.0),
                    duration: const Duration(milliseconds: 800),
                    curve: Curves.easeOut,
                    builder: (_, opacity, child) => Opacity(
                      opacity: opacity,
                      child: Transform.translate(
                        offset: Offset(0, (1 - opacity) * 16),
                        child: child,
                      ),
                    ),
                    child: Column(
                      children: [
                        const Text(
                          'SmartCampus AI',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 30,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 1.5,
                          ),
                        ),
                        const SizedBox(height: 8),
                        // Shimmer gold accent text
                        AnimatedBuilder(
                          animation: _shimmerCtrl,
                          builder: (context, child) {
                            return ShaderMask(
                              shaderCallback: (bounds) {
                                final dx =
                                    _shimmerCtrl.value * bounds.width * 3 -
                                        bounds.width;
                                return LinearGradient(
                                  begin: Alignment.centerLeft,
                                  end: Alignment.centerRight,
                                  colors: const [
                                    AppColors.goldDark,
                                    AppColors.goldLight,
                                    Colors.white,
                                    AppColors.goldLight,
                                    AppColors.goldDark,
                                  ],
                                  stops: const [0.0, 0.35, 0.5, 0.65, 1.0],
                                  transform: _SlideGradient(dx),
                                ).createShader(bounds);
                              },
                              child: const Text(
                                'Egitimin Gelecegi Burada',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 14,
                                  fontWeight: FontWeight.w500,
                                  fontStyle: FontStyle.italic,
                                  letterSpacing: 0.8,
                                ),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  ),

                  SizedBox(height: isCompact ? 28 : 40),

                  // ---- Login Form inside GlassCard ----
                  TweenAnimationBuilder<double>(
                    tween: Tween(begin: 0.0, end: 1.0),
                    duration: const Duration(milliseconds: 900),
                    curve: Curves.easeOutCubic,
                    builder: (_, value, child) => Opacity(
                      opacity: value,
                      child: Transform.translate(
                        offset: Offset(0, (1 - value) * 40),
                        child: child,
                      ),
                    ),
                    child: GlassCard(
                      padding: const EdgeInsets.all(24),
                      borderRadius: AppRadius.xl,
                      blur: 18,
                      color: AppColors.glassWhiteStrong,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // Username
                          TextField(
                            controller: _usernameCtrl,
                            style: const TextStyle(
                              color: AppColors.textPrimaryDark,
                              fontSize: 15,
                              fontWeight: FontWeight.w500,
                            ),
                            textInputAction: TextInputAction.next,
                            decoration: _premiumInputDecoration(
                              label: 'Kullanici Adi',
                              prefixIcon: Icons.person_outline,
                            ),
                          ),

                          const SizedBox(height: 18),

                          // Password
                          TextField(
                            controller: _passwordCtrl,
                            obscureText: _obscurePw,
                            style: const TextStyle(
                              color: AppColors.textPrimaryDark,
                              fontSize: 15,
                              fontWeight: FontWeight.w500,
                            ),
                            textInputAction: TextInputAction.done,
                            onSubmitted: (_) => _handleLogin(),
                            decoration: _premiumInputDecoration(
                              label: 'Sifre',
                              prefixIcon: Icons.lock_outline,
                              suffixIcon: IconButton(
                                icon: Icon(
                                  _obscurePw
                                      ? Icons.visibility_outlined
                                      : Icons.visibility_off_outlined,
                                  color: AppColors.textSecondaryDark,
                                  size: 22,
                                ),
                                onPressed: () =>
                                    setState(() => _obscurePw = !_obscurePw),
                              ),
                            ),
                          ),

                          const SizedBox(height: 10),

                          // Tenant (optional, collapsible)
                          Theme(
                            data: Theme.of(context).copyWith(
                              dividerColor: Colors.transparent,
                            ),
                            child: ExpansionTile(
                              title: Row(
                                children: [
                                  Icon(Icons.business_outlined,
                                      size: 16,
                                      color: AppColors.textTertiaryDark),
                                  const SizedBox(width: 8),
                                  Text(
                                    'Kurum Kodu (opsiyonel)',
                                    style: TextStyle(
                                      fontSize: 13,
                                      color: AppColors.textSecondaryDark,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ],
                              ),
                              tilePadding: EdgeInsets.zero,
                              childrenPadding:
                                  const EdgeInsets.only(bottom: 4, top: 4),
                              iconColor: AppColors.textTertiaryDark,
                              collapsedIconColor: AppColors.textTertiaryDark,
                              children: [
                                TextField(
                                  controller: _tenantCtrl,
                                  style: const TextStyle(
                                    color: AppColors.textPrimaryDark,
                                    fontSize: 14,
                                  ),
                                  decoration: _premiumInputDecoration(
                                    label: 'Kurum ID',
                                    prefixIcon: Icons.domain,
                                  ),
                                ),
                              ],
                            ),
                          ),

                          // Error message
                          if (_error != null) ...[
                            const SizedBox(height: 14),
                            Container(
                              padding: const EdgeInsets.all(14),
                              decoration: BoxDecoration(
                                color: AppColors.danger.withOpacity(0.12),
                                borderRadius: AppRadius.bMd,
                                border: Border.all(
                                  color: AppColors.danger.withOpacity(0.35),
                                  width: 1,
                                ),
                              ),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Container(
                                    padding: const EdgeInsets.all(4),
                                    decoration: BoxDecoration(
                                      color: AppColors.danger.withOpacity(0.15),
                                      shape: BoxShape.circle,
                                    ),
                                    child: const Icon(
                                      Icons.error_outline_rounded,
                                      color: AppColors.danger,
                                      size: 18,
                                    ),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Text(
                                      _error!,
                                      style: const TextStyle(
                                        color: AppColors.danger,
                                        fontSize: 13,
                                        height: 1.5,
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],

                          const SizedBox(height: 22),

                          // Login Button
                          GradientButton(
                            text: 'GIRIS YAP',
                            icon: Icons.login_rounded,
                            loading: _loading,
                            onPressed: _loading ? null : _handleLogin,
                            gradient: const LinearGradient(
                              begin: Alignment.centerLeft,
                              end: Alignment.centerRight,
                              colors: [
                                AppColors.primary,
                                AppColors.primaryDark,
                                Color(0xFF7C3AED),
                              ],
                            ),
                            height: 54,
                          ),
                        ],
                      ),
                    ),
                  ),

                  SizedBox(height: isCompact ? 20 : 36),

                  // ---- Version text ----
                  TweenAnimationBuilder<double>(
                    tween: Tween(begin: 0.0, end: 1.0),
                    duration: const Duration(milliseconds: 1200),
                    builder: (_, opacity, child) =>
                        Opacity(opacity: opacity * 0.45, child: child),
                    child: const Text(
                      'SmartCampus AI v25 | Premium Edition',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 11,
                        letterSpacing: 0.5,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

/// Gradient transform helper for the shimmer effect.
class _SlideGradient extends GradientTransform {
  final double offset;
  const _SlideGradient(this.offset);

  @override
  Matrix4? transform(Rect bounds, {TextDirection? textDirection}) {
    return Matrix4.translationValues(offset, 0, 0);
  }
}
