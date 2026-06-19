import 'package:flutter/material.dart';
import 'package:frontend/app/common/controllers/common/bottom_navigation_bar_controller.dart';
import 'package:get/get.dart';

class CustomBottomNavigationBar extends StatelessWidget {
  final double iconSize = 30;

  const CustomBottomNavigationBar({super.key});

  List<BottomNavigationBarItem> getBottomNavigationBarItemList(
      BuildContext context, List<Map<String, dynamic>> items) {
    final navTheme = Theme.of(context).bottomNavigationBarTheme;

    return items
        .map((e) => BottomNavigationBarItem(
              icon: Icon(e["icon"]),
              label: e["label"],
              backgroundColor: navTheme.backgroundColor,
            ))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final navTheme = Theme.of(context).bottomNavigationBarTheme;

    return GetBuilder<BottomNavigationBarController>(builder: (controller) {
      var visibleItems = controller.getVisibleItems();

      return BottomNavigationBar(
        type: visibleItems.length > 1
            ? BottomNavigationBarType.fixed
            : BottomNavigationBarType.shifting,
        selectedItemColor: navTheme.selectedItemColor,
        unselectedItemColor: navTheme.unselectedItemColor,
        currentIndex: controller.currentIndex.value,
        iconSize: iconSize,
        onTap: controller.setCurrentElement,
        items: getBottomNavigationBarItemList(context, visibleItems),
      );
    });
  }
}
