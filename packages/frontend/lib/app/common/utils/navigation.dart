import 'package:get/get.dart';

class Navigation {
  static currentPage() {
    return Get.currentRoute;
  }

  static goToPage(
      {required String pageRoute, Map<String, String>? parameters}) {
    Get.to(pageRoute, arguments: parameters);
  }

  static popAndGoToPage(
      {required String pageRoute, Map<String, String>? parameters}) {
    Get.offAllNamed(pageRoute, parameters: parameters);
  }

  static goBack() {
    Get.back();
  }
}
