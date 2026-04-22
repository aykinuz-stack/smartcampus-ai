import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:google_fonts/google_fonts.dart';

/// SmartCampus AI — Ultra Premium Design System
/// Dunya standartlarinda enterprise-grade tasarim dili.

// ═══════════════════════════════════════════════════════════
// RENKLER
// ═══════════════════════════════════════════════════════════

class AppColors {
  // Brand — Indigo/Violet gradient
  static const primary = Color(0xFF6366F1);       // Indigo 500
  static const primaryDark = Color(0xFF4338CA);    // Indigo 700
  static const primaryLight = Color(0xFF818CF8);   // Indigo 400
  static const primarySurface = Color(0xFFEEF2FF); // Indigo 50

  // Accent — Amber Gold
  static const gold = Color(0xFFF59E0B);           // Amber 500
  static const goldLight = Color(0xFFFBBF24);      // Amber 400
  static const goldDark = Color(0xFFD97706);       // Amber 600

  // Semantic
  static const success = Color(0xFF10B981);        // Emerald 500
  static const successLight = Color(0xFFD1FAE5);
  static const warning = Color(0xFFF59E0B);        // Amber 500
  static const warningLight = Color(0xFFFEF3C7);
  static const danger = Color(0xFFEF4444);         // Red 500
  static const dangerLight = Color(0xFFFEE2E2);
  static const info = Color(0xFF3B82F6);           // Blue 500
  static const infoLight = Color(0xFFDBEAFE);

  // Surface — Light
  static const surfaceLight = Color(0xFFF8FAFC);   // Slate 50
  static const cardLight = Color(0xFFFFFFFF);
  static const borderLight = Color(0xFFE2E8F0);    // Slate 200

  // Surface — Dark
  static const surfaceDark = Color(0xFF0F172A);    // Slate 900
  static const surfaceDarker = Color(0xFF020617);  // Slate 950
  static const cardDark = Color(0xFF1E293B);       // Slate 800
  static const cardDarkElevated = Color(0xFF334155); // Slate 700
  static const borderDark = Color(0xFF334155);     // Slate 700

  // Text — Light theme
  static const textPrimaryLight = Color(0xFF0F172A);   // Slate 900
  static const textSecondaryLight = Color(0xFF64748B); // Slate 500
  static const textTertiaryLight = Color(0xFF94A3B8);  // Slate 400

  // Text — Dark theme
  static const textPrimaryDark = Color(0xFFF1F5F9);   // Slate 100
  static const textSecondaryDark = Color(0xFF94A3B8);  // Slate 400
  static const textTertiaryDark = Color(0xFF64748B);   // Slate 500

  // Mood 5-level
  static const mood1 = Color(0xFFEF4444);
  static const mood2 = Color(0xFFF97316);
  static const mood3 = Color(0xFFF59E0B);
  static const mood4 = Color(0xFF22C55E);
  static const mood5 = Color(0xFF10B981);

  // Glassmorphism
  static Color glassWhite = Colors.white.withOpacity(0.08);
  static Color glassBorder = Colors.white.withOpacity(0.12);
  static Color glassWhiteStrong = Colors.white.withOpacity(0.15);
}


// ═══════════════════════════════════════════════════════════
// GRADYANLAR
// ═══════════════════════════════════════════════════════════

class AppGradients {
  static const primary = LinearGradient(
    begin: Alignment.topLeft, end: Alignment.bottomRight,
    colors: [Color(0xFF6366F1), Color(0xFF8B5CF6)],
  );

  static const primaryDark = LinearGradient(
    begin: Alignment.topLeft, end: Alignment.bottomRight,
    colors: [Color(0xFF4338CA), Color(0xFF6366F1)],
  );

  static const gold = LinearGradient(
    begin: Alignment.topLeft, end: Alignment.bottomRight,
    colors: [Color(0xFFF59E0B), Color(0xFFF97316)],
  );

  static const dark = LinearGradient(
    begin: Alignment.topCenter, end: Alignment.bottomCenter,
    colors: [Color(0xFF0F172A), Color(0xFF1E1B4B), Color(0xFF0F172A)],
  );

  static const darkCard = LinearGradient(
    begin: Alignment.topLeft, end: Alignment.bottomRight,
    colors: [Color(0xFF1E293B), Color(0xFF0F172A)],
  );

  static const success = LinearGradient(
    colors: [Color(0xFF10B981), Color(0xFF059669)],
  );

  static const danger = LinearGradient(
    colors: [Color(0xFFEF4444), Color(0xFFDC2626)],
  );

  static const shimmer = LinearGradient(
    colors: [Color(0x00FFFFFF), Color(0x33FFFFFF), Color(0x00FFFFFF)],
  );
}


// ═══════════════════════════════════════════════════════════
// GOLGE
// ═══════════════════════════════════════════════════════════

class AppShadows {
  static List<BoxShadow> soft = [
    BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2)),
    BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 24, offset: const Offset(0, 8)),
  ];

  static List<BoxShadow> medium = [
    BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 12, offset: const Offset(0, 4)),
    BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 32, offset: const Offset(0, 12)),
  ];

  static List<BoxShadow> strong = [
    BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 20, offset: const Offset(0, 8)),
    BoxShadow(color: Colors.black.withOpacity(0.06), blurRadius: 48, offset: const Offset(0, 20)),
  ];

  static List<BoxShadow> glow(Color color) => [
    BoxShadow(color: color.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 8)),
    BoxShadow(color: color.withOpacity(0.1), blurRadius: 40, spreadRadius: 2),
  ];

  static List<BoxShadow> none = [];
}


// ═══════════════════════════════════════════════════════════
// RADIUS
// ═══════════════════════════════════════════════════════════

class AppRadius {
  static const xs = 6.0;
  static const sm = 8.0;
  static const md = 12.0;
  static const lg = 16.0;
  static const xl = 20.0;
  static const xxl = 28.0;
  static const full = 999.0;

  static final bXs = BorderRadius.circular(xs);
  static final bSm = BorderRadius.circular(sm);
  static final bMd = BorderRadius.circular(md);
  static final bLg = BorderRadius.circular(lg);
  static final bXl = BorderRadius.circular(xl);
  static final bXxl = BorderRadius.circular(xxl);
  static final bFull = BorderRadius.circular(full);
}


// ═══════════════════════════════════════════════════════════
// SPACING
// ═══════════════════════════════════════════════════════════

class AppSpacing {
  static const xs = 4.0;
  static const sm = 8.0;
  static const md = 12.0;
  static const lg = 16.0;
  static const xl = 20.0;
  static const xxl = 24.0;
  static const xxxl = 32.0;
}


// ═══════════════════════════════════════════════════════════
// TEMA
// ═══════════════════════════════════════════════════════════

class AppTheme {
  static ThemeData light() {
    final base = ThemeData.light(useMaterial3: true);
    return base.copyWith(
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.surfaceLight,
      textTheme: GoogleFonts.interTextTheme(base.textTheme).apply(
        bodyColor: AppColors.textPrimaryLight,
        displayColor: AppColors.textPrimaryLight,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.surfaceLight,
        foregroundColor: AppColors.textPrimaryLight,
        elevation: 0,
        scrolledUnderElevation: 0.5,
        centerTitle: false,
        systemOverlayStyle: SystemUiOverlayStyle.dark,
        titleTextStyle: GoogleFonts.inter(
          color: AppColors.textPrimaryLight,
          fontSize: 18,
          fontWeight: FontWeight.w700,
        ),
      ),
      cardTheme: CardTheme(
        color: AppColors.cardLight,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: AppRadius.bLg,
          side: BorderSide(color: AppColors.borderLight.withOpacity(0.5)),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: AppRadius.bMd),
          textStyle: GoogleFonts.inter(fontSize: 15, fontWeight: FontWeight.w600),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.surfaceLight,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: BorderSide(color: AppColors.borderLight),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: BorderSide(color: AppColors.borderLight),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: const BorderSide(color: AppColors.primary, width: 2),
        ),
      ),
      dividerTheme: DividerThemeData(color: AppColors.borderLight.withOpacity(0.5)),
      colorScheme: base.colorScheme.copyWith(
        primary: AppColors.primary,
        secondary: AppColors.gold,
        error: AppColors.danger,
        surface: AppColors.surfaceLight,
      ),
      tabBarTheme: TabBarTheme(
        labelColor: AppColors.primary,
        unselectedLabelColor: AppColors.textSecondaryLight,
        indicatorColor: AppColors.primary,
        labelStyle: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 14),
      ),
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: AppColors.cardLight,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.textTertiaryLight,
        elevation: 8,
        type: BottomNavigationBarType.fixed,
        selectedLabelStyle: GoogleFonts.inter(fontSize: 11, fontWeight: FontWeight.w600),
        unselectedLabelStyle: GoogleFonts.inter(fontSize: 11),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: AppColors.primarySurface,
        selectedColor: AppColors.primary,
        labelStyle: GoogleFonts.inter(fontSize: 12),
        shape: RoundedRectangleBorder(borderRadius: AppRadius.bFull),
        side: BorderSide.none,
      ),
    );
  }

  static ThemeData dark() {
    final base = ThemeData.dark(useMaterial3: true);
    return base.copyWith(
      primaryColor: AppColors.primary,
      scaffoldBackgroundColor: AppColors.surfaceDark,
      textTheme: GoogleFonts.interTextTheme(base.textTheme).apply(
        bodyColor: AppColors.textPrimaryDark,
        displayColor: AppColors.textPrimaryDark,
      ),
      appBarTheme: AppBarTheme(
        backgroundColor: AppColors.surfaceDark,
        foregroundColor: AppColors.textPrimaryDark,
        elevation: 0,
        scrolledUnderElevation: 0.5,
        centerTitle: false,
        systemOverlayStyle: SystemUiOverlayStyle.light,
        titleTextStyle: GoogleFonts.inter(
          color: AppColors.textPrimaryDark,
          fontSize: 18,
          fontWeight: FontWeight.w700,
        ),
      ),
      cardTheme: CardTheme(
        color: AppColors.cardDark,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: AppRadius.bLg,
          side: BorderSide(color: AppColors.borderDark.withOpacity(0.3)),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: AppRadius.bMd),
          textStyle: GoogleFonts.inter(fontSize: 15, fontWeight: FontWeight.w600),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: AppColors.cardDark,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: BorderSide(color: AppColors.borderDark),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: BorderSide(color: AppColors.borderDark),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: AppRadius.bMd,
          borderSide: const BorderSide(color: AppColors.primaryLight, width: 2),
        ),
      ),
      dividerTheme: DividerThemeData(color: AppColors.borderDark.withOpacity(0.3)),
      colorScheme: base.colorScheme.copyWith(
        primary: AppColors.primary,
        secondary: AppColors.gold,
        error: AppColors.danger,
        surface: AppColors.surfaceDark,
      ),
      tabBarTheme: TabBarTheme(
        labelColor: AppColors.primaryLight,
        unselectedLabelColor: AppColors.textSecondaryDark,
        indicatorColor: AppColors.primaryLight,
        labelStyle: GoogleFonts.inter(fontWeight: FontWeight.w600, fontSize: 14),
      ),
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: AppColors.cardDark,
        selectedItemColor: AppColors.primaryLight,
        unselectedItemColor: AppColors.textTertiaryDark,
        elevation: 8,
        type: BottomNavigationBarType.fixed,
        selectedLabelStyle: GoogleFonts.inter(fontSize: 11, fontWeight: FontWeight.w600),
        unselectedLabelStyle: GoogleFonts.inter(fontSize: 11),
      ),
      chipTheme: ChipThemeData(
        backgroundColor: AppColors.cardDarkElevated,
        selectedColor: AppColors.primary,
        labelStyle: GoogleFonts.inter(fontSize: 12),
        shape: RoundedRectangleBorder(borderRadius: AppRadius.bFull),
        side: BorderSide.none,
      ),
    );
  }
}
