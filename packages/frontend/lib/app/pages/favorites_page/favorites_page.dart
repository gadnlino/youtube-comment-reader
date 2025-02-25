import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/video_widget.dart';
import 'package:frontend/app/common/controllers/favorites_page_controller.dart';
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
  const FavoritesPage({super.key});

  Widget _videoFavoritesView(BuildContext context) {
    return Obx(
      () {
        if (controller.loading.value) {
          return const Center(
            child: CircularProgressIndicator(
              color: Colors.white,
            ),
          );
        }

        if (controller.videoFavorites.isEmpty) {
          return const Expanded(
              child: Center(
            child: Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                "No videos favorited:(",
                style: TextStyle(fontSize: 25, color: Colors.white),
              ),
            ),
          ));
        }

        return Column(
          children: [
            Expanded(
              child: LazyLoadScrollView(
                isLoading: controller.loading.value,
                onEndOfPage: () {},
                scrollOffset: (MediaQuery.of(context).size.height - 50).toInt(),
                child: ListView.separated(
                    separatorBuilder: (context, index) => const CustomDivider(),
                    itemCount: controller.videoFavorites.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var video = controller.videoFavorites.elementAt(index);
                      return Column(
                        children: [
                          VideoWidget(
                            video: video,
                            favorited: controller.videoFavorites
                                .any((element) => element.id == video.id),
                            onFavoriteTap: () {
                              if (!controller.videoFavorites
                                  .any((element) => element.id == video.id)) {
                                controller.addVideoFavorite(video);
                              } else {
                                controller.removeVideoFavorite(video);
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
    return Obx(
      () {
        if (controller.loading.value) {
          return const Center(
            child: CircularProgressIndicator(
              color: Colors.white,
            ),
          );
        }

        if (controller.commentFavorites.isEmpty) {
          return const Expanded(
              child: Center(
            child: Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                "No comments favorited:(",
                style: TextStyle(fontSize: 25, color: Colors.white),
              ),
            ),
          ));
        }

        return Column(
          children: [
            Expanded(
              child: LazyLoadScrollView(
                isLoading: controller.loading.value,
                onEndOfPage: () {},
                scrollOffset: (MediaQuery.of(context).size.height - 50).toInt(),
                child: ListView.separated(
                    padding: const EdgeInsets.all(8.0),
                    separatorBuilder: (context, index) => const CustomDivider(),
                    itemCount: controller.commentFavorites.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var comment =
                          controller.commentFavorites.elementAt(index);
                      return Column(
                        children: [
                          Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4.0),
                            child: Text(
                              HtmlUnescape().convert(comment.videoTitle!),
                              style: const TextStyle(
                                  color: Colors.white, fontSize: 15),
                            ),
                          ),
                          Align(
                            alignment: Alignment.centerLeft,
                            child: Padding(
                              padding: const EdgeInsets.symmetric(
                                  vertical: 2.0, horizontal: 6.0),
                              child: Text(
                                '${comment.channelTitle} · ${Utils.formatDateOrNull(DateTime.parse(comment.videoPublishedAt!), 'dd/MM/yyyy')}',
                                style: TextStyle(
                                    fontSize: 12, color: Colors.grey[200]),
                              ),
                            ),
                          ),
                          CommentWidget(
                            comment: comment.comment!,
                            replies: comment.replies,
                            favorited: controller.commentFavorites.any(
                                (element) =>
                                    element.comment?.id == comment.comment?.id),
                            onFavoriteTap: () {
                              if (!controller.commentFavorites.any((element) =>
                                  element.comment?.id == comment.comment?.id)) {
                                controller.addCommentFavorite(
                                    comment.comment!, comment.replies);
                              } else {
                                controller
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
    return DefaultTabController(
        length: 2,
        child: Scaffold(
            appBar: AppBar(
              automaticallyImplyLeading: false,
              title: const Text(pageTitle),
              centerTitle: true,
              bottom: const TabBar(
                  indicatorColor: Colors.yellow,
                  labelColor: Colors.yellow,
                  unselectedLabelColor: Colors.white,
                  tabs: [
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
