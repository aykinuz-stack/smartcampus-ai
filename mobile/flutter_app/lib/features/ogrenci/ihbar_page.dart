import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/theme/app_theme.dart';

class IhbarPage extends ConsumerStatefulWidget {
  const IhbarPage({super.key});

  @override
  ConsumerState<IhbarPage> createState() => _IhbarPageState();
}

class _IhbarPageState extends ConsumerState<IhbarPage> {
  String? _kategori;
  String? _altKategori;
  final _aciklamaCtrl = TextEditingController();
  final _neredeCtrl = TextEditingController();
  final _neZamanCtrl = TextEditingController();
  String _kimIcin = 'Kendim hakkinda';
  bool _geriDonus = false;
  bool _gondering = false;
  Map<String, dynamic>? _kategoriler;
  String? _sonTakipKodu;

  @override
  void initState() {
    super.initState();
    _yukleKategoriler();
  }

  Future<void> _yukleKategoriler() async {
    try {
      final data = await ref.read(ihbarApiProvider).getKategoriler();
      setState(() => _kategoriler = data);
    } catch (_) {}
  }

  Future<void> _gonder() async {
    if (_kategori == null) {
      _toast('Lütfen bir kategori seç', AppColors.warning);
      return;
    }
    if (_aciklamaCtrl.text.trim().length < 20) {
      _toast('Açıklama en az 20 karakter olmalı', AppColors.warning);
      return;
    }
    setState(() => _gondering = true);
    try {
      final r = await ref.read(ihbarApiProvider).gonder(
        kategori: _kategori!,
        altKategori: _altKategori,
        aciklama: _aciklamaCtrl.text.trim(),
        nerede: _neredeCtrl.text.trim(),
        neZaman: _neZamanCtrl.text.trim(),
        kimIcin: _kimIcin,
        geriDonusIstiyor: _geriDonus,
      );
      if (!mounted) return;
      setState(() {
        _sonTakipKodu = r['takip_kodu'] as String? ?? '';
        _aciklamaCtrl.clear();
        _neredeCtrl.clear();
        _neZamanCtrl.clear();
        _kategori = null;
        _altKategori = null;
      });
      _showSuccess(r);
    } catch (e) {
      _toast('Hata: $e', AppColors.danger);
    } finally {
      if (mounted) setState(() => _gondering = false);
    }
  }

  void _toast(String msg, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), backgroundColor: color),
    );
  }

  void _showSuccess(Map<String, dynamic> r) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        icon: const Icon(Icons.verified_outlined, color: AppColors.success, size: 48),
        title: const Text('İhbarınız İletildi'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(r['mesaj'] ?? ''),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.primary.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  const Icon(Icons.fingerprint, color: AppColors.primary),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Anonim ID:', style: TextStyle(fontSize: 11)),
                        Text(r['anonim_id'] ?? '',
                            style: const TextStyle(fontFamily: 'monospace',
                                fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            if ((r['takip_kodu'] as String? ?? '').isNotEmpty) ...[
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.gold.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Takip Kodu (sakla):', style: TextStyle(fontSize: 11)),
                    Text(r['takip_kodu'],
                        style: const TextStyle(fontFamily: 'monospace',
                            fontWeight: FontWeight.bold, fontSize: 20)),
                  ],
                ),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Tamam')),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _aciklamaCtrl.dispose();
    _neredeCtrl.dispose();
    _neZamanCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final altKategoriler = _kategori != null && _kategoriler != null
        ? (_kategoriler![_kategori!]?['alt'] as List?)
        : null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('🚨 Anonim İhbar Hattı'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Gizlilik bilgisi
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.danger.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.danger.withOpacity(0.3)),
              ),
              child: Row(
                children: const [
                  Icon(Icons.shield_outlined, color: AppColors.danger),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Tamamen ANONİM. Kimliğin hiçbir yerde saklanmaz. '
                      'İsim veya tanıtıcı bilgi yazmana gerek yok.',
                      style: TextStyle(fontSize: 13),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            const Text('Konu Kategorisi *',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            if (_kategoriler == null)
              const Center(child: CircularProgressIndicator())
            else
              ..._kategoriler!.entries.map((e) {
                final k = e.key;
                final ad = e.value['ad'] as String;
                final seviye = e.value['seviye'] as String;
                final selected = _kategori == k;
                final color = seviye == 'Kritik'
                    ? AppColors.danger
                    : seviye == 'Yuksek' ? AppColors.warning : AppColors.info;

                return Padding(
                  padding: const EdgeInsets.only(bottom: 8),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(10),
                    onTap: () => setState(() {
                      _kategori = k;
                      _altKategori = null;
                    }),
                    child: Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: selected ? color.withOpacity(0.15) : null,
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: selected ? color : Colors.grey.withOpacity(0.3),
                          width: selected ? 2 : 1,
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            selected ? Icons.radio_button_checked : Icons.radio_button_off,
                            color: color,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(ad,
                                style: TextStyle(
                                    fontWeight: selected ? FontWeight.bold : FontWeight.w500)),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: color.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(seviye,
                                style: TextStyle(fontSize: 10, color: color,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              }),

            if (altKategoriler != null && altKategoriler.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Text('Alt Kategori (opsiyonel)',
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 6, runSpacing: 6,
                children: altKategoriler.map((alt) => ChoiceChip(
                      label: Text(alt as String, style: const TextStyle(fontSize: 12)),
                      selected: _altKategori == alt,
                      onSelected: (v) => setState(() => _altKategori = v ? alt : null),
                    )).toList(),
              ),
            ],

            const SizedBox(height: 20),
            const Text('Ne oldu? (isim verme — "bir öğrenci" gibi)',
                style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            TextField(
              controller: _aciklamaCtrl,
              maxLines: 5,
              maxLength: 2000,
              decoration: InputDecoration(
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                hintText: 'Yaşadığın/gördüğün durumu anlat...',
              ),
            ),

            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _neredeCtrl,
                    decoration: InputDecoration(
                      labelText: 'Nerede?',
                      hintText: 'örn. koridor',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _neZamanCtrl,
                    decoration: InputDecoration(
                      labelText: 'Ne zaman?',
                      hintText: 'örn. bugün',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _kimIcin,
              decoration: InputDecoration(
                labelText: 'Kimle ilgili?',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
              items: const [
                DropdownMenuItem(value: 'Kendim hakkinda', child: Text('Kendim hakkında')),
                DropdownMenuItem(value: 'Arkadasim hakkinda', child: Text('Arkadaşım hakkında')),
                DropdownMenuItem(value: 'Tanik olduğum olay', child: Text('Tanık olduğum olay')),
              ],
              onChanged: (v) => setState(() => _kimIcin = v!),
            ),
            const SizedBox(height: 12),
            CheckboxListTile(
              value: _geriDonus,
              onChanged: (v) => setState(() => _geriDonus = v ?? false),
              title: const Text('Takip kodu al', style: TextStyle(fontSize: 13)),
              subtitle: const Text('İhbarının durumunu sorgulayabilmek için (anonim kalır)',
                  style: TextStyle(fontSize: 11)),
              contentPadding: EdgeInsets.zero,
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 52,
              child: ElevatedButton.icon(
                onPressed: _gondering ? null : _gonder,
                icon: const Icon(Icons.lock_outline),
                label: _gondering
                    ? const SizedBox(
                        width: 20, height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('ANONİM GÖNDER', style: TextStyle(letterSpacing: 1.2)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.danger,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
