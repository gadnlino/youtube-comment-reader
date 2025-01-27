import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter_cache_manager/flutter_cache_manager.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/packages/cache_package.dart';
import 'package:frontend/app/common/packages/client_http_package.dart';
import 'package:get/get.dart';
import 'package:mime/mime.dart';

class MediaController extends GetxController {
  RxMap<int, Midia> midias = RxMap();
  final CachePackage _cachePackage = CachePackage();
  final ClientHttpPackage _clientHttpPackage = ClientHttpPackage();
  final BjjApi _bjjApi = BjjApi();
  final Map<int, DateTime> _tempoExpiracaoMidias = {};
  final int _tempoExpiracaoPadraoMidia = 90;

  void _setMedia(Midia media) {
    midias[media.idMidia!] = media;
    _tempoExpiracaoMidias[media.idMidia!] =
        DateTime.now().add(Duration(seconds: _tempoExpiracaoPadraoMidia));
  }

  Future downloadAndStoreFileFromUrl(String url) async {
    var imageBytes = await _clientHttpPackage.getBytes(url: url);

    await _cachePackage.putFile(
      fileUrl: url,
      fileBytes: imageBytes,
    );
  }

  Future<File> getDownloadedFileMedia(String url) async {
    return await _cachePackage.getFile(fileUrl: url);
  }

  Midia? getMedia(int? idMedia) {
    if (midias.containsKey(idMedia) &&
        _tempoExpiracaoMidias[idMedia!]!.compareTo(
                DateTime.now().subtract(const Duration(minutes: 1))) >
            0) {
      return midias[idMedia];
    }

    return null;
  }

  Future<File?> getMediaFile(int idMedia) async {
    Midia? m = getMedia(idMedia);

    if (m == null) return null;

    return await _cachePackage.getFile(fileUrl: m.urlMidia!);
  }

  Future<Midia?> storeMedia(int idMidia) async {
    var m = getMedia(idMidia);

    if (m != null) return m;

    Midia? midia = await _bjjApi.downloadMidia(idMidia);

    if (midia == null) return null;

    if (midia.urlMidia != null) {
      var imageBytes = await _clientHttpPackage.getBytes(url: midia.urlMidia!);

      await _cachePackage.putFile(
        fileUrl: midia.urlMidia!,
        fileBytes: imageBytes,
      );
    }

    _setMedia(midia);

    return midia;
  }

  Future<Midia> uploadMedia(Midia media, File file) async {
    var createdMedia = await _bjjApi.uploadMidia(media);

    String uploadUrl = createdMedia.urlMidia!;

    final len = await file.length();

    final mimeType = lookupMimeType(file.path);

    await _clientHttpPackage.put(
        url: uploadUrl,
        data: file.openRead(),
        options: Options(headers: {
          Headers.contentLengthHeader: len,
          Headers.contentTypeHeader: mimeType
        }));

    return createdMedia;
  }
}
