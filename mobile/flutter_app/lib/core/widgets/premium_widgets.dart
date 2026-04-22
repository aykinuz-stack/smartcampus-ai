import 'dart:ui';

import 'package:flutter/material.dart';

import '../theme/app_theme.dart';


/// SmartCampus AI — Ultra Premium Widget Kutuphanesi


// ═══════════════════════════════════════════════════════════
// GLASS CARD — Glassmorphism efektli kart
// ═══════════════════════════════════════════════════════════

class GlassCard extends StatelessWidget {
  final Widget child;
  final EdgeInsets? padding;
  final EdgeInsets? margin;
  final double borderRadius;
  final Color? color;
  final double blur;
  final VoidCallback? onTap;

  const GlassCard({
    super.key,
    required this.child,
    this.padding,
    this.margin,
    this.borderRadius = AppRadius.lg,
    this.color,
    this.blur = 12,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final bg = color ?? (isDark ? AppColors.glassWhite : Colors.white.withOpacity(0.7));
    final border = isDark ? AppColors.glassBorder : AppColors.borderLight.withOpacity(0.3);

    return Padding(
      padding: margin ?? EdgeInsets.zero,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(borderRadius),
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
          child: GestureDetector(
            onTap: onTap,
            child: Container(
              padding: padding ?? const EdgeInsets.all(AppSpacing.lg),
              decoration: BoxDecoration(
                color: bg,
                borderRadius: BorderRadius.circular(borderRadius),
                border: Border.all(color: border, width: 1),
                boxShadow: isDark ? AppShadows.none : AppShadows.soft,
              ),
              child: child,
            ),
          ),
        ),
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// GRADIENT BUTTON — Gradient arka planli buton
// ═══════════════════════════════════════════════════════════

class GradientButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool loading;
  final Gradient? gradient;
  final IconData? icon;
  final double? width;
  final double height;

  const GradientButton({
    super.key,
    required this.text,
    this.onPressed,
    this.loading = false,
    this.gradient,
    this.icon,
    this.width,
    this.height = 52,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width ?? double.infinity,
      height: height,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: onPressed != null ? (gradient ?? AppGradients.primary) : null,
          color: onPressed == null ? AppColors.textTertiaryLight : null,
          borderRadius: AppRadius.bMd,
          boxShadow: onPressed != null ? AppShadows.glow(AppColors.primary) : null,
        ),
        child: ElevatedButton(
          onPressed: loading ? null : onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            shape: RoundedRectangleBorder(borderRadius: AppRadius.bMd),
          ),
          child: loading
              ? const SizedBox(width: 22, height: 22,
                  child: CircularProgressIndicator(strokeWidth: 2.5, color: Colors.white))
              : Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    if (icon != null) ...[
                      Icon(icon, size: 20, color: Colors.white),
                      const SizedBox(width: 8),
                    ],
                    Text(text, style: const TextStyle(
                      fontSize: 15, fontWeight: FontWeight.w700,
                      letterSpacing: 0.5, color: Colors.white,
                    )),
                  ],
                ),
        ),
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// KPI CARD — Animasyonlu istatistik karti
// ═══════════════════════════════════════════════════════════

class KPICard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color color;
  final VoidCallback? onTap;
  final bool isEmoji;

  const KPICard({
    super.key,
    required this.icon,
    required this.label,
    required this.value,
    required this.color,
    this.onTap,
    this.isEmoji = false,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 10),
        decoration: BoxDecoration(
          color: isDark ? color.withOpacity(0.1) : color.withOpacity(0.06),
          borderRadius: AppRadius.bLg,
          border: Border.all(color: color.withOpacity(isDark ? 0.25 : 0.15)),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: color.withOpacity(0.12),
                shape: BoxShape.circle,
              ),
              child: isEmoji
                  ? Text(value, style: const TextStyle(fontSize: 18))
                  : Icon(icon, size: 18, color: color),
            ),
            const SizedBox(height: 8),
            if (!isEmoji)
              Text(value, style: TextStyle(
                fontSize: 20, fontWeight: FontWeight.w800, color: color,
              )),
            const SizedBox(height: 2),
            Text(label, style: TextStyle(
              fontSize: 10, fontWeight: FontWeight.w500,
              color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
            ), textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// SECTION HEADER — Bolum basligi
// ═══════════════════════════════════════════════════════════

class SectionHeader extends StatelessWidget {
  final String title;
  final String? trailing;
  final VoidCallback? onTrailingTap;
  final IconData? icon;

  const SectionHeader({
    super.key,
    required this.title,
    this.trailing,
    this.onTrailingTap,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          if (icon != null) ...[
            Icon(icon, size: 18, color: AppColors.primary),
            const SizedBox(width: 6),
          ],
          Text(title, style: const TextStyle(
            fontSize: 17, fontWeight: FontWeight.w700, letterSpacing: -0.3,
          )),
          const Spacer(),
          if (trailing != null)
            GestureDetector(
              onTap: onTrailingTap,
              child: Text(trailing!, style: TextStyle(
                fontSize: 13, fontWeight: FontWeight.w500,
                color: AppColors.primary,
              )),
            ),
        ],
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// FEATURE TILE — Premium ozellik karti
// ═══════════════════════════════════════════════════════════

class FeatureTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback? onTap;

  const FeatureTile({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.color,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: isDark ? AppColors.cardDark : AppColors.cardLight,
          borderRadius: AppRadius.bLg,
          border: Border.all(
            color: isDark
                ? color.withOpacity(0.15)
                : AppColors.borderLight.withOpacity(0.5),
          ),
          boxShadow: isDark ? AppShadows.none : AppShadows.soft,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [color.withOpacity(0.15), color.withOpacity(0.05)],
                ),
                borderRadius: AppRadius.bMd,
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            const Spacer(),
            Text(title, style: const TextStyle(
              fontSize: 13, fontWeight: FontWeight.w700,
            )),
            const SizedBox(height: 2),
            Text(subtitle, style: TextStyle(
              fontSize: 11,
              color: isDark ? AppColors.textTertiaryDark : AppColors.textSecondaryLight,
            )),
          ],
        ),
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// HERO BANNER — Gradient baslik karti
// ═══════════════════════════════════════════════════════════

class HeroBanner extends StatelessWidget {
  final String title;
  final String subtitle;
  final String? badge;
  final Gradient? gradient;
  final Widget? trailing;

  const HeroBanner({
    super.key,
    required this.title,
    required this.subtitle,
    this.badge,
    this.gradient,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: gradient ?? AppGradients.primary,
        borderRadius: AppRadius.bXl,
        boxShadow: AppShadows.glow(AppColors.primary),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.school_rounded, color: Colors.white, size: 24),
                    const SizedBox(width: 8),
                    const Text('SmartCampus AI', style: TextStyle(
                      color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w500,
                    )),
                    if (badge != null) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.15),
                          borderRadius: AppRadius.bFull,
                        ),
                        child: Text(badge!, style: const TextStyle(
                          color: Colors.white70, fontSize: 10,
                          fontWeight: FontWeight.w600, letterSpacing: 0.5,
                        )),
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: 12),
                Text(title, style: const TextStyle(
                  color: Colors.white, fontSize: 24, fontWeight: FontWeight.w800,
                  letterSpacing: -0.5,
                )),
                const SizedBox(height: 4),
                Text(subtitle, style: TextStyle(
                  color: Colors.white.withOpacity(0.7), fontSize: 13,
                )),
              ],
            ),
          ),
          if (trailing != null) trailing!,
        ],
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// STATUS BADGE — Durum etiketi
// ═══════════════════════════════════════════════════════════

class StatusBadge extends StatelessWidget {
  final String text;
  final Color color;
  final IconData? icon;

  const StatusBadge({
    super.key,
    required this.text,
    required this.color,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: AppRadius.bFull,
        border: Border.all(color: color.withOpacity(0.2)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(icon, size: 12, color: color),
            const SizedBox(width: 4),
          ],
          Text(text, style: TextStyle(
            color: color, fontSize: 11, fontWeight: FontWeight.w700,
          )),
        ],
      ),
    );
  }
}
