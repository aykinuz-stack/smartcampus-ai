import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:jwt_decoder/jwt_decoder.dart';

import '../api/api_client.dart';

class AuthUser {
  final String username;
  final String role;
  final String adSoyad;
  final String tenantId;
  final String studentId;
  final List<String> childrenIds;

  AuthUser({
    required this.username,
    required this.role,
    required this.adSoyad,
    required this.tenantId,
    required this.studentId,
    required this.childrenIds,
  });

  factory AuthUser.fromJson(Map<String, dynamic> j) => AuthUser(
        username: j['username'] ?? '',
        role: (j['role'] ?? '').toString(),
        adSoyad: j['ad_soyad'] ?? '',
        tenantId: j['tenant_id'] ?? 'default',
        studentId: j['student_id'] ?? '',
        childrenIds: List<String>.from(j['children_ids'] ?? []),
      );

  bool get isOgrenci => role.toLowerCase() == 'ogrenci';
  bool get isOgretmen => role.toLowerCase() == 'ogretmen';
  bool get isVeli => role.toLowerCase() == 'veli';
  bool get isRehber => role.toLowerCase() == 'rehber' || role.toLowerCase() == 'calisan';
  bool get isYonetici => ['yonetici', 'mudur', 'superadmin'].contains(role.toLowerCase());
}


class AuthService {
  final ApiClient _api;
  final _storage = const FlutterSecureStorage();

  AuthService(this._api);

  Future<AuthUser?> login(String username, String password,
      {String tenantId = 'default'}) async {
    try {
      final resp = await _api.post('/auth/login', data: {
        'username': username,
        'password': password,
        'tenant_id': tenantId,
      });
      final data = resp.data;
      await _storage.write(key: 'access_token', value: data['access_token']);
      await _storage.write(key: 'refresh_token', value: data['refresh_token']);
      await _storage.write(key: 'user_json', value: jsonEncode(data['user']));
      return AuthUser.fromJson(Map<String, dynamic>.from(data['user']));
    } catch (e) {
      return null;
    }
  }

  Future<AuthUser?> getCurrentUser() async {
    final userStr = await _storage.read(key: 'user_json');
    final token = await _storage.read(key: 'access_token');
    if (userStr == null || token == null) return null;

    // Token expired mı kontrol et
    if (JwtDecoder.isExpired(token)) {
      // Refresh denenir — api_client otomatik yapar
      return null;
    }
    try {
      return AuthUser.fromJson(Map<String, dynamic>.from(jsonDecode(userStr)));
    } catch (_) {
      return null;
    }
  }

  Future<void> logout() async {
    try {
      await _api.post('/auth/logout');
    } catch (_) {}
    await _storage.deleteAll();
  }
}


// Riverpod provider
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());
final authServiceProvider = Provider<AuthService>((ref) =>
    AuthService(ref.watch(apiClientProvider)));

final currentUserProvider = FutureProvider<AuthUser?>((ref) async {
  return ref.watch(authServiceProvider).getCurrentUser();
});
