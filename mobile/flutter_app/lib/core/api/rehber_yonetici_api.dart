import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';


class RehberApi {
  final ApiClient _api;
  RehberApi(this._api);

  Future<List<dynamic>> vakalar({String? durum, String? konu}) async {
    final params = <String, dynamic>{};
    if (durum != null) params['durum'] = durum;
    if (konu != null) params['konu'] = konu;
    final r = await _api.get('/rehber/vakalar', params: params);
    return List<dynamic>.from(r.data as List);
  }

  Future<Map<String, dynamic>> vakaAc({
    required String studentId,
    required String konu,
    required String aciklama,
    String oncelik = 'orta',
  }) async {
    final r = await _api.post('/rehber/vaka', data: {
      'student_id': studentId, 'konu': konu, 'aciklama': aciklama, 'oncelik': oncelik,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<void> vakaKapat(String vid) async {
    await _api.post('/rehber/vaka/$vid/kapat');
  }

  Future<List<dynamic>> gorusmeler({String? studentId}) async {
    final params = studentId != null ? {'student_id': studentId} : null;
    final r = await _api.get('/rehber/gorusmeler', params: params);
    return List<dynamic>.from(r.data as List);
  }

  Future<Map<String, dynamic>> gorusmeEkle({
    required String studentId,
    String? vakaId,
    int sureDakika = 30,
    required String notlar,
    String sonrakiAdim = '',
  }) async {
    final r = await _api.post('/rehber/gorusme', data: {
      'student_id': studentId, 'vaka_id': vakaId,
      'sure_dakika': sureDakika, 'notlar': notlar, 'sonraki_adim': sonrakiAdim,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>?> aileForm(String studentId) async {
    try {
      final r = await _api.get('/rehber/aile-form/$studentId');
      return r.data != null ? Map<String, dynamic>.from(r.data) : null;
    } catch (_) {
      return null;
    }
  }

  Future<Map<String, dynamic>> aileFormEkle(Map<String, dynamic> data) async {
    final r = await _api.post('/rehber/aile-form', data: data);
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> moodPanel({int days = 14}) async {
    final r = await _api.get('/rehber/mood-panel', params: {'days': days});
    return Map<String, dynamic>.from(r.data);
  }

  Future<List<dynamic>> ihbarListe({String? durum, String? kategori}) async {
    final params = <String, dynamic>{};
    if (durum != null) params['durum'] = durum;
    if (kategori != null) params['kategori'] = kategori;
    final r = await _api.get('/rehber/ihbar-liste', params: params);
    return List<dynamic>.from(r.data as List);
  }
}


class YoneticiApi {
  final ApiClient _api;
  YoneticiApi(this._api);

  Future<Map<String, dynamic>> dashboard() async {
    final r = await _api.get('/yonetici/dashboard');
    return Map<String, dynamic>.from(r.data);
  }

  Future<List<dynamic>> erkenUyariOzet() async {
    final r = await _api.get('/yonetici/erken-uyari/ozet');
    return List<dynamic>.from(r.data as List);
  }

  Future<List<dynamic>> riskliOgrenciler({double minSkor = 45}) async {
    final r = await _api.get('/yonetici/erken-uyari/riskli-ogrenciler',
        params: {'min_skor': minSkor});
    return List<dynamic>.from(r.data as List);
  }

  Future<List<dynamic>> onaylar() async {
    final r = await _api.get('/yonetici/onaylar');
    return List<dynamic>.from(r.data as List);
  }

  Future<void> onayAksiyon(String id, String aksiyon, {String not = ''}) async {
    await _api.post('/yonetici/onay-aksiyon', data: {
      'onay_id': id, 'aksiyon': aksiyon, 'not_metni': not,
    });
  }
}


final rehberApiProvider = Provider<RehberApi>((ref) => RehberApi(ref.watch(apiClientProvider)));
final yoneticiApiProvider = Provider<YoneticiApi>((ref) => YoneticiApi(ref.watch(apiClientProvider)));
