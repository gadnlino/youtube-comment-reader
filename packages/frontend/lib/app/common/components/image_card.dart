import 'package:flutter/material.dart';

class ImageCard extends StatelessWidget {
  Widget? child;
  Color? backgroundColor;
  Function? onPressed;
  double? width;
  double? height;

  ImageCard(
      {super.key,
      this.child,
      this.backgroundColor,
      this.onPressed,
      this.width = 130,
      this.height = 200});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
        if (onPressed != null) {
          onPressed!();
        }
      },
      child: Container(
        height: height,
        width: width,
        decoration: BoxDecoration(
            color: backgroundColor,
            borderRadius: const BorderRadius.all(Radius.circular(10))),
        child: child,
      ),
    );
  }
}
