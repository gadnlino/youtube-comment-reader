#!/bin/bash

# Flutter Integration Test Runner
# This script helps run the E2E integration tests for the mobile app

set -e  # Exit on error

echo "========================================"
echo "Flutter Integration Test Runner"
echo "========================================"
echo ""

# Check if Flutter is installed
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter is not installed or not in PATH"
    exit 1
fi

echo "✅ Flutter found: $(flutter --version | head -n 1)"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"
echo "📂 Working directory: $(pwd)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
flutter pub get
echo ""

# Check for connected devices
echo "📱 Checking for devices..."
DEVICES=$(flutter devices)
echo "$DEVICES"
echo ""

# Ask user which type of test to run
echo "Select test type:"
echo "1) Quick test (no device - logic only)"
echo "2) Full E2E test (requires device/emulator)"
echo "3) List devices only"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running quick tests (no device)..."
        echo ""
        flutter test integration_test/app_test.dart
        ;;
    2)
        echo ""
        echo "🧪 Running full E2E tests with device..."
        echo ""
        flutter drive \
            --driver=test_driver/integration_test.dart \
            --target=integration_test/app_test.dart
        ;;
    3)
        echo ""
        echo "📱 Available devices:"
        flutter devices
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "✅ Tests completed!"
echo "========================================"

