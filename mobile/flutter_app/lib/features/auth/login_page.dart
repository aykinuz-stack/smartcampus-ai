import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';

class LoginPage extends ConsumerStatefulWidget {
  const LoginPage({super.key});

  @override
  ConsumerState<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends ConsumerState<LoginPage> {
  final _usernameCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _tenantCtrl = TextEditingController(text: 'default');
  bool _loading = false;
  String? _error;
  bool _obscurePw = true;

  @override
  void dispose() {
    _usernameCtrl.dispose();
    _passwordCtrl.dispose();
    _tenantCtrl.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    final user = await ref.read(authServiceProvider).login(
          _usernameCtrl.text.trim(),
          _passwordCtrl.text,
          tenantId: _tenantCtrl.text.trim(),
        );
    setState(() => _loading = false);
    if (user != null) {
      // Rol bazlı yönlendirme
      if (user.isOgrenci) {
        if (mounted) context.go('/ogrenci');
      } else if (user.isVeli) {
        if (mounted) context.go('/veli');
      } else if (user.isOgretmen) {
        if (mounted) context.go('/ogretmen');
      } else if (user.isRehber) {
        if (mounted) context.go('/rehber');
      } else if (user.isYonetici) {
        if (mounted) context.go('/yonetici');
      } else {
        if (mounted) context.go('/home');
      }
    } else {
      setState(() => _error = 'Giriş başarısız. Kontrol et:\n'
          '• Kullanıcı adı ve şifre doğru mu?\n'
          '• Backend çalışıyor mu? (bilgisayar açık mı?)\n'
          '• Aynı Wi-Fi ağında mısın?');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [AppColors.surfaceDarker, AppColors.surfaceDark, AppColors.primaryDark],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Logo
                  Container(
                    width: 96,
                    height: 96,
                    decoration: BoxDecoration(
                      gradient: const LinearGradient(colors: [AppColors.primary, AppColors.gold]),
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(color: AppColors.primary.withOpacity(0.4), blurRadius: 24, spreadRadius: 2),
                      ],
                    ),
                    child: const Icon(Icons.school_rounded, size: 56, color: Colors.white),
                  ),
                  const SizedBox(height: 24),
                  const Text(
                    'SmartCampus AI',
                    style: TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textPrimaryDark,
                    ),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Eğitimin Geleceği Burada',
                    style: TextStyle(
                      fontSize: 14,
                      color: AppColors.gold,
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                  const SizedBox(height: 40),

                  // Login form
                  Card(
                    color: AppColors.cardDark,
                    elevation: 8,
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          TextField(
                            controller: _usernameCtrl,
                            style: const TextStyle(color: AppColors.textPrimaryDark),
                            decoration: InputDecoration(
                              labelText: 'Kullanıcı Adı',
                              prefixIcon: const Icon(Icons.person),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                          const SizedBox(height: 16),
                          TextField(
                            controller: _passwordCtrl,
                            obscureText: _obscurePw,
                            style: const TextStyle(color: AppColors.textPrimaryDark),
                            decoration: InputDecoration(
                              labelText: 'Şifre',
                              prefixIcon: const Icon(Icons.lock),
                              suffixIcon: IconButton(
                                icon: Icon(_obscurePw ? Icons.visibility : Icons.visibility_off),
                                onPressed: () => setState(() => _obscurePw = !_obscurePw),
                              ),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                            ),
                            onSubmitted: (_) => _handleLogin(),
                          ),
                          const SizedBox(height: 16),
                          ExpansionTile(
                            title: const Text('Kurum Kodu (opsiyonel)',
                                style: TextStyle(fontSize: 13)),
                            tilePadding: EdgeInsets.zero,
                            children: [
                              TextField(
                                controller: _tenantCtrl,
                                style: const TextStyle(color: AppColors.textPrimaryDark),
                                decoration: InputDecoration(
                                  labelText: 'Kurum ID',
                                  hintText: 'örn: uz_koleji',
                                  prefixIcon: const Icon(Icons.business),
                                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                ),
                              ),
                            ],
                          ),
                          if (_error != null) ...[
                            const SizedBox(height: 12),
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: AppColors.danger.withOpacity(0.15),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: AppColors.danger.withOpacity(0.4)),
                              ),
                              child: Row(
                                children: [
                                  const Icon(Icons.error_outline, color: AppColors.danger),
                                  const SizedBox(width: 8),
                                  Expanded(
                                    child: Text(_error!, style: const TextStyle(color: AppColors.danger)),
                                  ),
                                ],
                              ),
                            ),
                          ],
                          const SizedBox(height: 20),
                          SizedBox(
                            width: double.infinity,
                            height: 52,
                            child: ElevatedButton(
                              onPressed: _loading ? null : _handleLogin,
                              child: _loading
                                  ? const SizedBox(
                                      width: 24,
                                      height: 24,
                                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                                    )
                                  : const Text('GİRİŞ YAP', style: TextStyle(fontSize: 15, letterSpacing: 1.2)),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: 24),
                  Text(
                    'SmartCampus AI v1.0 · Native Android',
                    style: TextStyle(color: AppColors.textSecondaryDark.withOpacity(0.7), fontSize: 12),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
