import 'package:flutter/material.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/common/values/constants.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:get/get.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final _accessControlController = Get.find<AccessControlController>();
  CustomAppBar({super.key});

  Widget _buildAvatarWidget() {
    return Obx(() {
      Widget? child;
      dynamic backgroundImage;

      if (_accessControlController.arquivoFotoPessoa.value == null) {
        child = Text(_accessControlController.pessoaLogada.value!.nome != null
            ? Utils.getNameInitials(
                _accessControlController.pessoaLogada.value!.nome as String)
            : "");
      } else {
        backgroundImage = Image.file(
          _accessControlController.arquivoFotoPessoa.value!,
          fit: BoxFit.cover,
        ).image;
      }

      return CircleAvatar(
        backgroundColor: Colors.white,
        backgroundImage: backgroundImage,
        child: child,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text(
        Constants.appName,
        style: const TextStyle(fontSize: 30),
      ),
      actions: [
        InkWell(
            child: _buildAvatarWidget(),
            onTap: () {
              Navigation.popAndGoToPage(pageRoute: profilePageRoute);
            })
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
