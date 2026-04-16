import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


/// Rehber/Ogretmen/Yonetici icin ortak ogrenci secici
/// Sinif dropdown + liste arama
class OgrenciSeciciDialog extends ConsumerStatefulWidget {
  final String? baslik;
  const OgrenciSeciciDialog({super.key, this.baslik});

  @override
  ConsumerState<OgrenciSeciciDialog> createState() => _OgrenciSeciciDialogState();

  static Future<Map<String, dynamic>?> show(BuildContext context, {String? baslik}) {
    return showDialog<Map<String, dynamic>>(
      context: context,
      builder: (_) => OgrenciSeciciDialog(baslik: baslik),
    );
  }
}

class _OgrenciSeciciDialogState extends ConsumerState<OgrenciSeciciDialog> {
  List<Map<String, dynamic>> _siniflar = [];
  List<Map<String, dynamic>> _ogrenciler = [];
  String? _selectedSinif;
  String? _selectedSube;
  bool _loadingSiniflar = true;
  bool _loadingOgrenciler = false;
  final _aramaCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadSiniflar();
  }

  Future<void> _loadSiniflar() async {
    try {
      final s = await ref.read(ogretmenApiProvider).siniflarim();
      setState(() {
        _siniflar = s;
        _loadingSiniflar = false;
      });
    } catch (_) {
      setState(() => _loadingSiniflar = false);
    }
  }

  Future<void> _loadOgrenciler() async {
    if (_selectedSinif == null || _selectedSube == null) return;
    setState(() => _loadingOgrenciler = true);
    try {
      final r = await ref.read(ogretmenApiProvider).sinifOgrencileri(_selectedSinif!, _selectedSube!);
      setState(() {
        _ogrenciler = List<Map<String, dynamic>>.from(r['ogrenciler'] as List);
        _loadingOgrenciler = false;
      });
    } catch (_) {
      setState(() => _loadingOgrenciler = false);
    }
  }

  @override
  void dispose() {
    _aramaCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filtered = _aramaCtrl.text.isEmpty
        ? _ogrenciler
        : _ogrenciler.where((o) =>
            (o['ad_soyad'] as String? ?? '')
                .toLowerCase()
                .contains(_aramaCtrl.text.toLowerCase())).toList();

    return AlertDialog(
      title: Text(widget.baslik ?? 'Öğrenci Seç'),
      contentPadding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
      content: SizedBox(
        width: double.maxFinite,
        height: 400,
        child: Column(
          children: [
            // Sinif secici
            if (_loadingSiniflar)
              const LinearProgressIndicator()
            else
              DropdownButtonFormField<String>(
                value: _selectedSinif != null ? '$_selectedSinif|$_selectedSube' : null,
                decoration: const InputDecoration(
                  labelText: 'Sınıf',
                  isDense: true,
                  border: OutlineInputBorder(),
                ),
                items: _siniflar.map((s) {
                  final val = '${s['sinif']}|${s['sube']}';
                  return DropdownMenuItem(
                    value: val,
                    child: Text('${s['sinif']}/${s['sube']} (${s['ogrenci_sayisi']} öğrenci)'),
                  );
                }).toList(),
                onChanged: (v) {
                  if (v != null) {
                    final p = v.split('|');
                    setState(() {
                      _selectedSinif = p[0];
                      _selectedSube = p[1];
                    });
                    _loadOgrenciler();
                  }
                },
              ),
            const SizedBox(height: 10),
            // Arama
            if (_ogrenciler.isNotEmpty)
              TextField(
                controller: _aramaCtrl,
                decoration: const InputDecoration(
                  hintText: 'Ara...',
                  prefixIcon: Icon(Icons.search, size: 18),
                  isDense: true,
                  border: OutlineInputBorder(),
                ),
                onChanged: (_) => setState(() {}),
              ),
            const SizedBox(height: 10),
            Expanded(
              child: _loadingOgrenciler
                  ? const Center(child: CircularProgressIndicator())
                  : _ogrenciler.isEmpty
                      ? const Center(
                          child: Text('Önce sınıf seç', style: TextStyle(color: Colors.grey)),
                        )
                      : ListView.builder(
                          itemCount: filtered.length,
                          itemBuilder: (_, i) {
                            final o = filtered[i];
                            return ListTile(
                              dense: true,
                              leading: CircleAvatar(
                                radius: 18,
                                backgroundColor: AppColors.primary.withOpacity(0.15),
                                child: Text(
                                  o['numara'] ?? '?',
                                  style: const TextStyle(
                                      fontSize: 11, fontWeight: FontWeight.bold),
                                ),
                              ),
                              title: Text(o['ad_soyad'] ?? ''),
                              onTap: () => Navigator.pop(context, o),
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('İptal'),
        ),
      ],
    );
  }
}
