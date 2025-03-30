import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/video_widget.dart';
import 'package:frontend/app/common/controllers/common/favorites_controller.dart';
import 'package:frontend/app/common/controllers/pages/video_search_page_controller.dart';
import 'package:frontend/app/common/models/models.dart';
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
  final pageTitle = "Youtube Comment Reader";
  late FavoritesController _favoritesController;

  VideoSearchPage({super.key}) {
    _favoritesController = Get.find<FavoritesController>();
  }

  void _showFilterBottomSheet({
    required BuildContext context,
  }) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) {
        final keywordsController = TextEditingController(
            text: controller.currentFilterOptions.value.keywords);

        keywordsController.addListener(
          () {
            var newFiltersOptions = FilterOptions.fromJson(json
                .decode(json.encode(controller.currentFilterOptions.value)));

            newFiltersOptions.keywords = keywordsController.text;

            controller.currentFilterOptions.value = newFiltersOptions;
          },
        );

        return Obx(() => Padding(
              padding: EdgeInsets.only(
                bottom: MediaQuery.of(context).viewInsets.bottom,
                left: 16,
                right: 16,
                top: 24,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text("Search filters",
                      style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 16),
                  TextField(
                    controller: keywordsController,
                    decoration: const InputDecoration(
                      labelText: 'keywords',
                      hintText: 'Ex: flutter performance android',
                      border: OutlineInputBorder(),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text("Sort by:",
                        style: Theme.of(context).textTheme.labelLarge),
                  ),
                  RadioListTile<String>(
                    title: const Text("Most relevant"),
                    value: 'relevance',
                    groupValue: controller.currentFilterOptions.value.order,
                    onChanged: (val) {
                      var newFiltersOptions = FilterOptions.fromJson(
                          json.decode(json
                              .encode(controller.currentFilterOptions.value)));

                      newFiltersOptions.order = val;

                      controller.currentFilterOptions.value = newFiltersOptions;
                    },
                  ),
                  RadioListTile<String>(
                      title: const Text("Most recent"),
                      value: 'date',
                      groupValue: controller.currentFilterOptions.value.order,
                      onChanged: (val) {
                        var newFiltersOptions = FilterOptions.fromJson(
                            json.decode(json.encode(
                                controller.currentFilterOptions.value)));

                        newFiltersOptions.order = val;

                        controller.currentFilterOptions.value =
                            newFiltersOptions;
                      }),
                  const SizedBox(height: 8),
                  // Align(
                  //   alignment: Alignment.centerLeft,
                  //   child: Text("Commentary types:",
                  //       style: Theme.of(context).textTheme.labelLarge),
                  // ),
                  // CheckboxListTile(
                  //     title: const Text("Positives"),
                  //     value: controller.currentFilterOptions.value.showPositive,
                  //     onChanged: (val) {
                  //       var newFiltersOptions = FilterOptions.fromJson(
                  //           json.decode(json.encode(
                  //               controller.currentFilterOptions.value)));

                  //       newFiltersOptions.showPositive = val;

                  //       controller.currentFilterOptions.value =
                  //           newFiltersOptions;
                  //     }),
                  // CheckboxListTile(
                  //   title: const Text("Negatives"),
                  //   value: controller.currentFilterOptions.value.showNegative,
                  //   onChanged: (val) {
                  //     var newFiltersOptions = FilterOptions.fromJson(
                  //         json.decode(json
                  //             .encode(controller.currentFilterOptions.value)));

                  //     newFiltersOptions.showNegative = val;

                  //     controller.currentFilterOptions.value = newFiltersOptions;
                  //   },
                  // ),
                  // const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      TextButton(
                        onPressed: () {
                          Navigator.of(context).pop();
                          controller.clearFilters();
                          controller.reloadVideos();
                        },
                        child: const Text(
                          "Clear filters",
                          style: TextStyle(color: Colors.red),
                        ),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          Navigation.goBack();
                          controller.customSearch();
                        },
                        child: const Text("Search"),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                ],
              ),
            ));
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          automaticallyImplyLeading: false,
          centerTitle: true,
          title: Text(pageTitle),
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 3,
              ),
              child: IconButton(
                onPressed: () {
                  controller.reloadVideos();
                },
                icon: const Icon(Icons.refresh_sharp),
                color: Colors.white,
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 3,
              ),
              child: IconButton(
                onPressed: () => _showFilterBottomSheet(context: context),
                icon: const Icon(Icons.tune_rounded),
                color: Colors.white,
              ),
            )
          ],
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
                                  favorited: _favoritesController
                                      .existVideoFavorite(video.id),
                                  onFavoriteTap: () {
                                    if (!_favoritesController
                                        .existVideoFavorite(video.id)) {
                                      _favoritesController
                                          .addVideoFavorite(video);
                                    } else {
                                      _favoritesController
                                          .removeVideoFavorite(video);
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
