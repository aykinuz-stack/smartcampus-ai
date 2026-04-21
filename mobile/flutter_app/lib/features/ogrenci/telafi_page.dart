import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Telafi Gorevleri — RED/YELLOW/GREEN/BLUE renk bandi bazli
class TelafiPage extends ConsumerStatefulWidget {
  const TelafiPage({super.key});

  @override
  ConsumerState<TelafiPage> createState() => _TelafiPageState();
}

class _TelafiPageState extends ConsumerState<TelafiPage>
    with SingleTickerProviderStateMixin {
  Future<Map<String, dynamic>>? _future;
  late final TabController _tabCtrl;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  void _load() {
    setState(() {
      _future = ref.read(apiClientProvider)
          .get('/ogrenci/telafi-gorevleri')
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Telafi Gorevleri'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(text: 'Aktif'),
            Tab(text: 'Tamamlanan'),
          ],
        ),
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snap.hasError) {
            return Center(child: Text('Hata: ${snap.error}'));
          }
          final data = snap.data ?? {};
          final aktif = (data['aktif'] as List?) ?? [];
          final tamamlanan = (data['tamamlanan'] as List?) ?? [];

          return TabBarView(
            controller: _tabCtrl,
            children: [
              // Aktif
              aktif.isEmpty
                  ? const Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.check_circle, size: 64, color: AppColors.success),
                          SizedBox(height: 12),
                          Text('Aktif telafi gorevi yok',
                              style: TextStyle(fontSize: 16)),
                        ],
                      ),
                    )
                  : RefreshIndicator(
                      onRefresh: () async => _load(),
                      child: ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: aktif.length,
                        itemBuilder: (_, i) => _TelafiKart(
                          gorev: Map<String, dynamic>.from(aktif[i] as Map),
                          tamamlandi: false,
                        ),
                      ),
                    ),
              // Tamamlanan
              tamamlanan.isEmpty
                  ? const Center(child: Text('Henuz tamamlanan gorev yok'))
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: tamamlanan.length,
                      itemBuilder: (_, i) => _TelafiKart(
                        gorev: Map<String, dynamic>.from(tamamlanan[i] as Map),
                        tamamlandi: true,
                      ),
                    ),
            ],
          );
        },
      ),
    );
  }
}


class _TelafiKart extends StatelessWidget {
  final Map<String, dynamic> gorev;
  final bool tamamlandi;
  const _TelafiKart({required this.gorev, required this.tamamlandi});

  Color _renkFor(String band) {
    switch (band.toUpperCase()) {
      case 'RED': return AppColors.danger;
      case 'YELLOW': return AppColors.warning;
      case 'GREEN': return AppColors.success;
      case 'BLUE': return AppColors.info;
      default: return Colors.grey;
    }
  }

  String _turAciklama(String band) {
    switch (band.toUpperCase()) {
      case 'RED': return 'Ozet + Quiz (2 asama)';
      case 'YELLOW': return 'Pekistirme (5 soru)';
      case 'GREEN': return 'Haftalik tekrar (8 soru)';
      case 'BLUE': return 'Zor set + Hiz calismasi';
      default: return 'Telafi gorevi';
    }
  }

  @override
  Widget build(BuildContext context) {
    final ders = gorev['ders'] as String? ?? '';
    final band = gorev['band'] as String? ?? gorev['color_band'] as String? ?? 'YELLOW';
    final tur = gorev['task_type'] as String? ?? '';
    final tarih = gorev['created_at'] as String? ?? '';
    final status = gorev['status'] as String? ?? '';
    final soruSayisi = gorev['question_count'] as int? ?? 0;

    final c = _renkFor(band);

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(color: c, width: 4)),
        ),
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: c.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(band,
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: c)),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(ders,
                      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                ),
                if (tamamlandi)
                  const Icon(Icons.check_circle, color: AppColors.success, size: 20)
                else
                  Icon(Icons.pending, color: c, size: 20),
              ],
            ),
            const SizedBox(height: 8),
            Text(_turAciklama(band),
                style: TextStyle(fontSize: 12, color: Colors.grey[600])),
            if (tur.isNotEmpty)
              Text('Tur: $tur', style: TextStyle(fontSize: 11, color: Colors.grey[500])),
            const SizedBox(height: 6),
            Row(
              children: [
                if (soruSayisi > 0) ...[
                  Icon(Icons.quiz, size: 14, color: c),
                  const SizedBox(width: 4),
                  Text('$soruSayisi soru', style: TextStyle(fontSize: 11, color: c)),
                  const SizedBox(width: 12),
                ],
                Icon(Icons.calendar_today, size: 14, color: Colors.grey[500]),
                const SizedBox(width: 4),
                Text(tarih.length >= 10 ? tarih.substring(0, 10) : tarih,
                    style: TextStyle(fontSize: 11, color: Colors.grey[500])),
                const Spacer(),
                if (!tamamlandi)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: c.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(
                      status == 'in_progress' ? 'Devam ediyor' : 'Bekliyor',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: c),
                    ),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
