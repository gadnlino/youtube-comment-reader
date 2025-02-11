import 'dart:convert';

import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/packages/cache_package.dart';

class FavoriteManager {
  final CachePackage _cachePackage = CachePackage();

  final String videoCacheKey = 'ycr:favorites:videos';
  final String commentsCacheKey = 'ycr:favorites:comments';

  Future<List<YouTubeSearchItem>?> getVideoFavorites() async {
    String? resultStr = await _cachePackage.getString(videoCacheKey);

    List<YouTubeSearchItem>? result;

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeSearchItem.fromJson(e))
          .toList();
    }

    return result;
  }

  Future addVideoFavorite(YouTubeSearchItem video) async {
    String? resultStr = await _cachePackage.getString(videoCacheKey);

    List<YouTubeSearchItem>? result = List.empty();

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeSearchItem.fromJson(e))
          .toList();
    }

    await _cachePackage.putString(videoCacheKey, jsonEncode(result));
  }

  Future removeVideoFavorite(YouTubeSearchItem video) async {
    String? resultStr = await _cachePackage.getString(videoCacheKey);

    List<YouTubeSearchItem>? result = List.empty();

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeSearchItem.fromJson(e))
          .where((element) => element.id != video.id)
          .toList();
    }

    await _cachePackage.putString(videoCacheKey, jsonEncode(result));
  }

  Future<List<YouTubeCommentThreadSnippet>?> getCommentFavorites() async {
    String? resultStr = await _cachePackage.getString(commentsCacheKey);

    List<YouTubeCommentThreadSnippet>? result;

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeCommentThreadSnippet.fromJson(e))
          .toList();
    }

    return result;
  }
}
