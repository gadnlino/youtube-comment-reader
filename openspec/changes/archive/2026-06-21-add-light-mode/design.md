## Context

The YouTube Comment Reader frontend is a Flutter app using GetX for state management. It currently defines a single dark `ThemeData` in `app_theme.dart` and applies it via `GetMaterialApp(theme: appThemeData)`. Dozens of widgets hardcode `Colors.white`, `Colors.black`, and `appBackgroungColorDarkTheme` for text, icons, and surfaces. Typography is similarly scattered: widgets inline `fontSize: 10/12/15/20/25` and `fontFamily: "Poppins"` instead of using `textTheme`.

`shared_preferences` is already a dependency and wrapped by `CachePackage` for string key-value storage.

## Goals / Non-Goals

**Goals:**

- Ship a polished light theme that mirrors the dark theme's brand identity.
- Support Light / Dark / System theme modes with persisted preference.
- **Centralize palette** — all raw hex values in `theme_tokens.dart`; widgets read colors only via `Theme.of(context)` / `AppThemeExtension`.
- **Centralize typography** — define a Poppins-based text scale in `ThemeData.textTheme`; widgets use named styles instead of inline `fontSize` / `fontFamily`.
- Refactor hardcoded colors and typography with minimal visual regression in dark mode.
- Use existing GetX patterns for a global reactive theme controller.

**Non-Goals:**

- Per-screen custom themes or user-defined color pickers.
- Theming the backend, web admin, or non-Flutter packages.
- Redesigning layout or component structure beyond color/theming/typography.
- Android/iOS native splash or status-bar per-theme polish (can follow up separately).

## Decisions

### 1. Centralized theme module layout

**Choice:** Reorganize `lib/app/common/themes/` as:

```
themes/
├── theme_tokens.dart          # Raw light/dark palette (single edit surface for brand colors)
├── app_theme_extension.dart   # Semantic tokens (accent, favorited, button variants)
├── app_theme.dart             # Builds appLightTheme + appDarkTheme from tokens
└── app_theme_context.dart     # BuildContext extension shortcuts (optional, recommended)
```

**Rationale:** Separates raw palette from Material wiring from widget ergonomics. Changing brand yellow = edit `theme_tokens.dart` only. Changing how yellow maps to nav selection = edit `app_theme.dart` only.

**Alternatives considered:**
- Everything in one `app_theme.dart` — rejected; palette and ThemeData construction become tangled.
- Constants scattered in widgets with extension — rejected; doesn't achieve "one place" for palette.

### 2. Dual `ThemeData` + `themeMode` on `GetMaterialApp`

**Choice:** Define `appLightTheme` and `appDarkTheme` (rename current `appThemeData` → `appDarkTheme`), pass both to `GetMaterialApp` along with `themeMode` from a controller.

**Rationale:** Standard Flutter pattern; `ThemeMode.system` delegates to `MediaQuery.platformBrightnessOf(context)`.

**Alternatives considered:**
- Single `ThemeData` with manual brightness toggling — rejected; loses Material 3 color-scheme helpers and system integration.
- Third-party theme packages — rejected; unnecessary for two themes.

### 3. `ThemeController` (GetX) owns mode + persistence

**Choice:** New `ThemeController extends GetxController` with `Rx<ThemeMode> themeMode`, methods `setThemeMode(ThemeMode)`, async `loadSavedTheme()` called from `main()` before `runApp`.

**Persistence key:** `"theme_mode"` stored as `"light" | "dark" | "system"` via `CachePackage.putString` / `getString`.

**Rationale:** Matches existing controller pattern (`BottomNavigationBarController`, `FavoritesController`). Reactive `themeMode` drives `GetMaterialApp` rebuild via `Obx` wrapper or `GetBuilder`.

### 4. `theme_tokens.dart` — raw palette

**Choice:** Define light and dark token sets in one file. Example structure:

```dart
abstract class AppColorTokens {
  static const darkScaffold = Color(0xff062029);
  static const lightScaffold = Color(0xffF5F5F5);
  static const accentYellow = Color(0xffFFF50A);
  static const buttonPrimary = Color(0xfffff50a);
  static const buttonSuccess = Color(0xff35A3D2);
  static const buttonCancel = Color(0xffE85B3C);
  // ... foreground, divider, muted text per brightness
}
```

Both `appLightTheme` and `appDarkTheme` import tokens from here. **No widget imports this file directly.**

### 5. `AppThemeExtension` — semantic tokens

**Choice:** Add `AppThemeExtension` with fields derived from tokens: `accentYellow`, `favoritedColor`, `buttonPrimary`, `buttonSuccess`, `buttonCancel`, `mutedText`, `placeholderOverlay`. Register on both themes via `extensions: [...]`.

**Usage via context helper:**
```dart
context.appTheme.accentYellow
// instead of Theme.of(context).extension<AppThemeExtension>()!.accentYellow
```

**Rationale:** Semantic names survive palette renames; widgets never reference hex values.

### 6. Centralized typography scale

**Choice:** Define a full Poppins `textTheme` in `app_theme.dart` using `GoogleFonts.poppinsTextTheme()` as base, then override named styles to match current visual sizes:

| Current inline usage | Maps to `textTheme` style |
|----------------------|---------------------------|
| App bar title (20 bold) | `titleLarge` |
| Section / empty-state headers (25) | `headlineSmall` |
| Video/comment titles (15–16 bold) | `titleMedium` |
| Body / metadata (13–14) | `bodyMedium` |
| Small metadata (12) | `bodySmall` |
| Timestamps (10) | `labelSmall` |
| Button label (20) | `titleLarge` (or dedicated `labelLarge`) |
| Dialog / sheet labels | existing `labelLarge` (already used in 2 pages) |

Both light and dark themes share the same typography scale; only `color` on text styles comes from `ColorScheme.onSurface` / `onSurfaceVariant`.

**Widget rule:** No inline `fontSize`, `fontFamily`, or hardcoded text `color` in pages/components. Use `Theme.of(context).textTheme.<style>` optionally with `.copyWith(fontWeight: ...)` for weight-only overrides.

**Rationale:** Font scale changes (accessibility, rebrand) become a single-file edit. Eliminates duplicate `fontFamily: "Poppins"` in `CustomButton`.

### 7. Light theme color palette

**Choice:**

| Token | Dark (current) | Light (proposed) |
|-------|----------------|------------------|
| Scaffold / chrome bg | `#062029` | `#F5F5F5` |
| Primary text | white | `#1A1A1A` |
| Secondary text | white70 / white60 | `#616161` |
| App bar / bottom nav bg | `#062029` | `#FFFFFF` |
| Divider | white | `#E0E0E0` |
| Selected nav item | `#FFF50A` | `#FFF50A` (unchanged) |
| Unselected nav item | white | `#757575` |

Build light theme with `ColorScheme.fromSeed(seedColor: Colors.orange, brightness: Brightness.light)` then override scaffold, appBar, bottomNavigationBar, divider, and text themes from tokens.

### 8. Widget refactor strategy

**Choice:** Replace hardcoded styling incrementally per file:

**Colors:**
- Text/icons → `colorScheme.onSurface` or `onSurfaceVariant`
- Errors → `colorScheme.error`
- Dividers → `Theme.of(context).dividerColor`
- Bottom nav → `bottomNavigationBarTheme`
- Brand-specific (favorited, buttons) → `context.appTheme.*`
- Remove all imports of `appBackgroungColorDarkTheme` from non-theme files

**Typography:**
- Replace `TextStyle(fontSize: N, color: ...)` → `textTheme.<mappedStyle>`
- Keep `fontWeight` overrides inline where needed; never inline `fontSize` or `fontFamily`

**Rationale:** Minimizes diff size while ensuring light mode works; dark mode uses the same code paths.

### 9. Theme mode UI — app bar popup menu

**Choice:** Add a brightness icon to the app bar on primary pages opening a `PopupMenuButton<ThemeMode>` with Light / Dark / System options.

**Rationale:** No new route required; discoverable and consistent with Material patterns.

## Risks / Trade-offs

- **[Risk] Missed hardcoded colors or font sizes** → Some widgets stay white-on-white or wrong size in light mode. **Mitigation:** Grep for `Colors.white`, `Colors.black`, `appBackgroungColorDarkTheme`, `fontSize:`, and `fontFamily:` outside `themes/` after final pass.

- **[Risk] Flash of wrong theme on cold start** → Preference loads async. **Mitigation:** Await `loadSavedTheme()` in `main()` before `runApp`; default to `ThemeMode.system` if read fails.

- **[Risk] `CustomButton` neutral variant** → Transparent background with `onSurface` text may fail on busy backgrounds. **Mitigation:** Neutral buttons are rare; revisit if reported.

- **[Risk] Typography mapping changes visual rhythm slightly** → Mapping inline sizes to Material text roles may differ by 1px. **Mitigation:** Override `textTheme` sizes explicitly in `app_theme.dart` to match current pixel values exactly.

- **[Trade-off] No dynamic color / Material You** → Fixed palettes only; acceptable for v1.

## Migration Plan

1. Create centralized theme module first (tokens → extension → themes).
2. Refactor components, then pages, then wire controller + UI toggle.
3. Ship in a single frontend release; no data migration (new preference key only).
4. Rollback: revert commit; missing key falls back to System mode.

## Open Questions

- Should the theme toggle live on every page's app bar or only the search page? **Proposed:** all pages that expose an app bar, using a shared helper/widget if duplication appears.
- Should integration tests assert colors/fonts per theme or only widget presence? **Proposed:** wrap tests with explicit `ThemeData` where needed; no pixel/style assertions in v1.
