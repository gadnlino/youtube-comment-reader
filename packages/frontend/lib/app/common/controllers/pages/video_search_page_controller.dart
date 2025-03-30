import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:get/get.dart';

class VideoSearchPageController extends GetxController {
  final _ycvApi = YoutubeCommentViewerApi();

  Rx<bool> loadingMoreVideos = Rx(false);
  Rx<bool> reloading = Rx(false);
  Rx<FilterOptions> currentFilterOptions = Rx(FilterOptions());
  Rxn<YouTubeSearchResponse> videoSearchLastResponse = Rxn(null);
  RxList<YouTubeSearchItem> videoSearchList = RxList();

  Rx<YouTubeSearchParams> __searchParams = Rx(YouTubeSearchParams());
  Rxn<String> __pageToken = Rxn();

  @override
  void onInit() {
    (() async {
      loadMoreVideos();
    })();

    ever(currentFilterOptions, (callback) {
      __searchParams.value = YouTubeSearchParams(
          order: callback.order,
          q: callback.keywords,
          pageToken: __pageToken.value);
    });
    super.onInit();
  }

  loadMoreVideos() async {
    try {
      loadingMoreVideos.value = true;

      debugPrint("carregando mais videos");

      var searchResponse = await _ycvApi.searchVideos(__searchParams.value!);

      if (searchResponse != null && searchResponse.items.isNotEmpty) {
        for (var element in searchResponse.items) {
          videoSearchList.add(element);
        }
      }

      videoSearchLastResponse.value = searchResponse;
      __pageToken.value = searchResponse?.nextPageToken;
    } finally {
      loadingMoreVideos.value = false;
    }
  }

  reloadVideos() async {
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

  clearFilters() {
    currentFilterOptions.value = FilterOptions();
  }
}
