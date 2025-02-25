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

    List<YouTubeSearchItem>? result = List.empty(growable: true);

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeSearchItem.fromJson(e))
          .toList();
    }

    result.add(video);

    await _cachePackage.putString(videoCacheKey, jsonEncode(result));
  }

  Future removeVideoFavorite(YouTubeSearchItem video) async {
    String? resultStr = await _cachePackage.getString(videoCacheKey);

    List<YouTubeSearchItem>? result = List.empty(growable: true);

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => YouTubeSearchItem.fromJson(e))
          .where((element) => element.id != video.id)
          .toList();
    }

    await _cachePackage.putString(videoCacheKey, jsonEncode(result));
  }

  Future<List<CommentFavorite>?> getCommentFavorites() async {
    String? resultStr = await _cachePackage.getString(commentsCacheKey);

    List<CommentFavorite>? result;

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => CommentFavorite.fromJson(e))
          .toList();
    }

    return result;
  }

  Future addCommentFavorite(CommentFavorite comment) async {
    String? resultStr = await _cachePackage.getString(commentsCacheKey);

    List<CommentFavorite>? result = List.empty(growable: true);

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => CommentFavorite.fromJson(e))
          .toList();
    }

    result.add(comment);

    await _cachePackage.putString(commentsCacheKey, jsonEncode(result));
  }

  Future removeCommentFavorite(YouTubeComment comment) async {
    String? resultStr = await _cachePackage.getString(commentsCacheKey);

    List<CommentFavorite>? result = List.empty(growable: true);

    if (resultStr != null && resultStr.isNotEmpty) {
      result = (jsonDecode(resultStr) as List)
          .map((e) => CommentFavorite.fromJson(e))
          .where((element) => element.comment?.id != comment.id)
          .toList();
    }

    await _cachePackage.putString(commentsCacheKey, jsonEncode(result));
  }
}
