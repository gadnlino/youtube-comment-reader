import 'package:flutter/material.dart';
import 'package:frontend/app/common/themes/app_theme_context.dart';
import 'package:frontend/app/common/themes/app_theme_extension.dart';

enum ButtonType { primary, success, cancel, neutral }

class CustomButton extends StatelessWidget {
  final String text;
  final ButtonType type;
  final Function? onPressed;
  final bool disabled;

  const CustomButton({
    super.key,
    required this.text,
    required this.type,
    this.onPressed,
    this.disabled = false,
  });

  Color _getButtonColor(AppThemeExtension appTheme) {
    switch (type) {
      case ButtonType.primary:
        return appTheme.buttonPrimary;
      case ButtonType.success:
        return appTheme.buttonSuccess;
      case ButtonType.cancel:
        return appTheme.buttonCancel;
      case ButtonType.neutral:
        return Colors.transparent;
    }
  }

  Color _getTextColor(
      AppThemeExtension appTheme, ColorScheme colorScheme, ButtonType type) {
    switch (type) {
      case ButtonType.primary:
        return appTheme.buttonPrimaryText;
      case ButtonType.success:
        return appTheme.buttonSuccessText;
      case ButtonType.cancel:
        return appTheme.buttonCancelText;
      case ButtonType.neutral:
        return colorScheme.onSurface;
    }
  }

  @override
  Widget build(BuildContext context) {
    final appTheme = context.appTheme;
    final colorScheme = context.appColors;
    final textTheme = Theme.of(context).textTheme;

    return Material(
      color: Colors.transparent,
      child: MaterialButton(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        onPressed: () {
          if (onPressed != null) {
            onPressed!();
          }
        },
        height: 50,
        color: _getButtonColor(appTheme),
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: textTheme.titleLarge?.copyWith(
            color: _getTextColor(appTheme, colorScheme, type),
          ),
        ),
      ),
    );
  }
}
