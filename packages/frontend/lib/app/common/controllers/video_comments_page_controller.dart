import 'dart:convert';

import 'package:flutter/material.dart';
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
  Rxn<YouTubeSearchItem> selectedVideo = Rxn();

  Rxn<YouTubeCommentThreadsResponse> videoCommentsLastResponse = Rxn();
  Rxn<YouTubeCommentThreadsParams> searchParams = Rxn();
  RxList<YouTubeCommentThread> commentsThreadList = RxList();
  Rx<bool> commentsDisabledForVideo = Rx(false);

  RxList<YouTubeSearchItem> videoFavorites = RxList();
  RxList<CommentFavorite> commentFavorites = RxList();

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

        await loadCommentFavorites();
        await loadVideoFavorites();
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
        videoId: selectedVideo.value!.id,
        videoDescription: selectedVideo.value!.snippet.description,
        videoThumbnailUrl: selectedVideo.value!.snippet.thumbnails.high.url,
        videoTitle: selectedVideo.value!.snippet.title,
        channelTitle: selectedVideo.value!.snippet.channelTitle,
        videoPublishedAt: selectedVideo.value!.snippet.publishedAt);

    commentFavorites.add(favorite);

    await _favoriteManager.addCommentFavorite(favorite);
  }

  removeCommentFavorite(YouTubeComment comment) async {
    commentFavorites.value = commentFavorites
        .where((element) => element.comment?.id != comment.id)
        .toList();

    await _favoriteManager.removeCommentFavorite(comment);
  }

  loadVideoFavorites() async {
    var favorites = await _favoriteManager.getVideoFavorites();

    if (favorites != null) {
      videoFavorites.value = favorites;
    }
  }

  addVideoFavorite(YouTubeSearchItem video) async {
    videoFavorites.add(video);

    await _favoriteManager.addVideoFavorite(video);
  }

  removeVideoFavorite(YouTubeSearchItem video) async {
    videoFavorites.value =
        videoFavorites.where((element) => element.id != video.id).toList();

    await _favoriteManager.removeVideoFavorite(video);
  }
}
