import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';


class OgretmenApi {
  final ApiClient _api;
  OgretmenApi(this._api);

  Future<List<Map<String, dynamic>>> siniflarim() async {
    final r = await _api.get('/ogretmen/siniflarim');
    return List<Map<String, dynamic>>.from(r.data as List);
  }

  Future<Map<String, dynamic>> sinifOgrencileri(String sinif, String sube) async {
    final r = await _api.get('/ogretmen/sinif/$sinif/$sube');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> yoklamaKaydet({
    required String sinif,
    required String sube,
    required String ders,
    required int dersSaati,
    required String tarih,
    required List<Map<String, dynamic>> yoklamalar,
  }) async {
    final r = await _api.post('/ogretmen/yoklama', data: {
      'sinif': sinif,
      'sube': sube,
      'ders': ders,
      'ders_saati': dersSaati,
      'tarih': tarih,
      'yoklamalar': yoklamalar,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> notKaydet({
    required String sinif,
    required String sube,
    required String ders,
    required String donem,
    required String notTuru,
    required int notSirasi,
    required String tarih,
    required List<Map<String, dynamic>> notlar,
  }) async {
    final r = await _api.post('/ogretmen/not', data: {
      'sinif': sinif,
      'sube': sube,
      'ders': ders,
      'donem': donem,
      'not_turu': notTuru,
      'not_sirasi': notSirasi,
      'tarih': tarih,
      'notlar': notlar,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> dersDefteriEkle({
    required String sinif,
    required String sube,
    required String ders,
    required int dersSaati,
    required String tarih,
    required String islenenKonu,
    String ozelNot = '',
    String onlineLink = '',
    List<String>? kazanimlar,
  }) async {
    final r = await _api.post('/ogretmen/ders-defteri', data: {
      'sinif': sinif,
      'sube': sube,
      'ders': ders,
      'ders_saati': dersSaati,
      'tarih': tarih,
      'islenen_konu': islenenKonu,
      'ozel_not': ozelNot,
      'online_link': onlineLink,
      'kazanimlar': kazanimlar ?? [],
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<List<dynamic>> dersDefteriList(String sinif, String sube, {int limit = 30}) async {
    final r = await _api.get('/ogretmen/ders-defteri/$sinif/$sube', params: {'limit': limit});
    return List<dynamic>.from(r.data as List);
  }

  Future<Map<String, dynamic>> odevAta({
    required String baslik,
    required String ders,
    required String sinif,
    required String sube,
    String tur = 'yazili',
    String aciklama = '',
    required String verilisTarihi,
    required String teslimTarihi,
    String kaynakUrl = '',
  }) async {
    final r = await _api.post('/ogretmen/odev/ata', data: {
      'baslik': baslik,
      'ders': ders,
      'sinif': sinif,
      'sube': sube,
      'tur': tur,
      'aciklama': aciklama,
      'verilis_tarihi': verilisTarihi,
      'teslim_tarihi': teslimTarihi,
      'kaynak_url': kaynakUrl,
    });
    return Map<String, dynamic>.from(r.data);
  }
  Future<Map<String, dynamic>> sinavSonuclari({String? ders, String? sinif}) async {
    final params = <String, dynamic>{};
    if (ders != null) params['ders'] = ders;
    if (sinif != null) params['sinif'] = sinif;
    final r = await _api.get('/ogretmen/sinav-sonuclari', params: params);
    return Map<String, dynamic>.from(r.data);
  }
}


final ogretmenApiProvider = Provider<OgretmenApi>((ref) =>
    OgretmenApi(ref.watch(apiClientProvider)));
