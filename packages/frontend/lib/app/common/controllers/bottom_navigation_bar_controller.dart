import 'package:flutter/material.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/activities_page/activities_page.dart';
import 'package:frontend/app/pages/events_page/events_page.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:frontend/app/pages/pendencies_page/pendencies_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:get/get.dart';

class BottomNavigationBarController extends GetxController {
  var accessControlController = Get.find<AccessControlController>();
  var currentIndex = 0.obs;
  List<Map<String, dynamic>> bottomNavigationBarItems = [
    {
      "label": "Home",
      "icon": Icons.home,
      "route": feedPageRoute,
      "visible": true
    },
    {
      "label": "Favoritos",
      "icon": Icons.star,
      "route": activitiesPageRoute,
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
      Navigation.popAndGoToPage(pageRoute: route);
    });

    ever(accessControlController.ehProfessor, (value) {
      if (accessControlController.ehProfessor.value) {
        for (var element in bottomNavigationBarItems) {
          if (element["label"] == "Atividades" ||
              element["label"] == "Pendências") {
            element["visible"] = true;
          }
        }
      }
    });

    super.onInit();
  }
}
