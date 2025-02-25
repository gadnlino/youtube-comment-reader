import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/video_widget.dart';
import 'package:frontend/app/common/controllers/video_search_page_controller.dart';
import 'package:frontend/app/common/utils/navigation.dart';
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

class VideoSearchPage extends GetView<VideoSearchPageController> {
  const VideoSearchPage({super.key});

  void _showVideoSearchDialog() {
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
  }

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Youtube Comment Reader";
    return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
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
                onPressed: _showVideoSearchDialog,
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
                                  favorited: controller.videoFavorites
                                      .any((element) => element.id == video.id),
                                  onFavoriteTap: () {
                                    if (!controller.videoFavorites.any(
                                        (element) => element.id == video.id)) {
                                      controller.addVideoFavorite(video);
                                    } else {
                                      controller.removeVideoFavorite(video);
                                    }
                                  },
                                  onTap: () {
                                    Navigation.goToPage(
                                        pageRoute: videoCommentsPageRoute,
                                        parameters: {
                                          'video': jsonEncode(video)
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
