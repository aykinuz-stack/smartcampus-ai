import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/api/api_client.dart';
import '../../core/auth/auth_service.dart';
import '../../core/theme/app_theme.dart';
import '../../core/theme/theme_provider.dart';


/// Profil Sayfasi — tum roller icin
class ProfilPage extends ConsumerWidget {
  const ProfilPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userAsync = ref.watch(currentUserProvider);
    final themeMode = ref.watch(themeModeProvider);

    return userAsync.when(
      data: (user) {
        if (user == null) return const SizedBox();
        return Scaffold(
          appBar: AppBar(title: const Text('Profilim')),
          body: ListView(
            children: [
              // Profil header
              Container(
                padding: const EdgeInsets.all(24),
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft, end: Alignment.bottomRight,
                    colors: [AppColors.primary, AppColors.primaryDark],
                  ),
                ),
                child: Column(
                  children: [
                    // Avatar
                    Container(
                      width: 80, height: 80,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.white.withOpacity(0.2),
                        border: Border.all(color: AppColors.gold, width: 3),
                      ),
                      child: Center(
                        child: Text(
                          _initials(user.adSoyad),
                          style: const TextStyle(color: Colors.white,
                              fontSize: 28, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(user.adSoyad,
                        style: const TextStyle(color: Colors.white,
                            fontSize: 20, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 4),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(
                        color: AppColors.gold.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        _rolAdi(user.role),
                        style: const TextStyle(color: AppColors.gold, fontSize: 12,
                            fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),

              // Bilgiler
              const _SectionHeader('Hesap Bilgileri'),
              _InfoTile(icon: Icons.person, label: 'Ad Soyad', value: user.adSoyad),
              _InfoTile(icon: Icons.badge, label: 'Rol', value: _rolAdi(user.role)),
              _InfoTile(icon: Icons.fingerprint, label: 'ID', value: user.username),

              const _SectionHeader('Tercihler'),
              ListTile(
                leading: Icon(
                  themeMode == ThemeMode.dark ? Icons.dark_mode : Icons.light_mode,
                  color: AppColors.primary,
                ),
                title: const Text('Tema'),
                subtitle: Text(_temaAdi(themeMode)),
                trailing: IconButton(
                  icon: const Icon(Icons.swap_horiz),
                  onPressed: () => ref.read(themeModeProvider.notifier).cycle(),
                ),
              ),
              ListTile(
                leading: const Icon(Icons.notifications, color: AppColors.gold),
                title: const Text('Bildirimler'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => context.push('/bildirimler'),
              ),
              ListTile(
                leading: const Icon(Icons.settings, color: AppColors.info),
                title: const Text('Ayarlar'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => context.push('/ayarlar'),
              ),
              ListTile(
                leading: const Icon(Icons.lock_outline, color: AppColors.warning),
                title: const Text('Sifre Degistir'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showChangePasswordDialog(context, ref),
              ),

              const _SectionHeader('Uygulama'),
              ListTile(
                leading: const Icon(Icons.info_outline, color: AppColors.textSecondaryDark),
                title: const Text('SmartCampus AI'),
                subtitle: const Text('v22 · 75+ sayfa · 5 rol'),
              ),
              const SizedBox(height: 16),

              // Cikis
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: OutlinedButton.icon(
                  onPressed: () async {
                    await ref.read(authServiceProvider).logout();
                    if (context.mounted) context.go('/login');
                  },
                  icon: const Icon(Icons.logout, color: AppColors.danger),
                  label: const Text('Cikis Yap',
                      style: TextStyle(color: AppColors.danger)),
                  style: OutlinedButton.styleFrom(
                    side: const BorderSide(color: AppColors.danger),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                  ),
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        );
      },
      loading: () => const Scaffold(body: Center(child: CircularProgressIndicator())),
      error: (e, _) => Scaffold(body: Center(child: Text('Hata: $e'))),
    );
  }

  String _initials(String name) {
    final parts = name.split(' ');
    if (parts.length >= 2) return '${parts[0][0]}${parts[1][0]}';
    return name.isNotEmpty ? name[0] : '?';
  }

  String _rolAdi(String role) {
    switch (role.toLowerCase()) {
      case 'ogrenci': return 'Ogrenci';
      case 'veli': return 'Veli';
      case 'ogretmen': return 'Ogretmen';
      case 'rehber': return 'Rehber';
      case 'yonetici': return 'Yonetici';
      default: return role;
    }
  }

  String _temaAdi(ThemeMode m) {
    switch (m) {
      case ThemeMode.light: return 'Aydinlik';
      case ThemeMode.dark: return 'Karanlik';
      case ThemeMode.system: return 'Sistem';
    }
  }
}


void _showChangePasswordDialog(BuildContext context, WidgetRef ref) {
  final eskiCtrl = TextEditingController();
  final yeniCtrl = TextEditingController();
  final tekrarCtrl = TextEditingController();

  showDialog(
    context: context,
    builder: (ctx) {
      String? errorMsg;
      bool loading = false;

      return StatefulBuilder(
        builder: (ctx, setDialogState) {
          return AlertDialog(
            title: const Text('Sifre Degistir'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  TextField(
                    controller: eskiCtrl,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Eski Sifre',
                      prefixIcon: Icon(Icons.lock_outline),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: yeniCtrl,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Yeni Sifre',
                      prefixIcon: Icon(Icons.lock_rounded),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: tekrarCtrl,
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Yeni Sifre (Tekrar)',
                      prefixIcon: Icon(Icons.lock_rounded),
                    ),
                  ),
                  if (errorMsg != null) ...[
                    const SizedBox(height: 12),
                    Text(errorMsg!, style: const TextStyle(color: Colors.red, fontSize: 13)),
                  ],
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('Iptal'),
              ),
              ElevatedButton(
                onPressed: loading
                    ? null
                    : () async {
                        if (yeniCtrl.text != tekrarCtrl.text) {
                          setDialogState(() => errorMsg = 'Yeni sifreler uyusmuyor');
                          return;
                        }
                        if (yeniCtrl.text.length < 4) {
                          setDialogState(() => errorMsg = 'Sifre en az 4 karakter olmali');
                          return;
                        }
                        setDialogState(() {
                          loading = true;
                          errorMsg = null;
                        });
                        try {
                          final api = ref.read(apiClientProvider);
                          await api.post('/auth/change-password', data: {
                            'old_password': eskiCtrl.text,
                            'new_password': yeniCtrl.text,
                          });
                          if (ctx.mounted) {
                            Navigator.pop(ctx);
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Sifre basariyla degistirildi')),
                            );
                          }
                        } catch (e) {
                          setDialogState(() {
                            loading = false;
                            errorMsg = 'Sifre degistirilemedi. Eski sifrenizi kontrol edin.';
                          });
                        }
                      },
                child: loading
                    ? const SizedBox(
                        width: 18, height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Degistir'),
              ),
            ],
          );
        },
      );
    },
  );
}


class _SectionHeader extends StatelessWidget {
  final String title;
  const _SectionHeader(this.title);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
      child: Text(title,
          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700,
              color: AppColors.textSecondaryDark, letterSpacing: 0.5)),
    );
  }
}


class _InfoTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  const _InfoTile({required this.icon, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: AppColors.primary),
      title: Text(label, style: const TextStyle(fontSize: 13, color: AppColors.textSecondaryDark)),
      subtitle: Text(value, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w500)),
    );
  }
}
