import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';


class ErkenUyariPage extends ConsumerStatefulWidget {
  const ErkenUyariPage({super.key});

  @override
  ConsumerState<ErkenUyariPage> createState() => _ErkenUyariPageState();
}

class _ErkenUyariPageState extends ConsumerState<ErkenUyariPage> {
  Future<List<dynamic>>? _ozetFuture;
  Future<List<dynamic>>? _riskliFuture;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() {
      _ozetFuture = ref.read(yoneticiApiProvider).erkenUyariOzet();
      _riskliFuture = ref.read(yoneticiApiProvider).riskliOgrenciler();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('⚠️ Erken Uyarı')),
      body: RefreshIndicator(
        onRefresh: () async => _load(),
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Kategori bazli ozet
            const Text('Kategori Bazlı Risk',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            FutureBuilder<List<dynamic>>(
              future: _ozetFuture,
              builder: (_, snap) {
                if (snap.connectionState == ConnectionState.waiting) {
                  return const Padding(
                    padding: EdgeInsets.all(24),
                    child: Center(child: CircularProgressIndicator()),
                  );
                }
                final list = snap.data ?? [];
                if (list.isEmpty) return const Text('Henüz risk verisi yok (hesaplama gerekli)');
                return Column(
                  children: list.map((k) => _KategoriKart(data: k)).toList(),
                );
              },
            ),

            const SizedBox(height: 20),
            const Text('Riskli Öğrenciler (Skor 45+)',
                style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            const SizedBox(height: 10),
            FutureBuilder<List<dynamic>>(
              future: _riskliFuture,
              builder: (_, snap) {
                if (snap.connectionState == ConnectionState.waiting) {
                  return const Padding(
                    padding: EdgeInsets.all(24),
                    child: Center(child: CircularProgressIndicator()),
                  );
                }
                final list = snap.data ?? [];
                if (list.isEmpty) return const Text('Risk altında öğrenci yok 🎉');
                return Column(
                  children: list.map((r) => _RiskliOgrenci(data: r)).toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}


class _KategoriKart extends StatelessWidget {
  final dynamic data;
  const _KategoriKart({required this.data});

  @override
  Widget build(BuildContext context) {
    final toplam = (data['toplam'] as num?)?.toInt() ?? 0;
    final kritik = (data['kritik'] as num?)?.toInt() ?? 0;
    final yuksek = (data['yuksek'] as num?)?.toInt() ?? 0;
    final izlenen = (data['izlenen'] as num?)?.toInt() ?? 0;
    Color c = kritik > 0 ? AppColors.danger : (yuksek > 0 ? AppColors.warning : AppColors.info);

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(data['kategori'] ?? '',
                    style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600)),
                const Spacer(),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: c.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text('$toplam',
                      style: TextStyle(color: c, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              children: [
                _Seviye(label: '🟡 İzlenen', deger: izlenen, color: AppColors.info),
                const SizedBox(width: 8),
                _Seviye(label: '🟠 Yüksek', deger: yuksek, color: AppColors.warning),
                const SizedBox(width: 8),
                _Seviye(label: '🔴 Kritik', deger: kritik, color: AppColors.danger),
              ],
            ),
          ],
        ),
      ),
    );
  }
}


class _Seviye extends StatelessWidget {
  final String label;
  final int deger;
  final Color color;
  const _Seviye({required this.label, required this.deger, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 8),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(6),
        ),
        child: Column(
          children: [
            Text('$deger',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: const TextStyle(fontSize: 10)),
          ],
        ),
      ),
    );
  }
}


class _RiskliOgrenci extends StatelessWidget {
  final dynamic data;
  const _RiskliOgrenci({required this.data});

  @override
  Widget build(BuildContext context) {
    final skor = (data['behavioral_risk_score'] as num?)?.toDouble() ?? 0.0;
    Color c;
    if (skor >= 70) c = AppColors.danger;
    else if (skor >= 55) c = AppColors.warning;
    else c = AppColors.info;

    return Card(
      margin: const EdgeInsets.only(bottom: 6),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: c.withOpacity(0.15),
          child: Text(skor.toStringAsFixed(0),
              style: TextStyle(color: c, fontWeight: FontWeight.bold)),
        ),
        title: Text(data['student_name'] ?? '?',
            style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('Seviye: ${data['behavioral_risk_level'] ?? '-'}'),
        trailing: const Icon(Icons.chevron_right),
      ),
    );
  }
}
