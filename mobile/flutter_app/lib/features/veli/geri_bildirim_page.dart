import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/veli_api.dart';
import '../../core/theme/app_theme.dart';


class GeriBildirimPage extends ConsumerStatefulWidget {
  const GeriBildirimPage({super.key});

  @override
  ConsumerState<GeriBildirimPage> createState() => _GeriBildirimPageState();
}

class _GeriBildirimPageState extends ConsumerState<GeriBildirimPage> {
  String _kategori = 'memnuniyet';
  int? _puan;
  final _mesajCtrl = TextEditingController();
  bool _gondering = false;

  static const _kategoriler = {
    'memnuniyet': {'label': 'Memnuniyet', 'icon': Icons.sentiment_very_satisfied, 'color': AppColors.success},
    'oneri': {'label': 'Öneri', 'icon': Icons.lightbulb_outline, 'color': AppColors.info},
    'tesekkur': {'label': 'Teşekkür', 'icon': Icons.favorite, 'color': AppColors.gold},
    'sikayet': {'label': 'Şikayet', 'icon': Icons.report_problem_outlined, 'color': AppColors.warning},
  };

  Future<void> _gonder() async {
    if (_mesajCtrl.text.trim().length < 5) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('En az 5 karakter yaz')),
      );
      return;
    }
    setState(() => _gondering = true);
    try {
      await ref.read(veliApiProvider).geriBildirim(
        kategori: _kategori,
        puan: _puan,
        mesaj: _mesajCtrl.text.trim(),
      );
      if (!mounted) return;
      _mesajCtrl.clear();
      setState(() {
        _puan = null;
      });
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          icon: const Icon(Icons.verified_outlined, color: AppColors.success, size: 48),
          title: const Text('Teşekkürler'),
          content: const Text(
            'Geri bildiriminiz alındı. Yönetim en kısa sürede değerlendirecektir.',
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context), child: const Text('Tamam')),
          ],
        ),
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
    _mesajCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('💬 Geri Bildirim')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Kategori',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8, runSpacing: 8,
              children: _kategoriler.entries.map((e) {
                final k = e.key;
                final data = e.value;
                final selected = _kategori == k;
                return InkWell(
                  onTap: () => setState(() => _kategori = k),
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                    decoration: BoxDecoration(
                      color: selected
                          ? (data['color'] as Color).withOpacity(0.2)
                          : Colors.transparent,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(
                        color: selected ? data['color'] as Color : Colors.grey.withOpacity(0.3),
                        width: selected ? 2 : 1,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(data['icon'] as IconData,
                            color: data['color'] as Color, size: 20),
                        const SizedBox(width: 6),
                        Text(data['label'] as String,
                            style: TextStyle(
                                fontWeight: selected ? FontWeight.bold : FontWeight.w500)),
                      ],
                    ),
                  ),
                );
              }).toList(),
            ),

            if (_kategori == 'memnuniyet') ...[
              const SizedBox(height: 20),
              const Text('Puanınız', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (i) {
                  final s = i + 1;
                  return IconButton(
                    iconSize: 36,
                    icon: Icon(
                      _puan != null && _puan! >= s ? Icons.star : Icons.star_border,
                      color: AppColors.gold,
                    ),
                    onPressed: () => setState(() => _puan = s),
                  );
                }),
              ),
            ],

            const SizedBox(height: 20),
            const Text('Mesajınız',
                style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            TextField(
              controller: _mesajCtrl,
              maxLines: 6,
              maxLength: 2000,
              decoration: InputDecoration(
                hintText: 'Düşüncelerinizi, önerilerinizi veya şikayetlerinizi paylaşın...',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),

            const SizedBox(height: 20),
            SizedBox(
              height: 52,
              child: ElevatedButton.icon(
                onPressed: _gondering ? null : _gonder,
                icon: const Icon(Icons.send),
                label: _gondering
                    ? const SizedBox(width: 20, height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('GERİ BİLDİRİM GÖNDER', style: TextStyle(letterSpacing: 1.2)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
