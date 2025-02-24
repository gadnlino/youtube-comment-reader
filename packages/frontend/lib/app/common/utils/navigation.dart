import 'package:get/get.dart';

class Navigation {
  static currentPage() {
    return Get.currentRoute;
  }

  static goToPage(
      {required String pageRoute, Map<String, String>? parameters}) async {
    await Get.toNamed(pageRoute, parameters: parameters);
  }

  static popAndGoToPage(
      {required String pageRoute, Map<String, String>? parameters}) async {
    await Get.offAllNamed(pageRoute, parameters: parameters);
  }

  static goBack() {
    Get.back();
  }
}
