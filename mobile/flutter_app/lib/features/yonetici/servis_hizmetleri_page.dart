import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Servis Hizmetleri — okul servisleri yonetimi
class ServisHizmetleriPage extends ConsumerStatefulWidget {
  const ServisHizmetleriPage({super.key});

  @override
  ConsumerState<ServisHizmetleriPage> createState() => _ServisHizmetleriPageState();
}

class _ServisHizmetleriPageState extends ConsumerState<ServisHizmetleriPage> {
  List<Map<String, dynamic>> _servisler = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final r = await ref.read(apiClientProvider).get('/yonetici/servis-bilgileri');
      setState(() {
        _servisler = List<Map<String, dynamic>>.from(
          (r.data['servisler'] as List?)?.map((e) => Map<String, dynamic>.from(e as Map)) ?? [],
        );
        _loading = false;
      });
    } catch (_) {
      setState(() {
        _servisler = _ornekServisler;
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final aktif = _servisler.where((s) => s['aktif'] == true).length;

    return Scaffold(
      appBar: AppBar(title: const Text('Servis Hizmetleri')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: () async => _load(),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  // Ozet
                  Row(
                    children: [
                      _OzetKutu('Toplam', '${_servisler.length}', AppColors.primary, Icons.directions_bus),
                      const SizedBox(width: 10),
                      _OzetKutu('Aktif', '$aktif', AppColors.success, Icons.check_circle),
                      const SizedBox(width: 10),
                      _OzetKutu('Pasif', '${_servisler.length - aktif}', AppColors.danger, Icons.cancel),
                    ],
                  ),
                  const SizedBox(height: 20),

                  const Text('Servis Listesi',
                      style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 12),

                  ..._servisler.map((s) => _ServisKart(servis: s)),
                ],
              ),
            ),
    );
  }
}


class _OzetKutu extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  final IconData icon;
  const _OzetKutu(this.label, this.value, this.color, this.icon);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 22),
            const SizedBox(height: 4),
            Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: const TextStyle(fontSize: 11)),
          ],
        ),
      ),
    );
  }
}


class _ServisKart extends StatelessWidget {
  final Map<String, dynamic> servis;
  const _ServisKart({required this.servis});

  @override
  Widget build(BuildContext context) {
    final plaka = servis['plaka'] as String? ?? '';
    final guzergah = servis['guzergah'] as String? ?? '';
    final sofor = servis['sofor'] as String? ?? '';
    final ogrenciSayisi = servis['ogrenci_sayisi'] as int? ?? 0;
    final kapasite = servis['kapasite'] as int? ?? 0;
    final aktif = servis['aktif'] as bool? ?? true;
    final kalkis = servis['kalkis_saati'] as String? ?? '';
    final varis = servis['varis_saati'] as String? ?? '';

    Color c = aktif ? AppColors.success : AppColors.danger;

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ExpansionTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: c.withOpacity(0.12),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(Icons.directions_bus, color: c, size: 22),
        ),
        title: Text(plaka, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(guzergah, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
          decoration: BoxDecoration(
            color: c.withOpacity(0.12),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Text(aktif ? 'Aktif' : 'Pasif',
              style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: c)),
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _DetayRow(Icons.person, 'Sofor', sofor),
                _DetayRow(Icons.people, 'Ogrenci', '$ogrenciSayisi / $kapasite'),
                _DetayRow(Icons.access_time, 'Kalkis', kalkis),
                _DetayRow(Icons.flag, 'Varis', varis),
                const SizedBox(height: 8),
                // Doluluk bar
                LinearProgressIndicator(
                  value: kapasite > 0 ? ogrenciSayisi / kapasite : 0,
                  backgroundColor: Colors.grey.withOpacity(0.2),
                  color: ogrenciSayisi / (kapasite > 0 ? kapasite : 1) > 0.8
                      ? AppColors.danger : AppColors.success,
                ),
                const SizedBox(height: 4),
                Text('Doluluk: ${kapasite > 0 ? (ogrenciSayisi / kapasite * 100).toStringAsFixed(0) : 0}%',
                    style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


class _DetayRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _DetayRow(this.icon, this.label, this.value);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        children: [
          Icon(icon, size: 16, color: AppColors.textSecondaryDark),
          const SizedBox(width: 8),
          Text('$label: ', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          Text(value, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }
}


final _ornekServisler = <Map<String, dynamic>>[
  {
    'plaka': '34 ABC 123', 'guzergah': 'Kadikoy - Uskudar', 'sofor': 'Ahmet Yilmaz',
    'ogrenci_sayisi': 28, 'kapasite': 34, 'aktif': true,
    'kalkis_saati': '07:15', 'varis_saati': '07:50',
  },
  {
    'plaka': '34 DEF 456', 'guzergah': 'Maltepe - Kartal', 'sofor': 'Mehmet Demir',
    'ogrenci_sayisi': 22, 'kapasite': 30, 'aktif': true,
    'kalkis_saati': '07:00', 'varis_saati': '07:45',
  },
  {
    'plaka': '34 GHI 789', 'guzergah': 'Atasehir - Umraniye', 'sofor': 'Ali Kaya',
    'ogrenci_sayisi': 31, 'kapasite': 34, 'aktif': true,
    'kalkis_saati': '07:10', 'varis_saati': '07:55',
  },
  {
    'plaka': '34 JKL 012', 'guzergah': 'Pendik - Tuzla', 'sofor': 'Veli Celik',
    'ogrenci_sayisi': 0, 'kapasite': 28, 'aktif': false,
    'kalkis_saati': '-', 'varis_saati': '-',
  },
];
