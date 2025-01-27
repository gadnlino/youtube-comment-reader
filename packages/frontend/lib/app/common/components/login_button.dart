import 'package:flutter/material.dart';
import 'package:social_login_buttons/social_login_buttons.dart';

class LoginButton extends StatelessWidget {
  final SocialLoginButtonType socialMedia;
  final String? text;
  final Function onPressed;

  const LoginButton(
      {super.key,
      required this.socialMedia,
      required this.onPressed,
      this.text});
  @override
  Widget build(BuildContext context) {
    return SocialLoginButton(
      text: text,
      buttonType: socialMedia,
      onPressed: () => onPressed(),
    );
  }
}
