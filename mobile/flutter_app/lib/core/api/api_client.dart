import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

/// Global ApiClient provider — tüm API servisleri buradan tüketir.
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());

/// API Client — tüm HTTP isteklerin geçtiği merkezi nokta.
/// JWT token otomatik olarak eklenir, 401'de refresh denenir.
class ApiClient {
  // Bilgisayar IP'si — Aynı Wi-Fi'de çalışır
  static const String baseUrl = 'http://192.168.1.21:8000/api/v1';
  // Production: https://api.smartcampusai.com/api/v1

  static const _storage = FlutterSecureStorage();
  late final Dio _dio;

  ApiClient() {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 20),
      contentType: 'application/json',
    ));

    _dio.interceptors.add(_AuthInterceptor(_storage, _dio));
    _dio.interceptors.add(PrettyDioLogger(
      requestHeader: false,
      requestBody: true,
      responseBody: true,
      responseHeader: false,
      compact: true,
    ));
  }

  Future<Response> get(String path, {Map<String, dynamic>? params}) async {
    return _dio.get(path, queryParameters: params);
  }

  Future<Response> post(String path, {dynamic data}) async {
    return _dio.post(path, data: data);
  }

  Future<Response> put(String path, {dynamic data}) async {
    return _dio.put(path, data: data);
  }

  Future<Response> delete(String path) async {
    return _dio.delete(path);
  }

  Dio get dio => _dio;
}


/// Access token ekleyen + 401'de refresh eden interceptor.
class _AuthInterceptor extends Interceptor {
  final FlutterSecureStorage _storage;
  final Dio _dio;

  _AuthInterceptor(this._storage, this._dio);

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Access token ekle (login/refresh disinda)
    if (!options.path.contains('/auth/login') &&
        !options.path.contains('/auth/refresh')) {
      final token = await _storage.read(key: 'access_token');
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }
    handler.next(options);
  }

  @override
  Future<void> onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401 &&
        !err.requestOptions.path.contains('/auth/')) {
      // Token expired → refresh dene
      final refresh = await _storage.read(key: 'refresh_token');
      if (refresh != null) {
        try {
          final resp = await _dio.post('/auth/refresh',
              data: {'refresh_token': refresh});
          final newAccess = resp.data['access_token'] as String;
          final newRefresh = resp.data['refresh_token'] as String;
          await _storage.write(key: 'access_token', value: newAccess);
          await _storage.write(key: 'refresh_token', value: newRefresh);

          // Orijinal isteği tekrar dene
          err.requestOptions.headers['Authorization'] = 'Bearer $newAccess';
          final retry = await _dio.fetch(err.requestOptions);
          return handler.resolve(retry);
        } catch (_) {
          // Refresh başarısız — token'ları sil, login sayfasına yönlendir
          await _storage.deleteAll();
        }
      }
    }
    handler.next(err);
  }
}
