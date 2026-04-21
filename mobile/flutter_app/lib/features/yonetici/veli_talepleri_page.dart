import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Veli Talepleri — yonetici icin gelen veli talepleri listesi
class VeliTalepleriPage extends ConsumerStatefulWidget {
  const VeliTalepleriPage({super.key});

  @override
  ConsumerState<VeliTalepleriPage> createState() => _VeliTalepleriPageState();
}

class _VeliTalepleriPageState extends ConsumerState<VeliTalepleriPage>
    with SingleTickerProviderStateMixin {
  late final TabController _tabCtrl;
  List<Map<String, dynamic>> _talepler = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
    _load();
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final r = await ref.read(apiClientProvider).get('/yonetici/veli-talepleri');
      setState(() {
        _talepler = List<Map<String, dynamic>>.from(
          (r.data['talepler'] as List?)?.map((e) => Map<String, dynamic>.from(e as Map)) ?? [],
        );
        _loading = false;
      });
    } catch (_) {
      // Fallback statik veri
      setState(() {
        _talepler = _ornekTalepler;
        _loading = false;
      });
    }
  }

  List<Map<String, dynamic>> _filtrele(String durum) {
    if (durum == 'hepsi') return _talepler;
    return _talepler.where((t) => t['durum'] == durum).toList();
  }

  @override
  Widget build(BuildContext context) {
    final bekleyen = _filtrele('bekliyor');
    final onaylanan = _filtrele('onaylandi');
    final reddedilen = _filtrele('reddedildi');

    return Scaffold(
      appBar: AppBar(
        title: const Text('Veli Talepleri'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: [
            Tab(text: 'Bekleyen (${bekleyen.length})'),
            Tab(text: 'Onaylanan (${onaylanan.length})'),
            Tab(text: 'Reddedilen (${reddedilen.length})'),
          ],
        ),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabCtrl,
              children: [
                _TalepListesi(talepler: bekleyen, aksiyon: true),
                _TalepListesi(talepler: onaylanan, aksiyon: false),
                _TalepListesi(talepler: reddedilen, aksiyon: false),
              ],
            ),
    );
  }
}


class _TalepListesi extends StatelessWidget {
  final List<Map<String, dynamic>> talepler;
  final bool aksiyon;
  const _TalepListesi({required this.talepler, required this.aksiyon});

  @override
  Widget build(BuildContext context) {
    if (talepler.isEmpty) {
      return const Center(child: Text('Talep yok'));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: talepler.length,
      itemBuilder: (_, i) => _TalepKart(talep: talepler[i], aksiyon: aksiyon),
    );
  }
}


class _TalepKart extends StatelessWidget {
  final Map<String, dynamic> talep;
  final bool aksiyon;
  const _TalepKart({required this.talep, required this.aksiyon});

  Color _durumRenk(String durum) {
    switch (durum) {
      case 'bekliyor': return AppColors.warning;
      case 'onaylandi': return AppColors.success;
      case 'reddedildi': return AppColors.danger;
      default: return Colors.grey;
    }
  }

  IconData _turIkon(String tur) {
    switch (tur) {
      case 'izin': return Icons.event_busy;
      case 'randevu': return Icons.calendar_today;
      case 'belge': return Icons.description;
      case 'sikayet': return Icons.report;
      case 'bilgi': return Icons.info;
      default: return Icons.help;
    }
  }

  @override
  Widget build(BuildContext context) {
    final veli = talep['veli_adi'] as String? ?? '';
    final ogrenci = talep['ogrenci_adi'] as String? ?? '';
    final tur = talep['tur'] as String? ?? '';
    final mesaj = talep['mesaj'] as String? ?? '';
    final durum = talep['durum'] as String? ?? '';
    final tarih = talep['tarih'] as String? ?? '';
    final c = _durumRenk(durum);

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
                Icon(_turIkon(tur), color: c, size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(veli, style: const TextStyle(
                      fontSize: 14, fontWeight: FontWeight.w600)),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: c.withOpacity(0.12),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(tur.toUpperCase(),
                      style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: c)),
                ),
              ],
            ),
            if (ogrenci.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text('Ogrenci: $ogrenci',
                    style: TextStyle(fontSize: 12, color: Colors.grey[600])),
              ),
            const SizedBox(height: 6),
            Text(mesaj, style: const TextStyle(fontSize: 13),
                maxLines: 3, overflow: TextOverflow.ellipsis),
            const SizedBox(height: 8),
            Row(
              children: [
                Text(tarih.length >= 10 ? tarih.substring(0, 10) : tarih,
                    style: const TextStyle(fontSize: 10, color: AppColors.textSecondaryDark)),
                const Spacer(),
                if (aksiyon) ...[
                  TextButton(
                    onPressed: () {},
                    child: const Text('Reddet', style: TextStyle(color: AppColors.danger, fontSize: 12)),
                  ),
                  const SizedBox(width: 4),
                  ElevatedButton(
                    onPressed: () {},
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.success,
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                    ),
                    child: const Text('Onayla', style: TextStyle(fontSize: 12)),
                  ),
                ],
              ],
            ),
          ],
        ),
      ),
    );
  }
}


final _ornekTalepler = <Map<String, dynamic>>[
  {
    'id': 'vt_001', 'veli_adi': 'Ayse Yilmaz', 'ogrenci_adi': 'Mehmet Yilmaz',
    'tur': 'izin', 'mesaj': 'Ogretmen gorusmesi icin 23 Nisan\'da izin istiyorum.',
    'durum': 'bekliyor', 'tarih': '2026-04-21',
  },
  {
    'id': 'vt_002', 'veli_adi': 'Fatma Demir', 'ogrenci_adi': 'Ali Demir',
    'tur': 'belge', 'mesaj': 'Ogrenci belgesi talebim var. Banka icin gerekiyor.',
    'durum': 'bekliyor', 'tarih': '2026-04-20',
  },
  {
    'id': 'vt_003', 'veli_adi': 'Hasan Kaya', 'ogrenci_adi': 'Zeynep Kaya',
    'tur': 'randevu', 'mesaj': 'Sinif ogretmeniyle gorusme talep ediyorum.',
    'durum': 'onaylandi', 'tarih': '2026-04-19',
  },
  {
    'id': 'vt_004', 'veli_adi': 'Emine Celik', 'ogrenci_adi': 'Burak Celik',
    'tur': 'bilgi', 'mesaj': 'Yaz okulu programi hakkinda bilgi almak istiyorum.',
    'durum': 'onaylandi', 'tarih': '2026-04-18',
  },
  {
    'id': 'vt_005', 'veli_adi': 'Mustafa Oz', 'ogrenci_adi': 'Elif Oz',
    'tur': 'sikayet', 'mesaj': 'Servis gec geliyor, lutfen duzeltilsin.',
    'durum': 'reddedildi', 'tarih': '2026-04-17',
  },
];
