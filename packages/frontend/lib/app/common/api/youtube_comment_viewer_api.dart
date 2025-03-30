import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/exceptions/comments_disabled_exception.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/packages/client_http_package.dart';
import 'package:frontend/app/common/values/constants.dart';

class YoutubeCommentViewerApi {
  final ClientHttpPackage _clientHttp = ClientHttpPackage();

  Future<YouTubeSearchResponse?> searchVideos(
      YouTubeSearchParams params) async {
    Response? response;

    debugPrint('search videos with the following parameters:');
    debugPrint(jsonEncode(params.toJson()));

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/search", queryParameters: params.toJson());

      if (response.statusCode! >= 200 &&
          response.statusCode! <= 299 &&
          response.data != null) {
        return YouTubeSearchResponse.fromJson(response.data);
      }

      return null;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<YouTubeCommentThreadsResponse?> fetchComments(
      YouTubeCommentThreadsParams params) async {
    Response? response;

    if (params.searchTerms != null &&
        params.searchTerms!.isNotEmpty &&
        params.order == 'relevance') {
      params.order = null;
    }

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/video/comments",
          queryParameters: params.toJson(),
          options: Options(
              validateStatus: (status) =>
                  status != null &&
                  ((status >= 200 && status <= 299) || status == 403)));

      if (response.statusCode! >= 200 &&
          response.statusCode! <= 299 &&
          response.data != null) {
        return YouTubeCommentThreadsResponse.fromJson(response.data);
      }

      if (response.statusCode == 403 &&
          response.data != null &&
          (response.data as String).contains("commentsDisabled")) {
        throw CommentsDisabledException(
            "Comments are disable for this video/live");
      }

      return null;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<CommentsListResponse?> fetchCommentReplies(
      CommentsListParams params) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/video/comments",
          queryParameters: params.toJson());

      if (response.statusCode! >= 200 &&
          response.statusCode! <= 299 &&
          response.data != null) {
        return CommentsListResponse.fromJson(response.data);
      }

      return null;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }
}
