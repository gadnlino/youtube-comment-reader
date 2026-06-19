import 'package:flutter/material.dart';
import 'package:frontend/app/common/themes/theme_tokens.dart';

class AppThemeExtension extends ThemeExtension<AppThemeExtension> {
  const AppThemeExtension({
    required this.accentYellow,
    required this.favoritedColor,
    required this.buttonPrimary,
    required this.buttonSuccess,
    required this.buttonCancel,
    required this.buttonPrimaryText,
    required this.buttonSuccessText,
    required this.buttonCancelText,
    required this.mutedText,
    required this.placeholderOverlay,
    required this.imageFallbackBackground,
    required this.imageFallbackIcon,
    required this.nestedCommentLine,
    required this.iconMuted,
  });

  final Color accentYellow;
  final Color favoritedColor;
  final Color buttonPrimary;
  final Color buttonSuccess;
  final Color buttonCancel;
  final Color buttonPrimaryText;
  final Color buttonSuccessText;
  final Color buttonCancelText;
  final Color mutedText;
  final Color placeholderOverlay;
  final Color imageFallbackBackground;
  final Color imageFallbackIcon;
  final Color nestedCommentLine;
  final Color iconMuted;

  static const dark = AppThemeExtension(
    accentYellow: AppColorTokens.accentYellow,
    favoritedColor: AppColorTokens.accentYellow,
    buttonPrimary: AppColorTokens.buttonPrimary,
    buttonSuccess: AppColorTokens.buttonSuccess,
    buttonCancel: AppColorTokens.buttonCancel,
    buttonPrimaryText: AppColorTokens.buttonPrimaryText,
    buttonSuccessText: AppColorTokens.buttonSuccessText,
    buttonCancelText: AppColorTokens.buttonCancelText,
    mutedText: AppColorTokens.darkMuted,
    placeholderOverlay: AppColorTokens.darkPlaceholderOverlay,
    imageFallbackBackground: AppColorTokens.darkImageFallbackBackground,
    imageFallbackIcon: AppColorTokens.darkImageFallbackIcon,
    nestedCommentLine: AppColorTokens.darkNestedCommentLine,
    iconMuted: AppColorTokens.darkIconMuted,
  );

  static const light = AppThemeExtension(
    accentYellow: AppColorTokens.accentYellow,
    favoritedColor: AppColorTokens.accentYellow,
    buttonPrimary: AppColorTokens.buttonPrimary,
    buttonSuccess: AppColorTokens.buttonSuccess,
    buttonCancel: AppColorTokens.buttonCancel,
    buttonPrimaryText: AppColorTokens.buttonPrimaryText,
    buttonSuccessText: AppColorTokens.buttonSuccessText,
    buttonCancelText: AppColorTokens.buttonCancelText,
    mutedText: AppColorTokens.lightMuted,
    placeholderOverlay: AppColorTokens.lightPlaceholderOverlay,
    imageFallbackBackground: AppColorTokens.lightImageFallbackBackground,
    imageFallbackIcon: AppColorTokens.lightImageFallbackIcon,
    nestedCommentLine: AppColorTokens.lightNestedCommentLine,
    iconMuted: AppColorTokens.lightIconMuted,
  );

  @override
  AppThemeExtension copyWith({
    Color? accentYellow,
    Color? favoritedColor,
    Color? buttonPrimary,
    Color? buttonSuccess,
    Color? buttonCancel,
    Color? buttonPrimaryText,
    Color? buttonSuccessText,
    Color? buttonCancelText,
    Color? mutedText,
    Color? placeholderOverlay,
    Color? imageFallbackBackground,
    Color? imageFallbackIcon,
    Color? nestedCommentLine,
    Color? iconMuted,
  }) {
    return AppThemeExtension(
      accentYellow: accentYellow ?? this.accentYellow,
      favoritedColor: favoritedColor ?? this.favoritedColor,
      buttonPrimary: buttonPrimary ?? this.buttonPrimary,
      buttonSuccess: buttonSuccess ?? this.buttonSuccess,
      buttonCancel: buttonCancel ?? this.buttonCancel,
      buttonPrimaryText: buttonPrimaryText ?? this.buttonPrimaryText,
      buttonSuccessText: buttonSuccessText ?? this.buttonSuccessText,
      buttonCancelText: buttonCancelText ?? this.buttonCancelText,
      mutedText: mutedText ?? this.mutedText,
      placeholderOverlay: placeholderOverlay ?? this.placeholderOverlay,
      imageFallbackBackground:
          imageFallbackBackground ?? this.imageFallbackBackground,
      imageFallbackIcon: imageFallbackIcon ?? this.imageFallbackIcon,
      nestedCommentLine: nestedCommentLine ?? this.nestedCommentLine,
      iconMuted: iconMuted ?? this.iconMuted,
    );
  }

  @override
  AppThemeExtension lerp(ThemeExtension<AppThemeExtension>? other, double t) {
    if (other is! AppThemeExtension) return this;
    return AppThemeExtension(
      accentYellow: Color.lerp(accentYellow, other.accentYellow, t)!,
      favoritedColor: Color.lerp(favoritedColor, other.favoritedColor, t)!,
      buttonPrimary: Color.lerp(buttonPrimary, other.buttonPrimary, t)!,
      buttonSuccess: Color.lerp(buttonSuccess, other.buttonSuccess, t)!,
      buttonCancel: Color.lerp(buttonCancel, other.buttonCancel, t)!,
      buttonPrimaryText:
          Color.lerp(buttonPrimaryText, other.buttonPrimaryText, t)!,
      buttonSuccessText:
          Color.lerp(buttonSuccessText, other.buttonSuccessText, t)!,
      buttonCancelText:
          Color.lerp(buttonCancelText, other.buttonCancelText, t)!,
      mutedText: Color.lerp(mutedText, other.mutedText, t)!,
      placeholderOverlay:
          Color.lerp(placeholderOverlay, other.placeholderOverlay, t)!,
      imageFallbackBackground: Color.lerp(
          imageFallbackBackground, other.imageFallbackBackground, t)!,
      imageFallbackIcon:
          Color.lerp(imageFallbackIcon, other.imageFallbackIcon, t)!,
      nestedCommentLine:
          Color.lerp(nestedCommentLine, other.nestedCommentLine, t)!,
      iconMuted: Color.lerp(iconMuted, other.iconMuted, t)!,
    );
  }
}
