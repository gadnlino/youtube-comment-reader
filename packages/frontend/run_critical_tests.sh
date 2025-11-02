#!/bin/bash

# Critical User Flows Test Runner
# Runs only the essential E2E tests for the Flutter app

echo "======================================================================"
echo "🧪 Running Critical User Flows E2E Tests"
echo "======================================================================"
echo ""
echo "This will test:"
echo "  1. View video list"
echo "  2. Search videos by keyword"
echo "  3. Sort videos by date"
echo "  4. Favorite/unfavorite videos"
echo "  5. View comments"
echo "  6. Filter comments by sentiment"
echo "  7. Navigate to favorites tab"
echo ""
echo "Estimated duration: ~2 minutes"
echo ""
echo "======================================================================"
echo ""

# Set Flutter path
export PATH="/Users/guiavenas/development/flutter/bin:$PATH"

# Navigate to frontend directory
cd /Users/guiavenas/source/repos/youtube-comment-reader/packages/frontend

# Check if emulator is running
if ! adb devices | grep -q "emulator"; then
    echo "⚠️  No Android emulator detected!"
    echo "Please start an emulator first:"
    echo "  flutter emulators"
    echo "  flutter emulators --launch <emulator_id>"
    exit 1
fi

echo "✅ Emulator detected"
echo ""

# Run the test
echo "Starting test execution..."
echo ""

flutter drive \
  --driver=test_driver/integration_test.dart \
  --target=integration_test/critical_user_flows_test.dart \
  --flavor dev \
  -d $(adb devices | grep emulator | awk '{print $1}') \
  2>&1 | tee test_output.log

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "✅ ALL TESTS PASSED!"
    echo "======================================================================"
else
    echo ""
    echo "======================================================================"
    echo "❌ SOME TESTS FAILED - Check test_output.log for details"
    echo "======================================================================"
fi

echo ""
echo "📄 Full log saved to: test_output.log"
echo ""

