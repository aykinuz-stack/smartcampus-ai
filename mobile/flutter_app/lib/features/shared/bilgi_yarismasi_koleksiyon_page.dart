import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';
import 'quiz_game_page.dart';

/// Bilgi Yarışmaları Koleksiyonu — 4 yarışma türü
class BilgiYarismasiKoleksiyonPage extends ConsumerWidget {
  const BilgiYarismasiKoleksiyonPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Bilgi Yarışmaları')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Hero banner
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF1E1B4B), Color(0xFF7C3AED)],
                ),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(Icons.emoji_events, color: Color(0xFFFFD700), size: 28),
                      ),
                      const SizedBox(width: 14),
                      const Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Bilgi Yarışmaları',
                                style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                            Text('Koleksiyonu',
                                style: TextStyle(color: Colors.white70, fontSize: 14)),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _HeroBadge(label: '4 Yarışma', icon: Icons.category),
                      _HeroBadge(label: '3700+ Soru', icon: Icons.quiz),
                      _HeroBadge(label: '4 Seviye', icon: Icons.trending_up),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            const Text('Yarışma Seç',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),

            // 4 yarışma kartı
            _YarismaCard(
              baslik: 'Genel Kültür',
              aciklama: 'Tarih, Coğrafya, Bilim, Edebiyat, Spor',
              ikon: Icons.school,
              renk: const Color(0xFF7C3AED),
              soruSayisi: 250,
              onTap: () => _showGenelKulturDialog(context, ref),
            ),
            const SizedBox(height: 10),
            _YarismaCard(
              baslik: 'Kim Milyoner',
              aciklama: '15 soru, 3 joker, artan zorluk',
              ikon: Icons.emoji_events,
              renk: const Color(0xFFF59E0B),
              soruSayisi: 1997,
              onTap: () => _showSeviyeDialog(context, ref, 'kim-milyoner',
                  ['ilkokul', 'ortaokul', 'lise', 'yetiskin'], 15),
            ),
            const SizedBox(height: 10),
            _YarismaCard(
              baslik: 'Bilgi Yarışması',
              aciklama: '20 soru, kategori bazlı puanlama',
              ikon: Icons.quiz,
              renk: const Color(0xFF10B981),
              soruSayisi: 1500,
              onTap: () => _showSeviyeDialog(context, ref, 'bilgi-yarismasi',
                  ['ilkokul', 'ortaokul', 'lise'], 20),
            ),
            const SizedBox(height: 10),
            _YarismaCard(
              baslik: 'Kazanım Pekiştirme',
              aciklama: 'Ders/ünite bazlı soru bankası',
              ikon: Icons.auto_fix_high,
              renk: const Color(0xFF3B82F6),
              soruSayisi: 0,
              onTap: () => _showKPDialog(context, ref),
            ),
          ],
        ),
      ),
    );
  }

  void _showGenelKulturDialog(BuildContext context, WidgetRef ref) {
    final kategoriler = ['karisik', 'Tarih', 'Coğrafya', 'Bilim', 'Edebiyat', 'Spor', 'Türkiye'];
    String secili = 'karisik';
    int adet = 10;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setS) => Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Genel Kültür', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 14),
              const Text('Kategori', style: TextStyle(fontWeight: FontWeight.w600)),
              const SizedBox(height: 6),
              Wrap(
                spacing: 6, runSpacing: 6,
                children: kategoriler.map((k) => ChoiceChip(
                  label: Text(k == 'karisik' ? 'Karışık' : k),
                  selected: secili == k,
                  selectedColor: const Color(0xFF7C3AED).withOpacity(0.3),
                  onSelected: (_) => setS(() => secili = k),
                )).toList(),
              ),
              const SizedBox(height: 14),
              const Text('Soru Sayısı', style: TextStyle(fontWeight: FontWeight.w600)),
              const SizedBox(height: 6),
              Wrap(
                spacing: 8,
                children: [5, 10, 15, 20].map((n) => ChoiceChip(
                  label: Text('$n'),
                  selected: adet == n,
                  selectedColor: const Color(0xFF7C3AED).withOpacity(0.3),
                  onSelected: (_) => setS(() => adet = n),
                )).toList(),
              ),
              const SizedBox(height: 18),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.pop(ctx);
                    _startGK(context, ref, secili, adet);
                  },
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Başla'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF7C3AED),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ),
              const SizedBox(height: 10),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _startGK(BuildContext ctx, WidgetRef ref, String kategori, int adet) async {
    try {
      final api = ref.read(apiClientProvider);
      final r = await api.get('/quiz-koleksiyon/genel-kultur',
          params: {'kategori': kategori, 'adet': adet});
      final sorular = List<Map<String, dynamic>>.from(r.data['sorular']);
      if (!ctx.mounted) return;
      Navigator.push(ctx, MaterialPageRoute(
        builder: (_) => QuizGamePage(
          baslik: 'Genel Kültür',
          sorular: sorular,
          renk: const Color(0xFF7C3AED),
        ),
      ));
    } catch (e) {
      if (ctx.mounted) {
        ScaffoldMessenger.of(ctx).showSnackBar(
          SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger));
      }
    }
  }

  void _showSeviyeDialog(BuildContext context, WidgetRef ref,
      String tur, List<String> seviyeler, int adet) {
    final labels = {
      'ilkokul': 'İlkokul', 'ortaokul': 'Ortaokul',
      'lise': 'Lise', 'yetiskin': 'Yetişkin',
    };

    showModalBottomSheet(
      context: context,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(tur == 'kim-milyoner' ? 'Kim Milyoner' : 'Bilgi Yarışması',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            const Text('Seviye seç:'),
            const SizedBox(height: 10),
            ...seviyeler.map((s) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pop(ctx);
                    _startQuiz(context, ref, tur, s, adet);
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: tur == 'kim-milyoner'
                        ? const Color(0xFFF59E0B) : const Color(0xFF10B981),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                  child: Text(labels[s] ?? s,
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
            )),
            const SizedBox(height: 6),
          ],
        ),
      ),
    );
  }

  Future<void> _startQuiz(BuildContext ctx, WidgetRef ref,
      String tur, String seviye, int adet) async {
    try {
      final api = ref.read(apiClientProvider);
      final r = await api.get('/quiz-koleksiyon/$tur',
          params: {'seviye': seviye, 'adet': adet});
      final sorular = List<Map<String, dynamic>>.from(r.data['sorular']);
      if (!ctx.mounted) return;
      Navigator.push(ctx, MaterialPageRoute(
        builder: (_) => QuizGamePage(
          baslik: tur == 'kim-milyoner' ? 'Kim Milyoner' : 'Bilgi Yarışması',
          sorular: sorular,
          renk: tur == 'kim-milyoner'
              ? const Color(0xFFF59E0B) : const Color(0xFF10B981),
          timerSaniye: tur == 'kim-milyoner' ? 60 : 30,
        ),
      ));
    } catch (e) {
      if (ctx.mounted) {
        ScaffoldMessenger.of(ctx).showSnackBar(
          SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger));
      }
    }
  }

  void _showKPDialog(BuildContext context, WidgetRef ref) {
    int sinif = 9;
    String ders = 'Matematik';
    final dersler9 = ['Edebiyat', 'Matematik', 'Fizik', 'Kimya', 'Biyoloji',
        'Tarih', 'Coğrafya', 'Felsefe', 'Din Kültürü', 'İngilizce'];

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setS) => Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Kazanım Pekiştirme',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 14),
              DropdownButtonFormField<int>(
                value: sinif,
                decoration: const InputDecoration(labelText: 'Sınıf', isDense: true,
                    border: OutlineInputBorder()),
                items: List.generate(12, (i) =>
                    DropdownMenuItem(value: i + 1, child: Text('${i + 1}. Sınıf'))),
                onChanged: (v) => setS(() => sinif = v ?? 9),
              ),
              const SizedBox(height: 10),
              DropdownButtonFormField<String>(
                value: dersler9.contains(ders) ? ders : dersler9.first,
                decoration: const InputDecoration(labelText: 'Ders', isDense: true,
                    border: OutlineInputBorder()),
                items: dersler9.map((d) =>
                    DropdownMenuItem(value: d, child: Text(d))).toList(),
                onChanged: (v) => setS(() => ders = v ?? 'Matematik'),
              ),
              const SizedBox(height: 18),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.pop(ctx);
                    _startKP(context, ref, sinif, ders);
                  },
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Başla'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF3B82F6),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ),
              const SizedBox(height: 10),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _startKP(BuildContext ctx, WidgetRef ref, int sinif, String ders) async {
    try {
      final api = ref.read(apiClientProvider);
      final r = await api.get('/quiz-koleksiyon/kazanim-pekistirme/sorular',
          params: {'sinif': sinif, 'ders': ders, 'adet': 10});
      final sorular = List<Map<String, dynamic>>.from(r.data['sorular']);
      if (sorular.isEmpty) {
        if (ctx.mounted) {
          ScaffoldMessenger.of(ctx).showSnackBar(
            const SnackBar(content: Text('Bu ders için soru bulunamadı'),
                backgroundColor: AppColors.warning));
        }
        return;
      }
      if (!ctx.mounted) return;
      Navigator.push(ctx, MaterialPageRoute(
        builder: (_) => QuizGamePage(
          baslik: '$sinif. Sınıf $ders',
          sorular: sorular,
          renk: const Color(0xFF3B82F6),
        ),
      ));
    } catch (e) {
      if (ctx.mounted) {
        ScaffoldMessenger.of(ctx).showSnackBar(
          SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger));
      }
    }
  }
}


class _HeroBadge extends StatelessWidget {
  final String label;
  final IconData icon;
  const _HeroBadge({required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 11)),
      ],
    );
  }
}


class _YarismaCard extends StatelessWidget {
  final String baslik;
  final String aciklama;
  final IconData ikon;
  final Color renk;
  final int soruSayisi;
  final VoidCallback onTap;
  const _YarismaCard({
    required this.baslik, required this.aciklama, required this.ikon,
    required this.renk, required this.soruSayisi, required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(14),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: renk.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: renk.withOpacity(0.15),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(ikon, color: renk, size: 28),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(baslik, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 2),
                  Text(aciklama, style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
                ],
              ),
            ),
            if (soruSayisi > 0)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: renk.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text('$soruSayisi', style: TextStyle(color: renk,
                    fontSize: 12, fontWeight: FontWeight.bold)),
              ),
            const SizedBox(width: 6),
            Icon(Icons.chevron_right, color: renk),
          ],
        ),
      ),
    );
  }
}
