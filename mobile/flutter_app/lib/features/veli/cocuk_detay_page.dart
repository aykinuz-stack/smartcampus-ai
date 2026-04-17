import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Ultra Premium Cocuk Detay — Veli icin tek sayfada HER SEY.
/// Yoklama + Notlar + Sinav + Karne + Odev
class CocukDetayPage extends ConsumerStatefulWidget {
  final String studentId;
  final String studentName;
  const CocukDetayPage({
    super.key,
    required this.studentId,
    required this.studentName,
  });

  @override
  ConsumerState<CocukDetayPage> createState() => _CocukDetayPageState();
}

class _CocukDetayPageState extends ConsumerState<CocukDetayPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;

  Future<Map<String, dynamic>>? _yoklamaFuture;
  Future<Map<String, dynamic>>? _notlarFuture;
  Future<Map<String, dynamic>>? _sinavFuture;
  Future<Map<String, dynamic>>? _karneFuture;
  Future<Map<String, dynamic>>? _odevFuture;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 5, vsync: this);
    _loadAll();
  }

  void _loadAll() {
    final api = ref.read(apiClientProvider);
    final sid = widget.studentId;
    setState(() {
      _yoklamaFuture = api.get('/veli/cocuk/$sid/yoklama').then((r) =>
          Map<String, dynamic>.from(r.data));
      _notlarFuture = api.get('/veli/cocuk/$sid/notlar').then((r) =>
          Map<String, dynamic>.from(r.data));
      _sinavFuture = api.get('/veli/cocuk/$sid/sinav-sonuclari').then((r) =>
          Map<String, dynamic>.from(r.data));
      _karneFuture = api.get('/veli/cocuk/$sid/karne').then((r) =>
          Map<String, dynamic>.from(r.data));
      _odevFuture = api.get('/veli/cocuk/$sid/odevler').then((r) =>
          Map<String, dynamic>.from(r.data));
    });
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.studentName),
        bottom: TabBar(
          controller: _tabCtrl,
          isScrollable: true,
          tabs: const [
            Tab(icon: Icon(Icons.check_circle_outline, size: 20), text: 'Yoklama'),
            Tab(icon: Icon(Icons.grade, size: 20), text: 'Notlar'),
            Tab(icon: Icon(Icons.quiz, size: 20), text: 'Sınavlar'),
            Tab(icon: Icon(Icons.card_membership, size: 20), text: 'Karne'),
            Tab(icon: Icon(Icons.assignment, size: 20), text: 'Ödevler'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabCtrl,
        children: [
          _YoklamaTab(future: _yoklamaFuture),
          _NotlarTab(future: _notlarFuture),
          _SinavTab(future: _sinavFuture),
          _KarneTab(future: _karneFuture),
          _OdevTab(future: _odevFuture),
        ],
      ),
    );
  }
}


// ═══════════════════════════════════════════════════════════
// TAB 1: YOKLAMA
// ═══════════════════════════════════════════════════════════

class _YoklamaTab extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  const _YoklamaTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        final d = snap.data ?? {};
        final bugun = (d['bugun'] as List?) ?? [];
        final kayitlar = (d['son_kayitlar'] as List?) ?? [];

        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Ozet kartlar
            Row(children: [
              _Sayac(label: 'Özürsüz', val: '${d['toplam_ozursuz'] ?? 0}',
                  color: AppColors.danger, icon: Icons.close),
              const SizedBox(width: 8),
              _Sayac(label: 'Özürlü', val: '${d['toplam_ozurlu'] ?? 0}',
                  color: AppColors.info, icon: Icons.medical_information),
              const SizedBox(width: 8),
              _Sayac(label: 'Geç', val: '${d['toplam_gec'] ?? 0}',
                  color: AppColors.warning, icon: Icons.access_time),
              const SizedBox(width: 8),
              _Sayac(label: 'Bu Ay', val: '${d['bu_ay_ozursuz'] ?? 0}',
                  color: AppColors.primary, icon: Icons.calendar_today),
            ]),

            if (bugun.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text('Bugün', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              ...bugun.map((b) {
                final bb = b as Map;
                final durum = (bb['durum'] as String? ?? '').toLowerCase();
                final ok = durum == 'devam' || durum == 'var';
                return ListTile(
                  dense: true,
                  leading: Icon(ok ? Icons.check_circle : Icons.cancel,
                      color: ok ? AppColors.success : AppColors.danger),
                  title: Text('${bb['ders']} · ${bb['saat']}. ders'),
                  trailing: Text(durum.toUpperCase(),
                      style: TextStyle(color: ok ? AppColors.success : AppColors.danger,
                          fontWeight: FontWeight.bold, fontSize: 12)),
                );
              }),
            ],

            const SizedBox(height: 16),
            const Text('Son 30 Kayıt', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...kayitlar.map((k) {
              final kk = k as Map;
              final durum = (kk['durum'] as String? ?? '').toLowerCase();
              Color c;
              switch (durum) {
                case 'devamsiz': case 'ozursuz': c = AppColors.danger; break;
                case 'gec': c = AppColors.warning; break;
                default: c = AppColors.info;
              }
              return Card(
                margin: const EdgeInsets.only(bottom: 4),
                child: ListTile(
                  dense: true,
                  leading: Container(
                    width: 8, height: 40,
                    decoration: BoxDecoration(color: c, borderRadius: BorderRadius.circular(4)),
                  ),
                  title: Text('${kk['tarih']} · ${kk['ders']}', style: const TextStyle(fontSize: 13)),
                  trailing: Text(durum, style: TextStyle(color: c, fontSize: 11, fontWeight: FontWeight.bold)),
                ),
              );
            }),
          ],
        );
      },
    );
  }
}


// ═══════════════════════════════════════════════════════════
// TAB 2: NOTLAR
// ═══════════════════════════════════════════════════════════

class _NotlarTab extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  const _NotlarTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        final d = snap.data ?? {};
        final genelOrt = (d['genel_ortalama'] as num?)?.toDouble() ?? 0.0;
        final dersKart = (d['ders_kartlari'] as List?) ?? [];
        final sonNot = (d['son_notlar'] as List?) ?? [];

        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Genel ort
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: LinearGradient(colors: [
                  genelOrt >= 70 ? AppColors.success : AppColors.warning,
                  genelOrt >= 70 ? AppColors.success.withOpacity(0.7) : AppColors.warning.withOpacity(0.7),
                ]),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(children: [
                Text(genelOrt.toStringAsFixed(1),
                    style: const TextStyle(color: Colors.white, fontSize: 36, fontWeight: FontWeight.bold)),
                const SizedBox(width: 12),
                const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Genel', style: TextStyle(color: Colors.white70, fontSize: 12)),
                  Text('Ortalama', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600)),
                ]),
                const Spacer(),
                Text('${d['toplam_not'] ?? 0} not', style: const TextStyle(color: Colors.white70)),
              ]),
            ),

            const SizedBox(height: 16),
            const Text('Ders Ortalamaları', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...dersKart.map((dk) {
              final dd = dk as Map;
              final ort = (dd['ortalama'] as num).toDouble();
              Color c = ort >= 85 ? AppColors.success : ort >= 70 ? AppColors.info :
                        ort >= 50 ? AppColors.warning : AppColors.danger;
              return Card(
                margin: const EdgeInsets.only(bottom: 6),
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: c.withOpacity(0.15),
                    child: Text(ort.toStringAsFixed(0), style: TextStyle(color: c, fontWeight: FontWeight.bold)),
                  ),
                  title: Text(dd['ders'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                  subtitle: Text('${dd['not_sayisi']} not · En yüksek: ${(dd['en_yuksek'] as num).toStringAsFixed(0)}'),
                  trailing: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                    child: Text(dd['durum'] == 'basarili' ? '✓' : '⚠️',
                        style: TextStyle(color: c, fontWeight: FontWeight.bold)),
                  ),
                ),
              );
            }),

            const SizedBox(height: 16),
            const Text('Son Notlar', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            ...sonNot.map((n) {
              final nn = n as Map;
              final puan = (nn['puan'] as num?)?.toDouble() ?? 0.0;
              Color c = puan >= 85 ? AppColors.success : puan >= 70 ? AppColors.info :
                        puan >= 50 ? AppColors.warning : AppColors.danger;
              return ListTile(
                dense: true,
                leading: Text(puan.toStringAsFixed(0),
                    style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 18)),
                title: Text('${nn['ders']}', style: const TextStyle(fontSize: 13)),
                subtitle: Text('${nn['tur']} ${nn['sira']} · ${nn['tarih']} · ${nn['donem']}',
                    style: const TextStyle(fontSize: 11)),
              );
            }),
          ],
        );
      },
    );
  }
}


// ═══════════════════════════════════════════════════════════
// TAB 3: SINAV SONUCLARI
// ═══════════════════════════════════════════════════════════

class _SinavTab extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  const _SinavTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        final d = snap.data ?? {};
        final sonuclar = (d['sonuclar'] as List?) ?? [];

        if (sonuclar.isEmpty) {
          return const Center(child: Text('Henüz sınav sonucu yok'));
        }

        return ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: sonuclar.length,
          itemBuilder: (_, i) {
            final s = sonuclar[i] as Map;
            final puan = (s['puan'] as num?)?.toDouble() ?? 0.0;
            Color c = puan >= 85 ? AppColors.success : puan >= 70 ? AppColors.info :
                      puan >= 50 ? AppColors.warning : AppColors.danger;
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                leading: Container(
                  width: 50, height: 50,
                  decoration: BoxDecoration(
                    color: c.withOpacity(0.15), borderRadius: BorderRadius.circular(10)),
                  child: Center(
                    child: Text(puan.toStringAsFixed(0),
                        style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 20)),
                  ),
                ),
                title: Text(s['ders'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text('${s['tur'] ?? 'Yazılı'} · ${s['tarih'] ?? ''} · ${s['donem'] ?? ''}',
                    style: const TextStyle(fontSize: 12)),
              ),
            );
          },
        );
      },
    );
  }
}


// ═══════════════════════════════════════════════════════════
// TAB 4: KARNE
// ═══════════════════════════════════════════════════════════

class _KarneTab extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  const _KarneTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        final d = snap.data ?? {};
        final ogrenci = d['ogrenci'] as Map? ?? {};
        final karne = d['karne'] as Map? ?? {};
        final devamsizlik = (d['toplam_devamsizlik'] as num?)?.toInt() ?? 0;

        if (karne.isEmpty) {
          return const Center(child: Text('Karne verisi yok'));
        }

        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Ogrenci bilgi karti
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [AppColors.primaryDark, AppColors.primary]),
                borderRadius: BorderRadius.circular(14),
              ),
              child: Row(children: [
                CircleAvatar(
                  radius: 26,
                  backgroundColor: Colors.white.withOpacity(0.2),
                  child: Text((ogrenci['ad_soyad'] ?? '?')[0],
                      style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(width: 14),
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(ogrenci['ad_soyad'] ?? '',
                      style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                  Text('${ogrenci['sinif']}/${ogrenci['sube']} · No: ${ogrenci['numara']}',
                      style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 12)),
                ]),
                const Spacer(),
                Column(children: [
                  Text('$devamsizlik', style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                  Text('Devamsız', style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 10)),
                ]),
              ]),
            ),

            // Donem bazli karne
            ...karne.entries.map((e) {
              final donem = e.key;
              final data = e.value as Map;
              final dersler = (data['dersler'] as List?) ?? [];
              final genelOrt = (data['genel_ortalama'] as num?)?.toDouble() ?? 0.0;

              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 16),
                  Row(children: [
                    Text(donem, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    const Spacer(),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(
                        color: (genelOrt >= 70 ? AppColors.success : AppColors.warning).withOpacity(0.15),
                        borderRadius: BorderRadius.circular(8)),
                      child: Text('Ort: ${genelOrt.toStringAsFixed(1)}',
                          style: TextStyle(
                            color: genelOrt >= 70 ? AppColors.success : AppColors.warning,
                            fontWeight: FontWeight.bold)),
                    ),
                  ]),
                  const SizedBox(height: 8),
                  // Ders tablosu
                  Table(
                    border: TableBorder.all(color: Colors.grey.withOpacity(0.2)),
                    columnWidths: const {
                      0: FlexColumnWidth(3),
                      1: FlexColumnWidth(1.5),
                      2: FlexColumnWidth(1),
                      3: FlexColumnWidth(1),
                    },
                    children: [
                      TableRow(
                        decoration: BoxDecoration(color: AppColors.primary.withOpacity(0.1)),
                        children: const [
                          Padding(padding: EdgeInsets.all(8),
                              child: Text('Ders', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                          Padding(padding: EdgeInsets.all(8),
                              child: Text('Ort', textAlign: TextAlign.center,
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                          Padding(padding: EdgeInsets.all(8),
                              child: Text('Not', textAlign: TextAlign.center,
                                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12))),
                          Padding(padding: EdgeInsets.all(8),
                              child: Text(' ', textAlign: TextAlign.center)),
                        ],
                      ),
                      ...dersler.map((dd) {
                        final ddd = dd as Map;
                        final ort = (ddd['ortalama'] as num).toDouble();
                        Color c = ort >= 85 ? AppColors.success : ort >= 70 ? AppColors.info :
                                  ort >= 50 ? AppColors.warning : AppColors.danger;
                        return TableRow(children: [
                          Padding(padding: const EdgeInsets.all(8),
                              child: Text(ddd['ders'] ?? '', style: const TextStyle(fontSize: 12))),
                          Padding(padding: const EdgeInsets.all(8),
                              child: Text(ort.toStringAsFixed(1), textAlign: TextAlign.center,
                                  style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 13))),
                          Padding(padding: const EdgeInsets.all(8),
                              child: Text('${ddd['not_sayisi']}', textAlign: TextAlign.center,
                                  style: const TextStyle(fontSize: 12))),
                          Padding(padding: const EdgeInsets.all(8),
                              child: Icon(ddd['durum'] == 'basarili' ? Icons.check : Icons.warning,
                                  color: c, size: 16)),
                        ]);
                      }),
                    ],
                  ),
                ],
              );
            }),
          ],
        );
      },
    );
  }
}


// ═══════════════════════════════════════════════════════════
// TAB 5: ODEVLER
// ═══════════════════════════════════════════════════════════

class _OdevTab extends StatelessWidget {
  final Future<Map<String, dynamic>>? future;
  const _OdevTab({required this.future});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: future,
      builder: (_, snap) {
        if (snap.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        final d = snap.data ?? {};
        final bekleyen = (d['bekleyen_liste'] as List?) ?? [];
        final geciken = (d['geciken_liste'] as List?) ?? [];
        final teslim = (d['teslim_liste'] as List?) ?? [];

        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Ozet
            Row(children: [
              _Sayac(label: 'Bekleyen', val: '${d['bekleyen'] ?? 0}',
                  color: AppColors.info, icon: Icons.schedule),
              const SizedBox(width: 8),
              _Sayac(label: 'Geciken', val: '${d['geciken'] ?? 0}',
                  color: AppColors.danger, icon: Icons.warning),
              const SizedBox(width: 8),
              _Sayac(label: 'Teslim', val: '${d['teslim_edilen'] ?? 0}',
                  color: AppColors.success, icon: Icons.check),
            ]),

            if (geciken.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text('⚠️ Geciken Ödevler',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: AppColors.danger)),
              const SizedBox(height: 8),
              ...geciken.map((o) => _OdevKart(o: o as Map, renk: AppColors.danger)),
            ],

            if (bekleyen.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text('📋 Bekleyen Ödevler',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              ...bekleyen.map((o) => _OdevKart(o: o as Map, renk: AppColors.info)),
            ],

            if (teslim.isNotEmpty) ...[
              const SizedBox(height: 16),
              const Text('✅ Teslim Edilen',
                  style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              ...teslim.take(10).map((o) => _OdevKart(o: o as Map, renk: AppColors.success)),
            ],
          ],
        );
      },
    );
  }
}


// ═══════════════════════════════════════════════════════════
// ORTAK WIDGET'LAR
// ═══════════════════════════════════════════════════════════

class _Sayac extends StatelessWidget {
  final String label;
  final String val;
  final Color color;
  final IconData icon;
  const _Sayac({required this.label, required this.val,
                required this.color, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: 4),
          Text(val, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
          Text(label, style: const TextStyle(fontSize: 10)),
        ]),
      ),
    );
  }
}


class _OdevKart extends StatelessWidget {
  final Map o;
  final Color renk;
  const _OdevKart({required this.o, required this.renk});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 6),
      child: ListTile(
        dense: true,
        leading: Container(width: 4, height: 40,
            decoration: BoxDecoration(color: renk, borderRadius: BorderRadius.circular(2))),
        title: Text(o['baslik'] ?? '', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
        subtitle: Text('${o['ders']} · Son: ${o['teslim_tarihi'] ?? '-'}',
            style: const TextStyle(fontSize: 11)),
        trailing: o['puan'] != null
            ? Text('${(o['puan'] as num).toStringAsFixed(0)}',
                style: TextStyle(color: renk, fontWeight: FontWeight.bold))
            : Icon(o['teslim_edildi'] == true ? Icons.check : Icons.schedule,
                color: renk, size: 18),
      ),
    );
  }
}
