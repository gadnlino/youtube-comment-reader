import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/controllers/video_comments_page_controller.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/video_search_page/video_search_page.dart';
import 'package:get/get.dart';

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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(pageTitle),
          leading: IconButton(
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: videoSearchPageRoute);
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

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Cabeçalho do Post
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    controller.videoTitle.value != null
                        ? controller.videoTitle.value!
                        : "",
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
                // Imagem do Post
                Image.network(
                  controller.videoThumbnailUrl.value!,
                  width: double.infinity,
                  height: 150,
                  fit: BoxFit.fitWidth,
                ),
                // Comentário do Autor

                if (controller.videoDescription.value != null)
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text(
                      controller.videoDescription.value != null
                          ? controller.videoDescription.value!
                          : "",
                      style:
                          const TextStyle(fontSize: 16, color: Colors.white70),
                    ),
                  ),
                const Divider(),
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
                          "No comments :(",
                          style: TextStyle(fontSize: 25, color: Colors.white),
                        ),
                      ),
                    ));
                  }

                  return Expanded(
                    child: ListView.builder(
                      padding: const EdgeInsets.all(16.0),
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
                                          element.comment?.id == comment.id)) {
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
            );
          },
        ));
  }
}
