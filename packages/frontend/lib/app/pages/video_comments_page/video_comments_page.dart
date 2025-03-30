import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/comment_widget.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/controllers/common/favorites_controller.dart';
import 'package:frontend/app/common/controllers/pages/video_comments_page_controller.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:get/get.dart';
import 'package:html_unescape/html_unescape.dart';

const String videoCommentsPageRoute = "/video-comments";

class VideoCommentsPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => VideoCommentsPageController());
  }
}

class VideoCommentsPage extends GetView<VideoCommentsPageController> {
  final pageTitle = "Comments";

  late FavoritesController _favoritesController;

  VideoCommentsPage({super.key}) {
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
                      value: 'time',
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
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text("Commentary types:",
                        style: Theme.of(context).textTheme.labelLarge),
                  ),
                  CheckboxListTile(
                      title: const Text("Positives"),
                      value: controller.currentFilterOptions.value.showPositive,
                      onChanged: (val) {
                        var newFiltersOptions = FilterOptions.fromJson(
                            json.decode(json.encode(
                                controller.currentFilterOptions.value)));

                        newFiltersOptions.showPositive = val;

                        controller.currentFilterOptions.value =
                            newFiltersOptions;
                      }),
                  CheckboxListTile(
                    title: const Text("Negatives"),
                    value: controller.currentFilterOptions.value.showNegative,
                    onChanged: (val) {
                      var newFiltersOptions = FilterOptions.fromJson(
                          json.decode(json
                              .encode(controller.currentFilterOptions.value)));

                      newFiltersOptions.showNegative = val;

                      controller.currentFilterOptions.value = newFiltersOptions;
                    },
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      TextButton(
                        onPressed: () {
                          Navigator.of(context).pop();
                          controller.clearFilters();
                          controller.reloadComments();
                        },
                        child: const Text(
                          "Clear filters",
                          style: TextStyle(color: Colors.red),
                        ),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          Navigation.goBack();
                          controller.reloadComments();
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

  Widget _videoDescriptionSection(BuildContext context, String description) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Animated Size for smooth expanding/collapsing
        AnimatedSize(
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeInOut,
          child: ConstrainedBox(
            constraints: controller.videoDescriptionExpanded.value
                ? BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height *
                        .2) // No constraints when expanded
                : BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height *
                        0), // Limit height when collapsed
            child: SingleChildScrollView(
              child: Text(
                HtmlUnescape().convert(description),
                overflow: TextOverflow.fade,
                softWrap: true,
                style: const TextStyle(fontSize: 14, color: Colors.white70),
              ),
            ),
          ),
        ),

        // Show More / Show Less button
        GestureDetector(
          onTap: () {
            controller.videoDescriptionExpanded.value =
                !controller.videoDescriptionExpanded.value;
          },
          child: Padding(
            padding: const EdgeInsets.only(top: 5),
            child: Center(
              child: Text(
                controller.videoDescriptionExpanded.value
                    ? "Hide description"
                    : "Show description",
                style: const TextStyle(
                  color: Colors.white60,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(pageTitle),
          centerTitle: true,
          leading: IconButton(
              onPressed: () {
                Navigation.goBack();
              },
              icon: const Icon(Icons.arrow_back)),
          actions: [
            Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 3,
              ),
              child: IconButton(
                onPressed: () => controller.reloadComments(),
                icon: const Icon(Icons.refresh_sharp),
                color: Colors.white,
              ),
            ),
          ],
        ),
        body: Obx(
          () {
            if (controller.loadingComments.value || controller.loading.value) {
              return const Center(
                child: Padding(
                  padding: EdgeInsets.all(8.0),
                  child: CircularProgressIndicator(),
                ),
              );
            }

            bool videoFavorited = _favoritesController
                .existVideoFavorite(controller.selectedVideo.value!.id);

            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10.0),
              child: Column(
                children: [
                  const SizedBox(height: 2.5),
                  // Cabeçalho do Post
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Flexible(
                          child: Text(
                        controller.selectedVideo.value != null
                            ? HtmlUnescape().convert(
                                controller.selectedVideo.value!.snippet.title)
                            : "",
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      )),
                      IconButton(
                        icon: Icon(
                          videoFavorited ? Icons.star : Icons.star_border,
                          color: videoFavorited ? Colors.yellow : Colors.white,
                        ),
                        onPressed: () {
                          if (!videoFavorited) {
                            _favoritesController.addVideoFavorite(
                                controller.selectedVideo.value!);
                          } else {
                            _favoritesController.removeVideoFavorite(
                                controller.selectedVideo.value!);
                          }
                        },
                      )
                    ],
                  ),
                  const SizedBox(height: 10),
                  if (controller.selectedVideo.value != null &&
                      controller.selectedVideo.value!.snippet.thumbnails.high
                          .url.isNotEmpty)
                    // Imagem do Post
                    Image.network(
                      controller
                          .selectedVideo.value!.snippet.thumbnails.high.url,
                      height: MediaQuery.of(context).size.height * 0.2,
                      width: double.infinity,
                      fit: BoxFit.fitWidth,
                    ),
                  const SizedBox(height: 10),
                  // Comentário do Autor
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    _videoDescriptionSection(context,
                        controller.selectedVideo.value!.snippet.description),
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    const SizedBox(height: 10),
                  if (controller.selectedVideo.value != null &&
                      controller
                          .selectedVideo.value!.snippet.description.isNotEmpty)
                    const CustomDivider(),

                  const SizedBox(height: 10),
                  Row(
                    children: [
                      const Text(
                        "Comments",
                        style: TextStyle(color: Colors.white, fontSize: 20),
                      ),
                      const Spacer(),
                      IconButton(
                        onPressed: () =>
                            _showFilterBottomSheet(context: context),
                        icon: const Icon(Icons.tune_rounded),
                        color: Colors.white,
                      )
                    ],
                  ),
                  const SizedBox(height: 10),
                  // Lista Rolável de Comentários
                  Builder(builder: (ctx) {
                    if (controller.commentsDisabledForVideo.value) {
                      return const Expanded(
                          child: Center(
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Text(
                            "Comments disabled for this video :(",
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ),
                      ));
                    }

                    if (controller.commentsThreadList.isEmpty) {
                      return const Expanded(
                          child: Center(
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Text(
                            "No comments yet :/",
                            style: TextStyle(fontSize: 25, color: Colors.white),
                          ),
                        ),
                      ));
                    }

                    return Expanded(
                      child: ListView.builder(
                        itemCount: controller.commentsThreadList.length,
                        itemBuilder: (context, index) {
                          final comment =
                              controller.commentsThreadList.elementAt(index);
                          return Column(
                            children: [
                              Obx(
                                () {
                                  bool commentFavorited = _favoritesController
                                      .existCommentFavorite(comment.id);
                                  return CommentWidget(
                                    comment: comment.snippet.topLevelComment,
                                    replies: comment.replies?.comments,
                                    favorited: commentFavorited,
                                    onFavoriteTap: () {
                                      if (!commentFavorited) {
                                        _favoritesController.addCommentFavorite(
                                            comment.snippet.topLevelComment,
                                            comment.replies?.comments,
                                            controller.selectedVideo.value!.id,
                                            controller.selectedVideo.value
                                                ?.snippet.description,
                                            controller
                                                .selectedVideo
                                                .value
                                                ?.snippet
                                                .thumbnails
                                                .defaultThumbnail
                                                .url,
                                            controller.selectedVideo.value
                                                ?.snippet.title,
                                            controller.selectedVideo.value
                                                ?.snippet.channelTitle,
                                            controller.selectedVideo.value
                                                ?.snippet.publishedAt);
                                      } else {
                                        _favoritesController
                                            .removeCommentFavorite(comment
                                                .snippet.topLevelComment);
                                      }
                                    },
                                  );
                                },
                              )
                            ],
                          );
                        },
                      ),
                    );
                  }),
                ],
              ),
            );
          },
        ));
  }
}
