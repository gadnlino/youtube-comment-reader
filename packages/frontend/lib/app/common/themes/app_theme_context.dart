import 'package:flutter/material.dart';
import 'package:frontend/app/common/themes/app_theme_extension.dart';

extension AppThemeContext on BuildContext {
  AppThemeExtension get appTheme =>
      Theme.of(this).extension<AppThemeExtension>()!;

  ColorScheme get appColors => Theme.of(this).colorScheme;
}
