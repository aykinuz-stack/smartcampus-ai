import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class ZekaOyunlariPage extends ConsumerStatefulWidget {
  const ZekaOyunlariPage({super.key});
  @override
  ConsumerState<ZekaOyunlariPage> createState() => _ZekaOyunlariPageState();
}

class _ZekaOyunlariPageState extends ConsumerState<ZekaOyunlariPage> {
  Future<Map<String, dynamic>>? _future;
  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/zeka-oyunlari').then((r) => Map<String, dynamic>.from(r.data)));
  }

  static const _renkler = [AppColors.primary, AppColors.success, AppColors.warning,
    AppColors.info, Color(0xFFEC4899), AppColors.danger];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🧩 Zeka Oyunları')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final oyunlar = (snap.data?['oyunlar'] as List?) ?? [];

          return ListView(padding: const EdgeInsets.all(16), children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [Color(0xFF6366F1), Color(0xFFEC4899)]),
                borderRadius: BorderRadius.circular(16)),
              child: const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('🧩', style: TextStyle(fontSize: 36)),
                SizedBox(height: 8),
                Text('Zeka Oyunları', style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                Text('Beynini çalıştır, eğlenerek öğren!', style: TextStyle(color: Colors.white70, fontSize: 13)),
              ]),
            ),
            const SizedBox(height: 16),
            ...oyunlar.asMap().entries.map((e) {
              final i = e.key;
              final o = e.value as Map;
              final renk = _renkler[i % _renkler.length];
              final seviyeler = (o['seviye'] as List?) ?? [];
              return Card(margin: const EdgeInsets.only(bottom: 10), child: ListTile(
                leading: Container(
                  width: 50, height: 50,
                  decoration: BoxDecoration(color: renk.withOpacity(0.15), borderRadius: BorderRadius.circular(12)),
                  child: Center(child: Text(o['ikon'] ?? '🧩', style: const TextStyle(fontSize: 26))),
                ),
                title: Text(o['ad'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                subtitle: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(o['aciklama'] ?? '', style: const TextStyle(fontSize: 12)),
                  const SizedBox(height: 4),
                  Wrap(spacing: 4, children: seviyeler.map((s) => Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                    decoration: BoxDecoration(color: renk.withOpacity(0.1), borderRadius: BorderRadius.circular(4)),
                    child: Text(s.toString(), style: TextStyle(fontSize: 9, color: renk, fontWeight: FontWeight.bold)),
                  )).toList()),
                ]),
                trailing: Icon(Icons.play_circle, color: renk, size: 28),
                onTap: () {
                  if (o['id'] == 'hafiza') {
                    Navigator.push(context, MaterialPageRoute(builder: (_) => const _HafizaOyunuPage()));
                  } else {
                    ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('${o['ad']} — yakında'), backgroundColor: renk));
                  }
                },
              ));
            }),
          ]);
        },
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// HAFIZA OYUNU — Eslesen kartlari bul
// ═══════════════════════════════════════════════════════════

class _HafizaOyunuPage extends StatefulWidget {
  const _HafizaOyunuPage();
  @override
  State<_HafizaOyunuPage> createState() => _HafizaOyunuPageState();
}

class _HafizaOyunuPageState extends State<_HafizaOyunuPage> {
  late List<String> _kartlar;
  late List<bool> _acik;
  late List<bool> _eslesti;
  int? _ilkSecim;
  int _hamle = 0;
  int _eslesme = 0;
  bool _bekliyor = false;

  static const _emojiler = ['🐱', '🐶', '🌸', '🌞', '🦋', '🐟', '🍎', '🌈'];

  @override
  void initState() {
    super.initState();
    _yeniOyun();
  }

  void _yeniOyun() {
    final ciftler = [..._emojiler, ..._emojiler];
    ciftler.shuffle(Random());
    setState(() {
      _kartlar = ciftler;
      _acik = List.filled(16, false);
      _eslesti = List.filled(16, false);
      _ilkSecim = null;
      _hamle = 0;
      _eslesme = 0;
      _bekliyor = false;
    });
  }

  void _kartTikla(int idx) {
    if (_bekliyor || _acik[idx] || _eslesti[idx]) return;
    setState(() => _acik[idx] = true);

    if (_ilkSecim == null) {
      _ilkSecim = idx;
    } else {
      _hamle++;
      if (_kartlar[_ilkSecim!] == _kartlar[idx]) {
        setState(() { _eslesti[_ilkSecim!] = true; _eslesti[idx] = true; _eslesme++; });
        _ilkSecim = null;
      } else {
        _bekliyor = true;
        final first = _ilkSecim!;
        _ilkSecim = null;
        Future.delayed(const Duration(milliseconds: 800), () {
          if (mounted) setState(() { _acik[first] = false; _acik[idx] = false; _bekliyor = false; });
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final bitti = _eslesme == 8;
    return Scaffold(
      appBar: AppBar(title: Text('🧠 Hafıza Oyunu · $_hamle hamle')),
      body: Column(children: [
        if (bitti)
          Container(
            padding: const EdgeInsets.all(20), margin: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: AppColors.success.withOpacity(0.15), borderRadius: BorderRadius.circular(14)),
            child: Column(children: [
              const Text('🎉 Tebrikler!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              Text('$_hamle hamlede tamamladın!', style: const TextStyle(fontSize: 14)),
              const SizedBox(height: 12),
              ElevatedButton.icon(icon: const Icon(Icons.refresh), label: const Text('Tekrar'),
                  onPressed: _yeniOyun),
            ]),
          ),
        Expanded(
          child: GridView.builder(
            padding: const EdgeInsets.all(16),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 4, crossAxisSpacing: 8, mainAxisSpacing: 8),
            itemCount: 16,
            itemBuilder: (_, i) {
              final gorunur = _acik[i] || _eslesti[i];
              return GestureDetector(
                onTap: () => _kartTikla(i),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 300),
                  decoration: BoxDecoration(
                    color: _eslesti[i] ? AppColors.success.withOpacity(0.2)
                        : gorunur ? AppColors.primary.withOpacity(0.15) : AppColors.primary.withOpacity(0.08),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: _eslesti[i] ? AppColors.success
                        : gorunur ? AppColors.primary : Colors.grey.withOpacity(0.3), width: 2),
                  ),
                  child: Center(
                    child: Text(gorunur ? _kartlar[i] : '❓',
                        style: TextStyle(fontSize: gorunur ? 28 : 22)),
                  ),
                ),
              );
            },
          ),
        ),
      ]),
    );
  }
}
