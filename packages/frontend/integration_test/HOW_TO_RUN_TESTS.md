# Running E2E Tests

## Quick Start

### Run Critical User Flows (Recommended)
The fastest way to validate all core functionality:

```bash
cd /Users/guiavenas/source/repos/youtube-comment-reader/packages/frontend
./run_critical_tests.sh
```

**Duration**: ~2 minutes  
**Coverage**: All 7 critical user flows  
**File**: `integration_test/critical_user_flows_test.dart`

---

## Manual Test Execution

### Prerequisites
1. Start Android emulator:
   ```bash
   flutter emulators
   flutter emulators --launch <emulator_id>
   ```

2. Verify emulator is running:
   ```bash
   adb devices
   ```

### Run Critical User Flows Test
```bash
export PATH="/Users/guiavenas/development/flutter/bin:$PATH"
cd /Users/guiavenas/source/repos/youtube-comment-reader/packages/frontend

flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/critical_user_flows_test.dart \
  --flavor dev \
  -d emulator-5554
```

---

## Current Test Status

### ✅ Working Tests (6/7)
1. View default video list
2. Search videos by keyword
3. Sort videos by date
4. Favorite/unfavorite videos
5. View comments
6. Filter comments by sentiment

### ❌ Known Issue (1/7)
7. Navigate to favorites tab - **Layout bug in FavoritesPage**

**Error**: `Expanded` widget incorrectly placed inside `Semantics` instead of `Flex` parent

**To Fix**: Locate the FavoritesPage widget tree and ensure `Expanded` is a direct child of `Column` or `Row`, not wrapped in other widgets.

---

## After Fixing the Bug

Once you've fixed the FavoritesPage layout bug, simply run:

```bash
./run_critical_tests.sh
```

All 7 tests should pass! ✅

---

## Test Reports

- **Detailed Report**: `integration_test/CRITICAL_USER_FLOWS_TEST_REPORT.md`
- **Test Output**: `test_output.log` (generated after each run)

---

## Other Available Tests

### All Features Test (Comprehensive but slower)
```bash
flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/complete_all_features_test.dart \
  --flavor dev \
  -d emulator-5554
```

**Duration**: ~10-15 minutes (if it doesn't hang)  
**Tests**: 14 comprehensive tests including extended features

⚠️ **Note**: This test suite may experience hanging issues due to `pumpAndSettle()`. The critical flows test is more reliable.

---

## Troubleshooting

### Emulator not detected
```bash
flutter emulators
flutter emulators --launch <emulator_id>
```

### Build errors
```bash
cd android
./gradlew clean
cd ..
flutter pub get
```

### Firebase issues
Make sure `.env` file exists with Firebase credentials:
```
FIREBASE_API_KEY=...
FIREBASE_APP_ID=...
FIREBASE_MESSAGE_SENDER_ID=...
FIREBASE_PROJECT_ID=...
```

### Test hangs
- Use `critical_user_flows_test.dart` (uses `pump()` instead of `pumpAndSettle()`)
- Avoid `complete_all_features_test.dart` if experiencing hangs

---

## Understanding Test Results

### Success Output
```
✅ Flow 1: Viewing default video list...
✅ Found 8 videos
✅ FLOW 1 PASSED

...

🏆 CRITICAL USER FLOWS - TEST RESULTS
All critical user flows validated successfully!
```

### Failure Output
```
❌ Flow 7: Navigate to favorites tab [E]
Test failed. See exception logs above.

Failure in method: Flow 7: Navigate to favorites tab
```

Check the exception details in the output to understand what failed.

---

## Next Steps After All Tests Pass

1. ✅ Commit your bug fix
2. ✅ Run tests one more time to confirm
3. ✅ Update the monograph with final E2E test results
4. ✅ Include screenshots or test reports in your documentation

---

**Created**: November 2, 2025  
**Last Updated**: November 2, 2025

