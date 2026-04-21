import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Ortak Bildirim Sayfası — tüm roller kullanır.
class BildirimPage extends ConsumerStatefulWidget {
  const BildirimPage({super.key});

  @override
  ConsumerState<BildirimPage> createState() => _BildirimPageState();
}

class _BildirimPageState extends ConsumerState<BildirimPage> {
  Future<Map<String, dynamic>>? _future;
  bool _sadece0kunmamis = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() {
      _future = ref.read(apiClientProvider)
          .get('/bildirim/liste', params: {
            'limit': 50,
            'sadece_okunmamis': _sadece0kunmamis,
          })
          .then((r) => Map<String, dynamic>.from(r.data));
    });
  }

  Future<void> _okundu(String id) async {
    await ref.read(apiClientProvider).post('/bildirim/$id/okundu');
    _load();
  }

  Future<void> _tumunuOku() async {
    await ref.read(apiClientProvider).post('/bildirim/tumunu-oku');
    _load();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bildirimler'),
        actions: [
          IconButton(
            icon: const Icon(Icons.done_all),
            tooltip: 'Tümünü oku',
            onPressed: _tumunuOku,
          ),
          IconButton(
            icon: Icon(_sadece0kunmamis
                ? Icons.filter_alt
                : Icons.filter_alt_outlined),
            tooltip: _sadece0kunmamis ? 'Tümünü göster' : 'Sadece okunmamış',
            onPressed: () {
              setState(() => _sadece0kunmamis = !_sadece0kunmamis);
              _load();
            },
          ),
        ],
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
          final bildirimler = (data['bildirimler'] as List?) ?? [];
          final okunmamis = (data['okunmamis'] as int?) ?? 0;

          if (bildirimler.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.notifications_off_outlined,
                      size: 64, color: Colors.grey[400]),
                  const SizedBox(height: 12),
                  const Text('Bildirim yok',
                      style: TextStyle(fontSize: 16, color: AppColors.textSecondaryDark)),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: Column(
              children: [
                // Özet bar
                if (okunmamis > 0)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    color: AppColors.primary.withOpacity(0.08),
                    child: Text(
                      '$okunmamis okunmamış bildirim',
                      style: const TextStyle(fontSize: 13,
                          fontWeight: FontWeight.w600, color: AppColors.primary),
                    ),
                  ),
                Expanded(
                  child: ListView.builder(
                    itemCount: bildirimler.length,
                    itemBuilder: (_, i) {
                      final b = Map<String, dynamic>.from(bildirimler[i] as Map);
                      return _BildirimTile(
                        bildirim: b,
                        onOkundu: () => _okundu(b['id'] as String? ?? ''),
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _BildirimTile extends StatelessWidget {
  final Map<String, dynamic> bildirim;
  final VoidCallback onOkundu;
  const _BildirimTile({required this.bildirim, required this.onOkundu});

  IconData _iconFor(String tur) {
    switch (tur) {
      case 'sinav': return Icons.quiz;
      case 'odev': return Icons.assignment;
      case 'not': return Icons.grade;
      case 'uyari': return Icons.warning_amber;
      case 'duyuru': return Icons.campaign;
      case 'hatirlatma': return Icons.notifications_active;
      case 'onay': return Icons.approval;
      default: return Icons.notifications;
    }
  }

  Color _colorFor(String tur) {
    switch (tur) {
      case 'sinav': return AppColors.danger;
      case 'odev': return AppColors.gold;
      case 'not': return AppColors.success;
      case 'uyari': return AppColors.warning;
      case 'duyuru': return AppColors.primary;
      case 'hatirlatma': return AppColors.info;
      case 'onay': return const Color(0xFF7C3AED);
      default: return AppColors.info;
    }
  }

  @override
  Widget build(BuildContext context) {
    final baslik = bildirim['baslik'] as String? ?? '';
    final mesaj = bildirim['mesaj'] as String? ?? '';
    final tur = bildirim['tur'] as String? ?? '';
    final gonderen = bildirim['gonderen'] as String? ?? '';
    final tarih = bildirim['tarih'] as String? ?? '';
    final okundu = bildirim['okundu'] as bool? ?? false;

    final c = _colorFor(tur);

    // Tarih formatlama
    String zamanStr = '';
    try {
      final dt = DateTime.parse(tarih);
      final fark = DateTime.now().difference(dt);
      if (fark.inMinutes < 60) {
        zamanStr = '${fark.inMinutes} dk önce';
      } else if (fark.inHours < 24) {
        zamanStr = '${fark.inHours} saat önce';
      } else {
        zamanStr = '${fark.inDays} gün önce';
      }
    } catch (_) {
      zamanStr = tarih;
    }

    return InkWell(
      onTap: okundu ? null : onOkundu,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: okundu ? null : c.withOpacity(0.04),
          border: Border(
            left: BorderSide(color: c, width: okundu ? 2 : 4),
            bottom: BorderSide(color: Colors.grey.withOpacity(0.1)),
          ),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: c.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(_iconFor(tur), color: c, size: 20),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(baslik,
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: okundu ? FontWeight.w500 : FontWeight.w700,
                            ),
                            maxLines: 1, overflow: TextOverflow.ellipsis),
                      ),
                      if (!okundu)
                        Container(
                          width: 8, height: 8,
                          decoration: BoxDecoration(
                            color: c, shape: BoxShape.circle,
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(mesaj, style: TextStyle(fontSize: 12,
                      color: Colors.grey[600]),
                      maxLines: 2, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Text(gonderen,
                          style: const TextStyle(fontSize: 10,
                              fontWeight: FontWeight.w500,
                              color: AppColors.textSecondaryDark)),
                      const Spacer(),
                      Text(zamanStr,
                          style: const TextStyle(fontSize: 10,
                              color: AppColors.textSecondaryDark)),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
