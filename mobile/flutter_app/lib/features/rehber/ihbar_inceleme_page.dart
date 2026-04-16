import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/rehber_yonetici_api.dart';
import '../../core/theme/app_theme.dart';


class IhbarIncelemePage extends ConsumerStatefulWidget {
  const IhbarIncelemePage({super.key});

  @override
  ConsumerState<IhbarIncelemePage> createState() => _IhbarIncelemePageState();
}

class _IhbarIncelemePageState extends ConsumerState<IhbarIncelemePage> {
  Future<List<dynamic>>? _future;
  String? _durumFiltre;
  String? _kategoriFiltre;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(rehberApiProvider).ihbarListe(
      durum: _durumFiltre, kategori: _kategoriFiltre,
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🚨 İhbar İnceleme'),
        actions: [
          PopupMenuButton<String?>(
            icon: const Icon(Icons.filter_list),
            onSelected: (v) { setState(() => _durumFiltre = v); _load(); },
            itemBuilder: (_) => const [
              PopupMenuItem(value: null, child: Text('Hepsi')),
              PopupMenuItem(value: 'Yeni', child: Text('Yeni')),
              PopupMenuItem(value: 'Inceleniyor', child: Text('İnceleniyor')),
              PopupMenuItem(value: 'Mudahale Edildi', child: Text('Müdahale Edildi')),
              PopupMenuItem(value: 'Cozuldu', child: Text('Çözüldü')),
            ],
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final list = snap.data ?? [];
          if (list.isEmpty) {
            return const Center(
              child: Padding(
                padding: EdgeInsets.all(32),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.shield_outlined, size: 48, color: Colors.grey),
                    SizedBox(height: 12),
                    Text('İhbar yok'),
                  ],
                ),
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: list.length,
              itemBuilder: (_, i) => _IhbarKart(ihbar: list[i]),
            ),
          );
        },
      ),
    );
  }
}


class _IhbarKart extends StatelessWidget {
  final dynamic ihbar;
  const _IhbarKart({required this.ihbar});

  @override
  Widget build(BuildContext context) {
    final seviye = ihbar['seviye'] as String? ?? 'Orta';
    final kategori = ihbar['kategori_ad'] as String? ?? ihbar['kategori'] ?? '';
    final durum = ihbar['durum'] as String? ?? 'Yeni';

    Color seviyeColor;
    IconData kategoriIcon;
    switch (seviye.toLowerCase()) {
      case 'kritik': seviyeColor = AppColors.danger; break;
      case 'yuksek': seviyeColor = AppColors.warning; break;
      default: seviyeColor = AppColors.info;
    }
    switch ((ihbar['kategori'] as String? ?? '').toLowerCase()) {
      case 'akran_zorbaligi': kategoriIcon = Icons.report_problem; break;
      case 'intihar_riski': kategoriIcon = Icons.healing; break;
      case 'madde_kullanim': kategoriIcon = Icons.smoking_rooms; break;
      case 'cinsel_taciz': kategoriIcon = Icons.dangerous; break;
      case 'aile_ici_siddet': kategoriIcon = Icons.home; break;
      default: kategoriIcon = Icons.shield;
    }

    Color durumColor;
    switch (durum) {
      case 'Yeni': durumColor = AppColors.danger; break;
      case 'Inceleniyor': durumColor = AppColors.warning; break;
      case 'Mudahale Edildi': durumColor = AppColors.info; break;
      case 'Cozuldu': durumColor = AppColors.success; break;
      default: durumColor = Colors.grey;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ExpansionTile(
        leading: CircleAvatar(
          backgroundColor: seviyeColor.withOpacity(0.15),
          child: Icon(kategoriIcon, color: seviyeColor),
        ),
        title: Row(
          children: [
            Expanded(
              child: Text(kategori,
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: seviyeColor.withOpacity(0.15),
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(seviye,
                  style: TextStyle(color: seviyeColor, fontSize: 10, fontWeight: FontWeight.bold)),
            ),
          ],
        ),
        subtitle: Row(
          children: [
            Text(
              (ihbar['olusturma_tarihi'] as String? ?? '').substring(0,
                  (ihbar['olusturma_tarihi'] as String? ?? '').length.clamp(0, 16)),
              style: const TextStyle(fontSize: 11),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
              decoration: BoxDecoration(
                color: durumColor.withOpacity(0.15),
                borderRadius: BorderRadius.circular(3),
              ),
              child: Text(durum,
                  style: TextStyle(color: durumColor, fontSize: 9)),
            ),
          ],
        ),
        children: [
          Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _Detay(label: 'Alt Kategori', value: ihbar['alt_kategori']),
                _Detay(label: 'Nerede', value: ihbar['nerede']),
                _Detay(label: 'Ne Zaman', value: ihbar['ne_zaman']),
                _Detay(label: 'Kimle İlgili', value: ihbar['kim_icin']),
                const SizedBox(height: 8),
                const Text('Açıklama',
                    style: TextStyle(fontWeight: FontWeight.w600, fontSize: 12)),
                const SizedBox(height: 4),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.grey.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(ihbar['aciklama'] ?? '',
                      style: const TextStyle(fontSize: 13)),
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(Icons.fingerprint, size: 14, color: AppColors.textSecondaryDark),
                    const SizedBox(width: 4),
                    Text('Anonim ID: ${ihbar['anonim_id']}',
                        style: const TextStyle(
                            fontSize: 11, color: AppColors.textSecondaryDark,
                            fontFamily: 'monospace')),
                  ],
                ),
                const SizedBox(height: 12),
                if (durum != 'Cozuldu') ...[
                  const Divider(),
                  const SizedBox(height: 8),
                  Wrap(spacing: 8, children: [
                    if (durum == 'Yeni')
                      _DurumButonu(label: 'İncele', color: AppColors.warning,
                          onTap: () {}),
                    _DurumButonu(label: 'Müdahale', color: AppColors.info,
                        onTap: () {}),
                    _DurumButonu(label: 'Çözüldü', color: AppColors.success,
                        onTap: () {}),
                  ]),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}


class _Detay extends StatelessWidget {
  final String label;
  final dynamic value;
  const _Detay({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    final s = value?.toString() ?? '';
    if (s.isEmpty || s == '-') return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text('$label:',
                style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
          ),
          Expanded(child: Text(s, style: const TextStyle(fontSize: 12))),
        ],
      ),
    );
  }
}


class _DurumButonu extends StatelessWidget {
  final String label;
  final Color color;
  final VoidCallback onTap;
  const _DurumButonu({required this.label, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: onTap,
      style: TextButton.styleFrom(
        backgroundColor: color.withOpacity(0.1),
        foregroundColor: color,
      ),
      child: Text(label),
    );
  }
}
