import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'api_client.dart';


class VeliApi {
  final ApiClient _api;
  VeliApi(this._api);

  Future<List<Map<String, dynamic>>> cocuklarim() async {
    final r = await _api.get('/veli/cocuklarim');
    return List<Map<String, dynamic>>.from(r.data as List);
  }

  Future<Map<String, dynamic>> getKapsuller({String? studentId, int limit = 30}) async {
    final params = <String, dynamic>{'limit': limit};
    if (studentId != null) params['student_id'] = studentId;
    final r = await _api.get('/veli/kapsul', params: params);
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> randevularim() async {
    final r = await _api.get('/veli/randevularim');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> randevuAl({
    String? studentId,
    required String ogretmenId,
    String ogretmenAdi = '',
    required String tarih,
    required String saat,
    required String konu,
  }) async {
    final r = await _api.post('/veli/randevu/al', data: {
      'student_id': studentId,
      'ogretmen_id': ogretmenId,
      'ogretmen_adi': ogretmenAdi,
      'tarih': tarih,
      'saat': saat,
      'konu': konu,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<void> randevuIptal(String rid) async {
    await _api.post('/veli/randevu/$rid/iptal');
  }

  Future<List<String>> belgeTurler() async {
    final r = await _api.get('/veli/belge/turler');
    return List<String>.from(r.data['turler'] as List);
  }

  Future<Map<String, dynamic>> belgeTaleplerim() async {
    final r = await _api.get('/veli/belge/taleplerim');
    return Map<String, dynamic>.from(r.data);
  }

  Future<Map<String, dynamic>> belgeTalep({
    String? studentId,
    required String belgeTuru,
    String aciklama = '',
  }) async {
    final r = await _api.post('/veli/belge/talep', data: {
      'student_id': studentId,
      'belge_turu': belgeTuru,
      'aciklama': aciklama,
    });
    return Map<String, dynamic>.from(r.data);
  }

  Future<void> geriBildirim({
    required String kategori,
    int? puan,
    required String mesaj,
    String? studentId,
  }) async {
    await _api.post('/veli/geri-bildirim', data: {
      'kategori': kategori,
      'puan': puan,
      'mesaj': mesaj,
      'student_id': studentId,
    });
  }
}


final veliApiProvider = Provider<VeliApi>((ref) => VeliApi(ref.watch(apiClientProvider)));
