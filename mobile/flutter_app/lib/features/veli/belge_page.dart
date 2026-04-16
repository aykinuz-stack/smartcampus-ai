import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/veli_api.dart';
import '../../core/theme/app_theme.dart';


class BelgePage extends ConsumerStatefulWidget {
  const BelgePage({super.key});

  @override
  ConsumerState<BelgePage> createState() => _BelgePageState();
}

class _BelgePageState extends ConsumerState<BelgePage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(veliApiProvider).belgeTaleplerim());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📄 Belge Taleplerim')),
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.add),
        label: const Text('Yeni Talep'),
        onPressed: () async {
          await showModalBottomSheet(
            context: context,
            isScrollControlled: true,
            builder: (_) => const _YeniTalepSheet(),
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
          final talepler = (data['talepler'] as List?) ?? [];

          if (talepler.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.description_outlined, size: 64, color: Colors.grey),
                  SizedBox(height: 12),
                  Text('Talep yok', style: TextStyle(fontSize: 15)),
                  SizedBox(height: 4),
                  Text('Sağ alttan yeni belge talebi oluşturabilirsin',
                      style: TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
                ],
              ),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: talepler.length,
              itemBuilder: (_, i) => _BelgeKart(t: talepler[i]),
            ),
          );
        },
      ),
    );
  }
}


class _BelgeKart extends StatelessWidget {
  final dynamic t;
  const _BelgeKart({required this.t});

  @override
  Widget build(BuildContext context) {
    final durum = (t['durum'] as String? ?? '').toLowerCase();
    Color c;
    IconData icon;
    String label;
    switch (durum) {
      case 'bekliyor':
        c = AppColors.warning; icon = Icons.access_time; label = 'Bekliyor'; break;
      case 'hazirlaniyor':
        c = AppColors.info; icon = Icons.settings; label = 'Hazırlanıyor'; break;
      case 'hazir':
        c = AppColors.success; icon = Icons.check_circle; label = 'Hazır'; break;
      case 'teslim_edildi':
        c = AppColors.success; icon = Icons.done_all; label = 'Teslim Edildi'; break;
      case 'iptal':
        c = AppColors.danger; icon = Icons.cancel; label = 'İptal'; break;
      default:
        c = Colors.grey; icon = Icons.description; label = durum;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: c.withOpacity(0.15),
          child: Icon(icon, color: c),
        ),
        title: Text(t['belge_turu'] ?? '',
            style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if ((t['aciklama'] as String? ?? '').isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(t['aciklama'], style: const TextStyle(fontSize: 12)),
              ),
            Text(
              (t['talep_tarihi'] as String? ?? '').substring(0, 10),
              style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark),
            ),
          ],
        ),
        trailing: Container(
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: c.withOpacity(0.15),
            borderRadius: BorderRadius.circular(6),
          ),
          child: Text(label,
              style: TextStyle(color: c, fontSize: 11, fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }
}


class _YeniTalepSheet extends ConsumerStatefulWidget {
  const _YeniTalepSheet();

  @override
  ConsumerState<_YeniTalepSheet> createState() => _YeniTalepSheetState();
}

class _YeniTalepSheetState extends ConsumerState<_YeniTalepSheet> {
  String? _secilenTur;
  final _aciklamaCtrl = TextEditingController();
  List<String> _turler = [];
  bool _loadingTurler = true;
  bool _gondering = false;

  @override
  void initState() {
    super.initState();
    _loadTurler();
  }

  Future<void> _loadTurler() async {
    try {
      final t = await ref.read(veliApiProvider).belgeTurler();
      setState(() {
        _turler = t;
        _loadingTurler = false;
      });
    } catch (_) {
      setState(() => _loadingTurler = false);
    }
  }

  Future<void> _gonder() async {
    if (_secilenTur == null) return;
    setState(() => _gondering = true);
    try {
      await ref.read(veliApiProvider).belgeTalep(
        belgeTuru: _secilenTur!,
        aciklama: _aciklamaCtrl.text.trim(),
      );
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('✓ Belge talebi alındı'), backgroundColor: AppColors.success),
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
  void dispose() {
    _aciklamaCtrl.dispose();
    super.dispose();
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
            const Text('Yeni Belge Talebi',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 20),
            if (_loadingTurler)
              const Center(child: CircularProgressIndicator())
            else
              ..._turler.map((t) => RadioListTile<String>(
                    title: Text(t),
                    value: t,
                    groupValue: _secilenTur,
                    onChanged: (v) => setState(() => _secilenTur = v),
                    contentPadding: EdgeInsets.zero,
                  )),
            const SizedBox(height: 12),
            TextField(
              controller: _aciklamaCtrl,
              decoration: InputDecoration(
                labelText: 'Açıklama (opsiyonel)',
                hintText: 'örn: Kullanım amacı',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 20),
            SizedBox(
              height: 48,
              child: ElevatedButton(
                onPressed: (_secilenTur == null || _gondering) ? null : _gonder,
                child: _gondering
                    ? const SizedBox(width: 20, height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('TALEBİ GÖNDER'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
