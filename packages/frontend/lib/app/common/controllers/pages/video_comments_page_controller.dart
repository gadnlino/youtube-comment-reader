import 'dart:convert';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/exceptions/comments_disabled_exception.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:get/get.dart';

class VideoCommentsPageController extends GetxController {
  final _ycvApi = YoutubeCommentViewerApi();

  Rx<bool> loading = Rx(false);
  Rx<bool> loadingComments = Rx(false);
  Rxn<YouTubeSearchItem> selectedVideo = Rxn();

  Rxn<YouTubeCommentThreadsResponse> videoCommentsLastResponse = Rxn();
  Rxn<YouTubeCommentThreadsParams> searchParams = Rxn();
  RxList<YouTubeCommentThread> commentsThreadList = RxList();
  Rx<bool> commentsDisabledForVideo = Rx(false);

  Rx<bool> videoDescriptionExpanded = Rx(false);

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        selectedVideo.value =
            YouTubeSearchItem.fromJson(jsonDecode(Get.parameters['video']!));

        if (selectedVideo.value != null && selectedVideo.value!.id.isNotEmpty) {
          videoCommentsLastResponse.value = await _ycvApi.fetchComments(
              YouTubeCommentThreadsParams(
                  videoId: selectedVideo.value!.id, part: 'snippet,replies'));

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
              videoId: selectedVideo.value!.id,
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
