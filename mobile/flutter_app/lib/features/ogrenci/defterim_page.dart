import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../../core/theme/app_theme.dart';


/// Ogrenci Defterim — kisisel not defteri (offline-first, Hive)
class DefterimPage extends ConsumerStatefulWidget {
  const DefterimPage({super.key});

  @override
  ConsumerState<DefterimPage> createState() => _DefterimPageState();
}

class _DefterimPageState extends ConsumerState<DefterimPage> {
  List<Map<String, dynamic>> _notlar = [];
  String _filtre = 'hepsi'; // hepsi, ders, kisisel, sinav

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    try {
      final box = Hive.box<Map>('cached_data');
      final raw = box.get('defterim_notlar');
      if (raw != null) {
        setState(() {
          _notlar = List<Map<String, dynamic>>.from(
            (raw['notlar'] as List).map((e) => Map<String, dynamic>.from(e as Map)),
          );
        });
      }
    } catch (_) {}
  }

  void _save() {
    try {
      final box = Hive.box<Map>('cached_data');
      box.put('defterim_notlar', {'notlar': _notlar});
    } catch (_) {}
  }

  void _yeniNot() {
    _showEditor(null);
  }

  void _duzenle(int index) {
    _showEditor(index);
  }

  void _sil(int index) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Notu Sil'),
        content: const Text('Bu not silinsin mi?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Vazgec')),
          TextButton(
            onPressed: () {
              setState(() => _notlar.removeAt(index));
              _save();
              Navigator.pop(ctx);
            },
            child: const Text('Sil', style: TextStyle(color: AppColors.danger)),
          ),
        ],
      ),
    );
  }

  void _showEditor(int? index) {
    final existing = index != null ? _notlar[index] : null;
    final baslikCtrl = TextEditingController(text: existing?['baslik'] ?? '');
    final icerikCtrl = TextEditingController(text: existing?['icerik'] ?? '');
    String kategori = existing?['kategori'] ?? 'kisisel';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Padding(
          padding: EdgeInsets.only(
            left: 20, right: 20, top: 20,
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
          ),
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(index != null ? 'Notu Duzenle' : 'Yeni Not',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                TextField(
                  controller: baslikCtrl,
                  decoration: InputDecoration(
                    labelText: 'Baslik',
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                ),
                const SizedBox(height: 12),
                // Kategori
                Wrap(
                  spacing: 8,
                  children: [
                    _KategoriChip('kisisel', 'Kisisel', Icons.person, kategori,
                        (v) => setModalState(() => kategori = v)),
                    _KategoriChip('ders', 'Ders Notu', Icons.menu_book, kategori,
                        (v) => setModalState(() => kategori = v)),
                    _KategoriChip('sinav', 'Sinav', Icons.quiz, kategori,
                        (v) => setModalState(() => kategori = v)),
                    _KategoriChip('odev', 'Odev', Icons.assignment, kategori,
                        (v) => setModalState(() => kategori = v)),
                  ],
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: icerikCtrl,
                  maxLines: 6,
                  decoration: InputDecoration(
                    labelText: 'Icerik',
                    alignLabelWithHint: true,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                ),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.save),
                    label: Text(index != null ? 'Guncelle' : 'Kaydet'),
                    onPressed: () {
                      final baslik = baslikCtrl.text.trim();
                      final icerik = icerikCtrl.text.trim();
                      if (baslik.isEmpty && icerik.isEmpty) return;

                      final not = {
                        'baslik': baslik.isNotEmpty ? baslik : 'Isimsiz Not',
                        'icerik': icerik,
                        'kategori': kategori,
                        'tarih': DateTime.now().toIso8601String(),
                      };

                      setState(() {
                        if (index != null) {
                          _notlar[index] = not;
                        } else {
                          _notlar.insert(0, not);
                        }
                      });
                      _save();
                      Navigator.pop(ctx);
                    },
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  List<Map<String, dynamic>> get _filtrelenmis {
    if (_filtre == 'hepsi') return _notlar;
    return _notlar.where((n) => n['kategori'] == _filtre).toList();
  }

  @override
  Widget build(BuildContext context) {
    final list = _filtrelenmis;

    return Scaffold(
      appBar: AppBar(title: const Text('Defterim')),
      floatingActionButton: FloatingActionButton(
        onPressed: _yeniNot,
        backgroundColor: AppColors.primary,
        child: const Icon(Icons.add, color: Colors.white),
      ),
      body: Column(
        children: [
          // Filtre
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _FilterChip('hepsi', 'Hepsi (${_notlar.length})', _filtre,
                      (v) => setState(() => _filtre = v)),
                  _FilterChip('kisisel', 'Kisisel', _filtre,
                      (v) => setState(() => _filtre = v)),
                  _FilterChip('ders', 'Ders', _filtre,
                      (v) => setState(() => _filtre = v)),
                  _FilterChip('sinav', 'Sinav', _filtre,
                      (v) => setState(() => _filtre = v)),
                  _FilterChip('odev', 'Odev', _filtre,
                      (v) => setState(() => _filtre = v)),
                ],
              ),
            ),
          ),

          if (list.isEmpty)
            const Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.book, size: 64, color: AppColors.info),
                    SizedBox(height: 12),
                    Text('Henuz not yok', style: TextStyle(fontSize: 16)),
                    SizedBox(height: 4),
                    Text('+ butonuyla yeni not ekle',
                        style: TextStyle(fontSize: 13, color: AppColors.textSecondaryDark)),
                  ],
                ),
              ),
            )
          else
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.all(12),
                itemCount: list.length,
                itemBuilder: (_, i) {
                  final n = list[i];
                  final realIdx = _notlar.indexOf(n);
                  return _NotKart(
                    not: n,
                    onTap: () => _duzenle(realIdx),
                    onSil: () => _sil(realIdx),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}


class _FilterChip extends StatelessWidget {
  final String value;
  final String label;
  final String selected;
  final Function(String) onTap;
  const _FilterChip(this.value, this.label, this.selected, this.onTap);

  @override
  Widget build(BuildContext context) {
    final active = value == selected;
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ChoiceChip(
        label: Text(label, style: TextStyle(fontSize: 12,
            color: active ? Colors.white : null)),
        selected: active,
        selectedColor: AppColors.primary,
        onSelected: (_) => onTap(value),
      ),
    );
  }
}


class _KategoriChip extends StatelessWidget {
  final String value;
  final String label;
  final IconData icon;
  final String selected;
  final Function(String) onTap;
  const _KategoriChip(this.value, this.label, this.icon, this.selected, this.onTap);

  @override
  Widget build(BuildContext context) {
    final active = value == selected;
    return ChoiceChip(
      avatar: Icon(icon, size: 16, color: active ? Colors.white : AppColors.primary),
      label: Text(label, style: TextStyle(fontSize: 11,
          color: active ? Colors.white : null)),
      selected: active,
      selectedColor: AppColors.primary,
      onSelected: (_) => onTap(value),
    );
  }
}


class _NotKart extends StatelessWidget {
  final Map<String, dynamic> not;
  final VoidCallback onTap;
  final VoidCallback onSil;
  const _NotKart({required this.not, required this.onTap, required this.onSil});

  Color _renkFor(String kat) {
    switch (kat) {
      case 'ders': return AppColors.primary;
      case 'sinav': return AppColors.danger;
      case 'odev': return AppColors.gold;
      default: return AppColors.info;
    }
  }

  IconData _iconFor(String kat) {
    switch (kat) {
      case 'ders': return Icons.menu_book;
      case 'sinav': return Icons.quiz;
      case 'odev': return Icons.assignment;
      default: return Icons.note;
    }
  }

  @override
  Widget build(BuildContext context) {
    final baslik = not['baslik'] as String? ?? '';
    final icerik = not['icerik'] as String? ?? '';
    final kategori = not['kategori'] as String? ?? 'kisisel';
    final tarih = not['tarih'] as String? ?? '';
    final c = _renkFor(kategori);

    String zamanStr = '';
    try {
      final dt = DateTime.parse(tarih);
      final fark = DateTime.now().difference(dt);
      if (fark.inMinutes < 60) {
        zamanStr = '${fark.inMinutes} dk once';
      } else if (fark.inHours < 24) {
        zamanStr = '${fark.inHours} saat once';
      } else {
        zamanStr = '${fark.inDays} gun once';
      }
    } catch (_) {}

    return Dismissible(
      key: ValueKey(tarih),
      direction: DismissDirection.endToStart,
      background: Container(
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        color: AppColors.danger.withOpacity(0.2),
        child: const Icon(Icons.delete, color: AppColors.danger),
      ),
      confirmDismiss: (_) async {
        onSil();
        return false;
      },
      child: Card(
        margin: const EdgeInsets.only(bottom: 8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              border: Border(left: BorderSide(color: c, width: 4)),
            ),
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(_iconFor(kategori), size: 16, color: c),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(baslik,
                          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                          maxLines: 1, overflow: TextOverflow.ellipsis),
                    ),
                    Text(zamanStr,
                        style: const TextStyle(fontSize: 10, color: AppColors.textSecondaryDark)),
                  ],
                ),
                if (icerik.isNotEmpty) ...[
                  const SizedBox(height: 6),
                  Text(icerik, style: TextStyle(fontSize: 13, color: Colors.grey[600]),
                      maxLines: 3, overflow: TextOverflow.ellipsis),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
