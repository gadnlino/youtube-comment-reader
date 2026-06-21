## Why

The Flutter frontend currently ships with a single dark theme and hardcoded light-on-dark colors across pages and components. Users who prefer light backgrounds or who use the app in bright environments have no alternative, and the app does not respect the system appearance setting. Adding light mode improves accessibility, user comfort, and platform-native feel.

## What Changes

- Define a light `ThemeData` alongside the existing dark theme, with consistent brand colors (orange primary, yellow accent).
- Introduce theme mode selection: light, dark, and system default.
- Persist the user's theme preference across app restarts.
- Replace hardcoded `Colors.white`, `Colors.black`, and `appBackgroungColorDarkTheme` usages in widgets with theme-aware colors from `Theme.of(context)` or `ColorScheme`.
- Centralize the palette in `theme_tokens.dart` and semantic tokens in `AppThemeExtension` so future brand color changes require editing one file.
- Centralize typography in `ThemeData.textTheme` (Poppins via Google Fonts) so widgets stop hardcoding `fontSize` and `fontFamily`.
- Reorganize `lib/app/common/themes/` as the single theming layer (`theme_tokens.dart`, `app_theme_extension.dart`, `app_theme.dart`, optional `app_theme_context.dart`).
- Wire `GetMaterialApp` with both `theme` and `darkTheme`, driven by a theme controller.
- Add a UI control (settings entry or in-app toggle) for switching theme mode.

## Capabilities

### New Capabilities

- `app-theming`: Centralized theme layer (palette tokens, typography scale, light/dark `ThemeData`, semantic extensions) and theme-aware styling conventions for the Flutter frontend.
- `theme-preference`: User-selectable theme mode (light / dark / system) with persistence and application at startup.

### Modified Capabilities

<!-- No existing specs in openspec/specs/ -->

## Impact

- **Frontend package** (`packages/frontend/`): new `themes/` module files, `main.dart`, and ~10 widget/page files with hardcoded colors and typography.
- **New dependency**: `shared_preferences` (or existing storage if already present) for persisting theme mode.
- **GetX**: New `ThemeController` registered globally alongside existing controllers.
- **Tests**: Integration/widget tests may need theme-aware assertions or explicit theme wrapping.
- **No backend or API changes.**
