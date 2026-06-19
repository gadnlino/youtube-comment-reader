import 'package:flutter/material.dart';
import 'package:frontend/app/common/packages/cache_package.dart';
import 'package:get/get.dart';

class ThemeController extends GetxController {
  static const _storageKey = 'theme_mode';

  final themeMode = ThemeMode.system.obs;
  final CachePackage _cache = CachePackage();

  Future<void> loadSavedTheme() async {
    final saved = await _cache.getString(_storageKey);
    themeMode.value = _parseThemeMode(saved);
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    themeMode.value = mode;
    await _cache.putString(_storageKey, _themeModeToString(mode));
  }

  ThemeMode _parseThemeMode(String? value) {
    switch (value) {
      case 'light':
        return ThemeMode.light;
      case 'dark':
        return ThemeMode.dark;
      default:
        return ThemeMode.system;
    }
  }

  String _themeModeToString(ThemeMode mode) {
    switch (mode) {
      case ThemeMode.light:
        return 'light';
      case ThemeMode.dark:
        return 'dark';
      case ThemeMode.system:
        return 'system';
    }
  }
}
