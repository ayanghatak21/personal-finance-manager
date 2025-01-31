# Personal Finance Manager Mobile App

A cross-platform mobile application for managing personal finances, built with Flutter.

## Prerequisites

### For Android Development
1. Install [Android Studio](https://developer.android.com/studio)
2. Install the Android SDK (via Android Studio)
3. Install Flutter SDK and add it to your PATH
4. Run `flutter doctor` and resolve any issues

### For iOS Development
1. Install [Xcode](https://apps.apple.com/us/app/xcode/id497799835) (Mac only)
2. Install the iOS SDK (via Xcode)
3. Install Flutter SDK and add it to your PATH
4. Install CocoaPods: `sudo gem install cocoapods`
5. Run `flutter doctor` and resolve any issues

## Setup Instructions

1. Clone the repository
2. Navigate to the mobile directory: `cd mobile`
3. Install dependencies: `flutter pub get`

### Android Setup
1. Open Android Studio
2. Go to Tools > SDK Manager
3. Install the Android SDK platform tools
4. Create/setup an Android Virtual Device (AVD) for testing

### iOS Setup (Mac only)
1. Open Xcode and accept the license agreement
2. Install Xcode Command Line Tools
3. Set up an iOS Simulator for testing

## Running the App

### Android
```bash
# Run on an Android device/emulator
flutter run
```

### iOS (Mac only)
```bash
# Run on an iOS Simulator/device
flutter run
```

## Features

- Dashboard overview of finances
- Transaction management
- Financial analytics and charts
- Category-based expense tracking
- Budget planning and tracking (coming soon)
- Recurring transactions (coming soon)
- Data export functionality (coming soon)

## Project Structure

```
lib/
├── main.dart            # App entry point
├── models/             # Data models
├── screens/            # UI screens
├── widgets/           # Reusable widgets
├── services/          # Business logic
└── utils/             # Helper functions
```

## Troubleshooting

### Common Issues

1. "Flutter doctor shows red X's"
   - Follow the specific instructions provided by `flutter doctor -v`
   - Ensure all required SDKs are properly installed

2. "Gradle build fails"
   - Run `flutter clean`
   - Delete the build folder
   - Run `flutter pub get`
   - Try building again

3. "iOS build fails"
   - Run `pod install` in the ios folder
   - Ensure Xcode is up to date
   - Check if CocoaPods is properly installed

For additional help, consult the [Flutter documentation](https://docs.flutter.dev/) or open an issue in the repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request