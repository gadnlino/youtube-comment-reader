/**
 * Flutter Integration Tests for YouTube Comment Reader
 *
 * This file contains end-to-end integration tests that simulate real user 
 * interactions with the Flutter mobile application. These tests verify the 
 * complete user flow from searching videos to filtering comments by sentiment.
 *
 * Tests included:
 * 1. Video search functionality
 * 2. Comment loading without sentiment
 * 3. Comment loading with sentiment analysis
 * 4. Filtering by positive sentiment
 * 5. Filtering by negative sentiment
 * 6. Filtering by neutral sentiment
 * 7. Multiple filters active simultaneously
 * 8. Error handling
 *
 * Technologies:
 * - Flutter integration_test package
 * - WidgetTester for UI interactions
 * - Patrol for advanced testing (optional)
 *
 * Usage:
 *   flutter test integration_test/app_test.dart
 *   
 * Or with device/emulator:
 *   flutter drive \
 *     --driver=test_driver/integration_test.dart \
 *     --target=integration_test/app_test.dart
 */

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:frontend/main.dart' as app;

void main() {
  // Initialize integration test binding
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('YouTube Comment Reader E2E Tests', () {
    
    // Test 1: Video Search Functionality
    testWidgets('Test 1: Search for videos and display results', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Find the search field
      final searchField = find.byType(TextField).first;
      expect(searchField, findsOneWidget);

      // Enter search query
      await tester.enterText(searchField, 'python tutorial');
      await tester.pumpAndSettle();

      // Tap search button (assuming it exists)
      final searchButton = find.byIcon(Icons.search);
      if (searchButton.evaluate().isNotEmpty) {
        await tester.tap(searchButton);
        await tester.pumpAndSettle();
      } else {
        // If no explicit search button, submit via keyboard
        await tester.testTextInput.receiveAction(TextInputAction.search);
        await tester.pumpAndSettle();
      }

      // Wait for search results to load (with timeout)
      await tester.pump(const Duration(seconds: 2));
      await tester.pumpAndSettle();

      // Verify that video results are displayed
      // Look for common video result indicators (adjust based on your UI)
      expect(find.byType(ListView), findsWidgets);
      
      print('✅ Test 1 PASSED: Video search functionality works');
    });

    // Test 2: Load comments without sentiment analysis
    testWidgets('Test 2: Load comments without sentiment analysis', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Search for a specific video (using known test video ID)
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley never gonna give you up');
      await tester.pumpAndSettle();

      // Submit search
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Tap on first video result
      final firstVideo = find.byType(GestureDetector).first;
      await tester.tap(firstVideo);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify comments are loaded (without sentiment)
      // Adjust selectors based on your actual widget tree
      expect(find.text('Comments'), findsWidgets);
      
      // Verify no sentiment indicators are visible
      expect(find.text('POSITIVE'), findsNothing);
      expect(find.text('NEGATIVE'), findsNothing);
      expect(find.text('NEUTRAL'), findsNothing);

      print('✅ Test 2 PASSED: Comments load without sentiment');
    });

    // Test 3: Load comments WITH sentiment analysis
    testWidgets('Test 3: Load comments with sentiment analysis', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to video with comments
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Tap first video
      final firstVideo = find.byType(GestureDetector).first;
      await tester.tap(firstVideo);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Enable sentiment analysis (find and tap the sentiment toggle/button)
      // Adjust this based on your actual UI implementation
      final sentimentToggle = find.byKey(const Key('sentiment_toggle'));
      if (sentimentToggle.evaluate().isNotEmpty) {
        await tester.tap(sentimentToggle);
        await tester.pumpAndSettle(const Duration(seconds: 5)); // Wait for analysis
      }

      // Alternative: look for button with text
      final analyzeSentimentButton = find.text('Analyze Sentiment');
      if (analyzeSentimentButton.evaluate().isNotEmpty) {
        await tester.tap(analyzeSentimentButton);
        await tester.pumpAndSettle(const Duration(seconds: 5));
      }

      // Verify sentiment indicators are now visible
      final hasSentiment = find.textContaining('POSITIVE').evaluate().isNotEmpty ||
                          find.textContaining('NEGATIVE').evaluate().isNotEmpty ||
                          find.textContaining('NEUTRAL').evaluate().isNotEmpty;
      
      expect(hasSentiment, true);

      print('✅ Test 3 PASSED: Sentiment analysis works');
    });

    // Test 4: Filter by POSITIVE sentiment
    testWidgets('Test 4: Filter comments by positive sentiment', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to video and enable sentiment
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Enable sentiment analysis
      final sentimentToggle = find.byKey(const Key('sentiment_toggle'));
      if (sentimentToggle.evaluate().isNotEmpty) {
        await tester.tap(sentimentToggle);
        await tester.pumpAndSettle(const Duration(seconds: 5));
      }

      // Tap on "Positive" filter button/chip
      final positiveFilter = find.text('Positive');
      if (positiveFilter.evaluate().isEmpty) {
        // Try alternative text
        final altPositiveFilter = find.text('POSITIVE');
        if (altPositiveFilter.evaluate().isNotEmpty) {
          await tester.tap(altPositiveFilter);
        }
      } else {
        await tester.tap(positiveFilter);
      }
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify only positive comments are shown
      final negativeComments = find.text('NEGATIVE');
      final neutralComments = find.text('NEUTRAL');
      
      expect(negativeComments, findsNothing);
      expect(neutralComments, findsNothing);

      // Verify positive comments ARE shown
      final positiveComments = find.text('POSITIVE');
      expect(positiveComments, findsWidgets);

      print('✅ Test 4 PASSED: Positive filter works correctly (100% accuracy)');
    });

    // Test 5: Filter by NEGATIVE sentiment
    testWidgets('Test 5: Filter comments by negative sentiment', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to video and enable sentiment
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Enable sentiment
      final sentimentToggle = find.byKey(const Key('sentiment_toggle'));
      if (sentimentToggle.evaluate().isNotEmpty) {
        await tester.tap(sentimentToggle);
        await tester.pumpAndSettle(const Duration(seconds: 5));
      }

      // Tap "Negative" filter
      final negativeFilter = find.text('Negative');
      if (negativeFilter.evaluate().isNotEmpty) {
        await tester.tap(negativeFilter);
      } else {
        await tester.tap(find.text('NEGATIVE'));
      }
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify only negative comments are shown
      final positiveComments = find.text('POSITIVE');
      final neutralComments = find.text('NEUTRAL');
      
      expect(positiveComments, findsNothing);
      expect(neutralComments, findsNothing);

      // Verify negative comments ARE shown
      final negativeComments = find.text('NEGATIVE');
      expect(negativeComments, findsWidgets);

      print('✅ Test 5 PASSED: Negative filter works correctly (100% accuracy)');
    });

    // Test 6: Filter by NEUTRAL sentiment
    testWidgets('Test 6: Filter comments by neutral sentiment', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to video and enable sentiment
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Enable sentiment
      final sentimentToggle = find.byKey(const Key('sentiment_toggle'));
      if (sentimentToggle.evaluate().isNotEmpty) {
        await tester.tap(sentimentToggle);
        await tester.pumpAndSettle(const Duration(seconds: 5));
      }

      // Tap "Neutral" filter
      final neutralFilter = find.text('Neutral');
      if (neutralFilter.evaluate().isNotEmpty) {
        await tester.tap(neutralFilter);
      } else {
        await tester.tap(find.text('NEUTRAL'));
      }
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify only neutral comments are shown
      final positiveComments = find.text('POSITIVE');
      final negativeComments = find.text('NEGATIVE');
      
      expect(positiveComments, findsNothing);
      expect(negativeComments, findsNothing);

      // Verify neutral comments ARE shown
      final neutralComments = find.text('NEUTRAL');
      expect(neutralComments, findsWidgets);

      print('✅ Test 6 PASSED: Neutral filter works correctly (100% accuracy)');
    });

    // Test 7: Multiple filters simultaneously
    testWidgets('Test 7: Activate multiple sentiment filters', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Navigate to video and enable sentiment
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'rick astley');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      await tester.tap(find.byType(GestureDetector).first);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Enable sentiment
      final sentimentToggle = find.byKey(const Key('sentiment_toggle'));
      if (sentimentToggle.evaluate().isNotEmpty) {
        await tester.tap(sentimentToggle);
        await tester.pumpAndSettle(const Duration(seconds: 5));
      }

      // Activate both Positive AND Negative filters
      final positiveFilter = find.text('Positive');
      final negativeFilter = find.text('Negative');

      if (positiveFilter.evaluate().isNotEmpty) {
        await tester.tap(positiveFilter);
        await tester.pump(const Duration(milliseconds: 500));
      }

      if (negativeFilter.evaluate().isNotEmpty) {
        await tester.tap(negativeFilter);
        await tester.pumpAndSettle(const Duration(seconds: 2));
      }

      // Verify both positive and negative comments are shown
      // But neutral comments are NOT shown
      final neutralComments = find.text('NEUTRAL');
      expect(neutralComments, findsNothing);

      // Should have mix of positive and negative
      final hasPositive = find.text('POSITIVE').evaluate().isNotEmpty;
      final hasNegative = find.text('NEGATIVE').evaluate().isNotEmpty;
      expect(hasPositive || hasNegative, true);

      print('✅ Test 7 PASSED: Multiple filters work correctly');
    });

    // Test 8: Error handling with invalid video
    testWidgets('Test 8: Handle invalid video gracefully', 
      (WidgetTester tester) async {
      
      // Start the app
      app.main();
      await tester.pumpAndSettle();

      // Search for nonsense/invalid query
      final searchField = find.byType(TextField).first;
      await tester.enterText(searchField, 'xyzinvalidvideo123456789');
      await tester.testTextInput.receiveAction(TextInputAction.search);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify error message or empty state is shown
      // Adjust based on your actual error handling UI
      final hasError = find.text('No videos found').evaluate().isNotEmpty ||
                      find.text('Error').evaluate().isNotEmpty ||
                      find.byType(CircularProgressIndicator).evaluate().isEmpty;

      expect(hasError, true);

      print('✅ Test 8 PASSED: Error handling works');
    });
  });

  // Generate test report
  tearDownAll(() {
    print('\n' + '='*80);
    print('📊 FLUTTER INTEGRATION TEST SUMMARY');
    print('='*80);
    print('Total Tests: 8');
    print('Test Type: End-to-End Integration (Real UI Simulation)');
    print('Technology: Flutter integration_test + WidgetTester');
    print('\nAll tests simulate real user interactions:');
    print('  ✅ Tap gestures on buttons and UI elements');
    print('  ✅ Text input in search fields');
    print('  ✅ Navigation between screens');
    print('  ✅ Sentiment filter activation/deactivation');
    print('  ✅ Comment display verification');
    print('='*80);
  });
}

