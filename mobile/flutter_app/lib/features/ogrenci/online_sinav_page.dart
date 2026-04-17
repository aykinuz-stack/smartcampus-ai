import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class OnlineSinavPage extends ConsumerStatefulWidget {
  const OnlineSinavPage({super.key});
  @override
  ConsumerState<OnlineSinavPage> createState() => _OnlineSinavPageState();
}

class _OnlineSinavPageState extends ConsumerState<OnlineSinavPage> {
  Future<List<dynamic>>? _future;

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/ogrenci/notlar').then((r) {
      // Yaklasilan sinavlari goster (yazili notlar son tarih bazli)
      final notlar = (r.data['notlar'] as List?) ?? [];
      return notlar.where((n) => (n['not_turu'] ?? '').toString().toLowerCase()
          .contains('yazili')).take(15).toList();
    }));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📝 Online Sınav')),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final sinavlar = snap.data ?? [];

          return ListView(padding: const EdgeInsets.all(16), children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
                borderRadius: BorderRadius.circular(14)),
              child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('📝 Online Sınav Sistemi', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                SizedBox(height: 4),
                Text('QR kod veya link ile sınava gir, mobilde çöz', style: TextStyle(color: Colors.white70, fontSize: 12)),
              ]),
            ),
            const SizedBox(height: 16),

            // QR ile sinava gir
            Card(child: ListTile(
              leading: Container(
                width: 44, height: 44,
                decoration: BoxDecoration(color: AppColors.gold.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                child: const Icon(Icons.qr_code_scanner, color: AppColors.gold),
              ),
              title: const Text('QR ile Sınava Gir', style: TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Öğretmenin gösterdiği QR kodu tara', style: TextStyle(fontSize: 12)),
              trailing: const Icon(Icons.arrow_forward_ios, size: 14),
              onTap: () => ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('QR tarayıcı — yakında'), backgroundColor: AppColors.gold)),
            )),
            const SizedBox(height: 16),

            // Son sinav sonuclari
            const Text('Son Sınav Sonuçlarım', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            if (sinavlar.isEmpty)
              const Padding(padding: EdgeInsets.all(24), child: Center(child: Text('Sınav sonucu yok')))
            else
              ...sinavlar.map((s) {
                final ss = s as Map;
                final puan = (ss['puan'] as num?)?.toDouble() ?? 0;
                Color c = puan >= 85 ? AppColors.success : puan >= 70 ? AppColors.info :
                          puan >= 50 ? AppColors.warning : AppColors.danger;
                return Card(margin: const EdgeInsets.only(bottom: 6), child: ListTile(
                  leading: Container(
                    width: 44, height: 44,
                    decoration: BoxDecoration(color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                    child: Center(child: Text(puan.toStringAsFixed(0),
                        style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 16))),
                  ),
                  title: Text(ss['ders'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                  subtitle: Text('${ss['not_turu']} ${ss['not_sirasi']} · ${ss['tarih']}',
                      style: const TextStyle(fontSize: 11)),
                ));
              }),
          ]);
        },
      ),
    );
  }
}
