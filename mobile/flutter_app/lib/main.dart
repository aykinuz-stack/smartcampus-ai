import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';

import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Hive offline cache
  await Hive.initFlutter();
  await Hive.openBox<Map>('mood_queue');  // Offline mood queue
  await Hive.openBox<Map>('cached_data'); // Genel cache
  await Hive.openBox<String>('prefs');    // Kullanici tercihleri

  runApp(
    const ProviderScope(
      child: SmartCampusApp(),
    ),
  );
}
