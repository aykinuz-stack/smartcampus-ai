import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


/// Öğretmen Yoklama sayfası — sınıf seç, gün + ders + saat gir, hızlı işaretle.
class YoklamaPage extends ConsumerStatefulWidget {
  const YoklamaPage({super.key});

  @override
  ConsumerState<YoklamaPage> createState() => _YoklamaPageState();
}

class _YoklamaPageState extends ConsumerState<YoklamaPage> {
  String? _sinif;
  String? _sube;
  String _ders = 'Matematik';
  int _dersSaati = 1;
  DateTime _tarih = DateTime.now();
  List<Map<String, dynamic>> _ogrenciler = [];
  final Map<String, String> _durum = {};  // student_id -> devam/devamsiz/gec vs
  bool _yukleniyor = false;
  bool _kaydediyor = false;

  Future<void> _siniflarYukle() async {
    final s = await ref.read(ogretmenApiProvider).siniflarim();
    if (s.isNotEmpty && mounted) {
      setState(() {
        _sinif = s[0]['sinif'] as String;
        _sube = s[0]['sube'] as String;
      });
      _ogrencileriYukle();
    }
  }

  Future<void> _ogrencileriYukle() async {
    if (_sinif == null || _sube == null) return;
    setState(() => _yukleniyor = true);
    try {
      final r = await ref.read(ogretmenApiProvider).sinifOgrencileri(_sinif!, _sube!);
      final list = List<Map<String, dynamic>>.from(r['ogrenciler'] as List);
      // Default: hepsi devam
      final m = <String, String>{};
      for (var o in list) {
        m[o['id'] as String] = 'devam';
      }
      setState(() {
        _ogrenciler = list;
        _durum..clear()..addAll(m);
        _yukleniyor = false;
      });
    } catch (_) {
      setState(() => _yukleniyor = false);
    }
  }

  Future<void> _kaydet() async {
    if (_ogrenciler.isEmpty) return;
    setState(() => _kaydediyor = true);
    try {
      final yoklamalar = _ogrenciler.map((o) => {
        'student_id': o['id'],
        'turu': _durum[o['id']] ?? 'devam',
        'aciklama': '',
      }).toList();

      await ref.read(ogretmenApiProvider).yoklamaKaydet(
        sinif: _sinif!,
        sube: _sube!,
        ders: _ders,
        dersSaati: _dersSaati,
        tarih: DateFormat('yyyy-MM-dd').format(_tarih),
        yoklamalar: yoklamalar,
      );
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Yoklama kaydedildi'), backgroundColor: AppColors.success),
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
  void initState() {
    super.initState();
    _siniflarYukle();
  }

  @override
  Widget build(BuildContext context) {
    final devam = _durum.values.where((v) => v == 'devam').length;
    final devamsiz = _durum.values.where((v) => v == 'devamsiz').length;
    final gec = _durum.values.where((v) => v == 'gec').length;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Yoklama'),
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
          // Ayarlar paneli
          Container(
            padding: const EdgeInsets.all(12),
            color: Theme.of(context).cardColor,
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: _SinifSecici(
                        sinif: _sinif, sube: _sube,
                        onChange: (s, sb) {
                          setState(() { _sinif = s; _sube = sb; });
                          _ogrencileriYukle();
                        },
                      ),
                    ),
                    const SizedBox(width: 8),
                    Expanded(
                      child: _DersSecici(
                        value: _ders, onChange: (v) => setState(() => _ders = v),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: InkWell(
                        onTap: () async {
                          final t = await showDatePicker(
                            context: context, initialDate: _tarih,
                            firstDate: DateTime.now().subtract(const Duration(days: 30)),
                            lastDate: DateTime.now(),
                          );
                          if (t != null) setState(() => _tarih = t);
                        },
                        child: InputDecorator(
                          decoration: InputDecoration(
                            labelText: 'Tarih', isDense: true,
                            prefixIcon: const Icon(Icons.calendar_today, size: 18),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                          ),
                          child: Text(DateFormat('dd.MM.yyyy').format(_tarih)),
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),
                    SizedBox(
                      width: 100,
                      child: DropdownButtonFormField<int>(
                        value: _dersSaati,
                        decoration: InputDecoration(
                          labelText: 'Saat', isDense: true,
                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                        ),
                        items: List.generate(8, (i) =>
                            DropdownMenuItem(value: i + 1, child: Text('${i + 1}. ders'))),
                        onChanged: (v) => setState(() => _dersSaati = v ?? 1),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Ozet bar
          Container(
            color: AppColors.primary.withOpacity(0.08),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                _OzetSay('✓ Devam', '$devam', AppColors.success),
                const SizedBox(width: 12),
                _OzetSay('✗ Devamsız', '$devamsiz', AppColors.danger),
                const SizedBox(width: 12),
                _OzetSay('⏰ Geç', '$gec', AppColors.warning),
                const Spacer(),
                Text('Toplam: ${_ogrenciler.length}',
                    style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
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
                          return _OgrenciSatir(
                            ogrenci: o,
                            durum: _durum[o['id']] ?? 'devam',
                            onChange: (v) => setState(() => _durum[o['id'] as String] = v),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }
}


class _OzetSay extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _OzetSay(this.label, this.value, this.color);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Text('$label: $value',
          style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.bold)),
    );
  }
}


class _OgrenciSatir extends StatelessWidget {
  final Map<String, dynamic> ogrenci;
  final String durum;
  final Function(String) onChange;
  const _OgrenciSatir({
    required this.ogrenci, required this.durum, required this.onChange,
  });

  @override
  Widget build(BuildContext context) {
    Color c;
    switch (durum) {
      case 'devam': c = AppColors.success; break;
      case 'devamsiz': c = AppColors.danger; break;
      case 'gec': c = AppColors.warning; break;
      case 'izinli':
      case 'raporlu': c = AppColors.info; break;
      default: c = Colors.grey;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: c.withOpacity(0.05),
        border: Border(
          left: BorderSide(color: c, width: 4),
          bottom: BorderSide(color: Colors.grey.withOpacity(0.1)),
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 32, height: 32,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: Colors.grey.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: Text(ogrenci['numara'] ?? '?',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(ogrenci['ad_soyad'] ?? '',
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ),
          ToggleButtons(
            isSelected: [
              durum == 'devam',
              durum == 'devamsiz',
              durum == 'gec',
              durum == 'izinli',
            ],
            onPressed: (i) {
              const turler = ['devam', 'devamsiz', 'gec', 'izinli'];
              onChange(turler[i]);
            },
            borderRadius: BorderRadius.circular(8),
            constraints: const BoxConstraints(minWidth: 36, minHeight: 32),
            children: const [
              Icon(Icons.check, size: 18),
              Icon(Icons.close, size: 18),
              Icon(Icons.access_time, size: 18),
              Icon(Icons.medical_information_outlined, size: 18),
            ],
          ),
        ],
      ),
    );
  }
}


class _SinifSecici extends ConsumerStatefulWidget {
  final String? sinif;
  final String? sube;
  final Function(String, String) onChange;
  const _SinifSecici({required this.sinif, required this.sube, required this.onChange});

  @override
  ConsumerState<_SinifSecici> createState() => _SinifSeciciState();
}

class _SinifSeciciState extends ConsumerState<_SinifSecici> {
  List<Map<String, dynamic>> _siniflar = [];

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final s = await ref.read(ogretmenApiProvider).siniflarim();
      if (mounted) setState(() => _siniflar = s);
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    if (_siniflar.isEmpty) {
      return const InputDecorator(
        decoration: InputDecoration(labelText: 'Sınıf', isDense: true),
        child: Text('Yükleniyor...'),
      );
    }
    return DropdownButtonFormField<String>(
      value: widget.sinif != null && widget.sube != null
          ? '${widget.sinif}|${widget.sube}'
          : null,
      decoration: InputDecoration(
        labelText: 'Sınıf',
        isDense: true,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
      ),
      items: _siniflar.map((s) {
        final val = '${s['sinif']}|${s['sube']}';
        return DropdownMenuItem(
          value: val,
          child: Text('${s['sinif']}/${s['sube']} (${s['ogrenci_sayisi']})'),
        );
      }).toList(),
      onChanged: (v) {
        if (v != null) {
          final parts = v.split('|');
          widget.onChange(parts[0], parts[1]);
        }
      },
    );
  }
}


class _DersSecici extends StatelessWidget {
  final String value;
  final Function(String) onChange;
  const _DersSecici({required this.value, required this.onChange});

  static const _dersler = [
    'Matematik', 'Turkce', 'Fen Bilgisi', 'Sosyal Bilgiler',
    'Ingilizce', 'Tarih', 'Cografya', 'Fizik', 'Kimya', 'Biyoloji',
    'Edebiyat', 'Beden Egitimi', 'Muzik', 'Gorsel Sanatlar', 'Bilgisayar',
    'Din Kulturu', 'Rehberlik',
  ];

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: value,
      decoration: InputDecoration(
        labelText: 'Ders', isDense: true,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
      ),
      items: _dersler.map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
      onChanged: (v) => v != null ? onChange(v) : null,
    );
  }
}
