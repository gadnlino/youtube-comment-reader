import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_divider.dart';

import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/exceptions/CommentsDisabledException.dart';

import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';

import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/advance_ranking_page/advance_ranking_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/ranking_selection_page/ranking_selection_page.dart';
import 'package:frontend/app/pages/video_search_page/video_search_page.dart';
import 'package:get/get.dart';

const String videoCommentsPageRoute = "/video-comments";

class VideoCommentsPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => VideoCommentsPageController());
  }
}

class VideoCommentsPageController extends GetxController {
  final _ycvApi = YoutubeCommentViewerApi();
  final FavoriteManager _favoriteManager = FavoriteManager();

  Rx<bool> loading = Rx(false);
  Rx<bool> loadingComments = Rx(false);
  Rxn<String> videoId = Rxn();
  Rxn<String> videoTitle = Rxn();
  Rxn<String> videoDescription = Rxn();
  Rxn<String> videoThumbnailUrl = Rxn();
  Rxn<String> channelTitle = Rxn();
  Rxn<String> videoPublishedAt = Rxn();
  Rxn<YouTubeCommentThreadsResponse> videoCommentsLastResponse = Rxn(null);
  Rxn<YouTubeCommentThreadsParams> searchParams = Rxn(null);
  RxList<YouTubeCommentThread> commentsThreadList = RxList();
  Rx<bool> commentsDisabledForVideo = Rx(false);

  RxList<CommentFavorite> commentFavorites = RxList();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        videoId.value = Get.parameters['videoId'];
        videoTitle.value = Get.parameters['videoTitle'];
        videoDescription.value = Get.parameters['videoDescription'];
        videoThumbnailUrl.value = Get.parameters['thumbnailUrl'];
        channelTitle.value = Get.parameters['channelTitle'];
        videoPublishedAt.value = Get.parameters['publishedAt'];

        if (videoId.value != null && videoId.value!.isNotEmpty) {
          videoCommentsLastResponse.value = await _ycvApi.fetchComments(
              YouTubeCommentThreadsParams(
                  videoId: videoId.value, part: 'snippet,replies'));

          if (videoCommentsLastResponse.value != null &&
              videoCommentsLastResponse.value!.items.isNotEmpty) {
            commentsThreadList.value = videoCommentsLastResponse.value!.items;
          }

          await loadCommentFavorites();
        }
      } on CommentsDisabledException {
        commentsDisabledForVideo.value = true;
      } finally {
        loading.value = false;
      }
    })();

    super.onInit();
  }

  void loadMoreComments() async {
    try {
      loadingComments.value = true;

      var searchResponse = await _ycvApi.fetchComments(
          YouTubeCommentThreadsParams(
              videoId: videoId.value,
              pageToken: videoCommentsLastResponse.value!.nextPageToken,
              part: 'snippet,replies'));

      if (searchResponse != null) {
        commentsThreadList.addAll(searchResponse.items);
      }

      videoCommentsLastResponse.value = searchResponse;
    } finally {
      loadingComments.value = false;
    }
  }

  loadCommentFavorites() async {
    var favorites = await _favoriteManager.getCommentFavorites();

    if (favorites != null) {
      commentFavorites.value = favorites;
    }
  }

  addCommentFavorite(
      YouTubeComment comment, List<YouTubeComment>? replies) async {
    CommentFavorite favorite = CommentFavorite(
        comment: comment,
        replies: replies,
        videoId: videoId.value,
        videoDescription: videoDescription.value,
        videoThumbnailUrl: videoThumbnailUrl.value,
        videoTitle: videoTitle.value,
        channelTitle: channelTitle.value,
        videoPublishedAt: videoPublishedAt.value);

    commentFavorites.add(favorite);

    await _favoriteManager.addCommentFavorite(favorite);
  }

  removeCommentFavorite(YouTubeComment comment) async {
    commentFavorites.value = commentFavorites
        .where((element) => element.comment?.id != comment.id)
        .toList();

    await _favoriteManager.removeCommentFavorite(comment);
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
