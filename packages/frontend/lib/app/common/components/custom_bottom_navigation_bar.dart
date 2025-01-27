import 'package:flutter/material.dart';
import 'package:frontend/app/common/controllers/bottom_navigation_bar_controller.dart';
import 'package:frontend/app/common/themes/app_theme.dart';
import 'package:get/get.dart';

class CustomBottomNavigationBar extends StatelessWidget {
  final double iconSize = 30;

  const CustomBottomNavigationBar({super.key});

  List<BottomNavigationBarItem> getBottomNavigationBarItemList(
      List<Map<String, dynamic>> items) {
    return items
        .map((e) => BottomNavigationBarItem(
              icon: Icon(e["icon"]),
              label: e["label"],
              backgroundColor: appBackgroungColorDarkTheme,
            ))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    return GetBuilder<BottomNavigationBarController>(builder: (controller) {
      var visibleItems = controller.getVisibleItems();

      return BottomNavigationBar(
        type: visibleItems.length > 1
            ? BottomNavigationBarType.fixed
            : BottomNavigationBarType.shifting,
        selectedItemColor: const Color(0xffFFF50A),
        unselectedItemColor: Colors.white,
        currentIndex: controller.currentIndex.value,
        iconSize: iconSize,
        onTap: controller.setCurrentElement,
        items: getBottomNavigationBarItemList(visibleItems),
      );
    });
  }
}
