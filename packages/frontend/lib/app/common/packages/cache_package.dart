import 'dart:io';
import 'dart:typed_data';

import 'package:flutter_cache_manager/flutter_cache_manager.dart';
import 'package:shared_preferences/shared_preferences.dart';

class CachePackage {
  Future putString(String key, String value) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();

    await prefs.setString(key, value);
  }

  Future<String?> getString(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();

    return prefs.getString(key);
  }

  Future deleteString(String key) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();

    await prefs.remove(key);
  }

  Future putFile(
      {required String fileUrl, required Uint8List fileBytes}) async {
    await DefaultCacheManager().putFile(
      fileUrl,
      fileBytes,
    );
  }

  Future<File> getFile({required String fileUrl}) async {
    return await DefaultCacheManager().getSingleFile(fileUrl);
  }
}
