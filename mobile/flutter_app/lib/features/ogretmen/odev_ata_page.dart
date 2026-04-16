import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


class OdevAtaPage extends ConsumerStatefulWidget {
  const OdevAtaPage({super.key});

  @override
  ConsumerState<OdevAtaPage> createState() => _OdevAtaPageState();
}

class _OdevAtaPageState extends ConsumerState<OdevAtaPage> {
  final _baslikCtrl = TextEditingController();
  final _aciklamaCtrl = TextEditingController();
  final _kaynakCtrl = TextEditingController();
  String _sinif = '9';
  String _sube = 'A';
  String _ders = 'Matematik';
  String _tur = 'yazili';
  DateTime _verilisTarihi = DateTime.now();
  DateTime _teslimTarihi = DateTime.now().add(const Duration(days: 7));
  bool _gondering = false;

  Future<void> _gonder() async {
    if (_baslikCtrl.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Başlık en az 3 karakter')),
      );
      return;
    }
    setState(() => _gondering = true);
    try {
      await ref.read(ogretmenApiProvider).odevAta(
        baslik: _baslikCtrl.text.trim(),
        ders: _ders,
        sinif: _sinif, sube: _sube,
        tur: _tur,
        aciklama: _aciklamaCtrl.text.trim(),
        verilisTarihi: DateFormat('yyyy-MM-dd').format(_verilisTarihi),
        teslimTarihi: DateFormat('yyyy-MM-dd').format(_teslimTarihi),
        kaynakUrl: _kaynakCtrl.text.trim(),
      );
      if (!mounted) return;
      _baslikCtrl.clear();
      _aciklamaCtrl.clear();
      _kaynakCtrl.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('✓ Ödev $_sinif/$_sube sınıfına atandı'),
            backgroundColor: AppColors.success),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      if (mounted) setState(() => _gondering = false);
    }
  }

  @override
  void dispose() {
    _baslikCtrl.dispose();
    _aciklamaCtrl.dispose();
    _kaynakCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📝 Ödev Ata')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _baslikCtrl,
              decoration: const InputDecoration(
                labelText: 'Ödev Başlığı *',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            Row(children: [
              Expanded(
                child: DropdownButtonFormField<String>(
                  value: '$_sinif|$_sube',
                  decoration: const InputDecoration(labelText: 'Sınıf *', isDense: true),
                  items: const [
                    DropdownMenuItem(value: '9|A', child: Text('9/A')),
                    DropdownMenuItem(value: '9|B', child: Text('9/B')),
                    DropdownMenuItem(value: '10|A', child: Text('10/A')),
                    DropdownMenuItem(value: '11|A', child: Text('11/A')),
                  ],
                  onChanged: (v) {
                    if (v != null) {
                      final p = v.split('|');
                      setState(() { _sinif = p[0]; _sube = p[1]; });
                    }
                  },
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: DropdownButtonFormField<String>(
                  value: _ders,
                  decoration: const InputDecoration(labelText: 'Ders *', isDense: true),
                  items: const ['Matematik', 'Turkce', 'Fen', 'Tarih', 'Ingilizce']
                      .map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                  onChanged: (v) => setState(() => _ders = v ?? _ders),
                ),
              ),
            ]),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _tur,
              decoration: const InputDecoration(labelText: 'Ödev Türü', isDense: true),
              items: const [
                DropdownMenuItem(value: 'yazili', child: Text('📝 Yazılı')),
                DropdownMenuItem(value: 'link', child: Text('🔗 Link')),
                DropdownMenuItem(value: 'dosya', child: Text('📎 Dosya')),
                DropdownMenuItem(value: 'video', child: Text('🎥 Video')),
              ],
              onChanged: (v) => setState(() => _tur = v ?? _tur),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _aciklamaCtrl,
              maxLines: 4,
              decoration: const InputDecoration(
                labelText: 'Açıklama',
                hintText: 'Öğrenciler ne yapacak?',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _kaynakCtrl,
              decoration: const InputDecoration(
                labelText: 'Kaynak URL (opsiyonel)',
                prefixIcon: Icon(Icons.link),
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            Row(children: [
              Expanded(
                child: InkWell(
                  onTap: () async {
                    final t = await showDatePicker(
                      context: context, initialDate: _verilisTarihi,
                      firstDate: DateTime.now().subtract(const Duration(days: 1)),
                      lastDate: DateTime.now().add(const Duration(days: 30)),
                    );
                    if (t != null) setState(() => _verilisTarihi = t);
                  },
                  child: InputDecorator(
                    decoration: const InputDecoration(labelText: 'Veriliş', isDense: true),
                    child: Text(DateFormat('dd.MM.yyyy').format(_verilisTarihi)),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: InkWell(
                  onTap: () async {
                    final t = await showDatePicker(
                      context: context, initialDate: _teslimTarihi,
                      firstDate: DateTime.now(),
                      lastDate: DateTime.now().add(const Duration(days: 90)),
                    );
                    if (t != null) setState(() => _teslimTarihi = t);
                  },
                  child: InputDecorator(
                    decoration: const InputDecoration(labelText: 'Teslim *', isDense: true),
                    child: Text(DateFormat('dd.MM.yyyy').format(_teslimTarihi)),
                  ),
                ),
              ),
            ]),
            const SizedBox(height: 20),
            SizedBox(
              height: 52,
              child: ElevatedButton.icon(
                onPressed: _gondering ? null : _gonder,
                icon: _gondering
                    ? const SizedBox(width: 20, height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.assignment_add),
                label: const Text('ÖDEVI ATA'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
