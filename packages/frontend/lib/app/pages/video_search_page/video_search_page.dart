import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/api/youtube_comment_viewer_api.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_divider.dart';

import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/components/video_widget.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';

import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/packages/cache_package.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';

import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/advance_ranking_page/advance_ranking_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/ranking_selection_page/ranking_selection_page.dart';
import 'package:frontend/app/pages/video_comments_page/video_comments_page.dart';
import 'package:get/get.dart';
import 'package:lazy_load_scrollview/lazy_load_scrollview.dart';

const String videoSearchPageRoute = "/video-search";

class VideoSearchPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => VideoSearchPageController());
  }
}

class VideoSearchPageController extends GetxController {
  final _ycvApi = YoutubeCommentViewerApi();
  final _defaultSearchParams = YouTubeSearchParams(maxResults: 10);
  final FavoriteManager _favoriteManager = FavoriteManager();

  Rx<bool> loadingMoreVideos = Rx(false);
  Rx<bool> reloading = Rx(false);
  Rxn<YouTubeSearchResponse> videoSearchLastResponse = Rxn(null);
  Rxn<YouTubeSearchParams> searchParams = Rxn();
  RxList<YouTubeSearchItem> videoSearchList = RxList();

  RxList<YouTubeSearchItem> videoFavorites = RxList();

  @override
  void onInit() {
    searchParams.value = _defaultSearchParams;
    (() async {
      loadMoreVideos();
      loadFavorites();
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

  reload() async {
    if (!reloading.value) {
      searchParams.value = _defaultSearchParams;
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

  loadFavorites() async {
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
    videoFavorites.value = videoFavorites
        .where((element) => element.id.videoId != video.id.videoId)
        .toList();

    await _favoriteManager.removeVideoFavorite(video);
  }
}

class VideoSearchPage extends GetView<VideoSearchPageController> {
  const VideoSearchPage({super.key});

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Youtube Comment Reader";
    return Scaffold(
        appBar: AppBar(
          title: const Text(pageTitle),
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 3,
              ),
              child: IconButton(
                onPressed: controller.reload,
                icon: const Icon(Icons.refresh_sharp),
                color: Colors.white,
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 3,
              ),
              child: IconButton(
                onPressed: () {
                  Get.defaultDialog(
                      title: "Pesquisar videos",
                      backgroundColor: Colors.white,
                      radius: 5,
                      content: Column(
                        children: [
                          Obx(() => TextFormField(
                                initialValue: controller.searchParams.value?.q,
                                onChanged: (value) =>
                                    controller.searchParams.value!.q = value,
                                decoration: const InputDecoration(
                                  labelText: 'Nome ou termos do video',
                                ),
                              )),
                          Align(
                            alignment: Alignment.centerLeft,
                            child: TextButton(
                                onPressed: () {
                                  Navigation.goBack();
                                  controller.reload();
                                },
                                child: const Text(
                                  "Limpar filtros",
                                  style: TextStyle(fontSize: 12),
                                )),
                          )
                        ],
                      ),
                      textConfirm: "Pesquisar",
                      textCancel: "Cancelar",
                      confirmTextColor: Colors.white,
                      onConfirm: () async {
                        Navigation.goBack();
                        controller.customSearch();
                      });
                },
                icon: const Icon(Icons.filter_alt),
                color: Colors.white,
              ),
            )
          ],
          centerTitle: true,
        ),
        bottomNavigationBar: const CustomBottomNavigationBar(),
        body: Obx(
          () {
            if ((controller.loadingMoreVideos.value ||
                    controller.reloading.value) &&
                controller.videoSearchList.isEmpty) {
              return const Center(
                child: CircularProgressIndicator(
                  color: Colors.white,
                ),
              );
            }

            return Column(
              children: [
                Expanded(
                  child: LazyLoadScrollView(
                    isLoading: controller.loadingMoreVideos.value,
                    onEndOfPage: controller.loadMoreVideos,
                    scrollOffset:
                        (MediaQuery.of(context).size.height - 50).toInt(),
                    child: ListView.separated(
                        separatorBuilder: (context, index) =>
                            const CustomDivider(),
                        itemCount: controller.videoSearchList.length,
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.vertical,
                        itemBuilder: (BuildContext context, int index) {
                          var video =
                              controller.videoSearchList.elementAt(index);
                          return Column(
                            children: [
                              Obx(
                                () => VideoWidget(
                                  video: video,
                                  favorited: controller.videoFavorites.any(
                                      (element) =>
                                          element.id.videoId ==
                                          video.id.videoId),
                                  onFavoriteTap: () {
                                    if (!controller.videoFavorites.any(
                                        (element) =>
                                            element.id.videoId ==
                                            video.id.videoId)) {
                                      controller.addVideoFavorite(video);
                                    } else {
                                      controller.removeVideoFavorite(video);
                                    }
                                  },
                                  onTap: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute: videoCommentsPageRoute,
                                        parameters: {
                                          'videoId': video.id.videoId!,
                                          'videoTitle': video.snippet.title,
                                          'videoDescription':
                                              video.snippet.description,
                                          'thumbnailUrl':
                                              video.snippet.thumbnails.high.url,
                                          'channelTitle':
                                              video.snippet.channelTitle,
                                          'publishedAt':
                                              video.snippet.publishedAt,
                                        });
                                  },
                                ),
                              )
                            ],
                          );
                        }),
                  ),
                )
              ],
            );
          },
        ));
  }
}
