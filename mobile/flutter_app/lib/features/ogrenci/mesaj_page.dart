import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/ogrenci_api.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';


class MesajPage extends ConsumerStatefulWidget {
  const MesajPage({super.key});

  @override
  ConsumerState<MesajPage> createState() => _MesajPageState();
}

class _MesajPageState extends ConsumerState<MesajPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(mesajApiProvider).getListe());
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final userAsync = ref.watch(currentUserProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('💬 Mesajlarım'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(icon: Icon(Icons.inbox), text: 'Gelen'),
            Tab(icon: Icon(Icons.send), text: 'Giden'),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.edit),
        label: const Text('Yeni Mesaj'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        onPressed: () async {
          await showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            builder: (_) => const _YeniMesajSheet(),
          );
          _load();
        },
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (ctx, snap) {
          if (snap.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snap.data ?? {};
          final tumMesajlar = List<Map<String, dynamic>>.from(
              (data['mesajlar'] as List?) ?? []);
          final user = userAsync.valueOrNull;

          // Gelen/Giden ayır
          final gelen = <Map<String, dynamic>>[];
          final giden = <Map<String, dynamic>>[];
          for (final m in tumMesajlar) {
            final yon = (m['yon'] as String? ?? '').toLowerCase();
            final ad = user?.adSoyad ?? '';
            // Kullanıcı rolüne göre — öğrenciye/veliye gelen
            if (user?.isOgrenci == true || user?.isVeli == true) {
              if (yon.contains('to_veli') || yon.contains('to_ogrenci') ||
                  yon.startsWith('ogretmen_')) {
                gelen.add(m);
              } else {
                giden.add(m);
              }
            } else if (user?.isOgretmen == true) {
              if (yon.contains('to_ogretmen') || yon.startsWith('veli_') ||
                  yon.startsWith('ogrenci_')) {
                gelen.add(m);
              } else {
                giden.add(m);
              }
            } else {
              // Diğer roller — hepsi
              gelen.add(m);
            }
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: TabBarView(
              controller: _tabCtrl,
              children: [
                _MesajListe(mesajlar: gelen, gelenMi: true),
                _MesajListe(mesajlar: giden, gelenMi: false),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _MesajListe extends StatelessWidget {
  final List<Map<String, dynamic>> mesajlar;
  final bool gelenMi;
  const _MesajListe({required this.mesajlar, required this.gelenMi});

  @override
  Widget build(BuildContext context) {
    if (mesajlar.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              gelenMi ? Icons.inbox_outlined : Icons.send_outlined,
              size: 64, color: Colors.grey,
            ),
            const SizedBox(height: 12),
            Text(gelenMi ? 'Gelen mesaj yok' : 'Henüz mesaj göndermedin',
                style: const TextStyle(fontSize: 15)),
            if (!gelenMi) ...[
              const SizedBox(height: 6),
              const Text('Sağ alttan "Yeni Mesaj" ile başla',
                  style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
            ],
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: mesajlar.length,
      itemBuilder: (_, i) => _MesajKart(mesaj: mesajlar[i], gelen: gelenMi),
    );
  }
}


class _MesajKart extends StatelessWidget {
  final Map<String, dynamic> mesaj;
  final bool gelen;
  const _MesajKart({required this.mesaj, required this.gelen});

  @override
  Widget build(BuildContext context) {
    final ad = gelen
        ? (mesaj['ogretmen_adi'] as String? ?? 'Öğretmen')
        : 'Ben → ${mesaj['ogretmen_adi'] ?? 'Alıcı'}';
    final tarih = (mesaj['tarih'] as String? ?? '').substring(0,
        ((mesaj['tarih'] as String? ?? '').length).clamp(0, 16));
    final icerik = mesaj['mesaj'] as String? ?? '';
    final okundu = mesaj['okundu'] as bool? ?? true;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      color: gelen && !okundu ? AppColors.primary.withOpacity(0.08) : null,
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: gelen
              ? AppColors.info.withOpacity(0.15)
              : AppColors.primary.withOpacity(0.15),
          child: Icon(
            gelen ? Icons.inbox : Icons.send,
            color: gelen ? AppColors.info : AppColors.primary,
            size: 20,
          ),
        ),
        title: Row(
          children: [
            Expanded(
              child: Text(ad,
                  style: TextStyle(
                    fontWeight:
                        gelen && !okundu ? FontWeight.bold : FontWeight.w600,
                    fontSize: 14,
                  )),
            ),
            if (gelen && !okundu)
              Container(
                width: 8, height: 8,
                decoration: const BoxDecoration(
                  color: AppColors.primary,
                  shape: BoxShape.circle,
                ),
              ),
          ],
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                icerik,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(fontSize: 13),
              ),
              const SizedBox(height: 4),
              Text(tarih,
                  style: const TextStyle(
                      fontSize: 11, color: AppColors.textSecondaryDark)),
            ],
          ),
        ),
        isThreeLine: true,
        onTap: () {
          showDialog(
            context: context,
            builder: (_) => AlertDialog(
              title: Text(ad, style: const TextStyle(fontSize: 16)),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(tarih,
                      style: const TextStyle(
                          fontSize: 11, color: AppColors.textSecondaryDark)),
                  const SizedBox(height: 12),
                  Text(icerik, style: const TextStyle(fontSize: 14)),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Kapat'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}


class _YeniMesajSheet extends ConsumerStatefulWidget {
  const _YeniMesajSheet();

  @override
  ConsumerState<_YeniMesajSheet> createState() => _YeniMesajSheetState();
}

class _YeniMesajSheetState extends ConsumerState<_YeniMesajSheet> {
  final _aliciCtrl = TextEditingController();
  final _konuCtrl = TextEditingController();
  final _mesajCtrl = TextEditingController();
  String _aliciRol = 'ogretmen';
  bool _gondering = false;

  @override
  void dispose() {
    _aliciCtrl.dispose();
    _konuCtrl.dispose();
    _mesajCtrl.dispose();
    super.dispose();
  }

  Future<void> _gonder() async {
    if (_aliciCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Alıcı adı yaz')),
      );
      return;
    }
    if (_mesajCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Mesaj yaz')),
      );
      return;
    }
    setState(() => _gondering = true);
    try {
      final mesaj = _konuCtrl.text.trim().isNotEmpty
          ? '[${_konuCtrl.text.trim()}]\n\n${_mesajCtrl.text.trim()}'
          : _mesajCtrl.text.trim();
      await ref.read(mesajApiProvider).gonder(
            aliciRol: _aliciRol,
            aliciId: _aliciCtrl.text.trim().toLowerCase().replaceAll(' ', '_'),
            mesaj: mesaj,
          );
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('✓ Mesaj gönderildi'),
          backgroundColor: AppColors.success,
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Hata: $e'), backgroundColor: AppColors.danger),
      );
    } finally {
      if (mounted) setState(() => _gondering = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 20, right: 20, top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      child: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                const Icon(Icons.edit, color: AppColors.primary),
                const SizedBox(width: 10),
                const Text('Yeni Mesaj',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 20),
            DropdownButtonFormField<String>(
              value: _aliciRol,
              decoration: InputDecoration(
                labelText: 'Alıcı Rolü',
                prefixIcon: const Icon(Icons.person),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
              items: const [
                DropdownMenuItem(value: 'ogretmen', child: Text('👨‍🏫 Öğretmen')),
                DropdownMenuItem(value: 'rehber', child: Text('🧠 Rehber')),
                DropdownMenuItem(value: 'yonetici', child: Text('📊 Yönetici')),
                DropdownMenuItem(value: 'veli', child: Text('👨‍👩‍👧 Veli')),
              ],
              onChanged: (v) => setState(() => _aliciRol = v ?? 'ogretmen'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _aliciCtrl,
              decoration: InputDecoration(
                labelText: 'Alıcı Adı',
                hintText: 'Örn: Ahmet Yilmaz',
                prefixIcon: const Icon(Icons.badge),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _konuCtrl,
              decoration: InputDecoration(
                labelText: 'Konu (opsiyonel)',
                prefixIcon: const Icon(Icons.topic),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _mesajCtrl,
              maxLines: 6,
              decoration: InputDecoration(
                labelText: 'Mesaj *',
                hintText: 'Mesajınızı yazın...',
                alignLabelWithHint: true,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 52,
              child: ElevatedButton.icon(
                onPressed: _gondering ? null : _gonder,
                icon: _gondering
                    ? const SizedBox(
                        width: 20, height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.send),
                label: const Text('GÖNDER',
                    style: TextStyle(letterSpacing: 1.2)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
