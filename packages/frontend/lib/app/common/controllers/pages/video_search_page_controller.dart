import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';
import 'package:get/get.dart';

class VideoSearchPageController extends GetxController {
  final _ycvApi = YoutubeCommentViewerApi();
  final _defaultSearchParams = YouTubeSearchParams(maxResults: 10);

  Rx<bool> loadingMoreVideos = Rx(false);
  Rx<bool> reloading = Rx(false);
  Rxn<YouTubeSearchResponse> videoSearchLastResponse = Rxn(null);
  Rxn<YouTubeSearchParams> searchParams = Rxn();
  RxList<YouTubeSearchItem> videoSearchList = RxList();

  @override
  void onInit() {
    searchParams.value = __getDefaultSearchParams();
    (() async {
      loadMoreVideos();
    })();

    super.onInit();
  }

  loadMoreVideos() async {
    try {
      loadingMoreVideos.value = true;

      debugPrint("carregando mais videos");

      var searchResponse = await _ycvApi.searchVideos(searchParams.value!);

      if (searchResponse != null && searchResponse.items.isNotEmpty) {
        for (var element in searchResponse.items) {
          videoSearchList.add(element);
        }
      }

      videoSearchLastResponse.value = searchResponse;
      searchParams.value?.pageToken = searchResponse?.nextPageToken;
    } finally {
      loadingMoreVideos.value = false;
    }
  }

  reloadVideos() async {
    if (!reloading.value) {
      searchParams.value = __getDefaultSearchParams();
      videoSearchList = RxList<YouTubeSearchItem>();

      try {
        reloading.value = true;
        await loadMoreVideos();
      } finally {
        reloading.value = false;
      }
    }
  }

  customSearch() async {
    if (!reloading.value) {
      videoSearchList = RxList<YouTubeSearchItem>();

      try {
        reloading.value = true;
        await loadMoreVideos();
      } finally {
        reloading.value = false;
      }
    }
  }

  __getDefaultSearchParams() => YouTubeSearchParams.fromJson(
      json.decode(json.encode(_defaultSearchParams)));
}
