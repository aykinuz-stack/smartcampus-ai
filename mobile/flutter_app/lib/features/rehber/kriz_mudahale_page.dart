import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Kriz mudahale takip sayfasi - Rehber ogretmen gorunumu.
/// Acil / yuksek / orta siddet kayitlarini renk kodlu listeler.
class KrizMudahalePage extends ConsumerStatefulWidget {
  const KrizMudahalePage({super.key});

  @override
  ConsumerState<KrizMudahalePage> createState() => _KrizMudahalePageState();
}

class _KrizMudahalePageState extends ConsumerState<KrizMudahalePage> {
  List<Map<String, dynamic>> _records = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/kriz-mudahale');
      final data = resp.data;
      if (data is List) {
        _records = List<Map<String, dynamic>>.from(
          data.map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _records = _staticData();
      }
    } catch (_) {
      _records = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  List<Map<String, dynamic>> _staticData() => [
        {
          'id': 'kr_001',
          'ogrenci_adi': 'Elif Yilmaz',
          'sinif': '10-A',
          'kriz_turu': 'intihar_riski',
          'siddet': 'acil',
          'tarih': '2026-04-20',
          'alinan_aksiyonlar': [
            'Aile bilgilendirildi',
            'Psikiyatriste yonlendirildi',
            'Gunluk takip baslatildi',
          ],
          'durum': 'aktif',
        },
        {
          'id': 'kr_002',
          'ogrenci_adi': 'Burak Kaya',
          'sinif': '11-B',
          'kriz_turu': 'siddet',
          'siddet': 'yuksek',
          'tarih': '2026-04-19',
          'alinan_aksiyonlar': [
            'Disiplin kuruluna bildirildi',
            'Veli gorusmesi yapildi',
          ],
          'durum': 'aktif',
        },
        {
          'id': 'kr_003',
          'ogrenci_adi': 'Zeynep Demir',
          'sinif': '9-C',
          'kriz_turu': 'ihmal',
          'siddet': 'orta',
          'tarih': '2026-04-17',
          'alinan_aksiyonlar': [
            'Ev ziyareti planlandi',
            'Sosyal hizmetlere bildirildi',
          ],
          'durum': 'takipte',
        },
        {
          'id': 'kr_004',
          'ogrenci_adi': 'Can Arslan',
          'sinif': '12-A',
          'kriz_turu': 'diger',
          'siddet': 'orta',
          'tarih': '2026-04-15',
          'alinan_aksiyonlar': [
            'Bireysel gorusme yapildi',
            'Aile bilgilendirildi',
          ],
          'durum': 'cozuldu',
        },
      ];

  Color _siddetColor(String siddet) {
    switch (siddet) {
      case 'acil':
        return AppColors.danger;
      case 'yuksek':
        return AppColors.warning;
      case 'orta':
        return const Color(0xFFEAB308); // yellow-500
      default:
        return Colors.grey;
    }
  }

  String _siddetLabel(String siddet) {
    switch (siddet) {
      case 'acil':
        return 'ACIL';
      case 'yuksek':
        return 'YUKSEK';
      case 'orta':
        return 'ORTA';
      default:
        return siddet.toUpperCase();
    }
  }

  String _krizTuruLabel(String tur) {
    switch (tur) {
      case 'intihar_riski':
        return 'Intihar Riski';
      case 'siddet':
        return 'Siddet';
      case 'ihmal':
        return 'Ihmal';
      case 'diger':
        return 'Diger';
      default:
        return tur;
    }
  }

  IconData _krizTuruIcon(String tur) {
    switch (tur) {
      case 'intihar_riski':
        return Icons.crisis_alert;
      case 'siddet':
        return Icons.warning_amber_rounded;
      case 'ihmal':
        return Icons.child_care;
      case 'diger':
        return Icons.report_problem_outlined;
      default:
        return Icons.info_outline;
    }
  }

  bool get _hasAcil => _records.any((r) => r['siddet'] == 'acil');

  void _showCreateSheet() {
    final formKey = GlobalKey<FormState>();
    String ogrenciAdi = '';
    String sinif = '';
    String krizTuru = 'intihar_riski';
    String siddet = 'acil';
    String aksiyonlar = '';

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => Padding(
        padding: EdgeInsets.only(
          left: 20,
          right: 20,
          top: 20,
          bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
        ),
        child: Form(
          key: formKey,
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Yeni Kriz Kaydi',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Ogrenci Adi',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => ogrenciAdi = v ?? '',
                ),
                const SizedBox(height: 12),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Sinif (ornek: 10-A)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.class_),
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => sinif = v ?? '',
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: krizTuru,
                  decoration: const InputDecoration(
                    labelText: 'Kriz Turu',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.crisis_alert),
                  ),
                  items: const [
                    DropdownMenuItem(
                        value: 'intihar_riski', child: Text('Intihar Riski')),
                    DropdownMenuItem(value: 'siddet', child: Text('Siddet')),
                    DropdownMenuItem(value: 'ihmal', child: Text('Ihmal')),
                    DropdownMenuItem(value: 'diger', child: Text('Diger')),
                  ],
                  onChanged: (v) => krizTuru = v ?? 'diger',
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: siddet,
                  decoration: const InputDecoration(
                    labelText: 'Siddet Seviyesi',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.speed),
                  ),
                  items: const [
                    DropdownMenuItem(value: 'acil', child: Text('Acil')),
                    DropdownMenuItem(value: 'yuksek', child: Text('Yuksek')),
                    DropdownMenuItem(value: 'orta', child: Text('Orta')),
                  ],
                  onChanged: (v) => siddet = v ?? 'orta',
                ),
                const SizedBox(height: 12),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Alinan Aksiyonlar (satirla ayirin)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.checklist),
                  ),
                  maxLines: 3,
                  onSaved: (v) => aksiyonlar = v ?? '',
                ),
                const SizedBox(height: 20),
                ElevatedButton.icon(
                  onPressed: () {
                    if (formKey.currentState?.validate() ?? false) {
                      formKey.currentState?.save();
                      final newRecord = <String, dynamic>{
                        'id': 'kr_${DateTime.now().millisecondsSinceEpoch}',
                        'ogrenci_adi': ogrenciAdi,
                        'sinif': sinif,
                        'kriz_turu': krizTuru,
                        'siddet': siddet,
                        'tarih': DateTime.now().toString().substring(0, 10),
                        'alinan_aksiyonlar': aksiyonlar
                            .split('\n')
                            .where((s) => s.trim().isNotEmpty)
                            .toList(),
                        'durum': 'aktif',
                      };
                      setState(() => _records.insert(0, newRecord));
                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Kriz kaydi olusturuldu'),
                          backgroundColor: AppColors.success,
                        ),
                      );
                    }
                  },
                  icon: const Icon(Icons.save),
                  label: const Text('Kaydet'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Kriz Mudahale'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showCreateSheet,
        backgroundColor: AppColors.primary,
        icon: const Icon(Icons.add, color: Colors.white),
        label:
            const Text('Yeni Kayit', style: TextStyle(color: Colors.white)),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(14),
                children: [
                  // -- Acil uyari banneri --
                  if (_hasAcil)
                    Container(
                      margin: const EdgeInsets.only(bottom: 14),
                      padding: const EdgeInsets.symmetric(
                          horizontal: 14, vertical: 12),
                      decoration: BoxDecoration(
                        color: AppColors.danger.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(
                            color: AppColors.danger.withOpacity(0.4)),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.crisis_alert,
                              color: AppColors.danger, size: 28),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'ACIL DURUM MEVCUT',
                                  style: TextStyle(
                                    color: AppColors.danger,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 14,
                                  ),
                                ),
                                const SizedBox(height: 2),
                                Text(
                                  '${_records.where((r) => r['siddet'] == 'acil').length} acil seviye kriz kaydi bulunuyor',
                                  style: TextStyle(
                                    color: AppColors.danger.withOpacity(0.8),
                                    fontSize: 12,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),

                  // -- Ozet kartlari --
                  Row(
                    children: [
                      _CountBadge(
                        label: 'Acil',
                        count: _records
                            .where((r) => r['siddet'] == 'acil')
                            .length,
                        color: AppColors.danger,
                      ),
                      const SizedBox(width: 8),
                      _CountBadge(
                        label: 'Yuksek',
                        count: _records
                            .where((r) => r['siddet'] == 'yuksek')
                            .length,
                        color: AppColors.warning,
                      ),
                      const SizedBox(width: 8),
                      _CountBadge(
                        label: 'Orta',
                        count: _records
                            .where((r) => r['siddet'] == 'orta')
                            .length,
                        color: const Color(0xFFEAB308),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // -- Kayit listesi --
                  if (_records.isEmpty)
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Center(
                        child: Text('Kriz kaydi bulunamadi',
                            style:
                                TextStyle(color: AppColors.textSecondaryDark)),
                      ),
                    )
                  else
                    ..._records.map((r) => _KrizKarti(
                          record: r,
                          siddetColor: _siddetColor(r['siddet'] as String),
                          siddetLabel: _siddetLabel(r['siddet'] as String),
                          krizTuruLabel:
                              _krizTuruLabel(r['kriz_turu'] as String),
                          krizTuruIcon:
                              _krizTuruIcon(r['kriz_turu'] as String),
                        )),
                ],
              ),
            ),
    );
  }
}

// ---------------------------------------------------------------------------
// Count Badge
// ---------------------------------------------------------------------------
class _CountBadge extends StatelessWidget {
  final String label;
  final int count;
  final Color color;

  const _CountBadge({
    required this.label,
    required this.count,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: color.withOpacity(0.3)),
        ),
        child: Column(
          children: [
            Text(
              '$count',
              style: TextStyle(
                  fontSize: 22, fontWeight: FontWeight.bold, color: color),
            ),
            const SizedBox(height: 2),
            Text(label, style: TextStyle(fontSize: 12, color: color)),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Kriz Karti
// ---------------------------------------------------------------------------
class _KrizKarti extends StatelessWidget {
  final Map<String, dynamic> record;
  final Color siddetColor;
  final String siddetLabel;
  final String krizTuruLabel;
  final IconData krizTuruIcon;

  const _KrizKarti({
    required this.record,
    required this.siddetColor,
    required this.siddetLabel,
    required this.krizTuruLabel,
    required this.krizTuruIcon,
  });

  @override
  Widget build(BuildContext context) {
    final aksiyonlar = List<String>.from(record['alinan_aksiyonlar'] ?? []);
    final durum = record['durum'] as String? ?? '';

    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      clipBehavior: Clip.antiAlias,
      child: IntrinsicHeight(
        child: Row(
          children: [
            Container(width: 5, color: siddetColor),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Baslik satiri
                    Row(
                      children: [
                        CircleAvatar(
                          radius: 18,
                          backgroundColor: siddetColor.withOpacity(0.15),
                          child: Icon(krizTuruIcon,
                              color: siddetColor, size: 20),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                record['ogrenci_adi'] as String? ?? '-',
                                style: const TextStyle(
                                    fontSize: 15,
                                    fontWeight: FontWeight.w600),
                              ),
                              Text(
                                '${record['sinif']} - $krizTuruLabel',
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: siddetColor.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            siddetLabel,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: siddetColor,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    // Tarih ve durum
                    Row(
                      children: [
                        const Icon(Icons.calendar_today,
                            size: 13, color: AppColors.textSecondaryDark),
                        const SizedBox(width: 4),
                        Text(
                          record['tarih'] as String? ?? '-',
                          style: const TextStyle(
                              fontSize: 12,
                              color: AppColors.textSecondaryDark),
                        ),
                        const SizedBox(width: 12),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: durum == 'cozuldu'
                                ? AppColors.success.withOpacity(0.1)
                                : AppColors.info.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            durum == 'aktif'
                                ? 'Aktif'
                                : durum == 'takipte'
                                    ? 'Takipte'
                                    : 'Cozuldu',
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: durum == 'cozuldu'
                                  ? AppColors.success
                                  : AppColors.info,
                            ),
                          ),
                        ),
                      ],
                    ),
                    // Alinan aksiyonlar
                    if (aksiyonlar.isNotEmpty) ...[
                      const SizedBox(height: 10),
                      const Text(
                        'Alinan Aksiyonlar:',
                        style: TextStyle(
                            fontSize: 12, fontWeight: FontWeight.w600),
                      ),
                      const SizedBox(height: 4),
                      ...aksiyonlar.map((a) => Padding(
                            padding: const EdgeInsets.only(bottom: 2),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Icon(Icons.check_circle_outline,
                                    size: 14, color: AppColors.success),
                                const SizedBox(width: 6),
                                Expanded(
                                  child: Text(a,
                                      style: const TextStyle(fontSize: 12)),
                                ),
                              ],
                            ),
                          )),
                    ],
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
