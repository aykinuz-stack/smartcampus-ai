import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';


/// Smarti AI Chat — sesli giris + chat gecmisi + oneriler
class SmartiChatPage extends ConsumerStatefulWidget {
  const SmartiChatPage({super.key});
  @override
  ConsumerState<SmartiChatPage> createState() => _SmartiChatPageState();
}

class _SmartiChatPageState extends ConsumerState<SmartiChatPage> {
  final _ctrl = TextEditingController();
  final _scrollCtrl = ScrollController();
  final List<_ChatMsg> _messages = [];
  bool _loading = false;
  List<String> _oneriler = [];
  bool _listening = false;

  @override
  void initState() {
    super.initState();
    _loadHistory();
    _loadOnerileri();
    if (_messages.isEmpty) {
      _messages.add(_ChatMsg(
        text: 'Merhaba! Ben Smarti, SmartCampus AI asistanin.\nSana nasil yardimci olabilirim?',
        isUser: false,
        time: DateTime.now(),
      ));
    }
  }

  void _loadHistory() {
    try {
      final box = Hive.box<Map>('cached_data');
      final raw = box.get('smarti_history');
      if (raw != null) {
        final list = List<Map>.from(raw['messages'] as List? ?? []);
        for (final m in list.take(50)) {
          _messages.add(_ChatMsg(
            text: m['text'] as String? ?? '',
            isUser: m['isUser'] as bool? ?? false,
            time: DateTime.tryParse(m['time'] as String? ?? '') ?? DateTime.now(),
          ));
        }
      }
    } catch (_) {}
  }

  void _saveHistory() {
    try {
      final box = Hive.box<Map>('cached_data');
      final recent = _messages.take(100).map((m) => {
        'text': m.text,
        'isUser': m.isUser,
        'time': m.time.toIso8601String(),
      }).toList();
      box.put('smarti_history', {'messages': recent});
    } catch (_) {}
  }

  Future<void> _loadOnerileri() async {
    try {
      final r = await ref.read(apiClientProvider).get('/smarti/onerileri');
      setState(() => _oneriler = List<String>.from(r.data['oneriler'] as List));
    } catch (_) {}
  }

  Future<void> _gonder([String? hazirMesaj]) async {
    final text = hazirMesaj ?? _ctrl.text.trim();
    if (text.isEmpty) return;
    _ctrl.clear();

    setState(() {
      _messages.add(_ChatMsg(text: text, isUser: true, time: DateTime.now()));
      _loading = true;
    });
    _scroll();

    try {
      final r = await ref.read(apiClientProvider).post('/smarti/chat', data: {
        'mesaj': text,
      });
      final cevap = r.data['cevap'] as String? ?? 'Bir hata olustu.';
      setState(() {
        _messages.add(_ChatMsg(text: cevap, isUser: false, time: DateTime.now()));
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _messages.add(_ChatMsg(
          text: 'Baglanti hatasi. Lutfen tekrar deneyin.',
          isUser: false,
          time: DateTime.now(),
        ));
        _loading = false;
      });
    }
    _scroll();
    _saveHistory();
  }

  void _scroll() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(_scrollCtrl.position.maxScrollExtent + 100,
            duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      }
    });
  }

  void _gecmisiTemizle() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Sohbet Gecmisi'),
        content: const Text('Tum sohbet gecmisi silinsin mi?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Vazgec')),
          TextButton(
            onPressed: () {
              setState(() {
                _messages.clear();
                _messages.add(_ChatMsg(
                  text: 'Merhaba! Sohbet gecmisi temizlendi. Nasil yardimci olabilirim?',
                  isUser: false,
                  time: DateTime.now(),
                ));
              });
              try {
                Hive.box<Map>('cached_data').delete('smarti_history');
              } catch (_) {}
              Navigator.pop(ctx);
            },
            child: const Text('Temizle', style: TextStyle(color: AppColors.danger)),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    _scrollCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(children: [
          Container(
            width: 32, height: 32,
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [AppColors.primary, AppColors.gold]),
              borderRadius: BorderRadius.circular(8),
            ),
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 18),
          ),
          const SizedBox(width: 10),
          const Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Smarti AI', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            Text('Cevrimici', style: TextStyle(fontSize: 10, color: AppColors.success)),
          ]),
        ]),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_sweep_outlined),
            tooltip: 'Gecmisi temizle',
            onPressed: _gecmisiTemizle,
          ),
        ],
      ),
      body: Column(children: [
        // Oneri chipleri
        if (_oneriler.isNotEmpty && _messages.length <= 2)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(children: _oneriler.map((o) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: ActionChip(
                  label: Text(o, style: const TextStyle(fontSize: 12)),
                  backgroundColor: AppColors.primary.withOpacity(0.1),
                  onPressed: () => _gonder(o),
                ),
              )).toList()),
            ),
          ),

        // Mesajlar
        Expanded(
          child: ListView.builder(
            controller: _scrollCtrl,
            padding: const EdgeInsets.all(12),
            itemCount: _messages.length + (_loading ? 1 : 0),
            itemBuilder: (_, i) {
              if (i == _messages.length && _loading) {
                return _TypingIndicator();
              }
              return _MessageBubble(msg: _messages[i]);
            },
          ),
        ),

        // Input + voice
        SafeArea(
          top: false,
          child: Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05),
                  blurRadius: 4, offset: const Offset(0, -2))],
            ),
            child: Row(children: [
              // Mikrofon butonu
              Container(
                decoration: BoxDecoration(
                  color: _listening
                      ? AppColors.danger.withOpacity(0.15)
                      : Colors.grey.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  icon: Icon(
                    _listening ? Icons.mic : Icons.mic_none,
                    color: _listening ? AppColors.danger : AppColors.textSecondaryDark,
                  ),
                  onPressed: _toggleVoice,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: TextField(
                  controller: _ctrl,
                  decoration: InputDecoration(
                    hintText: 'Smarti\'ye sor...',
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none),
                    filled: true,
                    fillColor: Colors.grey.withOpacity(0.1),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  ),
                  maxLines: null,
                  textInputAction: TextInputAction.send,
                  onSubmitted: (_) => _gonder(),
                ),
              ),
              const SizedBox(width: 8),
              Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(colors: [AppColors.primary, AppColors.gold]),
                  shape: BoxShape.circle,
                ),
                child: IconButton(
                  icon: const Icon(Icons.send, color: Colors.white, size: 20),
                  onPressed: _loading ? null : () => _gonder(),
                ),
              ),
            ]),
          ),
        ),
      ]),
    );
  }

  void _toggleVoice() {
    // speech_to_text entegrasyonu — platform izin gerektirdiginden
    // burada sadece UI state toggle'i yapiyoruz. Gercek STT icin:
    // final stt = SpeechToText(); stt.listen(onResult: ...)
    setState(() => _listening = !_listening);
    if (_listening) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Sesli giris aktif — konusmaya baslayin...'),
          duration: Duration(seconds: 2),
          backgroundColor: AppColors.primary,
        ),
      );
      // 5 saniye sonra otomatik kapat (demo)
      Future.delayed(const Duration(seconds: 5), () {
        if (mounted && _listening) {
          setState(() => _listening = false);
        }
      });
    }
  }
}


class _ChatMsg {
  final String text;
  final bool isUser;
  final DateTime time;
  _ChatMsg({required this.text, required this.isUser, required this.time});
}


class _MessageBubble extends StatelessWidget {
  final _ChatMsg msg;
  const _MessageBubble({required this.msg});

  @override
  Widget build(BuildContext context) {
    final timeStr = '${msg.time.hour.toString().padLeft(2, '0')}:'
        '${msg.time.minute.toString().padLeft(2, '0')}';

    return Align(
      alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(14),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
        decoration: BoxDecoration(
          color: msg.isUser
              ? AppColors.primary.withOpacity(0.2)
              : Theme.of(context).cardColor,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(msg.isUser ? 16 : 4),
            bottomRight: Radius.circular(msg.isUser ? 4 : 16),
          ),
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.05),
                blurRadius: 4, offset: const Offset(0, 2)),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (!msg.isUser) ...[
                  Container(
                    width: 24, height: 24,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(colors: [AppColors.primary, AppColors.gold]),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: const Icon(Icons.smart_toy, color: Colors.white, size: 14),
                  ),
                  const SizedBox(width: 8),
                ],
                Flexible(
                  child: Text(msg.text, style: const TextStyle(fontSize: 14, height: 1.4)),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Align(
              alignment: Alignment.bottomRight,
              child: Text(timeStr,
                  style: TextStyle(fontSize: 10, color: Colors.grey[500])),
            ),
          ],
        ),
      ),
    );
  }
}


class _TypingIndicator extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Container(
            width: 24, height: 24,
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [AppColors.primary, AppColors.gold]),
              borderRadius: BorderRadius.circular(6),
            ),
            child: const Icon(Icons.smart_toy, color: Colors.white, size: 14),
          ),
          const SizedBox(width: 10),
          const SizedBox(width: 16, height: 16,
              child: CircularProgressIndicator(strokeWidth: 2)),
          const SizedBox(width: 8),
          const Text('Smarti dusunuyor...', style: TextStyle(fontSize: 13, fontStyle: FontStyle.italic)),
        ]),
      ),
    );
  }
}
