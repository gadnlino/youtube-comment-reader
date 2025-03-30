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

  Rx<FilterOptions> currentFilterOptions =
      Rx(FilterOptions(showPositive: true, showNegative: true));

  Rx<bool> videoDescriptionExpanded = Rx(false);

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        selectedVideo.value =
            YouTubeSearchItem.fromJson(jsonDecode(Get.parameters['video']!));

        if (selectedVideo.value != null && selectedVideo.value!.id.isNotEmpty) {
          videoCommentsLastResponse.value =
              await _ycvApi.fetchComments(__getDefaultSearchParams());

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

    ever(currentFilterOptions, (callback) {
      var newSearchParams = __getDefaultSearchParams();

      newSearchParams.searchTerms = callback.keywords;
      newSearchParams.order = callback.order;
      newSearchParams.pageToken = null;

      searchParams.value = newSearchParams;
    });

    super.onInit();
  }

  loadMoreComments() async {
    try {
      loadingComments.value = true;

      var searchResponse = await _ycvApi.fetchComments(searchParams.value!);

      if (searchResponse != null) {
        commentsThreadList.addAll(searchResponse.items);
      }

      videoCommentsLastResponse.value = searchResponse;
    } finally {
      loadingComments.value = false;
    }
  }

  reloadComments() async {
    if (!loadingComments.value) {
      commentsThreadList.value = [];

      try {
        loadingComments.value = true;
        await loadMoreComments();
      } finally {
        loadingComments.value = false;
      }
    }
  }

  clearFilters() {
    currentFilterOptions.value = FilterOptions();
  }

  YouTubeCommentThreadsParams __getDefaultSearchParams() {
    return YouTubeCommentThreadsParams(
        videoId: selectedVideo.value!.id,
        pageToken: videoCommentsLastResponse.value?.nextPageToken,
        part: 'snippet,replies');
  }
}
