/// Integration Test Driver
///
/// This file is required to run integration tests on physical devices or emulators.
/// It enables the test runner to communicate with the app during testing.
///
/// Usage:
///   flutter drive \
///     --driver=test_driver/integration_test.dart \
///     --target=integration_test/app_test.dart
library;

import 'package:integration_test/integration_test_driver.dart';

Future<void> main() => integrationDriver();

