import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/login_button.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/packages/cache_package.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:get/get.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:social_login_buttons/social_login_buttons.dart';

const String loginPageRoute = "/login";

class LoginPage extends StatelessWidget {
  final AccessControlController _accessControlController =
      Get.find<AccessControlController>();

  LoginPage({super.key}) {
    var cachePackage = CachePackage();

    (() async {
      var signInMethod = await cachePackage.getString('signInMethod');

      if (signInMethod != '' && signInMethod != null) {
        try {
          await _accessControlController.doLogin(signInMethod, silently: true);
        } catch (e) {
          debugPrint(e.toString());
        }
      }
    })();
  }

  Widget _buildTitleSection() {
    return const Padding(
      padding: EdgeInsets.all(32),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  "BEM VINDO",
                  style: TextStyle(
                    fontFamily: "Poppins",
                    fontWeight: FontWeight.bold,
                    fontSize: 40,
                    color: Colors.white,
                  ),
                ),
                Text(
                  "AO jAPP",
                  style: TextStyle(
                    fontFamily: "Poppins",
                    fontWeight: FontWeight.bold,
                    fontSize: 40,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildButtonSection() {
    return SizedBox(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Padding(
            padding: const EdgeInsets.all(10),
            child: LoginButton(
                text: "Login com o Facebook",
                socialMedia: SocialLoginButtonType.facebook,
                onPressed: () {}),
          ),
          Padding(
              padding: const EdgeInsets.all(10),
              child: LoginButton(
                  text: "Login com a conta do Google",
                  socialMedia: SocialLoginButtonType.google,
                  onPressed: () async {
                    await _accessControlController.doLogin('GOOGLE');
                  })),
        ],
      ),
    );
  }

  Widget _buildImageSection() {
    return const Image(
      image: AssetImage('assets/images/login_image_01.jpg'),
      height: 360,
      fit: BoxFit.cover,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildImageSection(),
            const SizedBox(
              height: 20,
            ),
            _buildTitleSection(),
            const SizedBox(
              height: 20,
            ),
            _buildButtonSection(),
          ],
        ),
      ),
    );
  }
}
