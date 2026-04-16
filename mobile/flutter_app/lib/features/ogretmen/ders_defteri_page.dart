import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../../core/api/ogretmen_api.dart';
import '../../core/theme/app_theme.dart';


class DersDefteriPage extends ConsumerStatefulWidget {
  const DersDefteriPage({super.key});

  @override
  ConsumerState<DersDefteriPage> createState() => _DersDefteriPageState();
}

class _DersDefteriPageState extends ConsumerState<DersDefteriPage> {
  String _sinif = '9';
  String _sube = 'A';
  String _ders = 'Matematik';
  int _dersSaati = 1;
  DateTime _tarih = DateTime.now();
  final _konuCtrl = TextEditingController();
  final _notCtrl = TextEditingController();
  final _linkCtrl = TextEditingController();
  Future<List<dynamic>>? _gecmisFuture;
  bool _kaydediyor = false;

  @override
  void initState() {
    super.initState();
    _loadGecmis();
  }

  void _loadGecmis() {
    setState(() =>
        _gecmisFuture = ref.read(ogretmenApiProvider).dersDefteriList(_sinif, _sube));
  }

  Future<void> _kaydet() async {
    if (_konuCtrl.text.trim().length < 3) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Konu en az 3 karakter olmalı')),
      );
      return;
    }
    setState(() => _kaydediyor = true);
    try {
      await ref.read(ogretmenApiProvider).dersDefteriEkle(
        sinif: _sinif, sube: _sube, ders: _ders,
        dersSaati: _dersSaati,
        tarih: DateFormat('yyyy-MM-dd').format(_tarih),
        islenenKonu: _konuCtrl.text.trim(),
        ozelNot: _notCtrl.text.trim(),
        onlineLink: _linkCtrl.text.trim(),
      );
      if (!mounted) return;
      _konuCtrl.clear();
      _notCtrl.clear();
      _linkCtrl.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Ders defteri kaydı eklendi'),
            backgroundColor: AppColors.success),
      );
      _loadGecmis();
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
    _konuCtrl.dispose();
    _notCtrl.dispose();
    _linkCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📓 Ders Defteri')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
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
                        setState(() {
                          _sinif = p[0]; _sube = p[1];
                        });
                        _loadGecmis();
                      }
                    },
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: DropdownButtonFormField<String>(
                    value: _ders,
                    decoration: const InputDecoration(labelText: 'Ders', isDense: true),
                    items: const ['Matematik', 'Turkce', 'Fizik', 'Tarih', 'Ingilizce']
                        .map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                    onChanged: (v) => setState(() => _ders = v ?? _ders),
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
                      decoration: const InputDecoration(labelText: 'Tarih', isDense: true),
                      child: Text(DateFormat('dd.MM.yyyy').format(_tarih)),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(
                  width: 100,
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
            const SizedBox(height: 16),
            TextField(
              controller: _konuCtrl,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'İşlenen Konu *',
                hintText: 'Örn: Üslü sayılar — giriş',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _notCtrl,
              maxLines: 2,
              decoration: const InputDecoration(
                labelText: 'Özel Not (opsiyonel)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _linkCtrl,
              decoration: const InputDecoration(
                labelText: 'Online Ders Linki (opsiyonel)',
                prefixIcon: Icon(Icons.link),
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 48,
              child: ElevatedButton.icon(
                onPressed: _kaydediyor ? null : _kaydet,
                icon: _kaydediyor
                    ? const SizedBox(width: 16, height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.save),
                label: const Text('DEFTERE KAYDET'),
              ),
            ),
            const SizedBox(height: 20),
            const Text('Geçmiş Kayıtlar',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            FutureBuilder<List<dynamic>>(
              future: _gecmisFuture,
              builder: (_, snap) {
                final kayitlar = snap.data ?? [];
                if (kayitlar.isEmpty) return const Text('Kayıt yok');
                return Column(
                  children: kayitlar.take(10).map((k) => Card(
                    child: ListTile(
                      title: Text(k['islenen_konu'] ?? '',
                          style: const TextStyle(fontWeight: FontWeight.w600)),
                      subtitle: Text('${k['tarih']} · ${k['ders']} · ${k['ders_saati']}. ders'),
                    ),
                  )).toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
