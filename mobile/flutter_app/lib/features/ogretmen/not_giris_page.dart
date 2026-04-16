import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


class NotGirisPage extends ConsumerStatefulWidget {
  const NotGirisPage({super.key});

  @override
  ConsumerState<NotGirisPage> createState() => _NotGirisPageState();
}

class _NotGirisPageState extends ConsumerState<NotGirisPage> {
  String? _sinif;
  String? _sube;
  String _ders = 'Matematik';
  String _donem = '1. Donem';
  String _notTuru = 'yazili';
  int _notSirasi = 1;
  DateTime _tarih = DateTime.now();
  List<Map<String, dynamic>> _ogrenciler = [];
  final Map<String, TextEditingController> _puanCtrl = {};
  bool _yukleniyor = false;
  bool _kaydediyor = false;

  Future<void> _ogrencileriYukle() async {
    if (_sinif == null || _sube == null) return;
    setState(() => _yukleniyor = true);
    try {
      final r = await ref.read(ogretmenApiProvider).sinifOgrencileri(_sinif!, _sube!);
      final list = List<Map<String, dynamic>>.from(r['ogrenciler'] as List);
      // Her ogrenci icin controller
      for (var c in _puanCtrl.values) { c.dispose(); }
      _puanCtrl.clear();
      for (var o in list) {
        _puanCtrl[o['id'] as String] = TextEditingController();
      }
      setState(() {
        _ogrenciler = list;
        _yukleniyor = false;
      });
    } catch (_) {
      setState(() => _yukleniyor = false);
    }
  }

  Future<void> _kaydet() async {
    final girilenler = _puanCtrl.entries
        .where((e) => e.value.text.trim().isNotEmpty)
        .map((e) {
      final val = double.tryParse(e.value.text.trim().replaceAll(',', '.'));
      if (val == null || val < 0 || val > 100) return null;
      return {'student_id': e.key, 'puan': val, 'aciklama': ''};
    }).whereType<Map<String, dynamic>>().toList();

    if (girilenler.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Hiç not girilmedi')),
      );
      return;
    }

    setState(() => _kaydediyor = true);
    try {
      await ref.read(ogretmenApiProvider).notKaydet(
        sinif: _sinif!, sube: _sube!, ders: _ders,
        donem: _donem, notTuru: _notTuru, notSirasi: _notSirasi,
        tarih: DateFormat('yyyy-MM-dd').format(_tarih),
        notlar: girilenler,
      );
      if (!mounted) return;
      for (var c in _puanCtrl.values) { c.clear(); }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('✓ ${girilenler.length} not kaydedildi'),
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
  void dispose() {
    for (var c in _puanCtrl.values) { c.dispose(); }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Not Girişi'),
        actions: [
          TextButton.icon(
            onPressed: _kaydediyor ? null : _kaydet,
            icon: _kaydediyor
                ? const SizedBox(width: 16, height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2))
                : const Icon(Icons.save, color: Colors.white),
            label: const Text('KAYDET', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            color: Theme.of(context).cardColor,
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _sinif != null ? '$_sinif|$_sube' : null,
                        decoration: const InputDecoration(labelText: 'Sınıf', isDense: true),
                        items: _dummySiniflar.map((s) =>
                            DropdownMenuItem(value: s, child: Text(s.replaceAll('|', '/')))).toList(),
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
                        items: _dersler.map((d) =>
                            DropdownMenuItem(value: d, child: Text(d))).toList(),
                        onChanged: (v) => setState(() => _ders = v ?? _ders),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _donem,
                        decoration: const InputDecoration(labelText: 'Dönem', isDense: true),
                        items: const [
                          DropdownMenuItem(value: '1. Donem', child: Text('1. Dönem')),
                          DropdownMenuItem(value: '2. Donem', child: Text('2. Dönem')),
                        ],
                        onChanged: (v) => setState(() => _donem = v ?? _donem),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: DropdownButtonFormField<String>(
                        value: _notTuru,
                        decoration: const InputDecoration(labelText: 'Tür', isDense: true),
                        items: const [
                          DropdownMenuItem(value: 'yazili', child: Text('Yazılı')),
                          DropdownMenuItem(value: 'sozlu', child: Text('Sözlü')),
                          DropdownMenuItem(value: 'proje', child: Text('Proje')),
                          DropdownMenuItem(value: 'performans', child: Text('Performans')),
                        ],
                        onChanged: (v) => setState(() => _notTuru = v ?? _notTuru),
                      ),
                    ),
                    const SizedBox(width: 8),
                    SizedBox(
                      width: 80,
                      child: DropdownButtonFormField<int>(
                        value: _notSirasi,
                        decoration: const InputDecoration(labelText: 'Sıra', isDense: true),
                        items: List.generate(5, (i) =>
                            DropdownMenuItem(value: i + 1, child: Text('${i + 1}'))),
                        onChanged: (v) => setState(() => _notSirasi = v ?? 1),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          Expanded(
            child: _yukleniyor
                ? const Center(child: CircularProgressIndicator())
                : _ogrenciler.isEmpty
                    ? const Center(child: Text('Sınıf seç'))
                    : ListView.builder(
                        itemCount: _ogrenciler.length,
                        itemBuilder: (_, i) {
                          final o = _ogrenciler[i];
                          return ListTile(
                            leading: CircleAvatar(child: Text(o['numara'] ?? '?')),
                            title: Text(o['ad_soyad'] ?? ''),
                            trailing: SizedBox(
                              width: 80,
                              child: TextField(
                                controller: _puanCtrl[o['id']],
                                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                                textAlign: TextAlign.center,
                                decoration: const InputDecoration(
                                  hintText: '0-100',
                                  isDense: true,
                                  border: OutlineInputBorder(),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}


const _dummySiniflar = ['9|A', '9|B', '10|A', '10|B', '11|A', '11|B', '12|A'];
const _dersler = ['Matematik', 'Turkce', 'Fen Bilgisi', 'Ingilizce', 'Tarih', 'Fizik', 'Kimya', 'Biyoloji'];
