import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/exceptions/CommentsDisabledException.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/dto/pessoa_academia_dto.dart';
import 'package:frontend/app/common/models/dto/pessoa_federacao_dto.dart';
import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/dto/professor_pessoa_dto.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:frontend/app/common/models/graduacao.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/packages/client_http_package.dart';
import 'package:frontend/app/common/values/constants.dart';

class YoutubeCommentViewerApi {
  final ClientHttpPackage _clientHttp = ClientHttpPackage();

  Future<YouTubeSearchResponse?> searchVideos(
      YouTubeSearchParams params) async {
    Response? response;

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
