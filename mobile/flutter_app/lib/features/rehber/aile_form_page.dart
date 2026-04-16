import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';
import '../../shared/widgets/ogrenci_secici.dart';


class AileFormPage extends ConsumerStatefulWidget {
  const AileFormPage({super.key});

  @override
  ConsumerState<AileFormPage> createState() => _AileFormPageState();
}

class _AileFormPageState extends ConsumerState<AileFormPage> {
  Map<String, dynamic>? _ogrenci;
  Map<String, dynamic>? _mevcutForm;
  bool _yukleniyor = false;
  bool _kaydediyor = false;

  final _anneEgitimCtrl = TextEditingController();
  final _babaEgitimCtrl = TextEditingController();
  final _anneMeslekCtrl = TextEditingController();
  final _babaMeslekCtrl = TextEditingController();
  final _evDurumCtrl = TextEditingController();
  final _ozelDurumCtrl = TextEditingController();
  int _kardesSayisi = 0;
  String _aileDurumu = 'birlikte';

  @override
  void dispose() {
    _anneEgitimCtrl.dispose();
    _babaEgitimCtrl.dispose();
    _anneMeslekCtrl.dispose();
    _babaMeslekCtrl.dispose();
    _evDurumCtrl.dispose();
    _ozelDurumCtrl.dispose();
    super.dispose();
  }

  Future<void> _ogrenciSec() async {
    final secilen = await OgrenciSeciciDialog.show(context, baslik: 'Aile formu için öğrenci seç');
    if (secilen != null) {
      setState(() {
        _ogrenci = secilen;
        _mevcutForm = null;
        _yukleniyor = true;
      });
      // Mevcut form varsa yukle
      final f = await ref.read(rehberApiProvider).aileForm(secilen['id'] as String);
      if (mounted) {
        setState(() {
          _mevcutForm = f;
          _yukleniyor = false;
          if (f != null) {
            _anneEgitimCtrl.text = f['anne_egitim'] ?? '';
            _babaEgitimCtrl.text = f['baba_egitim'] ?? '';
            _anneMeslekCtrl.text = f['anne_meslek'] ?? '';
            _babaMeslekCtrl.text = f['baba_meslek'] ?? '';
            _evDurumCtrl.text = f['ev_durumu'] ?? '';
            _ozelDurumCtrl.text = f['ozel_durum'] ?? '';
            _kardesSayisi = (f['kardes_sayisi'] as num?)?.toInt() ?? 0;
            _aileDurumu = f['aile_durumu'] ?? 'birlikte';
          }
        });
      }
    }
  }

  Future<void> _kaydet() async {
    if (_ogrenci == null) return;
    setState(() => _kaydediyor = true);
    try {
      await ref.read(rehberApiProvider).aileFormEkle({
        'student_id': _ogrenci!['id'],
        'anne_egitim': _anneEgitimCtrl.text.trim(),
        'baba_egitim': _babaEgitimCtrl.text.trim(),
        'anne_meslek': _anneMeslekCtrl.text.trim(),
        'baba_meslek': _babaMeslekCtrl.text.trim(),
        'kardes_sayisi': _kardesSayisi,
        'aile_durumu': _aileDurumu,
        'ev_durumu': _evDurumCtrl.text.trim(),
        'ozel_durum': _ozelDurumCtrl.text.trim(),
      });
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Aile formu kaydedildi'),
            backgroundColor: AppColors.success),
      );
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
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('👨‍👩‍👧 Aile Bilgi Formu')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            InkWell(
              onTap: _ogrenciSec,
              child: Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  border: Border.all(color: AppColors.primary.withOpacity(0.4)),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.person, color: AppColors.primary),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        _ogrenci == null
                            ? 'Öğrenci Seç'
                            : '${_ogrenci!['ad_soyad']} · ${_ogrenci!['sinif']}/${_ogrenci!['sube']}',
                        style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                      ),
                    ),
                    if (_mevcutForm != null)
                      const Icon(Icons.edit_note, color: AppColors.warning)
                    else if (_ogrenci != null)
                      const Icon(Icons.add, color: AppColors.success),
                  ],
                ),
              ),
            ),
            if (_mevcutForm != null) ...[
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: AppColors.info.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.info_outline, size: 16, color: AppColors.info),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        'Mevcut form yüklendi. Değişiklik yapıp kaydedebilirsin.',
                        style: const TextStyle(fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ],

            if (_yukleniyor)
              const Padding(
                padding: EdgeInsets.all(24),
                child: Center(child: CircularProgressIndicator()),
              )
            else if (_ogrenci != null) ...[
              const SizedBox(height: 20),

              const Text('Ebeveyn Bilgileri',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              const SizedBox(height: 10),
              Row(children: [
                Expanded(
                  child: TextField(
                    controller: _anneEgitimCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Anne Eğitim', isDense: true, border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _babaEgitimCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Baba Eğitim', isDense: true, border: OutlineInputBorder(),
                    ),
                  ),
                ),
              ]),
              const SizedBox(height: 8),
              Row(children: [
                Expanded(
                  child: TextField(
                    controller: _anneMeslekCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Anne Meslek', isDense: true, border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _babaMeslekCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Baba Meslek', isDense: true, border: OutlineInputBorder(),
                    ),
                  ),
                ),
              ]),

              const SizedBox(height: 16),
              const Text('Aile Durumu',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              const SizedBox(height: 8),
              Wrap(spacing: 8, children: [
                ChoiceChip(
                  label: const Text('Birlikte'),
                  selected: _aileDurumu == 'birlikte',
                  onSelected: (_) => setState(() => _aileDurumu = 'birlikte'),
                ),
                ChoiceChip(
                  label: const Text('Ayrı / Boşanmış'),
                  selected: _aileDurumu == 'ayri',
                  onSelected: (_) => setState(() => _aileDurumu = 'ayri'),
                ),
                ChoiceChip(
                  label: const Text('Vefat'),
                  selected: _aileDurumu == 'vefat',
                  onSelected: (_) => setState(() => _aileDurumu = 'vefat'),
                ),
              ]),

              const SizedBox(height: 16),
              Row(
                children: [
                  const Text('Kardeş Sayısı: ', style: TextStyle(fontSize: 14)),
                  Expanded(
                    child: Slider(
                      value: _kardesSayisi.toDouble(),
                      min: 0, max: 10, divisions: 10,
                      label: '$_kardesSayisi',
                      onChanged: (v) => setState(() => _kardesSayisi = v.toInt()),
                    ),
                  ),
                  Text('$_kardesSayisi', style: const TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),

              const SizedBox(height: 16),
              TextField(
                controller: _evDurumCtrl,
                decoration: const InputDecoration(
                  labelText: 'Ev Durumu',
                  hintText: 'Kira / mülk / paylaşımlı vs',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _ozelDurumCtrl,
                maxLines: 4,
                decoration: const InputDecoration(
                  labelText: 'Özel Durum *',
                  hintText: 'Şiddet, istismar, ihmal, ekonomik kriz, ebeveyn kaybı vs.',
                  helperText: 'Açık anahtar kelimeler yaz — motor okur ve aile riski skoru üretir.',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                height: 50,
                child: ElevatedButton.icon(
                  onPressed: _kaydediyor ? null : _kaydet,
                  icon: _kaydediyor
                      ? const SizedBox(width: 20, height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.save),
                  label: Text(_mevcutForm != null ? 'FORMU GÜNCELLE' : 'FORMU KAYDET'),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
