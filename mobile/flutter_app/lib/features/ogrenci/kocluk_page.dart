import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class KoclukPage extends ConsumerStatefulWidget {
  const KoclukPage({super.key});
  @override
  ConsumerState<KoclukPage> createState() => _KoclukPageState();
}

class _KoclukPageState extends ConsumerState<KoclukPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/ogrenci/notlar').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🏅 Eğitim Koçluğu')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final genelOrt = (d['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
          final dersler = (d['ders_ozetleri'] as List?) ?? [];

          return ListView(padding: const EdgeInsets.all(16), children: [
            // Hero
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [AppColors.gold, Color(0xFFD97706)]),
                borderRadius: BorderRadius.circular(16)),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                const Text('🏅', style: TextStyle(fontSize: 36)),
                const SizedBox(height: 8),
                const Text('Eğitim Koçluğu', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                Text('Kişisel gelişim planın + hedefler + koç desteği',
                    style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 12)),
              ]),
            ),
            const SizedBox(height: 16),

            // Akademik durum ozet
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: (genelOrt >= 70 ? AppColors.success : AppColors.warning).withOpacity(0.1),
                borderRadius: BorderRadius.circular(12)),
              child: Row(children: [
                Text(genelOrt.toStringAsFixed(1),
                    style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold,
                        color: genelOrt >= 70 ? AppColors.success : AppColors.warning)),
                const SizedBox(width: 12),
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('Genel Ortalama', style: TextStyle(fontWeight: FontWeight.bold)),
                  Text(genelOrt >= 85 ? 'Mükemmel! 🌟' : genelOrt >= 70 ? 'İyi gidiyorsun 👍' :
                       genelOrt >= 50 ? 'Geliştirebilirsin 💪' : 'Desteğe ihtiyacın var ⚠️',
                      style: const TextStyle(fontSize: 12)),
                ]),
              ]),
            ),
            const SizedBox(height: 16),

            // Guclu / zayif dersler
            if (dersler.isNotEmpty) ...[
              const Text('📊 Ders Bazlı Durum', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 10),
              ...dersler.map((dd) {
                final d = dd as Map;
                final ort = (d['ortalama'] as num).toDouble();
                Color c = ort >= 85 ? AppColors.success : ort >= 70 ? AppColors.info :
                          ort >= 50 ? AppColors.warning : AppColors.danger;
                String durum = ort >= 85 ? '🌟 Güçlü' : ort >= 70 ? '✓ İyi' :
                               ort >= 50 ? '⚠️ Geliştir' : '🔴 Odaklan';
                return Card(margin: const EdgeInsets.only(bottom: 6), child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: c.withOpacity(0.15),
                    child: Text(ort.toStringAsFixed(0), style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 13)),
                  ),
                  title: Text(d['ders'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                  subtitle: LinearProgressIndicator(
                    value: ort / 100, minHeight: 4,
                    backgroundColor: c.withOpacity(0.1), valueColor: AlwaysStoppedAnimation(c)),
                  trailing: Text(durum, style: TextStyle(fontSize: 10, color: c)),
                ));
              }),
            ],
            const SizedBox(height: 16),

            // SMART hedef
            const Text('🎯 Hedefler (SMART)', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            _HedefKart(hedef: 'Matematik ortalamasını 75\'e çıkar', durum: 'devam', ilerleme: 0.6),
            _HedefKart(hedef: 'Haftalık 3 kitap oku', durum: 'devam', ilerleme: 0.4),
            _HedefKart(hedef: 'İngilizce CEFR A2 seviyesi', durum: 'devam', ilerleme: 0.7),
            const SizedBox(height: 16),

            // Koc ile gorusme
            Card(child: ListTile(
              leading: Container(
                width: 44, height: 44,
                decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                child: const Icon(Icons.person, color: AppColors.gold),
              ),
              title: const Text('Koçunla Görüş', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Haftalık 1:1 görüşme planla', style: TextStyle(fontSize: 12)),
              trailing: const Icon(Icons.arrow_forward_ios, size: 14),
              onTap: () => ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Koç görüşme — yakında'), backgroundColor: AppColors.gold)),
            )),
          ]);
        },
      ),
    );
  }
}


class _HedefKart extends StatelessWidget {
  final String hedef; final String durum; final double ilerleme;
  const _HedefKart({required this.hedef, required this.durum, required this.ilerleme});

  @override
  Widget build(BuildContext context) {
    return Card(margin: const EdgeInsets.only(bottom: 8), child: Padding(
      padding: const EdgeInsets.all(12),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          const Icon(Icons.flag, color: AppColors.gold, size: 18),
          const SizedBox(width: 8),
          Expanded(child: Text(hedef, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13))),
          Text('%${(ilerleme * 100).toStringAsFixed(0)}', style: const TextStyle(
              color: AppColors.gold, fontWeight: FontWeight.bold)),
        ]),
        const SizedBox(height: 8),
        ClipRRect(
          borderRadius: BorderRadius.circular(6),
          child: LinearProgressIndicator(value: ilerleme, minHeight: 8,
              backgroundColor: AppColors.gold.withOpacity(0.1),
              valueColor: const AlwaysStoppedAnimation(AppColors.gold)),
        ),
      ]),
    ));
  }
}
