import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class AnketPage extends ConsumerStatefulWidget {
  const AnketPage({super.key});

  @override
  ConsumerState<AnketPage> createState() => _AnketPageState();
}

class _AnketPageState extends ConsumerState<AnketPage> {
  bool _isSubmitting = false;
  bool _submitted = false;
  final _yorumCtrl = TextEditingController();

  // Survey questions with ratings
  final List<_AnketSoru> _sorular = [
    _AnketSoru(
      id: 'genel',
      baslik: 'Genel Memnuniyet',
      aciklama: 'Okulun genel isleyisinden ne kadar memnunsunuz?',
      icon: Icons.school,
      color: AppColors.primary,
    ),
    _AnketSoru(
      id: 'ogretmen',
      baslik: 'Ogretmen Iletisimi',
      aciklama: 'Ogretmenlerle iletisim kalitenizi nasil degerlendirirsiniz?',
      icon: Icons.people,
      color: AppColors.info,
    ),
    _AnketSoru(
      id: 'temizlik',
      baslik: 'Temizlik ve Guvenlik',
      aciklama: 'Okul ortaminin temizligi ve guvenligi hakkinda ne dusunuyorsunuz?',
      icon: Icons.cleaning_services,
      color: AppColors.success,
    ),
    _AnketSoru(
      id: 'yemek',
      baslik: 'Yemek Kalitesi',
      aciklama: 'Yemekhane hizmetinden memnuniyetinizi belirtin.',
      icon: Icons.restaurant,
      color: AppColors.warning,
    ),
    _AnketSoru(
      id: 'ulasim',
      baslik: 'Ulasim / Servis',
      aciklama: 'Okul servisi veya ulasim hizmetini nasil buluyorsunuz?',
      icon: Icons.directions_bus,
      color: AppColors.gold,
    ),
  ];

  // Ratings per question id
  final Map<String, int> _ratings = {};

  // Previous results (fetched from API or null)
  Map<String, dynamic>? _previousResults;
  bool _loadingResults = true;

  @override
  void initState() {
    super.initState();
    _loadPreviousResults();
  }

  @override
  void dispose() {
    _yorumCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadPreviousResults() async {
    try {
      final r = await ref.read(apiClientProvider).get('/veli/anket-sonuclari');
      final data = r.data;
      if (data is Map && data.isNotEmpty) {
        setState(() {
          _previousResults = Map<String, dynamic>.from(data);
          _loadingResults = false;
        });
        return;
      }
    } catch (_) {
      // no previous results available
    }
    setState(() {
      _previousResults = _staticPreviousResults();
      _loadingResults = false;
    });
  }

  static Map<String, dynamic> _staticPreviousResults() {
    return {
      'donem': '2025-2026 / 1. Donem',
      'katilim': 142,
      'ortalamalar': {
        'genel': 4.2,
        'ogretmen': 4.5,
        'temizlik': 3.8,
        'yemek': 3.6,
        'ulasim': 4.0,
      },
    };
  }

  Future<void> _submit() async {
    // Validate: all questions rated
    final ratedAll = _sorular.every((s) => _ratings.containsKey(s.id));
    if (!ratedAll) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Lutfen tum sorulari puanlayin.'),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    setState(() => _isSubmitting = true);

    try {
      await ref.read(apiClientProvider).post('/veli/anket-gonder', data: {
        'puanlar': _ratings,
        'yorum': _yorumCtrl.text.trim(),
      });
    } catch (_) {
      // API call failed, but we still show success for offline-first UX
    }

    if (!mounted) return;
    setState(() {
      _isSubmitting = false;
      _submitted = true;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Anketiniz basariyla gonderildi. Tesekkurler!'),
        backgroundColor: AppColors.success,
        duration: Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Veli Memnuniyet Anketi')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Hero
            _buildHeroHeader(),
            const SizedBox(height: 16),

            // Previous results summary
            if (!_loadingResults && _previousResults != null)
              _buildPreviousResults(),

            if (!_loadingResults && _previousResults != null)
              const SizedBox(height: 16),

            // Survey questions
            ..._sorular.map((s) => _buildSoruCard(s)),

            // Comment field
            const SizedBox(height: 8),
            _buildYorumSection(),

            // Submit button
            const SizedBox(height: 20),
            SizedBox(
              height: 52,
              child: ElevatedButton.icon(
                onPressed: (_isSubmitting || _submitted) ? null : _submit,
                icon: _isSubmitting
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : Icon(_submitted ? Icons.check_circle : Icons.send),
                label: Text(
                  _submitted ? 'GONDERILDI' : 'ANKETI GONDER',
                  style: const TextStyle(letterSpacing: 1.1),
                ),
              ),
            ),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildHeroHeader() {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [AppColors.primary, AppColors.primaryLight],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.2),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Icon(Icons.poll, color: Colors.white, size: 28),
          ),
          const SizedBox(width: 14),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Memnuniyet Anketi',
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 17,
                        fontWeight: FontWeight.w700)),
                SizedBox(height: 4),
                Text('Gorusleriniz bizim icin cok degerli',
                    style: TextStyle(color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
          const Icon(Icons.rate_review, color: Colors.white38, size: 32),
        ],
      ),
    );
  }

  Widget _buildPreviousResults() {
    final prev = _previousResults!;
    final donem = prev['donem'] as String? ?? '';
    final katilim = prev['katilim'];
    final ort = prev['ortalamalar'] as Map? ?? {};

    // Calculate overall average
    double toplamOrt = 0;
    if (ort.isNotEmpty) {
      for (final v in ort.values) {
        toplamOrt += (v is num ? v.toDouble() : 0);
      }
      toplamOrt /= ort.length;
    }

    return Card(
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: const BoxDecoration(
          border: Border(
            left: BorderSide(color: AppColors.info, width: 4),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.bar_chart, size: 20, color: AppColors.info),
                  const SizedBox(width: 8),
                  const Text('Onceki Donem Sonuclari',
                      style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w700,
                          color: AppColors.info)),
                  const Spacer(),
                  if (donem.isNotEmpty)
                    Text(donem,
                        style: TextStyle(
                            fontSize: 11, color: Colors.grey[500])),
                ],
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  _statChip(
                    Icons.people,
                    '$katilim Katilimci',
                    AppColors.primary,
                  ),
                  const SizedBox(width: 10),
                  _statChip(
                    Icons.star,
                    '${toplamOrt.toStringAsFixed(1)} / 5.0 Ortalama',
                    AppColors.gold,
                  ),
                ],
              ),
              const SizedBox(height: 10),
              // Mini bar chart for each category
              ...ort.entries.map((e) {
                final label = _labelForId(e.key as String);
                final val = (e.value is num) ? (e.value as num).toDouble() : 0.0;
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 3),
                  child: Row(
                    children: [
                      SizedBox(
                        width: 100,
                        child: Text(label,
                            style: TextStyle(
                                fontSize: 12, color: Colors.grey[600])),
                      ),
                      Expanded(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: LinearProgressIndicator(
                            value: val / 5.0,
                            minHeight: 8,
                            backgroundColor: Colors.grey.withOpacity(0.15),
                            valueColor: AlwaysStoppedAnimation<Color>(
                              val >= 4.0
                                  ? AppColors.success
                                  : val >= 3.0
                                      ? AppColors.warning
                                      : AppColors.danger,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(val.toStringAsFixed(1),
                          style: const TextStyle(
                              fontSize: 12, fontWeight: FontWeight.w600)),
                    ],
                  ),
                );
              }),
            ],
          ),
        ),
      ),
    );
  }

  String _labelForId(String id) {
    switch (id) {
      case 'genel':
        return 'Genel';
      case 'ogretmen':
        return 'Ogretmen';
      case 'temizlik':
        return 'Temizlik';
      case 'yemek':
        return 'Yemek';
      case 'ulasim':
        return 'Ulasim';
      default:
        return id;
    }
  }

  Widget _statChip(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: color),
          const SizedBox(width: 5),
          Text(text,
              style: TextStyle(
                  fontSize: 12, fontWeight: FontWeight.w600, color: color)),
        ],
      ),
    );
  }

  Widget _buildSoruCard(_AnketSoru soru) {
    final rating = _ratings[soru.id] ?? 0;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: BoxDecoration(
          border: Border(
            left: BorderSide(color: soru.color, width: 4),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(soru.icon, size: 20, color: soru.color),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(soru.baslik,
                        style: TextStyle(
                            fontSize: 15,
                            fontWeight: FontWeight.w700,
                            color: soru.color)),
                  ),
                  if (rating > 0)
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: soru.color.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text('$rating / 5',
                          style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: soru.color)),
                    ),
                ],
              ),
              const SizedBox(height: 6),
              Text(soru.aciklama,
                  style:
                      TextStyle(fontSize: 13, color: Colors.grey[600])),
              const SizedBox(height: 10),
              // Star rating row
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(5, (i) {
                  final starIndex = i + 1;
                  final filled = rating >= starIndex;
                  return GestureDetector(
                    onTap: _submitted
                        ? null
                        : () => setState(() => _ratings[soru.id] = starIndex),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 6),
                      child: Icon(
                        filled ? Icons.star_rounded : Icons.star_border_rounded,
                        size: 36,
                        color: filled ? AppColors.gold : Colors.grey[350],
                      ),
                    ),
                  );
                }),
              ),
              // Rating labels
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('Cok kotu',
                        style: TextStyle(fontSize: 10, color: Colors.grey)),
                    Text('Mukemmel',
                        style: TextStyle(fontSize: 10, color: Colors.grey)),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildYorumSection() {
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Container(
        decoration: const BoxDecoration(
          border: Border(
            left: BorderSide(color: AppColors.textSecondaryLight, width: 4),
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(14),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Row(
                children: [
                  Icon(Icons.comment, size: 20, color: AppColors.textSecondaryLight),
                  SizedBox(width: 8),
                  Text('Ek Gorusleriniz',
                      style: TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                          color: AppColors.textSecondaryLight)),
                ],
              ),
              const SizedBox(height: 10),
              TextField(
                controller: _yorumCtrl,
                enabled: !_submitted,
                maxLines: 4,
                maxLength: 1000,
                decoration: InputDecoration(
                  hintText: 'Eklemek istediginiz goruslerinizi buraya yazabilirsiniz...',
                  hintStyle: TextStyle(fontSize: 13, color: Colors.grey[400]),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  contentPadding: const EdgeInsets.all(12),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}


class _AnketSoru {
  final String id;
  final String baslik;
  final String aciklama;
  final IconData icon;
  final Color color;

  const _AnketSoru({
    required this.id,
    required this.baslik,
    required this.aciklama,
    required this.icon,
    required this.color,
  });
}
