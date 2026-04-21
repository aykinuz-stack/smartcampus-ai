import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


class ServisTakipPage extends ConsumerStatefulWidget {
  const ServisTakipPage({super.key});

  @override
  ConsumerState<ServisTakipPage> createState() => _ServisTakipPageState();
}

class _ServisTakipPageState extends ConsumerState<ServisTakipPage> {
  Future<List<Map<String, dynamic>>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = _fetchServisBilgileri());
  }

  Future<List<Map<String, dynamic>>> _fetchServisBilgileri() async {
    try {
      final r = await ref.read(apiClientProvider).get('/veli/servis-bilgileri');
      final data = r.data;
      if (data is Map && data['rotalar'] != null) {
        return List<Map<String, dynamic>>.from(data['rotalar'] as List);
      }
      if (data is List) {
        return List<Map<String, dynamic>>.from(data);
      }
      return _staticData();
    } catch (_) {
      return _staticData();
    }
  }

  static List<Map<String, dynamic>> _staticData() {
    return [
      {
        'rota_adi': 'Rota A - Merkez',
        'sofor_adi': 'Ahmet Yilmaz',
        'kalkis_saati': '07:30',
        'tahmini_varis': '08:05',
        'durum': 'yolda',
        'plaka': '34 ABC 123',
        'ogrenci_sayisi': 18,
      },
      {
        'rota_adi': 'Rota B - Sahil',
        'sofor_adi': 'Mehmet Demir',
        'kalkis_saati': '07:15',
        'tahmini_varis': '07:55',
        'durum': 'tamamlandi',
        'plaka': '34 DEF 456',
        'ogrenci_sayisi': 22,
      },
      {
        'rota_adi': 'Rota C - Tepeustu',
        'sofor_adi': 'Ali Kaya',
        'kalkis_saati': '07:45',
        'tahmini_varis': '08:20',
        'durum': 'bekleniyor',
        'plaka': '34 GHI 789',
        'ogrenci_sayisi': 15,
      },
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Servis Takip')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final rotalar = snap.data ?? [];

          if (rotalar.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.directions_bus_outlined, size: 64, color: Colors.grey),
                  SizedBox(height: 12),
                  Text('Servis bilgisi bulunamadi',
                      style: TextStyle(fontSize: 15)),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: rotalar.length,
              itemBuilder: (_, i) => _ServisKart(data: rotalar[i]),
            ),
          );
        },
      ),
    );
  }
}


class _ServisKart extends StatelessWidget {
  final Map<String, dynamic> data;
  const _ServisKart({required this.data});

  @override
  Widget build(BuildContext context) {
    final durum = (data['durum'] as String? ?? '').toLowerCase();
    Color durumColor;
    IconData durumIcon;
    String durumLabel;

    switch (durum) {
      case 'yolda':
        durumColor = AppColors.success;
        durumIcon = Icons.directions_bus;
        durumLabel = 'Yolda';
        break;
      case 'bekleniyor':
        durumColor = AppColors.warning;
        durumIcon = Icons.access_time;
        durumLabel = 'Bekleniyor';
        break;
      case 'tamamlandi':
        durumColor = Colors.grey;
        durumIcon = Icons.check_circle;
        durumLabel = 'Tamamlandi';
        break;
      default:
        durumColor = AppColors.info;
        durumIcon = Icons.info_outline;
        durumLabel = durum.isNotEmpty ? durum : 'Bilinmiyor';
    }

    final rotaAdi = data['rota_adi'] as String? ?? '';
    final soforAdi = data['sofor_adi'] as String? ?? '';
    final kalkis = data['kalkis_saati'] as String? ?? '';
    final varis = data['tahmini_varis'] as String? ?? '';
    final plaka = data['plaka'] as String? ?? '';
    final ogrenciSayisi = data['ogrenci_sayisi'];

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header: route name + status badge
            Row(
              children: [
                Icon(Icons.route, color: AppColors.primary, size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(rotaAdi,
                      style: const TextStyle(
                          fontSize: 16, fontWeight: FontWeight.w600)),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: durumColor.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(durumIcon, size: 14, color: durumColor),
                      const SizedBox(width: 4),
                      Text(durumLabel,
                          style: TextStyle(
                              color: durumColor,
                              fontSize: 12,
                              fontWeight: FontWeight.bold)),
                    ],
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),
            const Divider(height: 1),
            const SizedBox(height: 12),

            // Driver info
            Row(
              children: [
                const Icon(Icons.person, size: 18,
                    color: AppColors.textSecondaryLight),
                const SizedBox(width: 8),
                Text('Sofor: ',
                    style: TextStyle(
                        fontSize: 13, color: Colors.grey[600])),
                Text(soforAdi,
                    style: const TextStyle(
                        fontSize: 13, fontWeight: FontWeight.w500)),
              ],
            ),
            const SizedBox(height: 8),

            // Plate
            if (plaka.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: Row(
                  children: [
                    const Icon(Icons.confirmation_number_outlined,
                        size: 18, color: AppColors.textSecondaryLight),
                    const SizedBox(width: 8),
                    Text('Plaka: ',
                        style: TextStyle(
                            fontSize: 13, color: Colors.grey[600])),
                    Text(plaka,
                        style: const TextStyle(
                            fontSize: 13, fontWeight: FontWeight.w500)),
                  ],
                ),
              ),

            // Times row
            Row(
              children: [
                _timeChip(
                    Icons.departure_board, 'Kalkis: $kalkis', AppColors.info),
                const SizedBox(width: 12),
                _timeChip(
                    Icons.flag, 'Varis: $varis', AppColors.success),
              ],
            ),

            // Student count
            if (ogrenciSayisi != null) ...[
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.groups_outlined, size: 18,
                      color: AppColors.textSecondaryLight),
                  const SizedBox(width: 8),
                  Text('$ogrenciSayisi ogrenci',
                      style: TextStyle(
                          fontSize: 12, color: Colors.grey[600])),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _timeChip(IconData icon, String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.08),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: color),
          const SizedBox(width: 4),
          Text(text,
              style: TextStyle(
                  fontSize: 12, color: color, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
