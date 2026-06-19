import 'package:flutter/material.dart';

abstract final class AppColorTokens {
  // Brand (shared across light and dark)
  static const accentYellow = Color(0xffFFF50A);
  static const buttonPrimary = Color(0xfffff50a);
  static const buttonSuccess = Color(0xff35A3D2);
  static const buttonCancel = Color(0xffE85B3C);
  static const buttonPrimaryText = Color(0xff000000);
  static const buttonSuccessText = Color(0xff000000);
  static const buttonCancelText = Color(0xffffffff);

  // Dark palette
  static const darkScaffold = Color(0xff062029);
  static const darkChrome = Color(0xff062029);
  static const darkOnSurface = Color(0xffffffff);
  static const darkOnSurfaceVariant = Color(0xB3FFFFFF);
  static const darkMuted = Color(0x99FFFFFF);
  static const darkDivider = Color(0xffffffff);
  static const darkUnselectedNav = Color(0xffffffff);
  static const darkIconMuted = Color(0xff9E9E9E);
  static const darkNestedCommentLine = Color(0x4D9E9E9E);
  static const darkPlaceholderOverlay = Color(0x73000000);
  static const darkImageFallbackBackground = Color(0xffffffff);
  static const darkImageFallbackIcon = Color(0xff000000);
  static const darkMetadata = Color(0xffEEEEEE);

  // Light palette
  static const lightScaffold = Color(0xffF5F5F5);
  static const lightChrome = Color(0xffffffff);
  static const lightOnSurface = Color(0xff1A1A1A);
  static const lightOnSurfaceVariant = Color(0xff616161);
  static const lightMuted = Color(0xff757575);
  static const lightDivider = Color(0xffE0E0E0);
  static const lightUnselectedNav = Color(0xff757575);
  static const lightIconMuted = Color(0xff9E9E9E);
  static const lightNestedCommentLine = Color(0x4D9E9E9E);
  static const lightPlaceholderOverlay = Color(0x73000000);
  static const lightImageFallbackBackground = Color(0xffE0E0E0);
  static const lightImageFallbackIcon = Color(0xff616161);
  static const lightMetadata = Color(0xff616161);
}
