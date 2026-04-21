import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';


/// Tema yönetimi — Hive ile kalıcı.
class ThemeNotifier extends StateNotifier<ThemeMode> {
  ThemeNotifier() : super(ThemeMode.system) {
    _load();
  }

  static const _boxName = 'prefs';
  static const _key = 'theme_mode';

  void _load() {
    try {
      final box = Hive.box<String>(_boxName);
      final val = box.get(_key, defaultValue: 'system');
      state = _fromString(val ?? 'system');
    } catch (_) {
      state = ThemeMode.system;
    }
  }

  void setTheme(ThemeMode mode) {
    state = mode;
    try {
      final box = Hive.box<String>(_boxName);
      box.put(_key, _toString(mode));
    } catch (_) {}
  }

  void toggle() {
    if (state == ThemeMode.dark) {
      setTheme(ThemeMode.light);
    } else {
      setTheme(ThemeMode.dark);
    }
  }

  void cycle() {
    switch (state) {
      case ThemeMode.system:
        setTheme(ThemeMode.light);
        break;
      case ThemeMode.light:
        setTheme(ThemeMode.dark);
        break;
      case ThemeMode.dark:
        setTheme(ThemeMode.system);
        break;
    }
  }

  static ThemeMode _fromString(String s) {
    switch (s) {
      case 'light': return ThemeMode.light;
      case 'dark': return ThemeMode.dark;
      default: return ThemeMode.system;
    }
  }

  static String _toString(ThemeMode m) {
    switch (m) {
      case ThemeMode.light: return 'light';
      case ThemeMode.dark: return 'dark';
      case ThemeMode.system: return 'system';
    }
  }
}


/// Riverpod provider
final themeModeProvider = StateNotifierProvider<ThemeNotifier, ThemeMode>(
    (ref) => ThemeNotifier());
