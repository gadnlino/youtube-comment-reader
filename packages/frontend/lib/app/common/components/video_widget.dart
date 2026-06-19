import 'package:flutter/material.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/themes/app_theme_context.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:html_unescape/html_unescape.dart';

class VideoWidget extends StatelessWidget {
  final YouTubeSearchItem video;
  void Function()? onTap;
  bool favorited;
  void Function()? onFavoriteTap;

  VideoWidget(
      {super.key,
      required this.video,
      this.onTap,
      this.favorited = false,
      this.onFavoriteTap});

  @override
  Widget build(BuildContext context) {
    final appTheme = context.appTheme;
    final textTheme = Theme.of(context).textTheme;

    return InkWell(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(8.0),
              child: Image.network(
                video.snippet.thumbnails.defaultThumbnail.url,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) => Stack(
                  children: [
                    Container(
                        color: appTheme.imageFallbackBackground,
                        height: video.snippet.thumbnails.defaultThumbnail.height
                            .toDouble(),
                        width: video.snippet.thumbnails.defaultThumbnail.width
                            .toDouble()),
                    SizedBox(
                      height: video.snippet.thumbnails.defaultThumbnail.height
                          .toDouble(),
                      width: video.snippet.thumbnails.defaultThumbnail.width
                          .toDouble(),
                      child: Icon(
                        Icons.question_mark_outlined,
                        color: appTheme.imageFallbackIcon,
                        size: 30,
                      ),
                    )
                  ],
                ),
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    HtmlUnescape().convert(video.snippet.title),
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                    style: textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${video.snippet.channelTitle} · ${Utils.formatDateOrNull(DateTime.parse(video.snippet.publishedAt), 'dd/MM/yyyy')}',
                    style: textTheme.bodySmall,
                  ),
                ],
              ),
            ),
            IconButton(
              icon: Icon(
                favorited ? Icons.star : Icons.star_border,
                color: favorited
                    ? appTheme.favoritedColor
                    : context.appColors.onSurface,
              ),
              onPressed: onFavoriteTap,
            ),
          ],
        ),
      ),
    );
  }
}
