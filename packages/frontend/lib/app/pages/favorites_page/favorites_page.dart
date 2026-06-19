import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/theme_mode_button.dart';
import 'package:frontend/app/common/components/video_widget.dart';
import 'package:frontend/app/common/controllers/common/favorites_controller.dart';
import 'package:frontend/app/common/controllers/pages/favorites_page_controller.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/video_comments_page/video_comments_page.dart';
import 'package:get/get.dart';
import 'package:html_unescape/html_unescape.dart';
import 'package:lazy_load_scrollview/lazy_load_scrollview.dart';

const String favoritesPageRoute = "/favorites";

class FavoritesPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => FavoritesPageController());
  }
}

class FavoritesPage extends GetView<FavoritesPageController> {
  late FavoritesController _favoritesController;

  FavoritesPage({super.key}) {
    _favoritesController = Get.find<FavoritesController>();
  }

  Widget _videoFavoritesView(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Obx(
      () {
        if (_favoritesController.loading.value) {
          return Center(
            child: CircularProgressIndicator(
              color: Theme.of(context).colorScheme.onSurface,
            ),
          );
        }

        if (_favoritesController.videoFavorites.isEmpty) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "No videos favorited:(",
                style: textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
            ),
          );
        }

        return Column(
          children: [
            Expanded(
              child: LazyLoadScrollView(
                isLoading: _favoritesController.loading.value,
                onEndOfPage: () {},
                scrollOffset: (MediaQuery.of(context).size.height - 50).toInt(),
                child: ListView.separated(
                    separatorBuilder: (context, index) => const CustomDivider(),
                    itemCount: _favoritesController.videoFavorites.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var video =
                          _favoritesController.videoFavorites.elementAt(index);
                      return Column(
                        children: [
                          VideoWidget(
                            video: video,
                            favorited: _favoritesController.videoFavorites
                                .any((element) => element.id == video.id),
                            onFavoriteTap: () {
                              if (!_favoritesController.videoFavorites
                                  .any((element) => element.id == video.id)) {
                                _favoritesController.addVideoFavorite(video);
                              } else {
                                _favoritesController.removeVideoFavorite(video);
                              }
                            },
                            onTap: () {
                              Navigation.goToPage(
                                  pageRoute: videoCommentsPageRoute,
                                  parameters: {'video': jsonEncode(video)});
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
    );
  }

  Widget _commentFavoritesView(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;

    return Obx(
      () {
        if (_favoritesController.loading.value) {
          return Center(
            child: CircularProgressIndicator(
              color: Theme.of(context).colorScheme.onSurface,
            ),
          );
        }

        if (_favoritesController.commentFavorites.isEmpty) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "No comments favorited:(",
                style: textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
            ),
          );
        }

        return Column(
          children: [
            Expanded(
              child: LazyLoadScrollView(
                isLoading: _favoritesController.loading.value,
                onEndOfPage: () {},
                scrollOffset: (MediaQuery.of(context).size.height - 50).toInt(),
                child: ListView.separated(
                    padding: const EdgeInsets.all(8.0),
                    separatorBuilder: (context, index) => const CustomDivider(),
                    itemCount: _favoritesController.commentFavorites.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var comment = _favoritesController.commentFavorites
                          .elementAt(index);
                      return Column(
                        children: [
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Text(
                              HtmlUnescape().convert(comment.videoTitle!),
                              style: textTheme.titleMedium,
                            ),
                          ),
                          Align(
                            alignment: Alignment.centerLeft,
                            child: Padding(
                              padding: const EdgeInsets.symmetric(
                                  vertical: 2.0, horizontal: 6.0),
                              child: Text(
                                '${comment.channelTitle} · ${Utils.formatDateOrNull(DateTime.parse(comment.videoPublishedAt!), 'dd/MM/yyyy')}',
                                style: textTheme.bodySmall,
                              ),
                            ),
                          ),
                          CommentWidget(
                            comment: comment.comment!,
                            replies: comment.replies,
                            favorited: _favoritesController.commentFavorites
                                .any((element) =>
                                    element.comment?.id == comment.comment?.id),
                            onFavoriteTap: () {
                              if (!_favoritesController.commentFavorites.any(
                                  (element) =>
                                      element.comment?.id ==
                                      comment.comment?.id)) {
                                _favoritesController.addCommentFavorite(
                                    comment.comment!,
                                    comment.replies,
                                    comment.videoId,
                                    comment.videoDescription,
                                    comment.videoThumbnailUrl,
                                    comment.videoTitle,
                                    comment.channelTitle,
                                    comment.videoPublishedAt);
                              } else {
                                _favoritesController
                                    .removeCommentFavorite(comment.comment!);
                              }
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
    );
  }

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Favorites";
    final tabBarTheme = Theme.of(context).tabBarTheme;

    return DefaultTabController(
        length: 2,
        child: Scaffold(
            appBar: AppBar(
              automaticallyImplyLeading: false,
              title: const Text(pageTitle),
              centerTitle: true,
              actions: const [ThemeModeButton()],
              bottom: TabBar(
                  indicatorColor: tabBarTheme.indicatorColor,
                  labelColor: tabBarTheme.labelColor,
                  unselectedLabelColor: tabBarTheme.unselectedLabelColor,
                  tabs: const [
                    Tab(
                      text: "Comments",
                      icon: Icon(Icons.comment),
                    ),
                    Tab(
                      text: "Videos",
                      icon: Icon(Icons.video_library),
                    ),
                  ]),
            ),
            bottomNavigationBar: const CustomBottomNavigationBar(),
            body: TabBarView(
              children: [
                _commentFavoritesView(context),
                _videoFavoritesView(context),
              ],
            )));
  }
}
