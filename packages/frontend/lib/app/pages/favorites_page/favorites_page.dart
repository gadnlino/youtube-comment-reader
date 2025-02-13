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

const String favoritesPageRoute = "/favorites";

class FavoritesPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => FavoritesPageController());
  }
}

class FavoritesPageController extends GetxController {
  final FavoriteManager _favoriteManager = FavoriteManager();

  Rx<bool> loadingMoreVideos = Rx(false);

  RxList<YouTubeSearchItem> videoFavorites = RxList();
  RxList<CommentFavorite> commentFavorites = RxList();

  @override
  void onInit() {
    (() async {
      await loadVideoFavorites();
      await loadCommentFavorites();
    })();

    super.onInit();
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
    videoFavorites.value = videoFavorites
        .where((element) => element.id.videoId != video.id.videoId)
        .toList();

    await _favoriteManager.removeVideoFavorite(video);
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
    );

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

class FavoritesPage extends GetView<FavoritesPageController> {
  const FavoritesPage({super.key});

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Favorites";
    return Scaffold(
        appBar: AppBar(
          title: const Text(pageTitle),
          actions: [
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
                      content: Container(),
                      textConfirm: "Pesquisar",
                      textCancel: "Cancelar",
                      confirmTextColor: Colors.white,
                      onConfirm: () async {
                        Navigation.goBack();
                        // controller.customSearch();
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
            if (controller.loadingMoreVideos.value) {
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
                    // onEndOfPage: controller.loadMoreVideos,
                    onEndOfPage: () {},
                    scrollOffset:
                        (MediaQuery.of(context).size.height - 50).toInt(),
                    child: ListView.separated(
                        separatorBuilder: (context, index) =>
                            const CustomDivider(),
                        itemCount: controller.videoFavorites.length,
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.vertical,
                        itemBuilder: (BuildContext context, int index) {
                          var video =
                              controller.videoFavorites.elementAt(index);
                          return Column(
                            children: [
                              VideoWidget(
                                video: video,
                                favorited: controller.videoFavorites.any(
                                    (element) =>
                                        element.id.videoId == video.id.videoId),
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
                                            video.snippet.thumbnails.high.url
                                      });
                                },
                              ),
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
