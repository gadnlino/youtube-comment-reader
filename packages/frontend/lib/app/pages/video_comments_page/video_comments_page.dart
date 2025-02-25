import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/controllers/video_comments_page_controller.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:get/get.dart';
import 'package:html_unescape/html_unescape.dart';

const String videoCommentsPageRoute = "/video-comments";

class VideoCommentsPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => VideoCommentsPageController());
  }
}

class VideoCommentsPage extends GetView<VideoCommentsPageController> {
  final pageTitle = "Comments";
  const VideoCommentsPage({super.key});

  Widget _videoDescriptionSection(BuildContext context, String description) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Animated Size for smooth expanding/collapsing
        AnimatedSize(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeInOut,
          child: ConstrainedBox(
            constraints: controller.videoDescriptionExpanded.value
                ? BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height *
                        .2) // No constraints when expanded
                : BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height *
                        .045), // Limit height when collapsed
            child: SingleChildScrollView(
              child: Text(
                HtmlUnescape().convert(description),
                overflow: TextOverflow.fade,
                softWrap: true,
                style: const TextStyle(fontSize: 14, color: Colors.white70),
              ),
            ),
          ),
        ),

        // Show More / Show Less button
        GestureDetector(
          onTap: () {
            controller.videoDescriptionExpanded.value =
                !controller.videoDescriptionExpanded.value;
          },
          child: Padding(
            padding: const EdgeInsets.only(top: 5),
            child: Center(
              child: Text(
                controller.videoDescriptionExpanded.value
                    ? "Show less"
                    : "Show more",
                style: const TextStyle(
                  color: Colors.white60,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(pageTitle),
          leading: IconButton(
              onPressed: () {
                Navigation.goBack();
              },
              icon: const Icon(Icons.arrow_back)),
        ),
        body: Obx(
          () {
            if (controller.loadingComments.value || controller.loading.value) {
              return const Center(
                child: Padding(
                  padding: EdgeInsets.all(8.0),
                  child: CircularProgressIndicator(),
                ),
              );
            }

            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10.0),
              child: Column(
                children: [
                  const SizedBox(height: 10),
                  // Cabeçalho do Post
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Flexible(
                          child: Text(
                        controller.selectedVideo.value != null
                            ? HtmlUnescape().convert(
                                controller.selectedVideo.value!.snippet.title)
                            : "",
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      )),
                      IconButton(
                        icon: Icon(
                          Icons.star,
                          color: controller.videoFavorites.any((element) =>
                                  element.id ==
                                  controller.selectedVideo.value!.id)
                              ? Colors.yellow
                              : Colors.white,
                        ),
                        onPressed: () {
                          if (!controller.videoFavorites.any((element) =>
                              element.id ==
                              controller.selectedVideo.value!.id)) {
                            controller.addVideoFavorite(
                                controller.selectedVideo.value!);
                          } else {
                            controller.removeVideoFavorite(
                                controller.selectedVideo.value!);
                          }
                        },
                      )
                    ],
                  ),
                  const SizedBox(height: 10),
                  if (controller.selectedVideo.value != null &&
                      controller.selectedVideo.value!.snippet.thumbnails.high
                          .url.isNotEmpty)
                    // Imagem do Post
                    Image.network(
                      controller
                          .selectedVideo.value!.snippet.thumbnails.high.url,
                      height: MediaQuery.of(context).size.height * 0.2,
                      width: double.infinity,
                      fit: BoxFit.fitWidth,
                    ),
                  const SizedBox(height: 10),
                  // Comentário do Autor
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    _videoDescriptionSection(context,
                        controller.selectedVideo.value!.snippet.description),
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    const SizedBox(height: 10),
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    const CustomDivider(),

                  const SizedBox(height: 10),
                  // Lista Rolável de Comentários
                  Builder(builder: (ctx) {
                    if (controller.commentsDisabledForVideo.value) {
                      return const Expanded(
                          child: Center(
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Text(
                            "Comments disabled for this video :(",
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ),
                      ));
                    }

                    if (controller.commentsThreadList.isEmpty) {
                      return const Expanded(
                          child: Center(
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Text(
                            "No comments yet :(",
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ),
                      ));
                    }

                    return Expanded(
                      child: ListView.builder(
                        itemCount: controller.commentsThreadList.length,
                        itemBuilder: (context, index) {
                          final comment =
                              controller.commentsThreadList.elementAt(index);
                          return Column(
                            children: [
                              Obx(
                                () => CommentWidget(
                                  comment: comment.snippet.topLevelComment,
                                  replies: comment.replies?.comments,
                                  favorited: controller.commentFavorites.any(
                                      (element) =>
                                          element.comment?.id == comment.id),
                                  onFavoriteTap: () {
                                    if (!controller.commentFavorites.any(
                                        (element) =>
                                            element.comment?.id ==
                                            comment.id)) {
                                      controller.addCommentFavorite(
                                          comment.snippet.topLevelComment,
                                          comment.replies?.comments);
                                    } else {
                                      controller.removeCommentFavorite(
                                          comment.snippet.topLevelComment);
                                    }
                                  },
                                ),
                              )
                            ],
                          );
                        },
                      ),
                    );
                  }),
                ],
              ),
            );
          },
        ));
  }
}
