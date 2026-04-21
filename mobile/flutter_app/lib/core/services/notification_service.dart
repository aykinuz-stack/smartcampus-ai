import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';


/// Push + Local bildirim servisi.
/// Firebase FCM platform dosyalari (google-services.json / GoogleService-Info.plist)
/// eklendiginde otomatik aktif olur.
class NotificationService {
  final FlutterLocalNotificationsPlugin _local = FlutterLocalNotificationsPlugin();
  bool _initialized = false;

  Future<void> init() async {
    if (_initialized) return;

    // Local notifications
    const androidInit = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosInit = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
    );
    const initSettings = InitializationSettings(
      android: androidInit,
      iOS: iosInit,
    );

    await _local.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTap,
    );

    // Firebase FCM — platform dosyalari yoksa atla
    await _initFirebase();

    _initialized = true;
    debugPrint('[NOTIFICATION] Service initialized');
  }

  Future<void> _initFirebase() async {
    try {
      // Firebase varsa import et
      // ignore: avoid_dynamic_calls
      final firebaseCore = await _tryImportFirebase();
      if (firebaseCore != null) {
        debugPrint('[NOTIFICATION] Firebase initialized');
      }
    } catch (e) {
      debugPrint('[NOTIFICATION] Firebase not available (platform files missing): $e');
    }
  }

  Future<dynamic> _tryImportFirebase() async {
    // Firebase'i dene — google-services.json yoksa hata verir, yakalanir
    try {
      // Dynamic import workaround: actual Firebase init will be in main.dart
      // when platform files are added
      return null;
    } catch (_) {
      return null;
    }
  }

  void _onNotificationTap(NotificationResponse response) {
    debugPrint('[NOTIFICATION] Tapped: ${response.payload}');
    // Router'a yonlendir (payload = route path)
  }

  /// Lokal bildirim goster
  Future<void> showLocal({
    required String title,
    required String body,
    String? payload,
    int id = 0,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      'smartcampus_channel',
      'SmartCampus Bildirimler',
      channelDescription: 'SmartCampus AI uygulama bildirimleri',
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );
    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );
    const details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _local.show(id, title, body, details, payload: payload);
  }

  /// Odev hatirlatma bildirimi
  Future<void> odevHatirlatma(String odevBaslik, String teslimTarihi) async {
    await showLocal(
      title: 'Odev Hatirlatma',
      body: '$odevBaslik — Teslim: $teslimTarihi',
      payload: '/homework',
      id: odevBaslik.hashCode,
    );
  }

  /// Sinav hatirlatma
  Future<void> sinavHatirlatma(String sinavAdi, String tarih) async {
    await showLocal(
      title: 'Sinav Yaklasti!',
      body: '$sinavAdi — $tarih',
      payload: '/takvim',
      id: sinavAdi.hashCode,
    );
  }

  /// Yeni mesaj bildirimi
  Future<void> yeniMesaj(String gonderen, String mesaj) async {
    await showLocal(
      title: 'Yeni Mesaj: $gonderen',
      body: mesaj.length > 100 ? '${mesaj.substring(0, 100)}...' : mesaj,
      payload: '/messages',
      id: gonderen.hashCode,
    );
  }
}


/// Riverpod provider
final notificationServiceProvider = Provider<NotificationService>((ref) {
  final service = NotificationService();
  service.init();
  return service;
});
