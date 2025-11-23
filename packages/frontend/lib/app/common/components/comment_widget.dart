import 'package:flutter/material.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:html_unescape/html_unescape.dart';

class CommentWidget extends StatefulWidget {
  final YouTubeComment comment;
  final List<YouTubeComment>? replies;
  final int level; // Depth level for indentation
  final bool favorited;
  final void Function()? onFavoriteTap;

  const CommentWidget(
      {super.key,
      required this.comment,
      this.replies,
      this.level = 0,
      this.favorited = false,
      this.onFavoriteTap});

  @override
  State<CommentWidget> createState() => _CommentWidgetState();
}

class _CommentWidgetState extends State<CommentWidget> {
  bool _isExpanded = true;

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Linhas verticais para cada nível de aninhamento
        if (widget.level > 0)
          ...List.generate(widget.level, (index) {
            return Positioned(
              left: index * 12.0 + 2.0,
              top: 0,
              bottom: 0,
              width: 2.0,
              child: Container(
                color: Colors.grey.withOpacity(0.3),
              ),
            );
          }),
        // Conteúdo do comentário
        Padding(
          padding: EdgeInsets.only(
              left: widget.level * 12.0 + 5.0,
              top: 8.0,
              bottom: 8.0,
              right: 8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    backgroundImage: NetworkImage(
                        widget.comment.snippet.authorProfileImageUrl),
                  ),
                  const SizedBox(
                    width: 2.5,
                  ),
                  Text(
                    "${widget.comment.snippet.authorDisplayName} ",
                    style: const TextStyle(
                        fontWeight: FontWeight.w500, color: Colors.white),
                  ),
                  Expanded(
                      child: Align(
                    alignment: Alignment.centerRight,
                    child: Text(
                      Utils.formatDateOrNull(
                              DateTime.parse(
                                  widget.comment.snippet.publishedAt),
                              "dd/MM/yyyy HH:mm") ??
                          "",
                      style: const TextStyle(color: Colors.white, fontSize: 10),
                    ),
                  ))
                ],
              ),
              const SizedBox(height: 4.0),
              Text(HtmlUnescape().convert(widget.comment.snippet.textOriginal),
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
                    widget.comment.snippet.likeCount.toString(),
                    style: const TextStyle(color: Colors.white),
                  ),
                  const SizedBox(width: 4.0),
                  if (widget.replies != null && widget.replies!.isNotEmpty)
                    const Icon(Icons.comment, size: 16, color: Colors.grey),
                  if (widget.replies != null && widget.replies!.isNotEmpty)
                    const SizedBox(width: 4.0),
                  if (widget.replies != null && widget.replies!.isNotEmpty)
                    Text(
                        "${widget.replies!.length} ${widget.replies!.length == 1 ? 'reply' : 'replies'}",
                        style: const TextStyle(color: Colors.white)),
                  IconButton(
                      onPressed: widget.onFavoriteTap,
                      icon: Icon(
                          widget.favorited ? Icons.star : Icons.star_border,
                          color:
                              widget.favorited ? Colors.yellow : Colors.white))
                ],
              ),
              const SizedBox(height: 4.0),
              Builder(
                builder: (context) {
                  if (widget.replies != null && widget.replies!.isNotEmpty) {
                    return Column(
                      children: [
                        GestureDetector(
                          onTap: () {
                            setState(() {
                              _isExpanded = !_isExpanded;
                            });
                          },
                          child: SizedBox(
                            height: 20,
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  _isExpanded
                                      ? Icons.expand_less
                                      : Icons.expand_more,
                                  color: Colors.white,
                                  size: 16,
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  _isExpanded ? "Hide replies" : "Show replies",
                                  style: const TextStyle(
                                      color: Colors.white, fontSize: 13),
                                ),
                              ],
                            ),
                          ),
                        ),
                        AnimatedSize(
                          duration: const Duration(milliseconds: 200),
                          curve: Curves.easeInOut,
                          child: _isExpanded
                              ? Column(
                                  children: [
                                    ListView.builder(
                                      shrinkWrap: true,
                                      physics:
                                          const NeverScrollableScrollPhysics(),
                                      itemCount: widget.replies != null
                                          ? widget.replies!.length
                                          : 0,
                                      itemBuilder: (context, index) {
                                        return CommentWidget(
                                            comment: widget.replies![index],
                                            level: widget.level + 1);
                                      },
                                    )
                                  ],
                                )
                              : const SizedBox.shrink(),
                        ),
                      ],
                    );
                  }
                  return Container();
                },
              ),
            ],
          ),
        ),
      ],
    );
  }
}
