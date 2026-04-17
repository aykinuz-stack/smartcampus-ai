import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

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

  @override
  void initState() {
    super.initState();
    _loadOnerileri();
    // Karsilama mesaji
    _messages.add(_ChatMsg(
      text: 'Merhaba! 👋 Ben Smarti, SmartCampus AI asistanınım.\nSize nasıl yardımcı olabilirim?',
      isUser: false,
    ));
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
      _messages.add(_ChatMsg(text: text, isUser: true));
      _loading = true;
    });
    _scroll();

    try {
      final r = await ref.read(apiClientProvider).post('/smarti/chat', data: {
        'mesaj': text,
      });
      final cevap = r.data['cevap'] as String? ?? 'Bir hata oluştu.';
      setState(() {
        _messages.add(_ChatMsg(text: cevap, isUser: false));
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _messages.add(_ChatMsg(
          text: '⚠️ Bağlantı hatası. Lütfen tekrar deneyin.',
          isUser: false,
        ));
        _loading = false;
      });
    }
    _scroll();
  }

  void _scroll() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(_scrollCtrl.position.maxScrollExtent + 100,
            duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      }
    });
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
            Text('Çevrimiçi', style: TextStyle(fontSize: 10, color: AppColors.success)),
          ]),
        ]),
      ),
      body: Column(children: [
        // Oneri chipleri (ust kisim, ilk gosterim)
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

        // Input
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
}


class _ChatMsg {
  final String text;
  final bool isUser;
  _ChatMsg({required this.text, required this.isUser});
}


class _MessageBubble extends StatelessWidget {
  final _ChatMsg msg;
  const _MessageBubble({required this.msg});

  @override
  Widget build(BuildContext context) {
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
        child: Row(
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
          const Text('Smarti düşünüyor...', style: TextStyle(fontSize: 13, fontStyle: FontStyle.italic)),
        ]),
      ),
    );
  }
}
