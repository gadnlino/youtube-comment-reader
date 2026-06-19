import 'package:flutter/material.dart';
import 'package:frontend/app/common/controllers/common/theme_controller.dart';
import 'package:get/get.dart';

class ThemeModeButton extends StatelessWidget {
  const ThemeModeButton({super.key});

  @override
  Widget build(BuildContext context) {
    final themeController = Get.find<ThemeController>();
    final iconColor = Theme.of(context).appBarTheme.iconTheme?.color;

    return Obx(() {
      final currentMode = themeController.themeMode.value;

      return PopupMenuButton<ThemeMode>(
        tooltip: 'Theme mode',
        icon: Icon(Icons.brightness_6, color: iconColor),
        onSelected: themeController.setThemeMode,
        itemBuilder: (context) => [
          _buildItem(
            label: 'Light',
            value: ThemeMode.light,
            currentMode: currentMode,
          ),
          _buildItem(
            label: 'Dark',
            value: ThemeMode.dark,
            currentMode: currentMode,
          ),
          _buildItem(
            label: 'System',
            value: ThemeMode.system,
            currentMode: currentMode,
          ),
        ],
      );
    });
  }

  PopupMenuItem<ThemeMode> _buildItem({
    required String label,
    required ThemeMode value,
    required ThemeMode currentMode,
  }) {
    return PopupMenuItem(
      value: value,
      child: Row(
        children: [
          SizedBox(
            width: 24,
            child: currentMode == value
                ? const Icon(Icons.check, size: 18)
                : null,
          ),
          Text(label),
        ],
      ),
    );
  }
}
