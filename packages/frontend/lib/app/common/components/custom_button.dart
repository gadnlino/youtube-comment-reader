import 'package:flutter/material.dart';

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

  Color getButtonColor() {
    Color color;

    switch (type) {
      case ButtonType.primary:
        color = const Color(0xfffff50a);
        break;
      case ButtonType.success:
        color = const Color(0xff35A3D2);
        break;
      case ButtonType.cancel:
        color = const Color(0xffE85B3C);
        break;
      case ButtonType.neutral:
        color = Colors.transparent;
        break;
    }

    return color;
  }

  Color getTextColor() {
    Color color;

    switch (type) {
      case ButtonType.primary:
        color = const Color(0xff000000);
        break;
      case ButtonType.success:
        color = const Color(0xff000000);
        break;
      case ButtonType.cancel:
        color = const Color(0xffffffff);
        break;
      case ButtonType.neutral:
        color = const Color(0xff000000);
        break;
    }

    return color;
  }

  @override
  Widget build(BuildContext context) {
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
        color: getButtonColor(),
        child: Text(
          text,
          textAlign: TextAlign.center,
          style: TextStyle(
              color: getTextColor(), fontFamily: "Poppins", fontSize: 20),
        ),
      ),
    );
  }
}
