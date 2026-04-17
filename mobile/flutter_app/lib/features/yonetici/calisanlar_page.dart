import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class CalisanlarPage extends ConsumerStatefulWidget {
  const CalisanlarPage({super.key});
  @override
  ConsumerState<CalisanlarPage> createState() => _CalisanlarPageState();
}

class _CalisanlarPageState extends ConsumerState<CalisanlarPage> {
  Future<Map<String, dynamic>>? _future;
  String _arama = '';

  @override
  void initState() { super.initState(); _load(); }
  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/yonetici/calisanlar').then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('👥 Aktif Çalışanlar')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _future,
        builder: (_, snap) {
          if (snap.connectionState == ConnectionState.waiting)
            return const Center(child: CircularProgressIndicator());
          final d = snap.data ?? {};
          final liste = List<Map<String, dynamic>>.from((d['liste'] as List?) ?? []);
          final brans = Map<String, dynamic>.from(d['brans_dagilimi'] as Map? ?? {});

          final filtered = _arama.isEmpty ? liste
              : liste.where((c) => (c['ad_soyad'] as String? ?? '').toLowerCase().contains(_arama.toLowerCase())
                  || (c['brans'] as String? ?? '').toLowerCase().contains(_arama.toLowerCase())).toList();

          return RefreshIndicator(
            onRefresh: () async => _load(),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              // Ozet
              Row(children: [
                Expanded(child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${d['aktif'] ?? 0}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.primary)),
                    const Text('Aktif', style: TextStyle(fontSize: 11)),
                  ]),
                )),
                const SizedBox(width: 8),
                Expanded(child: Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                  child: Column(children: [
                    Text('${brans.length}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppColors.info)),
                    const Text('Branş', style: TextStyle(fontSize: 11)),
                  ]),
                )),
              ]),
              const SizedBox(height: 12),

              // Brans dagilimi chips
              Wrap(spacing: 6, runSpacing: 6, children: brans.entries.map((e) =>
                  Chip(label: Text('${e.key}: ${e.value}', style: const TextStyle(fontSize: 10)),
                      backgroundColor: AppColors.primary.withOpacity(0.08))).toList()),
              const SizedBox(height: 12),

              // Arama
              TextField(
                decoration: InputDecoration(hintText: 'Ara (isim veya branş)...',
                    prefixIcon: const Icon(Icons.search, size: 18), isDense: true,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10))),
                onChanged: (v) => setState(() => _arama = v),
              ),
              const SizedBox(height: 12),

              Text('${filtered.length} çalışan', style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
              const SizedBox(height: 8),
              ...filtered.map((c) => Card(
                margin: const EdgeInsets.only(bottom: 6),
                child: ListTile(
                  dense: true,
                  leading: CircleAvatar(
                    radius: 20, backgroundColor: AppColors.primary.withOpacity(0.15),
                    child: Text((c['ad_soyad'] as String? ?? '?')[0],
                        style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.primary)),
                  ),
                  title: Text(c['ad_soyad'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                  subtitle: Text('${c['brans']} · ${c['email'] ?? ''}', style: const TextStyle(fontSize: 11)),
                  trailing: Text(c['durum'] ?? 'aktif',
                      style: TextStyle(fontSize: 10, color: c['durum'] == 'aktif' ? AppColors.success : Colors.grey)),
                ),
              )),
            ]),
          );
        },
      ),
    );
  }
}
