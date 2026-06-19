import 'package:flutter/material.dart';
import 'package:frontend/app/common/themes/app_theme_extension.dart';
import 'package:frontend/app/common/themes/theme_tokens.dart';
import 'package:google_fonts/google_fonts.dart';

TextTheme _buildAppTextTheme(Color onSurface, Color onSurfaceVariant) {
  final base = GoogleFonts.poppinsTextTheme();
  return base.copyWith(
    labelSmall: base.labelSmall?.copyWith(
      fontSize: 10,
      color: onSurfaceVariant,
    ),
    bodySmall: base.bodySmall?.copyWith(
      fontSize: 12,
      color: onSurfaceVariant,
    ),
    bodyMedium: base.bodyMedium?.copyWith(
      fontSize: 14,
      color: onSurface,
    ),
    titleMedium: base.titleMedium?.copyWith(
      fontSize: 15,
      fontWeight: FontWeight.bold,
      color: onSurface,
    ),
    titleLarge: base.titleLarge?.copyWith(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: onSurface,
    ),
    headlineSmall: base.headlineSmall?.copyWith(
      fontSize: 25,
      color: onSurface,
    ),
    labelLarge: base.labelLarge?.copyWith(
      color: onSurface,
    ),
  );
}

ThemeData _buildTheme({
  required Brightness brightness,
  required Color scaffoldBackground,
  required Color chromeBackground,
  required Color onSurface,
  required Color onSurfaceVariant,
  required Color dividerColor,
  required Color selectedNavColor,
  required Color unselectedNavColor,
  required AppThemeExtension extension,
}) {
  final textTheme = _buildAppTextTheme(onSurface, onSurfaceVariant);
  final colorScheme = ColorScheme.fromSeed(
    seedColor: Colors.orange,
    brightness: brightness,
    surface: scaffoldBackground,
    onSurface: onSurface,
  );

  return ThemeData(
    brightness: brightness,
    colorScheme: colorScheme,
    textTheme: textTheme,
    scaffoldBackgroundColor: scaffoldBackground,
    dividerColor: dividerColor,
    extensions: [extension],
    appBarTheme: AppBarTheme(
      backgroundColor: chromeBackground,
      foregroundColor: onSurface,
      titleTextStyle: textTheme.titleLarge,
      iconTheme: IconThemeData(color: onSurface),
    ),
    bottomNavigationBarTheme: BottomNavigationBarThemeData(
      backgroundColor: chromeBackground,
      selectedItemColor: selectedNavColor,
      unselectedItemColor: unselectedNavColor,
    ),
    tabBarTheme: TabBarThemeData(
      indicatorColor: selectedNavColor,
      labelColor: selectedNavColor,
      unselectedLabelColor: unselectedNavColor,
    ),
    progressIndicatorTheme: ProgressIndicatorThemeData(
      color: onSurface,
    ),
  );
}

final ThemeData appDarkTheme = _buildTheme(
  brightness: Brightness.dark,
  scaffoldBackground: AppColorTokens.darkScaffold,
  chromeBackground: AppColorTokens.darkChrome,
  onSurface: AppColorTokens.darkOnSurface,
  onSurfaceVariant: AppColorTokens.darkOnSurfaceVariant,
  dividerColor: AppColorTokens.darkDivider,
  selectedNavColor: AppColorTokens.accentYellow,
  unselectedNavColor: AppColorTokens.darkUnselectedNav,
  extension: AppThemeExtension.dark,
);

final ThemeData appLightTheme = _buildTheme(
  brightness: Brightness.light,
  scaffoldBackground: AppColorTokens.lightScaffold,
  chromeBackground: AppColorTokens.lightChrome,
  onSurface: AppColorTokens.lightOnSurface,
  onSurfaceVariant: AppColorTokens.lightOnSurfaceVariant,
  dividerColor: AppColorTokens.lightDivider,
  selectedNavColor: AppColorTokens.accentYellow,
  unselectedNavColor: AppColorTokens.lightUnselectedNav,
  extension: AppThemeExtension.light,
);
