import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

/// Toplanti ve kurul yonetimi sayfasi - Yonetici gorunumu.
/// Yaklasan ve gecmis toplantilar, tur bazli renk kodlama.
class ToplantiKurullarPage extends ConsumerStatefulWidget {
  const ToplantiKurullarPage({super.key});

  @override
  ConsumerState<ToplantiKurullarPage> createState() =>
      _ToplantiKurullarPageState();
}

class _ToplantiKurullarPageState extends ConsumerState<ToplantiKurullarPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<Map<String, dynamic>> _meetings = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _load();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiClientProvider);
      final resp = await api.get('/yonetici/toplantilar');
      final data = resp.data;
      if (data is List) {
        _meetings = List<Map<String, dynamic>>.from(
          data.map((e) => Map<String, dynamic>.from(e as Map)),
        );
      } else {
        _meetings = _staticData();
      }
    } catch (_) {
      _meetings = _staticData();
    }
    if (mounted) setState(() => _loading = false);
  }

  List<Map<String, dynamic>> _staticData() {
    final now = DateTime(2026, 4, 21);
    return [
      {
        'id': 'tp_001',
        'baslik': 'Nisan Ogretmenler Kurulu',
        'tarih': '2026-04-25',
        'saat': '14:00',
        'yer': 'Konferans Salonu',
        'katilimci_sayisi': 42,
        'tur': 'ogretmenler_kurulu',
        'gundem': [
          'Donem sonu degerlendirme',
          'Sinav takvimi',
          'Ogrenci disiplin konulari',
        ],
      },
      {
        'id': 'tp_002',
        'baslik': 'Matematik Zumre Toplantisi',
        'tarih': '2026-04-23',
        'saat': '10:30',
        'yer': 'Toplanti Odasi 1',
        'katilimci_sayisi': 8,
        'tur': 'zumre',
        'gundem': [
          'Mufredat ilerleme durumu',
          'Ortak sinav hazirligi',
        ],
      },
      {
        'id': 'tp_003',
        'baslik': 'Veli Bilgilendirme Toplantisi',
        'tarih': '2026-04-28',
        'saat': '18:00',
        'yer': 'Spor Salonu',
        'katilimci_sayisi': 120,
        'tur': 'veli',
        'gundem': [
          'YKS hazirlik sureci',
          'Rehberlik hizmetleri',
          'Yaz okulu bilgilendirme',
        ],
      },
      {
        'id': 'tp_004',
        'baslik': 'Idari Kurul Toplantisi',
        'tarih': '2026-04-22',
        'saat': '09:00',
        'yer': 'Mudur Odasi',
        'katilimci_sayisi': 6,
        'tur': 'idari',
        'gundem': [
          'Butce revizyonu',
          'Personel planlamasi',
        ],
      },
      {
        'id': 'tp_005',
        'baslik': 'Okul Gelistirme Toplantisi',
        'tarih': '2026-05-05',
        'saat': '13:00',
        'yer': 'Konferans Salonu',
        'katilimci_sayisi': 15,
        'tur': 'diger',
        'gundem': [
          'Dijital donusum projesi',
          'Fiziksel altyapi iyilestirme',
        ],
      },
      // Gecmis toplantilar
      {
        'id': 'tp_006',
        'baslik': 'Mart Ogretmenler Kurulu',
        'tarih': '2026-03-28',
        'saat': '14:00',
        'yer': 'Konferans Salonu',
        'katilimci_sayisi': 40,
        'tur': 'ogretmenler_kurulu',
        'gundem': [
          'Ara tatil degerlendirmesi',
          'Akademik basari analizi',
        ],
      },
      {
        'id': 'tp_007',
        'baslik': 'Fen Bilimleri Zumre',
        'tarih': '2026-04-10',
        'saat': '11:00',
        'yer': 'Laboratuvar',
        'katilimci_sayisi': 6,
        'tur': 'zumre',
        'gundem': [
          'Deney malzemesi temini',
          'Proje odevleri degerlendirme',
        ],
      },
      {
        'id': 'tp_008',
        'baslik': 'Subat Veli Toplantisi',
        'tarih': '2026-02-20',
        'saat': '18:00',
        'yer': 'Spor Salonu',
        'katilimci_sayisi': 110,
        'tur': 'veli',
        'gundem': [
          'Karne bilgilendirme',
          'Ikinci donem planlama',
        ],
      },
    ];
  }

  Color _turColor(String tur) {
    switch (tur) {
      case 'ogretmenler_kurulu':
        return AppColors.primary;
      case 'zumre':
        return AppColors.info;
      case 'veli':
        return AppColors.success;
      case 'idari':
        return AppColors.warning;
      case 'diger':
        return AppColors.gold;
      default:
        return Colors.grey;
    }
  }

  String _turLabel(String tur) {
    switch (tur) {
      case 'ogretmenler_kurulu':
        return 'Ogretmenler Kurulu';
      case 'zumre':
        return 'Zumre';
      case 'veli':
        return 'Veli';
      case 'idari':
        return 'Idari';
      case 'diger':
        return 'Diger';
      default:
        return tur;
    }
  }

  IconData _turIcon(String tur) {
    switch (tur) {
      case 'ogretmenler_kurulu':
        return Icons.groups;
      case 'zumre':
        return Icons.school;
      case 'veli':
        return Icons.family_restroom;
      case 'idari':
        return Icons.admin_panel_settings;
      case 'diger':
        return Icons.event_note;
      default:
        return Icons.event;
    }
  }

  String _countdownText(String tarihStr) {
    try {
      final tarih = DateTime.parse(tarihStr);
      final now = DateTime(2026, 4, 21); // Simulated today
      final diff = tarih.difference(now).inDays;
      if (diff == 0) return 'Bugun';
      if (diff == 1) return 'Yarin';
      if (diff < 0) return '${-diff} gun once';
      return '$diff gun kaldi';
    } catch (_) {
      return '-';
    }
  }

  Color _countdownColor(String tarihStr) {
    try {
      final tarih = DateTime.parse(tarihStr);
      final now = DateTime(2026, 4, 21);
      final diff = tarih.difference(now).inDays;
      if (diff <= 1) return AppColors.danger;
      if (diff <= 3) return AppColors.warning;
      return AppColors.info;
    } catch (_) {
      return Colors.grey;
    }
  }

  bool _isUpcoming(String tarihStr) {
    try {
      final tarih = DateTime.parse(tarihStr);
      final now = DateTime(2026, 4, 21);
      return !tarih.isBefore(now);
    } catch (_) {
      return false;
    }
  }

  List<Map<String, dynamic>> get _upcoming =>
      _meetings.where((m) => _isUpcoming(m['tarih'] as String)).toList()
        ..sort((a, b) =>
            (a['tarih'] as String).compareTo(b['tarih'] as String));

  List<Map<String, dynamic>> get _past =>
      _meetings.where((m) => !_isUpcoming(m['tarih'] as String)).toList()
        ..sort((a, b) =>
            (b['tarih'] as String).compareTo(a['tarih'] as String));

  void _showScheduleSheet() {
    final formKey = GlobalKey<FormState>();
    String baslik = '';
    String tarih = '';
    String saat = '';
    String yer = '';
    String tur = 'ogretmenler_kurulu';

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
                  'Yeni Toplanti Planla',
                  style: TextStyle(
                      fontSize: 18, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Toplanti Basligi',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.title),
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => baslik = v ?? '',
                ),
                const SizedBox(height: 12),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Tarih (YYYY-MM-DD)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.calendar_today),
                    hintText: '2026-05-01',
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => tarih = v ?? '',
                ),
                const SizedBox(height: 12),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Saat (HH:MM)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.access_time),
                    hintText: '14:00',
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => saat = v ?? '',
                ),
                const SizedBox(height: 12),
                TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Yer',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.location_on),
                  ),
                  validator: (v) =>
                      (v == null || v.isEmpty) ? 'Zorunlu alan' : null,
                  onSaved: (v) => yer = v ?? '',
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: tur,
                  decoration: const InputDecoration(
                    labelText: 'Toplanti Turu',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.category),
                  ),
                  items: const [
                    DropdownMenuItem(
                        value: 'ogretmenler_kurulu',
                        child: Text('Ogretmenler Kurulu')),
                    DropdownMenuItem(value: 'zumre', child: Text('Zumre')),
                    DropdownMenuItem(value: 'veli', child: Text('Veli')),
                    DropdownMenuItem(value: 'idari', child: Text('Idari')),
                    DropdownMenuItem(value: 'diger', child: Text('Diger')),
                  ],
                  onChanged: (v) => tur = v ?? 'diger',
                ),
                const SizedBox(height: 20),
                ElevatedButton.icon(
                  onPressed: () {
                    if (formKey.currentState?.validate() ?? false) {
                      formKey.currentState?.save();
                      final newMeeting = <String, dynamic>{
                        'id':
                            'tp_${DateTime.now().millisecondsSinceEpoch}',
                        'baslik': baslik,
                        'tarih': tarih,
                        'saat': saat,
                        'yer': yer,
                        'katilimci_sayisi': 0,
                        'tur': tur,
                        'gundem': <String>[],
                      };
                      setState(() => _meetings.add(newMeeting));
                      Navigator.pop(ctx);
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text('Toplanti planlandirildi'),
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
        title: const Text('Toplanti & Kurullar'),
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: _load),
        ],
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: AppColors.primary,
          labelColor: AppColors.primary,
          unselectedLabelColor: AppColors.textSecondaryDark,
          tabs: [
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.upcoming, size: 18),
                  const SizedBox(width: 6),
                  const Text('Yaklasan'),
                  if (_upcoming.isNotEmpty) ...[
                    const SizedBox(width: 6),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(
                        color: AppColors.primary.withOpacity(0.15),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        '${_upcoming.length}',
                        style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                            color: AppColors.primary),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.history, size: 18),
                  const SizedBox(width: 6),
                  const Text('Gecmis'),
                ],
              ),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showScheduleSheet,
        backgroundColor: AppColors.primary,
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('Yeni Toplanti',
            style: TextStyle(color: Colors.white)),
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabController,
              children: [
                // Yaklasan
                _buildMeetingList(_upcoming, isUpcoming: true),
                // Gecmis
                _buildMeetingList(_past, isUpcoming: false),
              ],
            ),
    );
  }

  Widget _buildMeetingList(List<Map<String, dynamic>> list,
      {required bool isUpcoming}) {
    if (list.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              isUpcoming ? Icons.event_available : Icons.history,
              size: 48,
              color: Colors.grey,
            ),
            const SizedBox(height: 12),
            Text(
              isUpcoming
                  ? 'Yaklasan toplanti yok'
                  : 'Gecmis toplanti kaydedilmemis',
              style: const TextStyle(color: AppColors.textSecondaryDark),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.all(14),
        itemCount: list.length,
        itemBuilder: (_, i) {
          final m = list[i];
          final tur = m['tur'] as String? ?? 'diger';
          final color = _turColor(tur);
          final tarih = m['tarih'] as String? ?? '';
          final gundem = List<String>.from(m['gundem'] ?? []);

          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12)),
            clipBehavior: Clip.antiAlias,
            child: IntrinsicHeight(
              child: Row(
                children: [
                  Container(width: 5, color: color),
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.all(14),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Baslik satiri
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                width: 42,
                                height: 42,
                                decoration: BoxDecoration(
                                  color: color.withOpacity(0.12),
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Icon(_turIcon(tur),
                                    color: color, size: 22),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment:
                                      CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      m['baslik'] as String? ?? '-',
                                      style: const TextStyle(
                                          fontSize: 15,
                                          fontWeight: FontWeight.w600),
                                    ),
                                    const SizedBox(height: 4),
                                    Container(
                                      padding: const EdgeInsets.symmetric(
                                          horizontal: 8, vertical: 3),
                                      decoration: BoxDecoration(
                                        color: color.withOpacity(0.1),
                                        borderRadius:
                                            BorderRadius.circular(6),
                                      ),
                                      child: Text(
                                        _turLabel(tur),
                                        style: TextStyle(
                                          fontSize: 11,
                                          fontWeight: FontWeight.w600,
                                          color: color,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              // Countdown badge (sadece yaklasan)
                              if (isUpcoming)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 5),
                                  decoration: BoxDecoration(
                                    color: _countdownColor(tarih)
                                        .withOpacity(0.12),
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                  child: Text(
                                    _countdownText(tarih),
                                    style: TextStyle(
                                      fontSize: 11,
                                      fontWeight: FontWeight.bold,
                                      color: _countdownColor(tarih),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          // Detay satiri
                          Row(
                            children: [
                              const Icon(Icons.calendar_today,
                                  size: 13,
                                  color: AppColors.textSecondaryDark),
                              const SizedBox(width: 4),
                              Text(
                                tarih,
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                              const SizedBox(width: 12),
                              const Icon(Icons.access_time,
                                  size: 13,
                                  color: AppColors.textSecondaryDark),
                              const SizedBox(width: 4),
                              Text(
                                m['saat'] as String? ?? '-',
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                              const SizedBox(width: 12),
                              const Icon(Icons.location_on,
                                  size: 13,
                                  color: AppColors.textSecondaryDark),
                              const SizedBox(width: 4),
                              Expanded(
                                child: Text(
                                  m['yer'] as String? ?? '-',
                                  style: const TextStyle(
                                      fontSize: 12,
                                      color:
                                          AppColors.textSecondaryDark),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 6),
                          Row(
                            children: [
                              const Icon(Icons.people,
                                  size: 13,
                                  color: AppColors.textSecondaryDark),
                              const SizedBox(width: 4),
                              Text(
                                '${m['katilimci_sayisi'] ?? 0} katilimci',
                                style: const TextStyle(
                                    fontSize: 12,
                                    color: AppColors.textSecondaryDark),
                              ),
                            ],
                          ),
                          // Gundem
                          if (gundem.isNotEmpty) ...[
                            const SizedBox(height: 10),
                            const Text(
                              'Gundem:',
                              style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600),
                            ),
                            const SizedBox(height: 4),
                            ...gundem.map((g) => Padding(
                                  padding:
                                      const EdgeInsets.only(bottom: 2),
                                  child: Row(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        '\u2022 ',
                                        style: TextStyle(
                                            color: color, fontSize: 13),
                                      ),
                                      Expanded(
                                        child: Text(g,
                                            style: const TextStyle(
                                                fontSize: 12)),
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
        },
      ),
    );
  }
}
