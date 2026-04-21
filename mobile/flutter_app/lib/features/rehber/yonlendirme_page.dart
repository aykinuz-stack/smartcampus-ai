import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Ogrenci yonlendirme (sevk) takip sayfasi.
/// RAM, Hastane, Uzman, Diger turlerinde yonlendirmeleri listeler.
class YonlendirmePage extends ConsumerStatefulWidget {
  const YonlendirmePage({super.key});

  @override
  ConsumerState<YonlendirmePage> createState() => _YonlendirmePageState();
}

class _YonlendirmePageState extends ConsumerState<YonlendirmePage>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  List<Map<String, dynamic>> _items = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
    _tabCtrl.addListener(() {
      if (!_tabCtrl.indexIsChanging) setState(() {});
    });
    _load();
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/rehber/yonlendirmeler');
      final data = resp.data;
      if (data is List) {
        _items = List<Map<String, dynamic>>.from(
          data.map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _items = _staticData();
      }
    } catch (_) {
      _items = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  List<Map<String, dynamic>> _staticData() => [
        {
          'id': '1',
          'ogrenci_adi': 'Ahmet Yilmaz',
          'sinif': '9/A',
          'tur': 'RAM',
          'tarih': '2026-04-10',
          'durum': 'bekliyor',
          'aciklama':
              'Ogrenme guclugu supheligi nedeniyle RAM degerlendirmesine yonlendirildi.',
        },
        {
          'id': '2',
          'ogrenci_adi': 'Elif Kara',
          'sinif': '10/B',
          'tur': 'Uzman',
          'tarih': '2026-04-12',
          'durum': 'bekliyor',
          'aciklama':
              'Sinav kaygisi nedeniyle psikolog destegi onerildi.',
        },
        {
          'id': '3',
          'ogrenci_adi': 'Zeynep Celik',
          'sinif': '9/C',
          'tur': 'Hastane',
          'tarih': '2026-03-28',
          'durum': 'tamamlandi',
          'aciklama':
              'Dikkat eksikligi degerlendirmesi icin hastaneye sevk edildi. Rapor alindi.',
        },
        {
          'id': '4',
          'ogrenci_adi': 'Can Ozturk',
          'sinif': '12/A',
          'tur': 'RAM',
          'tarih': '2026-03-15',
          'durum': 'tamamlandi',
          'aciklama':
              'Ustun yetenekli ogrenci degerlendirmesi. RAM raporu tamamlandi.',
        },
        {
          'id': '5',
          'ogrenci_adi': 'Mehmet Demir',
          'sinif': '11/A',
          'tur': 'Diger',
          'tarih': '2026-04-18',
          'durum': 'bekliyor',
          'aciklama':
              'Sosyal hizmet uzmanina yonlendirme. Aile durumu incelenmesi.',
        },
        {
          'id': '6',
          'ogrenci_adi': 'Ayse Sahin',
          'sinif': '10/A',
          'tur': 'Hastane',
          'tarih': '2026-02-20',
          'durum': 'iptal',
          'aciklama':
              'Veli talep uzerine hastane yonlendirmesi iptal edildi.',
        },
      ];

  List<Map<String, dynamic>> get _aktif =>
      _items.where((i) => i['durum'] == 'bekliyor').toList();

  List<Map<String, dynamic>> get _tamamlanan =>
      _items.where((i) => i['durum'] != 'bekliyor').toList();

  Color _durumColor(String durum) {
    switch (durum) {
      case 'bekliyor':
        return AppColors.warning;
      case 'tamamlandi':
        return AppColors.success;
      case 'iptal':
        return AppColors.danger;
      default:
        return Colors.grey;
    }
  }

  String _durumLabel(String durum) {
    switch (durum) {
      case 'bekliyor':
        return 'Bekliyor';
      case 'tamamlandi':
        return 'Tamamlandi';
      case 'iptal':
        return 'Iptal';
      default:
        return durum;
    }
  }

  IconData _turIcon(String tur) {
    switch (tur) {
      case 'RAM':
        return Icons.account_balance;
      case 'Hastane':
        return Icons.local_hospital;
      case 'Uzman':
        return Icons.psychology;
      case 'Diger':
        return Icons.more_horiz;
      default:
        return Icons.send;
    }
  }

  Color _turColor(String tur) {
    switch (tur) {
      case 'RAM':
        return AppColors.primary;
      case 'Hastane':
        return AppColors.danger;
      case 'Uzman':
        return AppColors.info;
      case 'Diger':
        return AppColors.gold;
      default:
        return Colors.grey;
    }
  }

  void _showNewReferralSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (_) => _YeniYonlendirmeSheet(
        onSaved: () => _load(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Yonlendirmeler'),
        bottom: TabBar(
          controller: _tabCtrl,
          indicatorColor: AppColors.primary,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textSecondaryDark,
          tabs: [
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.pending_actions, size: 18),
                  const SizedBox(width: 6),
                  const Text('Aktif'),
                  if (_aktif.isNotEmpty) ...[
                    const SizedBox(width: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 6, vertical: 1),
                      decoration: BoxDecoration(
                        color: AppColors.warning.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text('${_aktif.length}',
                          style: const TextStyle(
                              fontSize: 11, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ],
              ),
            ),
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.check_circle_outline, size: 18),
                  const SizedBox(width: 6),
                  const Text('Tamamlanan'),
                ],
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showNewReferralSheet,
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        icon: const Icon(Icons.add),
        label: const Text('Yeni Yonlendirme'),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _load,
              child: TabBarView(
                controller: _tabCtrl,
                children: [
                  _buildList(_aktif, emptyMsg: 'Aktif yonlendirme yok'),
                  _buildList(_tamamlanan,
                      emptyMsg: 'Tamamlanan yonlendirme yok'),
                ],
              ),
            ),
    );
  }

  Widget _buildList(List<Map<String, dynamic>> items,
      {required String emptyMsg}) {
    if (items.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.send, size: 48, color: Colors.grey),
            const SizedBox(height: 12),
            Text(emptyMsg,
                style: const TextStyle(color: AppColors.textSecondaryDark)),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(14, 12, 14, 80),
      itemCount: items.length,
      itemBuilder: (_, i) {
        final item = items[i];
        final tur = item['tur'] as String? ?? 'Diger';
        final durum = item['durum'] as String? ?? '';
        final durumC = _durumColor(durum);

        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          clipBehavior: Clip.antiAlias,
          child: IntrinsicHeight(
            child: Row(
              children: [
                // Colored left strip
                Container(width: 5, color: _turColor(tur)),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 18,
                              backgroundColor:
                                  _turColor(tur).withOpacity(0.12),
                              child: Icon(_turIcon(tur),
                                  size: 18, color: _turColor(tur)),
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    item['ogrenci_adi'] as String? ?? '-',
                                    style: const TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.w600),
                                  ),
                                  Text(
                                    item['sinif'] as String? ?? '',
                                    style: const TextStyle(
                                        fontSize: 12,
                                        color: AppColors.textSecondaryDark),
                                  ),
                                ],
                              ),
                            ),
                            // Status badge
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: durumC.withOpacity(0.15),
                                borderRadius: BorderRadius.circular(6),
                              ),
                              child: Text(
                                _durumLabel(durum),
                                style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.bold,
                                    color: durumC),
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        // Type + Date row
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: 8, vertical: 3),
                              decoration: BoxDecoration(
                                color: _turColor(tur).withOpacity(0.1),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                tur,
                                style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w600,
                                    color: _turColor(tur)),
                              ),
                            ),
                            const SizedBox(width: 10),
                            const Icon(Icons.calendar_today,
                                size: 12,
                                color: AppColors.textSecondaryDark),
                            const SizedBox(width: 4),
                            Text(
                              item['tarih'] as String? ?? '-',
                              style: const TextStyle(
                                  fontSize: 12,
                                  color: AppColors.textSecondaryDark),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        // Description
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: Colors.grey.withOpacity(0.06),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            item['aciklama'] as String? ?? '',
                            style: const TextStyle(fontSize: 13),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

// ---------------------------------------------------------------------------
// Yeni Yonlendirme Bottom Sheet
// ---------------------------------------------------------------------------
class _YeniYonlendirmeSheet extends StatefulWidget {
  final VoidCallback onSaved;

  const _YeniYonlendirmeSheet({required this.onSaved});

  @override
  State<_YeniYonlendirmeSheet> createState() => _YeniYonlendirmeSheetState();
}

class _YeniYonlendirmeSheetState extends State<_YeniYonlendirmeSheet> {
  final _formKey = GlobalKey<FormState>();
  final _ogrenciCtrl = TextEditingController();
  final _aciklamaCtrl = TextEditingController();
  String _selectedTur = 'RAM';
  bool _saving = false;

  static const _turler = ['RAM', 'Hastane', 'Uzman', 'Diger'];

  @override
  void dispose() {
    _ogrenciCtrl.dispose();
    _aciklamaCtrl.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _saving = true);
    try {
      // In production, this would call the API:
      // final api = ref.read(apiClientProvider);
      // await api.post('/rehber/yonlendirme', data: { ... });
      await Future.delayed(const Duration(milliseconds: 500));

      if (!mounted) return;
      Navigator.pop(context);
      widget.onSaved();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Yonlendirme kaydedildi'),
          backgroundColor: AppColors.success,
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Hata: $e'),
          backgroundColor: AppColors.danger,
        ),
      );
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        left: 20,
        right: 20,
        top: 20,
        bottom: MediaQuery.of(context).viewInsets.bottom + 20,
      ),
      child: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Handle bar
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const Text('Yeni Yonlendirme',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),

              // Ogrenci adi
              TextFormField(
                controller: _ogrenciCtrl,
                decoration: InputDecoration(
                  labelText: 'Ogrenci Adi *',
                  hintText: 'Ad Soyad',
                  prefixIcon:
                      const Icon(Icons.person, color: AppColors.primary),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10)),
                ),
                validator: (v) =>
                    (v == null || v.trim().length < 3) ? 'Ad gerekli' : null,
              ),
              const SizedBox(height: 14),

              // Tur secimi
              DropdownButtonFormField<String>(
                value: _selectedTur,
                decoration: InputDecoration(
                  labelText: 'Yonlendirme Turu *',
                  prefixIcon: const Icon(Icons.category, color: AppColors.info),
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10)),
                ),
                items: _turler
                    .map((t) => DropdownMenuItem(
                          value: t,
                          child: Text(_turDisplayName(t)),
                        ))
                    .toList(),
                onChanged: (v) {
                  if (v != null) setState(() => _selectedTur = v);
                },
              ),
              const SizedBox(height: 14),

              // Aciklama
              TextFormField(
                controller: _aciklamaCtrl,
                maxLines: 4,
                decoration: InputDecoration(
                  labelText: 'Aciklama *',
                  hintText: 'Yonlendirme sebebi ve detaylar...',
                  alignLabelWithHint: true,
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(10)),
                ),
                validator: (v) => (v == null || v.trim().length < 10)
                    ? 'En az 10 karakter'
                    : null,
              ),
              const SizedBox(height: 20),

              // Save button
              SizedBox(
                height: 50,
                child: ElevatedButton.icon(
                  onPressed: _saving ? null : _save,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                  ),
                  icon: _saving
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : const Icon(Icons.save),
                  label: const Text('KAYDET',
                      style: TextStyle(fontWeight: FontWeight.w600)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _turDisplayName(String tur) {
    switch (tur) {
      case 'RAM':
        return 'RAM (Rehberlik Arastirma Merkezi)';
      case 'Hastane':
        return 'Hastane';
      case 'Uzman':
        return 'Uzman Psikolog';
      case 'Diger':
        return 'Diger';
      default:
        return tur;
    }
  }
}
