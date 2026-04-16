import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';
import '../../shared/widgets/ogrenci_secici.dart';


class GorusmePage extends ConsumerStatefulWidget {
  const GorusmePage({super.key});

  @override
  ConsumerState<GorusmePage> createState() => _GorusmePageState();
}

class _GorusmePageState extends ConsumerState<GorusmePage> {
  Future<List<dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(rehberApiProvider).gorusmeler());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🗣️ Görüşme Kayıtları')),
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.add),
        label: const Text('Yeni Görüşme'),
        onPressed: () async {
          await showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            builder: (_) => const _YeniGorusmeSheet(),
          );
          _load();
        },
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final list = snap.data ?? [];
          if (list.isEmpty) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(32),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.record_voice_over, size: 48, color: Colors.grey),
                    SizedBox(height: 12),
                    Text('Henüz görüşme kaydı yok'),
                    SizedBox(height: 4),
                    Text('Sağ altta "Yeni Görüşme" butonuyla başla',
                        style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
                  ],
                ),
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: list.length,
              itemBuilder: (_, i) {
                final g = list[i];
                return Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ExpansionTile(
                    leading: const CircleAvatar(
                      backgroundColor: AppColors.info,
                      child: Icon(Icons.chat, color: Colors.white),
                    ),
                    title: Text('Öğrenci ID: ${g['student_id']?.toString().substring(0, 8) ?? '-'}',
                        style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                    subtitle: Text(
                      '${(g['tarih'] ?? '').toString().substring(0, 16)} · ${g['sure_dakika']} dk',
                      style: const TextStyle(fontSize: 12),
                    ),
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(14),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            if ((g['gorusen'] as String? ?? '').isNotEmpty) ...[
                              Text('Görüşen: ${g['gorusen']}',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.w600, color: AppColors.gold)),
                              const SizedBox(height: 8),
                            ],
                            const Text('Notlar',
                                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
                            const SizedBox(height: 4),
                            Container(
                              padding: const EdgeInsets.all(10),
                              decoration: BoxDecoration(
                                color: Colors.grey.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(g['notlar'] ?? '',
                                  style: const TextStyle(fontSize: 13)),
                            ),
                            if ((g['sonraki_adim'] as String? ?? '').isNotEmpty) ...[
                              const SizedBox(height: 8),
                              const Text('Sonraki Adım',
                                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
                              const SizedBox(height: 4),
                              Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: AppColors.warning.withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(6),
                                ),
                                child: Text(g['sonraki_adim'] ?? '',
                                    style: const TextStyle(fontSize: 13)),
                              ),
                            ],
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}


class _YeniGorusmeSheet extends ConsumerStatefulWidget {
  const _YeniGorusmeSheet();

  @override
  ConsumerState<_YeniGorusmeSheet> createState() => _YeniGorusmeSheetState();
}

class _YeniGorusmeSheetState extends ConsumerState<_YeniGorusmeSheet> {
  Map<String, dynamic>? _ogrenci;
  int _sure = 30;
  final _notCtrl = TextEditingController();
  final _sonrakiCtrl = TextEditingController();
  bool _gondering = false;

  @override
  void dispose() {
    _notCtrl.dispose();
    _sonrakiCtrl.dispose();
    super.dispose();
  }

  Future<void> _gonder() async {
    if (_ogrenci == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Öğrenci seç')),
      );
      return;
    }
    if (_notCtrl.text.trim().length < 10) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Notlar en az 10 karakter')),
      );
      return;
    }
    setState(() => _gondering = true);
    try {
      await ref.read(rehberApiProvider).gorusmeEkle(
        studentId: _ogrenci!['id'] as String,
        sureDakika: _sure,
        notlar: _notCtrl.text.trim(),
        sonrakiAdim: _sonrakiCtrl.text.trim(),
      );
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Görüşme kaydedildi'), backgroundColor: AppColors.success),
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
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 20, right: 20, top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Yeni Görüşme Kaydı',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),

            // Ogrenci secici
            InkWell(
              onTap: () async {
                final secilen = await OgrenciSeciciDialog.show(context);
                if (secilen != null) setState(() => _ogrenci = secilen);
              },
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey.withOpacity(0.4)),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.person, color: AppColors.primary),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        _ogrenci == null
                            ? 'Öğrenci Seç *'
                            : '${_ogrenci!['ad_soyad']} · ${_ogrenci!['sinif']}/${_ogrenci!['sube']}',
                        style: TextStyle(
                          fontSize: 14,
                          color: _ogrenci == null ? Colors.grey : null,
                        ),
                      ),
                    ),
                    const Icon(Icons.arrow_drop_down),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                const Text('Süre:', style: TextStyle(fontSize: 14)),
                Expanded(
                  child: Slider(
                    value: _sure.toDouble(),
                    min: 10, max: 120,
                    divisions: 11,
                    label: '$_sure dk',
                    onChanged: (v) => setState(() => _sure = v.toInt()),
                  ),
                ),
                Text('$_sure dk', style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 12),

            TextField(
              controller: _notCtrl,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'Notlar *',
                hintText: 'Görüşmede konuşulan konular, tespitler...',
                border: OutlineInputBorder(),
                helperText: 'Anahtar kelimeler (zorbalık, intihar, madde vs) açık yaz — motor okur.',
              ),
            ),
            const SizedBox(height: 12),

            TextField(
              controller: _sonrakiCtrl,
              maxLines: 2,
              decoration: const InputDecoration(
                labelText: 'Sonraki Adım (opsiyonel)',
                hintText: 'örn. 1 hafta sonra kontrol görüşmesi',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),

            SizedBox(
              height: 50,
              child: ElevatedButton.icon(
                onPressed: _gondering ? null : _gonder,
                icon: _gondering
                    ? const SizedBox(width: 20, height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.save),
                label: const Text('GÖRÜŞMEYİ KAYDET'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
