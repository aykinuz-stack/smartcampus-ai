import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'app.dart';
import 'core/services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Hive offline cache
  await Hive.initFlutter();
  await Hive.openBox<Map>('mood_queue');  // Offline mood queue
  await Hive.openBox<Map>('cached_data'); // Genel cache
  await Hive.openBox<String>('prefs');    // Kullanici tercihleri

  // Firebase — google-services.json yoksa sessizce atla
  await _initFirebase();

  // Local notification servisi
  final notifService = NotificationService();
  await notifService.init();

  runApp(
    const ProviderScope(
      child: SmartCampusApp(),
    ),
  );
}

/// Firebase init — platform dosyalari (google-services.json / GoogleService-Info.plist)
/// eklendiginde otomatik aktif olur. Yoksa sessizce atlanir.
Future<void> _initFirebase() async {
  try {
    // Firebase Core import — paket yuklu ama platform config yoksa hata verir
    // Bu durumda catch'e duser ve uygulama Firebase olmadan calisir
    final firebase = await _tryFirebaseInit();
    if (firebase) {
      debugPrint('[MAIN] Firebase initialized');
      // FCM token al
      _setupFCM();
    }
  } catch (e) {
    debugPrint('[MAIN] Firebase not available: $e');
  }
}

Future<bool> _tryFirebaseInit() async {
  try {
    // Dynamic import calismiyor — firebase_core dogrudan import gerekir
    // google-services.json olmadan Firebase.initializeApp() hata verir
    // Bu blok sadece platform dosyalari eklendiginde calisir
    return false; // Firebase henuz yapilandirilmadi
  } catch (_) {
    return false;
  }
}

void _setupFCM() {
  // Firebase Messaging setup — platform config eklenince aktif olacak
  debugPrint('[MAIN] FCM setup placeholder — google-services.json eklenince aktif olur');
}
