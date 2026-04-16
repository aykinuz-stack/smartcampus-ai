import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';

/// Öğrenci mood check-in sayfası — 5 saniyede kaydet.
class MoodCheckinPage extends ConsumerStatefulWidget {
  const MoodCheckinPage({super.key});

  @override
  ConsumerState<MoodCheckinPage> createState() => _MoodCheckinPageState();
}

class _MoodCheckinPageState extends ConsumerState<MoodCheckinPage> {
  int? _selectedLevel;
  final Set<String> _selectedTags = {};
  bool _submitting = false;
  Map<String, dynamic>? _todayCheckin;

  static const _moodOptions = [
    {'level': 5, 'emoji': '😄', 'label': 'Harika', 'color': AppColors.mood5},
    {'level': 4, 'emoji': '🙂', 'label': 'İyi', 'color': AppColors.mood4},
    {'level': 3, 'emoji': '😐', 'label': 'İdare eder', 'color': AppColors.mood3},
    {'level': 2, 'emoji': '😟', 'label': 'Kötü', 'color': AppColors.mood2},
    {'level': 1, 'emoji': '😢', 'label': 'Çok kötü', 'color': AppColors.mood1},
  ];

  static const _tags = [
    '💪 Enerjik', '😴 Yorgun', '😰 Kaygılı', '😠 Sinirli',
    '🤔 Kafam karışık', '💔 Üzgün', '🎉 Heyecanlı', '🙏 Şükürlü',
    '😕 Yalnız', '😤 Stresli', '🤕 Hasta', '🥱 Uyuşuk',
  ];

  @override
  void initState() {
    super.initState();
    _loadToday();
  }

  Future<void> _loadToday() async {
    try {
      final resp = await ref.read(apiClientProvider).get('/mood/today');
      if (resp.data != null) {
        setState(() {
          _todayCheckin = Map<String, dynamic>.from(resp.data);
          _selectedLevel = _todayCheckin!['level'];
          _selectedTags.clear();
          _selectedTags.addAll(List<String>.from(_todayCheckin!['tags'] ?? []));
        });
      }
    } catch (_) {}
  }

  Future<void> _submit() async {
    if (_selectedLevel == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Lütfen bir seviye seç')),
      );
      return;
    }
    setState(() => _submitting = true);
    try {
      final resp = await ref.read(apiClientProvider).post(
        '/mood/checkin',
        data: {
          'level': _selectedLevel,
          'tags': _selectedTags.toList(),
          'not': '',
        },
      );
      if (resp.statusCode == 201) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Row(children: const [
              Icon(Icons.check_circle, color: Colors.white),
              SizedBox(width: 8),
              Text('Ruh halin kaydedildi. Sağlıklı günler!'),
            ]),
            backgroundColor: AppColors.success,
            duration: const Duration(seconds: 2),
          ),
        );
        setState(() => _todayCheckin = Map<String, dynamic>.from(resp.data));
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Bugünkü Ruh Halin'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Gizlilik bilgisi
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: AppColors.info.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.info.withOpacity(0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.lock_outline, color: AppColors.info),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Text(
                      'Gizli. Sadece rehber öğretmen görebilir — arkadaşların ve öğretmenlerin göremez.',
                      style: TextStyle(fontSize: 13),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            if (_todayCheckin != null) ...[
              Card(
                color: AppColors.primary.withOpacity(0.15),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      Text(
                        _moodOptions.firstWhere(
                                (m) => m['level'] == _todayCheckin!['level'])['emoji']
                            as String,
                        style: const TextStyle(fontSize: 40),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Bugün işaretledin:',
                                style: TextStyle(fontSize: 13, color: AppColors.textSecondaryDark)),
                            Text(
                              _moodOptions.firstWhere(
                                      (m) => m['level'] == _todayCheckin!['level'])['label']
                                  as String,
                              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                            ),
                            if ((_todayCheckin!['tags'] as List).isNotEmpty)
                              Padding(
                                padding: const EdgeInsets.only(top: 4),
                                child: Text(
                                  (_todayCheckin!['tags'] as List).join(' · '),
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: isDark ? AppColors.textSecondaryDark : AppColors.textSecondaryLight,
                                  ),
                                ),
                              ),
                            const SizedBox(height: 4),
                            const Text('İstersen değiştirebilirsin:',
                                style: TextStyle(fontSize: 12, color: AppColors.gold)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),
            ],

            const Text(
              'Nasıl hissediyorsun?',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 12),

            // 5 emoji
            ..._moodOptions.map((m) {
              final isSelected = _selectedLevel == m['level'];
              final color = m['color'] as Color;
              return Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: GestureDetector(
                  onTap: () => setState(() => _selectedLevel = m['level'] as int),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: isSelected ? color.withOpacity(0.2) : (isDark ? AppColors.cardDark : Colors.white),
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(
                        color: isSelected ? color : Colors.grey.withOpacity(0.3),
                        width: isSelected ? 2.5 : 1,
                      ),
                    ),
                    child: Row(
                      children: [
                        Text(m['emoji'] as String, style: const TextStyle(fontSize: 36)),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Text(
                            m['label'] as String,
                            style: TextStyle(
                              fontSize: 17,
                              fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                              color: isSelected ? color : null,
                            ),
                          ),
                        ),
                        if (isSelected) Icon(Icons.check_circle, color: color),
                      ],
                    ),
                  ),
                ),
              );
            }),

            const SizedBox(height: 20),
            const Text(
              'Etiketler (opsiyonel)',
              style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _tags.map((tag) {
                final isSelected = _selectedTags.contains(tag);
                return FilterChip(
                  label: Text(tag),
                  selected: isSelected,
                  onSelected: (v) {
                    setState(() {
                      if (v) _selectedTags.add(tag);
                      else _selectedTags.remove(tag);
                    });
                  },
                );
              }).toList(),
            ),

            const SizedBox(height: 28),
            SizedBox(
              height: 56,
              child: ElevatedButton(
                onPressed: _submitting ? null : _submit,
                child: _submitting
                    ? const SizedBox(width: 24, height: 24,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text(_todayCheckin != null ? 'GÜNCELLE' : 'KAYDET',
                        style: const TextStyle(fontSize: 16, letterSpacing: 1.2)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
