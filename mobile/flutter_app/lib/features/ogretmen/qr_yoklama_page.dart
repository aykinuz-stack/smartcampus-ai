import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


/// QR Yoklama — QR kod ile öğrenci taratarak hızlı yoklama
///
/// Akış:
/// 1. Öğretmen sınıf + ders + saat seçer
/// 2. "QR Tarama Başlat" butonuna basar → kamera açılır
/// 3. Öğrenci öğrenci kartındaki QR kodu gösterir
/// 4. Her okutma "devam" olarak işaretler
/// 5. Okutmayanlar otomatik "devamsız" kalır
class QRYoklamaPage extends ConsumerStatefulWidget {
  const QRYoklamaPage({super.key});

  @override
  ConsumerState<QRYoklamaPage> createState() => _QRYoklamaPageState();
}

class _QRYoklamaPageState extends ConsumerState<QRYoklamaPage> {
  String _sinif = '9';
  String _sube = 'A';
  String _ders = 'Matematik';
  int _dersSaati = 1;
  DateTime _tarih = DateTime.now();

  final MobileScannerController _cameraCtrl = MobileScannerController();
  bool _taraniyor = false;
  bool _kaydediyor = false;

  List<Map<String, dynamic>> _ogrenciler = [];
  final Set<String> _okutulanIds = {};
  final List<String> _sonOkutulanlar = [];

  Future<void> _ogrencileriYukle() async {
    try {
      final r = await ref.read(ogretmenApiProvider).sinifOgrencileri(_sinif, _sube);
      if (!mounted) return;
      setState(() {
        _ogrenciler = List<Map<String, dynamic>>.from(r['ogrenciler'] as List);
        _okutulanIds.clear();
        _sonOkutulanlar.clear();
      });
    } catch (_) {}
  }

  void _qrOkundu(BarcodeCapture capture) {
    final barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;
    final kod = barcodes.first.rawValue;
    if (kod == null) return;

    // QR formatı: "stu_<id>" veya direkt student_id
    final studentId = kod.startsWith('stu_') ? kod : 'stu_$kod';

    if (_okutulanIds.contains(studentId)) return;  // Tekrar

    final ogrenci = _ogrenciler.firstWhere(
      (o) => o['id'] == studentId,
      orElse: () => {},
    );
    if (ogrenci.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('❌ Öğrenci bu sınıfta değil: $studentId'),
          backgroundColor: AppColors.danger,
          duration: const Duration(seconds: 1),
        ),
      );
      return;
    }

    setState(() {
      _okutulanIds.add(studentId);
      _sonOkutulanlar.insert(0, ogrenci['ad_soyad'] ?? '?');
      if (_sonOkutulanlar.length > 5) _sonOkutulanlar.removeRange(5, _sonOkutulanlar.length);
    });

    // Kısa titreşim/ses hissi — snackbar
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('✓ ${ogrenci['ad_soyad']}'),
        backgroundColor: AppColors.success,
        duration: const Duration(milliseconds: 800),
      ),
    );
  }

  Future<void> _kaydet() async {
    if (_ogrenciler.isEmpty) return;
    setState(() => _kaydediyor = true);
    try {
      final yoklamalar = _ogrenciler.map((o) => {
        'student_id': o['id'],
        'turu': _okutulanIds.contains(o['id']) ? 'devam' : 'devamsiz',
        'aciklama': _okutulanIds.contains(o['id']) ? 'QR okundu' : '',
      }).toList();

      await ref.read(ogretmenApiProvider).yoklamaKaydet(
        sinif: _sinif, sube: _sube, ders: _ders,
        dersSaati: _dersSaati,
        tarih: DateFormat('yyyy-MM-dd').format(_tarih),
        yoklamalar: yoklamalar,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('✓ Yoklama kaydedildi: ${_okutulanIds.length} devam, '
              '${_ogrenciler.length - _okutulanIds.length} devamsız'),
          backgroundColor: AppColors.success,
        ),
      );
      setState(() {
        _taraniyor = false;
        _cameraCtrl.stop();
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      if (mounted) setState(() => _kaydediyor = false);
    }
  }

  @override
  void initState() {
    super.initState();
    _ogrencileriYukle();
  }

  @override
  void dispose() {
    _cameraCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📱 QR Yoklama'),
        actions: [
          if (_taraniyor)
            IconButton(
              icon: const Icon(Icons.flash_on),
              onPressed: () => _cameraCtrl.toggleTorch(),
            ),
          if (_taraniyor)
            IconButton(
              icon: const Icon(Icons.cameraswitch),
              onPressed: () => _cameraCtrl.switchCamera(),
            ),
        ],
      ),
      body: Column(
        children: [
          // Ayarlar
          Container(
            padding: const EdgeInsets.all(12),
            color: Theme.of(context).cardColor,
            child: Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<String>(
                    value: '$_sinif|$_sube',
                    decoration: const InputDecoration(labelText: 'Sınıf', isDense: true),
                    items: const [
                      DropdownMenuItem(value: '9|A', child: Text('9/A')),
                      DropdownMenuItem(value: '9|B', child: Text('9/B')),
                      DropdownMenuItem(value: '10|A', child: Text('10/A')),
                      DropdownMenuItem(value: '10|B', child: Text('10/B')),
                      DropdownMenuItem(value: '11|A', child: Text('11/A')),
                      DropdownMenuItem(value: '12|A', child: Text('12/A')),
                    ],
                    onChanged: (v) {
                      if (v != null) {
                        final p = v.split('|');
                        setState(() { _sinif = p[0]; _sube = p[1]; });
                        _ogrencileriYukle();
                      }
                    },
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: DropdownButtonFormField<String>(
                    value: _ders,
                    decoration: const InputDecoration(labelText: 'Ders', isDense: true),
                    items: const ['Matematik', 'Turkce', 'Fizik', 'Ingilizce']
                        .map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                    onChanged: (v) => setState(() => _ders = v ?? _ders),
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(
                  width: 70,
                  child: DropdownButtonFormField<int>(
                    value: _dersSaati,
                    decoration: const InputDecoration(labelText: 'Saat', isDense: true),
                    items: List.generate(8, (i) =>
                        DropdownMenuItem(value: i + 1, child: Text('${i + 1}.'))),
                    onChanged: (v) => setState(() => _dersSaati = v ?? 1),
                  ),
                ),
              ],
            ),
          ),

          // Ozet bar
          Container(
            color: AppColors.primary.withOpacity(0.08),
            padding: const EdgeInsets.all(10),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.success.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text('✓ Okutulan: ${_okutulanIds.length}',
                      style: const TextStyle(
                          color: AppColors.success, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.danger.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                      '✗ Eksik: ${_ogrenciler.length - _okutulanIds.length}',
                      style: const TextStyle(
                          color: AppColors.danger, fontWeight: FontWeight.bold)),
                ),
                const Spacer(),
                Text('Toplam: ${_ogrenciler.length}',
                    style: const TextStyle(fontSize: 12)),
              ],
            ),
          ),

          // Tarayici / Son okutulanlar
          Expanded(
            child: _taraniyor
                ? Stack(
                    children: [
                      MobileScanner(
                        controller: _cameraCtrl,
                        onDetect: _qrOkundu,
                      ),
                      // Overlay: son okutulanlar listesi
                      Positioned(
                        top: 12, left: 12, right: 12,
                        child: Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.7),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text('QR kodlarını sırayla tarat',
                                  style: TextStyle(color: Colors.white,
                                      fontWeight: FontWeight.bold)),
                              const SizedBox(height: 4),
                              Text('Son 5 okutulan:',
                                  style: TextStyle(color: Colors.white.withOpacity(0.7),
                                      fontSize: 11)),
                              ..._sonOkutulanlar.take(5).map((ad) => Padding(
                                padding: const EdgeInsets.only(top: 2),
                                child: Text('✓ $ad',
                                    style: const TextStyle(color: AppColors.success,
                                        fontSize: 12)),
                              )),
                            ],
                          ),
                        ),
                      ),
                      // Alt butonlar
                      Positioned(
                        bottom: 16, left: 16, right: 16,
                        child: Row(
                          children: [
                            Expanded(
                              child: ElevatedButton.icon(
                                icon: const Icon(Icons.stop),
                                label: const Text('DURDUR'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.danger,
                                  padding: const EdgeInsets.symmetric(vertical: 14),
                                ),
                                onPressed: () {
                                  setState(() => _taraniyor = false);
                                  _cameraCtrl.stop();
                                },
                              ),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: ElevatedButton.icon(
                                icon: _kaydediyor
                                    ? const SizedBox(width: 18, height: 18,
                                        child: CircularProgressIndicator(
                                            strokeWidth: 2, color: Colors.white))
                                    : const Icon(Icons.save),
                                label: const Text('KAYDET'),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.success,
                                  padding: const EdgeInsets.symmetric(vertical: 14),
                                ),
                                onPressed: _kaydediyor ? null : _kaydet,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  )
                : Column(
                    children: [
                      const SizedBox(height: 20),
                      const Icon(Icons.qr_code_scanner, size: 100, color: AppColors.primary),
                      const SizedBox(height: 12),
                      const Text('QR Yoklama Hazır',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 32),
                        child: Text(
                          'Öğrencilerin okul kartındaki QR kodu kameraya tutmaları yeterli. '
                          'Her okutulan "devam" işaretlenir, okutmayanlar otomatik "devamsız" kalır.',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 13, color: AppColors.textSecondaryDark),
                        ),
                      ),
                      const SizedBox(height: 20),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.play_arrow),
                        label: const Text('QR TARAMAYI BAŞLAT',
                            style: TextStyle(letterSpacing: 1.2)),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary,
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                        ),
                        onPressed: _ogrenciler.isEmpty ? null : () {
                          setState(() => _taraniyor = true);
                          _cameraCtrl.start();
                        },
                      ),
                      const SizedBox(height: 20),
                      if (_okutulanIds.isNotEmpty)
                        ElevatedButton.icon(
                          icon: const Icon(Icons.save),
                          label: Text('KAYDET (${_okutulanIds.length} öğrenci)'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.success,
                          ),
                          onPressed: _kaydediyor ? null : _kaydet,
                        ),
                      const SizedBox(height: 20),
                      if (_ogrenciler.isNotEmpty)
                        Expanded(
                          child: ListView.builder(
                            itemCount: _ogrenciler.length,
                            itemBuilder: (_, i) {
                              final o = _ogrenciler[i];
                              final okutuldu = _okutulanIds.contains(o['id']);
                              return ListTile(
                                dense: true,
                                leading: Icon(
                                  okutuldu ? Icons.check_circle : Icons.radio_button_off,
                                  color: okutuldu ? AppColors.success : Colors.grey,
                                ),
                                title: Text(o['ad_soyad'] ?? ''),
                                subtitle: Text('No: ${o['numara']}'),
                              );
                            },
                          ),
                        ),
                    ],
                  ),
          ),
        ],
      ),
    );
  }
}
