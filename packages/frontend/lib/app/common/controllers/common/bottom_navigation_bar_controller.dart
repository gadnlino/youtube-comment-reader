import 'package:flutter/material.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/favorites_page/favorites_page.dart';
import 'package:frontend/app/pages/video_search_page/video_search_page.dart';
import 'package:get/get.dart';

class BottomNavigationBarController extends GetxController {
  var currentIndex = 0.obs;
  List<Map<String, dynamic>> bottomNavigationBarItems = [
    {
      "label": "Home",
      "icon": Icons.home,
      "route": videoSearchPageRoute,
      "visible": true
    },
    {
      "label": "Favorites",
      "icon": Icons.star,
      "route": favoritesPageRoute,
      "visible": true
    },
  ];

  getVisibleItems() =>
      bottomNavigationBarItems.where((e) => e["visible"] == true).toList();

  setCurrentElement(int idx) {
    currentIndex.value = idx;
  }

  @override
  void onInit() {
    ever(currentIndex, (value) {
      String route = getVisibleItems()[value]["route"];
      Navigation.goToPage(pageRoute: route);
    });

    super.onInit();
  }
}
