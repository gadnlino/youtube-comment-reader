import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/exceptions/comments_disabled_exception.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';
import 'package:get/get.dart';

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
