import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/themes/app_theme_context.dart';

class CustomCachedNetworkImage extends StatelessWidget {
  String url;
  BoxFit? fit;
  double? height;
  double? width;

  CustomCachedNetworkImage(
      {super.key, required this.url, this.fit, this.height, this.width});

  @override
  Widget build(BuildContext context) {
    return CachedNetworkImage(
      imageUrl: url,
      fit: fit,
      height: height,
      width: width,
      placeholder: (context, url) => CircularProgressIndicator(
        color: context.appTheme.placeholderOverlay,
      ),
      errorWidget: (context, url, error) => const Icon(Icons.error),
    );
  }
}
