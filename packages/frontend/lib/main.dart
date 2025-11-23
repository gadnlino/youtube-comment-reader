import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:frontend/app/common/controllers/common/bottom_navigation_bar_controller.dart';
import 'package:frontend/app/common/controllers/common/favorites_controller.dart';
import 'package:frontend/app/common/themes/app_theme.dart';
import 'package:frontend/app/pages/favorites_page/favorites_page.dart';
import 'package:frontend/app/pages/video_comments_page/video_comments_page.dart';
import 'package:frontend/app/pages/video_search_page/video_search_page.dart';
import 'package:get/get.dart';

Future main() async {
  //https://stackoverflow.com/questions/61124989/error-google-fonts-was-unable-to-load-font
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load(fileName: ".env");

  // Wait a bit to ensure Flutter engine is fully ready
  await Future.delayed(const Duration(milliseconds: 100));

  // Initialize Firebase using default initialization (reads from google-services.json)
  // This is the recommended approach when using the Google Services plugin
  try {
    await Firebase.initializeApp();
    debugPrint("✅ Firebase initialized successfully");
  } catch (e) {
    // If default initialization fails, fall back to manual initialization
    debugPrint("Default Firebase initialization failed: $e");
    debugPrint("Attempting manual initialization with .env values...");
    try {
      await Firebase.initializeApp(
        options: FirebaseOptions(
          apiKey: dotenv.get("FIREBASE_API_KEY"),
          appId: dotenv.get("FIREBASE_APP_ID"),
          messagingSenderId: dotenv.get("FIREBASE_MESSAGE_SENDER_ID"),
          projectId: dotenv.get("FIREBASE_PROJECT_ID"),
          storageBucket: "${dotenv.get("FIREBASE_PROJECT_ID")}.appspot.com",
        ),
      );
      debugPrint("✅ Firebase initialized manually");
    } catch (e2) {
      debugPrint("❌ Manual Firebase initialization also failed: $e2");
      // Don't rethrow - allow app to continue without Firebase for now
      // This will help identify if Firebase is actually needed at startup
      debugPrint("⚠️  Continuing without Firebase initialization");
    }
  }

  // injecting global controllers, in dependency order
  Get.put(BottomNavigationBarController(), permanent: true);
  Get.put(FavoritesController());

  runApp(GetMaterialApp(
    theme: appThemeData,
    initialRoute: '/',
    getPages: [
      GetPage(
        name: '/',
        page: () => VideoSearchPage(),
        binding: VideoSearchPageBinding(),
      ),
      GetPage(
        name: videoCommentsPageRoute,
        page: () => VideoCommentsPage(),
        binding: VideoCommentsPageBinding(),
      ),
      GetPage(
        name: favoritesPageRoute,
        page: () => FavoritesPage(),
        binding: FavoritesPageBinding(),
      ),
    ],
  ));
}
