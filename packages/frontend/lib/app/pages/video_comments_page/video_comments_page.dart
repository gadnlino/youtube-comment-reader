import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_divider.dart';

import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/exceptions/CommentsDisabledException.dart';

import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/models.dart';

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

  Rx<bool> loading = Rx(false);
  Rx<bool> loadingComments = Rx(false);
  Rxn<String> videoId = Rxn();
  Rxn<String> videoTitle = Rxn();
  Rxn<String> videoDescription = Rxn();
  Rxn<String> videoThumbnailUrl = Rxn();
  Rxn<YouTubeCommentThreadsResponse> videoCommentsLastResponse = Rxn(null);
  Rxn<YouTubeCommentThreadsParams> searchParams = Rxn(null);
  RxList<YouTubeCommentThread> commentsThreadList = RxList();
  Rx<bool> commentsDisabledForVideo = Rx(false);

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        videoId.value = Get.parameters['videoId'];
        videoTitle.value = Get.parameters['videoTitle'];
        videoDescription.value = Get.parameters['videoDescription'];
        videoThumbnailUrl.value = Get.parameters['thumbnailUrl'];

        if (videoId.value != null && videoId.value!.isNotEmpty) {
          videoCommentsLastResponse.value = await _ycvApi.fetchComments(
              YouTubeCommentThreadsParams(
                  videoId: videoId.value, part: 'snippet,replies'));

          if (videoCommentsLastResponse.value != null &&
              videoCommentsLastResponse.value!.items.isNotEmpty) {
            commentsThreadList.value = videoCommentsLastResponse.value!.items;
          }
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
}

class VideoCommentsPage extends GetView<VideoCommentsPageController> {
  final pageTitle = "Comments";
  const VideoCommentsPage({super.key});

  Widget build2(BuildContext context) {
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
            return Column(
              children: [
                // Video Section
                Container(
                  padding: const EdgeInsets.all(8.0),
                  color: Colors.black,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        controller.videoTitle.value != null
                            ? controller.videoTitle.value!
                            : "",
                        style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.bold,
                            color: Colors.white),
                      ),
                      const SizedBox(height: 8),
                      Wrap(
                        alignment: WrapAlignment.center,
                        children: [
                          Text(
                            controller.videoDescription.value != null
                                ? controller.videoDescription.value!
                                : "",
                            style:
                                TextStyle(fontSize: 12, color: Colors.white70),
                          )
                        ],
                      ),
                      ConstrainedBox(
                        constraints: BoxConstraints(
                          minHeight: 0,
                          minWidth: 0,
                        ),
                        child: SingleChildScrollView(
                          child: Text(
                            controller.videoDescription.value != null
                                ? controller.videoDescription.value!
                                : "",
                            style: const TextStyle(
                                fontSize: 12, color: Colors.white70),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                // Comments Section
                Column(
                  children: [
                    NotificationListener<ScrollNotification>(
                      onNotification: (ScrollNotification scrollInfo) {
                        if (scrollInfo.metrics.pixels ==
                            scrollInfo.metrics.maxScrollExtent) {
                          controller.loadMoreComments();
                        }
                        return true;
                      },
                      child: ListView.separated(
                        separatorBuilder: (a, b) => const CustomDivider(),
                        itemCount: controller.commentsThreadList.length +
                            (controller.loadingComments.value ? 1 : 0),
                        itemBuilder: (context, index) {
                          if (index == controller.commentsThreadList.length) {
                            return const Center(
                              child: Padding(
                                padding: EdgeInsets.all(8.0),
                                child: CircularProgressIndicator(),
                              ),
                            );
                          }
                          final comment =
                              controller.commentsThreadList.elementAt(index);
                          return Column(
                            children: [
                              CommentWidget(
                                comment: comment.snippet.topLevelComment,
                                replies: comment.replies?.comments,
                              ),
                            ],
                          );
                        },
                      ),
                    )
                  ],
                ),
              ],
            );
          },
        ));
  }

  @override
  Widget build(BuildContext context) {
    // Dados de exemplo
    const postTitle = "Título do Post";
    //const postImage = "https://via.placeholder.com/400"; // URL de exemplo
    const postImage =
        "https://techhubdigital.com/wp-content/uploads/2020/06/YouTube-Thumbnail-Size-Pr.jpg"; // URL de exemplo
    const postComment = "Este é o comentário do autor do post.";
    final comments = List.generate(
      20,
      (index) => {
        'author': 'User$index',
        'content': 'Este é o comentário número $index.',
        'commentsCount': index * 2,
        'upvotes': index * 5,
      },
    );

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
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    controller.videoDescription.value != null
                        ? controller.videoDescription.value!
                        : "",
                    style: const TextStyle(fontSize: 16, color: Colors.white70),
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
                            CommentWidget(
                              comment: comment.snippet.topLevelComment,
                              replies: comment.replies?.comments,
                            ),
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

class CommentWidget extends StatelessWidget {
  final YouTubeComment comment;
  final List<YouTubeComment>? replies;
  final int level; // Depth level for indentation

  const CommentWidget({
    super.key,
    required this.comment,
    this.replies,
    this.level = 0,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          left: level * 12.0 + 10, top: 8.0, bottom: 8.0, right: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundImage:
                    NetworkImage(comment.snippet.authorProfileImageUrl),
              ),
              const SizedBox(width: 8.0),
              Expanded(
                child: Text(
                  comment.snippet.authorDisplayName,
                  style: const TextStyle(
                      fontWeight: FontWeight.bold, color: Colors.white),
                ),
              ),
            ],
          ),
          const SizedBox(height: 4.0),
          Text(comment.snippet.textOriginal,
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
              const SizedBox(width: 16.0),
              if (replies != null && replies!.isNotEmpty)
                const Icon(Icons.comment, size: 16, color: Colors.grey),
              if (replies != null && replies!.isNotEmpty)
                const SizedBox(width: 4.0),
              if (replies != null && replies!.isNotEmpty)
                Text(
                    "${replies!.length} ${replies!.length == 1 ? 'reply' : 'replies'}",
                    style: const TextStyle(color: Colors.white)),
            ],
          ),
          const SizedBox(height: 4.0),
          if (replies != null && replies!.isNotEmpty)
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: replies != null ? replies!.length : 0,
              itemBuilder: (context, index) {
                return CommentWidget(
                    comment: replies![index], level: level + 1);
              },
            ),
        ],
      ),
    );
  }
}
