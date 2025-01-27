import 'dart:typed_data';

import 'package:dio/dio.dart';

class ClientHttpPackage {
  final Dio _dio = Dio();

  Future<Response> get(
      {required String url,
      Map<String, dynamic>? queryParameters,
      Options? options}) async {
    Response response =
        await _dio.get(url, queryParameters: queryParameters, options: options);

    return response;
  }

  Future<Uint8List> getBytes(
      {required String url, Map<String, dynamic>? queryParameters}) async {
    var response =
        await _dio.get(url, options: Options(responseType: ResponseType.bytes));

    return response.data;
  }

  Future<Response> post(
      {required String url,
      required dynamic data,
      Map<String, dynamic>? queryParameters}) async {
    Response response = await _dio.post(url,
        data: data,
        queryParameters: queryParameters,
        options: Options(contentType: "application/json"));

    return response;
  }

  Future<Response> put(
      {required String url,
      required dynamic data,
      Map<String, dynamic>? queryParameters,
      Options? options}) async {
    Response response = await _dio.put(url,
        data: data, queryParameters: queryParameters, options: options);

    return response;
  }

  Future<Response> delete(
      {required String url,
      dynamic data,
      Map<String, dynamic>? queryParameters}) async {
    Response response =
        await _dio.delete(url, data: data, queryParameters: queryParameters);

    return response;
  }
}
