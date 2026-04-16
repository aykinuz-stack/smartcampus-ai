import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';


/// Ogrenci API servisi — notlar, devamsizlik, odev.
class OgrenciApi {
  final ApiClient _api;
  OgrenciApi(this._api);

  Future<Map<String, dynamic>> getNotlar({String? donem}) async {
    final r = await _api.get('/ogrenci/notlar',
        params: donem != null ? {'donem': donem} : null);
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> getDevamsizlik() async {
    final r = await _api.get('/ogrenci/devamsizlik');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> getOdevler() async {
    final r = await _api.get('/ogrenci/odevler');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> teslimEt(String odevId, {String? dosyaUrl, String? not}) async {
    final r = await _api.post('/ogrenci/odev/teslim', data: {
      'odev_id': odevId,
      'dosya_url': dosyaUrl,
      'not': not ?? '',
    });
    return Map<String, dynamic>.from(r.data);
  }
}


/// Mesajlasma API servisi.
class MesajApi {
  final ApiClient _api;
  MesajApi(this._api);

  Future<Map<String, dynamic>> getListe({int limit = 50}) async {
    final r = await _api.get('/mesaj/liste', params: {'limit': limit});
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> gonder({
    required String aliciRol,
    required String aliciId,
    required String mesaj,
    String? studentId,
  }) async {
    final r = await _api.post('/mesaj/gonder', data: {
      'alici_rol': aliciRol,
      'alici_id': aliciId,
      'mesaj': mesaj,
      'student_id': studentId,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<void> markRead(String mesajId) async {
    await _api.post('/mesaj/$mesajId/okundu');
  }
}


/// Ihbar Hatti API servisi (anonim).
class IhbarApi {
  final ApiClient _api;
  IhbarApi(this._api);

  Future<Map<String, dynamic>> getKategoriler() async {
    final r = await _api.get('/ihbar/kategoriler');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> gonder({
    required String kategori,
    String? altKategori,
    required String aciklama,
    String? nerede,
    String? neZaman,
    String kimIcin = 'Kendim hakkinda',
    bool geriDonusIstiyor = false,
  }) async {
    final r = await _api.post('/ihbar/gonder', data: {
      'kategori': kategori,
      'alt_kategori': altKategori ?? '',
      'aciklama': aciklama,
      'nerede': nerede ?? '',
      'ne_zaman': neZaman ?? '',
      'kim_icin': kimIcin,
      'geri_donus_istiyor': geriDonusIstiyor,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> durumSorgula(String takipKodu) async {
    final r = await _api.post('/ihbar/durum', data: {'takip_kodu': takipKodu});
    return Map<String, dynamic>.from(r.data);
  }
}


// Riverpod providers
final ogrenciApiProvider = Provider<OgrenciApi>((ref) =>
    OgrenciApi(ref.watch(apiClientProvider)));

final mesajApiProvider = Provider<MesajApi>((ref) =>
    MesajApi(ref.watch(apiClientProvider)));

final ihbarApiProvider = Provider<IhbarApi>((ref) =>
    IhbarApi(ref.watch(apiClientProvider)));
