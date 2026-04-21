import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../api/api_client.dart';


/// Offline-first cache servisi.
/// Online: API'den cek + Hive'a kaydet.
/// Offline: Hive'dan oku.
class OfflineCacheService {
  final ApiClient _api;
  final Box<Map> _cache;

  OfflineCacheService(this._api, this._cache);

  /// Baglanti durumunu kontrol et
  Future<bool> get isOnline async {
    final result = await Connectivity().checkConnectivity();
    return !result.contains(ConnectivityResult.none);
  }

  /// Genel cache-first GET istegi.
  /// Online ise API'den cek + cache'le. Offline ise cache'den oku.
  Future<Map<String, dynamic>> cachedGet(
    String path, {
    Map<String, dynamic>? params,
    Duration maxAge = const Duration(minutes: 15),
  }) async {
    final cacheKey = _cacheKey(path, params);

    // Cache'de var mi ve taze mi?
    final cached = _cache.get(cacheKey);
    if (cached != null) {
      final ts = cached['_cached_at'] as String?;
      if (ts != null) {
        final cachedAt = DateTime.tryParse(ts);
        if (cachedAt != null &&
            DateTime.now().difference(cachedAt) < maxAge) {
          debugPrint('[CACHE] HIT: $path');
          return Map<String, dynamic>.from(cached)..remove('_cached_at');
        }
      }
    }

    // Online mi?
    if (await isOnline) {
      try {
        final r = await _api.get(path, params: params);
        final data = Map<String, dynamic>.from(r.data);

        // Cache'e kaydet
        _cache.put(cacheKey, {
          ...data,
          '_cached_at': DateTime.now().toIso8601String(),
        });
        debugPrint('[CACHE] FRESH: $path');
        return data;
      } catch (e) {
        debugPrint('[CACHE] API error, falling back: $e');
        // API hatasi — cache varsa onu don
        if (cached != null) {
          return Map<String, dynamic>.from(cached)..remove('_cached_at');
        }
        rethrow;
      }
    }

    // Offline — cache varsa don
    if (cached != null) {
      debugPrint('[CACHE] OFFLINE: $path');
      return Map<String, dynamic>.from(cached)..remove('_cached_at');
    }

    throw Exception('Baglanti yok ve cache bos');
  }

  /// Cache'i temizle
  void invalidate(String path, {Map<String, dynamic>? params}) {
    final key = _cacheKey(path, params);
    _cache.delete(key);
  }

  /// Tum cache'i temizle
  Future<void> clearAll() async {
    await _cache.clear();
  }

  /// Cache boyutu
  int get cacheSize => _cache.length;

  String _cacheKey(String path, Map<String, dynamic>? params) {
    if (params == null || params.isEmpty) return path;
    final sorted = params.entries.toList()
      ..sort((a, b) => a.key.compareTo(b.key));
    return '$path?${sorted.map((e) => '${e.key}=${e.value}').join('&')}';
  }
}


/// Baglanti durumu provider'i
final connectivityProvider = StreamProvider<List<ConnectivityResult>>((ref) {
  return Connectivity().onConnectivityChanged;
});

/// Offline cache provider
final offlineCacheProvider = Provider<OfflineCacheService>((ref) {
  final api = ref.watch(apiClientProvider);
  final box = Hive.box<Map>('cached_data');
  return OfflineCacheService(api, box);
});
