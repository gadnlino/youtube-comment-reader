## 1. Centralized theme module

- [x] 1.1 Create `theme_tokens.dart` with all raw light/dark palette values (scaffold, foreground, accent, button variants, divider, muted text)
- [x] 1.2 Create `app_theme_extension.dart` with semantic tokens (accent, favorited, button colors, muted text, placeholder overlay) derived from tokens
- [x] 1.3 Create `app_theme_context.dart` with `BuildContext` extension shortcuts (e.g., `context.appTheme`, `context.appColors`)
- [x] 1.4 Define shared Poppins `textTheme` scale in `app_theme.dart` mapping current sizes (labelSmall 10, bodySmall 12, bodyMedium 13–14, titleMedium 15–16, titleLarge 20, headlineSmall 25)
- [x] 1.5 Build `appDarkTheme` and `appLightTheme` from tokens — configure `ColorScheme`, scaffold, app bar, bottom nav, divider, and text themes
- [x] 1.6 Remove exported `appBackgroungColorDarkTheme`; keep it internal to the themes module only

## 2. Theme controller and app wiring

- [x] 2.1 Create `ThemeController` (GetX) with `themeMode`, `setThemeMode()`, and `loadSavedTheme()` using `CachePackage` key `"theme_mode"`
- [x] 2.2 Register `ThemeController` in `main.dart`, await `loadSavedTheme()` before `runApp`
- [x] 2.3 Wrap `GetMaterialApp` with reactive binding: pass `theme`, `darkTheme`, and `themeMode` from the controller

## 3. Refactor shared components (colors + typography)

- [x] 3.1 Update `custom_bottom_navigation_bar.dart` — theme colors from `bottomNavigationBarTheme` / extension; no direct token imports
- [x] 3.2 Update `custom_divider.dart` — use `Theme.of(context).dividerColor`
- [x] 3.3 Update `comment_widget.dart` — replace hardcoded colors with theme/extension; replace inline font sizes with `textTheme` styles
- [x] 3.4 Update `video_widget.dart` — replace hardcoded colors and font sizes with theme/extension styles
- [x] 3.5 Update `custom_button.dart` — button colors from `AppThemeExtension`; label style from `textTheme.titleLarge` (no inline `fontFamily`/`fontSize`)
- [x] 3.6 Update `custom_cached_network_image.dart` — placeholder color from theme extension

## 4. Refactor pages (colors + typography)

- [x] 4.1 Update `video_search_page.dart` — theme colors for icons/text; `colorScheme.error` for error text; extend existing `textTheme` usage
- [x] 4.2 Update `video_comments_page.dart` — replace all hardcoded white/white70/white60 colors and inline font sizes with theme styles
- [x] 4.3 Update `favorites_page.dart` — replace hardcoded colors, TabBar colors, and font sizes with theme/extension styles

## 5. Theme mode UI

- [x] 5.1 Add a shared theme-mode control (app bar brightness icon + popup menu for Light / Dark / System)
- [x] 5.2 Integrate the control on search, comments, and favorites pages (or via shared app bar helper)
- [x] 5.3 Visually indicate the currently selected theme mode in the menu

## 6. Verification

- [x] 6.1 Grep outside `themes/` for `Color(0x`, `Colors.white`, `Colors.black`, `appBackgroungColorDarkTheme`, `fontSize:`, and `fontFamily:`; fix any stragglers
- [ ] 6.2 Manual smoke test: light, dark, and system modes on search, comments, and favorites flows
- [x] 6.3 Verify theme preference persists after app restart
- [x] 6.4 Confirm a palette change in `theme_tokens.dart` propagates without widget edits (spot-check one token)
- [x] 6.5 Confirm a typography change in `app_theme.dart` propagates without widget edits (spot-check one text style)
- [x] 6.6 Update integration test in `complete_all_features_test.dart` to use new theme exports (`appDarkTheme` / both themes)
