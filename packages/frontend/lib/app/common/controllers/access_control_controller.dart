import 'dart:io';

import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/packages/cache_package.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:frontend/app/pages/login_page/login_page.dart';
import 'package:frontend/app/pages/user_registration_page/user_registration_page.dart';
import 'package:get/get.dart';
import 'package:google_sign_in/google_sign_in.dart';

class AccessControlController extends GetxController {
  final _cachePackage = CachePackage();
  final GoogleSignIn _googleSignIn = GoogleSignIn(scopes: ["profile", "email"]);
  final BjjApi _bjjApi = BjjApi();
  // final _pessoaController = Get.find<PessoaController>();
  final _mediaController = Get.find<MediaController>();
  Rxn<Pessoa> pessoaLogada = Rxn(null);
  Rxn<File> arquivoFotoPessoa = Rxn(null);
  Rx<String> emailPessoaLogada = ''.obs;
  Rx<String> nomePessoaLogada = ''.obs;
  Rx<String> urlFotoPessoaLogada = ''.obs;
  Rx<bool> ehProfessor = false.obs;
  Rx<bool> loading = false.obs;

  @override
  void onInit() {
    ever(emailPessoaLogada, (email) async {
      try {
        loading.value = true;

        if (pessoaLogada.value != null) {
          //carrega foto da pessoa logada
          if (pessoaLogada.value!.idFoto != null) {
            if (pessoaLogada.value!.idFoto != null) {
              int idMedia = pessoaLogada.value!.idFoto!;

              Midia? fotoPessoa = await _mediaController.storeMedia(idMedia);

              if (fotoPessoa != null) {
                arquivoFotoPessoa.value =
                    await _mediaController.getMediaFile(idMedia);
              }
            }
          }
        }
      } finally {
        loading.value = false;
      }
    });

    super.onInit();
  }

  Future doLogin(String signInMethod, {bool silently = false}) async {
    if (signInMethod == 'GOOGLE') {
      try {
        GoogleSignInAccount? googleSignInAccount;

        if (!silently) {
          googleSignInAccount = await _googleSignIn.signIn();
        } else {
          googleSignInAccount =
              await _googleSignIn.signInSilently(suppressErrors: false);
        }

        if (googleSignInAccount != null) {
          final GoogleSignInAuthentication googleSignInAuthentication =
              await googleSignInAccount.authentication;

          final AuthCredential credential = GoogleAuthProvider.credential(
            accessToken: googleSignInAuthentication.accessToken,
            //https://stackoverflow.com/a/77430388
            idToken: googleSignInAuthentication.idToken,
          );

          final UserCredential userCredential =
              await FirebaseAuth.instance.signInWithCredential(credential);

          final User? user = userCredential.user;

          if (user != null) {
            // Cache id and access tokens

            await _cachePackage.putString(
                'idToken', googleSignInAuthentication.idToken ?? '');

            await _cachePackage.putString(
                'accessToken', googleSignInAuthentication.accessToken ?? '');

            await _cachePackage.putString('signInMethod', signInMethod);

            if (user.email != null) {
              emailPessoaLogada.value = user.email!;
            }

            if (user.photoURL != null) {
              urlFotoPessoaLogada.value = user.photoURL!;
            }

            if (user.displayName != null) {
              nomePessoaLogada.value = user.displayName!;
            }

            var usuarioExistente = await _bjjApi.buscarPessoa(
              user.email!,
            );

            pessoaLogada.value = await _bjjApi.buscarPessoa(user.email!);

            if (pessoaLogada.value != null) {
              ehProfessor.value =
                  await _bjjApi.pessoaEhProfessor(pessoaLogada.value!.email!);
            } else {
              ehProfessor.value = false;
            }

            if (usuarioExistente != null) {
              Navigation.popAndGoToPage(pageRoute: feedPageRoute);
            } else {
              Navigation.popAndGoToPage(pageRoute: userRegistrationPageRoute);
            }
          }
        }
      } catch (e) {
        debugPrint(e.toString());
        rethrow;
      }
    }
  }

  Future doLogout() async {
    if (await _googleSignIn.isSignedIn()) {
      await _googleSignIn.signOut();

      await _cachePackage.deleteString('idToken');

      await _cachePackage.deleteString('accessToken');

      await _cachePackage.deleteString('signInMethod');

      Navigation.popAndGoToPage(pageRoute: loginPageRoute);
    }
  }
}
