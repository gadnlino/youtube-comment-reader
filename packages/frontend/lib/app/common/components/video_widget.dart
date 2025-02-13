import 'package:flutter/material.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/favorites_page/favorites_page.dart';
import 'package:get/get.dart';

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
                        color: Colors.white,
                        height: video.snippet.thumbnails.defaultThumbnail.height
                            .toDouble(),
                        width: video.snippet.thumbnails.defaultThumbnail.width
                            .toDouble()),
                    SizedBox(
                      height: video.snippet.thumbnails.defaultThumbnail.height
                          .toDouble(),
                      width: video.snippet.thumbnails.defaultThumbnail.width
                          .toDouble(),
                      child: const Icon(
                        Icons.question_mark_outlined,
                        color: Colors.black,
                        size: 30,
                      ),
                    )
                  ],
                ),
              ),
            ),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    video.snippet.title,
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${video.snippet.channelTitle} · ${Utils.formatDateOrNull(DateTime.parse(video.snippet.publishedAt), 'dd/MM/yyyy')}',
                    style: TextStyle(fontSize: 12, color: Colors.grey[200]),
                  ),
                ],
              ),
            ),
            IconButton(
              icon: Icon(
                Icons.star,
                color: favorited ? Colors.yellow : Colors.white,
              ),
              onPressed: onFavoriteTap,
            ),
          ],
        ),
      ),
    );
  }
}
