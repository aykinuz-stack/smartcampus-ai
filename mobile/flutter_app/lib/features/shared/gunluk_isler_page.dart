import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Günlük İşler — bugünkü devamsız, geç, izinli öğrenciler
class GunlukIslerPage extends ConsumerStatefulWidget {
  const GunlukIslerPage({super.key});
  @override
  ConsumerState<GunlukIslerPage> createState() => _GunlukIslerPageState();
}

class _GunlukIslerPageState extends ConsumerState<GunlukIslerPage> {
  Future<Map<String, dynamic>>? _future;

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    setState(() => _future = ref.read(apiClientProvider)
        .get('/gunluk-isler')
        .then((r) => Map<String, dynamic>.from(r.data)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Günlük İşler'),
        actions: [IconButton(icon: const Icon(Icons.refresh), onPressed: _load)],
      ),
      body: RefreshIndicator(
        onRefresh: () async => _load(),
        child: FutureBuilder<Map<String, dynamic>>(
          future: _future,
          builder: (ctx, snap) {
            if (snap.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snap.hasError) {
              return Center(child: Text('Hata: ${snap.error}'));
            }
            final d = snap.data ?? {};
            return _buildContent(d);
          },
        ),
      ),
    );
  }

  Widget _buildContent(Map<String, dynamic> d) {
    final tarih = d['tarih'] ?? '';
    final yoklamaAlinan = d['yoklama_alinan'] ?? 0;
    final devamsizSayisi = d['devamsiz_sayisi'] ?? 0;
    final gecSayisi = d['gec_sayisi'] ?? 0;
    final izinliSayisi = d['izinli_sayisi'] ?? 0;
    final devamsizlar = List<Map<String, dynamic>>.from(d['devamsiz'] ?? []);
    final gecler = List<Map<String, dynamic>>.from(d['gec'] ?? []);
    final izinliler = List<Map<String, dynamic>>.from(d['izinli'] ?? []);

    // Öğretmen ek bilgileri (null-safe)
    List<Map<String, dynamic>> bugunDersleri = [];
    try { bugunDersleri = List<Map<String, dynamic>>.from(d['bugun_ders_programi'] ?? []); } catch (_) {}
    final bugunGun = (d['bugun_gun'] ?? '').toString();
    final teslimOdev = (d['teslim_edilen_odev'] as num?)?.toInt() ?? 0;
    final nobetVar = d['nobet_var'] == true;
    final okunmamisMesaj = (d['okunmamis_mesaj'] as num?)?.toInt() ?? 0;
    List<String> dogumGunu = [];
    try { dogumGunu = List<String>.from(d['dogum_gunu'] ?? []); } catch (_) {}
    final dersDefterEksik = (d['ders_defteri_eksik'] as num?)?.toInt() ?? 0;
    final hasOgretmenData = bugunDersleri.isNotEmpty || nobetVar || okunmamisMesaj > 0;

    return SingleChildScrollView(
      physics: const AlwaysScrollableScrollPhysics(),
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Tarih banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFF1E1B4B), Color(0xFF6366F1)]),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('📋 Günlük Yoklama Durumu',
                    style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 4),
                Text(tarih, style: const TextStyle(color: Colors.white70, fontSize: 13)),
              ],
            ),
          ),
          const SizedBox(height: 14),

          // KPI satırı
          Row(children: [
            _KpiCard(label: 'Yoklama', value: '$yoklamaAlinan', color: AppColors.primary, icon: Icons.check_circle),
            const SizedBox(width: 8),
            _KpiCard(label: 'Devamsız', value: '$devamsizSayisi', color: AppColors.danger, icon: Icons.person_off),
            const SizedBox(width: 8),
            _KpiCard(label: 'Geç', value: '$gecSayisi', color: AppColors.warning, icon: Icons.access_time),
            const SizedBox(width: 8),
            _KpiCard(label: 'İzinli', value: '$izinliSayisi', color: AppColors.info, icon: Icons.medical_information),
          ]),
          const SizedBox(height: 14),

          // ── ÖĞRETMEN EK BİLGİLERİ ──
          if (hasOgretmenData) ...[
            // Nöbet uyarısı
            if (nobetVar)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                margin: const EdgeInsets.only(bottom: 10),
                decoration: BoxDecoration(
                  color: AppColors.warning.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppColors.warning)),
                child: const Row(children: [
                  Icon(Icons.shield, color: AppColors.warning, size: 20),
                  SizedBox(width: 8),
                  Text('Bugün nöbet günün!', style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.warning)),
                ]),
              ),

            // Okunmamış mesaj + teslim ödev + ders defteri eksik
            Row(children: [
              if (okunmamisMesaj > 0)
                _MiniInfo(icon: Icons.mail, text: '$okunmamisMesaj mesaj', color: AppColors.primary),
              if (teslimOdev > 0)
                _MiniInfo(icon: Icons.assignment_turned_in, text: '$teslimOdev ödev teslim', color: AppColors.success),
              if (dersDefterEksik > 0)
                _MiniInfo(icon: Icons.edit_note, text: '$dersDefterEksik ders defteri eksik', color: AppColors.warning),
            ]),
            if (okunmamisMesaj > 0 || teslimOdev > 0 || dersDefterEksik > 0)
              const SizedBox(height: 10),

            // Bugünkü ders programı
            if (bugunDersleri.isNotEmpty) ...[
              ExpansionTile(
                leading: const Icon(Icons.schedule, color: AppColors.success, size: 20),
                title: Text('Derslerim ($bugunGun) — ${bugunDersleri.length} ders',
                    style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: AppColors.success)),
                initiallyExpanded: false,
                children: bugunDersleri.map((ders) {
                  final saat = '${ders['saat'] ?? '?'}';
                  final saatKisa = saat.length > 5 ? saat.substring(0, 5) : saat;
                  return ListTile(
                    dense: true,
                    leading: CircleAvatar(
                      radius: 14, backgroundColor: AppColors.success.withOpacity(0.15),
                      child: Text(saatKisa, style: const TextStyle(fontSize: 9, fontWeight: FontWeight.bold)),
                    ),
                    title: Text('${ders['ders'] ?? ''}', style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
                    trailing: Text('${ders['sinif'] ?? ''}/${ders['sube'] ?? ''}',
                        style: const TextStyle(fontSize: 12, color: AppColors.textSecondaryDark)),
                  );
                }).toList(),
              ),
              const SizedBox(height: 10),
            ],

            // Doğum günleri
            if (dogumGunu.isNotEmpty) ...[
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: const Color(0xFFEAB308).withOpacity(0.1),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: const Color(0xFFEAB308).withOpacity(0.3))),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Row(children: [
                    Text('🎂', style: TextStyle(fontSize: 18)),
                    SizedBox(width: 8),
                    Text('Doğum Günleri', style: TextStyle(fontWeight: FontWeight.bold)),
                  ]),
                  const SizedBox(height: 6),
                  ...dogumGunu.map((d) => Text('  • $d', style: const TextStyle(fontSize: 13))),
                ]),
              ),
              const SizedBox(height: 10),
            ],
          ],

          // Devamsız öğrenciler
          if (devamsizlar.isNotEmpty) ...[
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: AppColors.danger.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.danger.withOpacity(0.4)),
              ),
              child: Row(children: [
                const Icon(Icons.person_off, color: AppColors.danger, size: 20),
                const SizedBox(width: 8),
                Text('Devamsız Öğrenciler ($devamsizSayisi)',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.danger)),
              ]),
            ),
            const SizedBox(height: 8),
            ...devamsizlar.map((stu) => _DevamsizKart(data: stu)),
            const SizedBox(height: 14),
          ] else
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.success.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10)),
              child: const Row(children: [
                Icon(Icons.check_circle, color: AppColors.success),
                SizedBox(width: 10),
                Text('Bugün devamsız öğrenci yok!',
                    style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.success)),
              ]),
            ),

          // Geç kalanlar
          if (gecler.isNotEmpty) ...[
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: AppColors.warning.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.warning.withOpacity(0.4)),
              ),
              child: Row(children: [
                const Icon(Icons.access_time, color: AppColors.warning, size: 20),
                const SizedBox(width: 8),
                Text('Geç Kalanlar ($gecSayisi)',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.warning)),
              ]),
            ),
            const SizedBox(height: 8),
            ...gecler.map((g) => _MiniKart(
              adSoyad: g['ad_soyad'] ?? '',
              sinif: '${g['sinif']}/${g['sube']}',
              ders: '${g['ders']} (${g['ders_saati']}. ders)',
              color: AppColors.warning,
            )),
          ],

          // İzinliler
          if (izinliler.isNotEmpty) ...[
            const SizedBox(height: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: AppColors.info.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: AppColors.info.withOpacity(0.4)),
              ),
              child: Row(children: [
                const Icon(Icons.medical_information, color: AppColors.info, size: 20),
                const SizedBox(width: 8),
                Text('İzinli / Raporlu ($izinliSayisi)',
                    style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.info)),
              ]),
            ),
            const SizedBox(height: 8),
            ...izinliler.map((i) => _MiniKart(
              adSoyad: i['ad_soyad'] ?? '',
              sinif: '${i['sinif']}/${i['sube']}',
              ders: '${i['ders']} (${i['ders_saati']}. ders)',
              color: AppColors.info,
            )),
          ],

          if (yoklamaAlinan == 0)
            Container(
              width: double.infinity,
              margin: const EdgeInsets.only(top: 14),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.warning.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10)),
              child: const Row(children: [
                Icon(Icons.warning_amber, color: AppColors.warning),
                SizedBox(width: 10),
                Expanded(child: Text('Bugün henüz yoklama alınmamış.',
                    style: TextStyle(color: AppColors.warning))),
              ]),
            ),
        ],
      ),
    );
  }
}


class _KpiCard extends StatelessWidget {
  final String label, value;
  final Color color;
  final IconData icon;
  const _KpiCard({required this.label, required this.value, required this.color, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Expanded(child: Container(
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10),
        border: Border.all(color: color.withOpacity(0.3))),
      child: Column(children: [
        Icon(icon, color: color, size: 18),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 10)),
      ]),
    ));
  }
}


class _DevamsizKart extends StatelessWidget {
  final Map<String, dynamic> data;
  const _DevamsizKart({required this.data});

  @override
  Widget build(BuildContext context) {
    final dersler = List<String>.from(data['dersler'] ?? []);
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.danger.withOpacity(0.05),
        borderRadius: BorderRadius.circular(10),
        border: Border(left: BorderSide(color: AppColors.danger, width: 4)),
      ),
      child: Row(children: [
        CircleAvatar(
          radius: 18,
          backgroundColor: AppColors.danger.withOpacity(0.15),
          child: Text((data['ad_soyad'] ?? '?')[0],
              style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.danger)),
        ),
        const SizedBox(width: 10),
        Expanded(child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(data['ad_soyad'] ?? '', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
            Text('${data['sinif']}/${data['sube']} · No: ${data['numara']}',
                style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
            if (dersler.isNotEmpty)
              Text(dersler.join(', '), style: const TextStyle(fontSize: 11, color: AppColors.danger)),
          ],
        )),
        if ((data['veli_telefon'] ?? '').isNotEmpty)
          Column(children: [
            const Icon(Icons.phone, size: 14, color: AppColors.textSecondaryDark),
            Text(data['veli_telefon'] ?? '', style: const TextStyle(fontSize: 9, color: AppColors.textSecondaryDark)),
          ]),
      ]),
    );
  }
}


class _MiniInfo extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color color;
  const _MiniInfo({required this.icon, required this.text, required this.color});
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(right: 8),
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(icon, color: color, size: 14),
        const SizedBox(width: 4),
        Text(text, style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: color)),
      ]),
    );
  }
}


class _MiniKart extends StatelessWidget {
  final String adSoyad, sinif, ders;
  final Color color;
  const _MiniKart({required this.adSoyad, required this.sinif, required this.ders, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(8),
        border: Border(left: BorderSide(color: color, width: 3)),
      ),
      child: Row(children: [
        Expanded(child: Text(adSoyad, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13))),
        Text(sinif, style: const TextStyle(fontSize: 11, color: AppColors.textSecondaryDark)),
        const SizedBox(width: 8),
        Text(ders, style: TextStyle(fontSize: 10, color: color)),
      ]),
    );
  }
}
