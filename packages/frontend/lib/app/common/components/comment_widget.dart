import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:html_unescape/html_unescape.dart';

class CommentWidget extends StatelessWidget {
  final YouTubeComment comment;
  final List<YouTubeComment>? replies;
  final int level; // Depth level for indentation
  bool favorited;
  void Function()? onFavoriteTap;

  CommentWidget(
      {super.key,
      required this.comment,
      this.replies,
      this.level = 0,
      this.favorited = false,
      this.onFavoriteTap});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          left: level * 12.0 + 5.0, top: 8.0, bottom: 8.0, right: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundImage:
                    NetworkImage(comment.snippet.authorProfileImageUrl),
              ),
              const SizedBox(
                width: 2.5,
              ),
              Text(
                "${comment.snippet.authorDisplayName} ",
                style: const TextStyle(
                    fontWeight: FontWeight.w500, color: Colors.white),
              ),
              Expanded(
                  child: Align(
                alignment: Alignment.centerRight,
                child: Text(
                  Utils.formatDateOrNull(
                          DateTime.parse(comment.snippet.publishedAt),
                          "dd/MM/yyyy HH:mm") ??
                      "",
                  style: const TextStyle(color: Colors.white, fontSize: 10),
                ),
              ))
            ],
          ),
          const SizedBox(height: 4.0),
          Text(HtmlUnescape().convert(comment.snippet.textOriginal),
              style: const TextStyle(color: Colors.white)),
          const SizedBox(height: 4.0),
          Row(
            children: [
              const Icon(
                Icons.thumb_up,
                size: 16,
                color: Colors.grey,
              ),
              const SizedBox(width: 4.0),
              Text(
                comment.snippet.likeCount.toString(),
                style: const TextStyle(color: Colors.white),
              ),
              const SizedBox(width: 4.0),
              if (replies != null && replies!.isNotEmpty)
                const Icon(Icons.comment, size: 16, color: Colors.grey),
              if (replies != null && replies!.isNotEmpty)
                const SizedBox(width: 4.0),
              if (replies != null && replies!.isNotEmpty)
                Text(
                    "${replies!.length} ${replies!.length == 1 ? 'reply' : 'replies'}",
                    style: const TextStyle(color: Colors.white)),
              IconButton(
                  onPressed: onFavoriteTap,
                  icon: Icon(Icons.star,
                      color: favorited ? Colors.yellow : Colors.white))
            ],
          ),
          const SizedBox(height: 4.0),
          Builder(
            builder: (context) {
              if (replies != null && replies!.isNotEmpty) {
                return ListTileTheme(
                    minVerticalPadding: 0,
                    child: ExpansionTile(
                      tilePadding: EdgeInsets.zero,
                      iconColor: Colors.white,
                      collapsedIconColor: Colors.white,
                      title: const Center(
                        child: Text("Show replies",
                            style:
                                TextStyle(color: Colors.white, fontSize: 13)),
                      ),
                      children: [
                        ListView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: replies != null ? replies!.length : 0,
                          itemBuilder: (context, index) {
                            return CommentWidget(
                                comment: replies![index], level: level + 1);
                          },
                        )
                      ],
                    ));
              }
              return Container();
            },
          ),
        ],
      ),
    );
  }
}
