## ADDED Requirements

### Requirement: Light theme definition

The frontend SHALL provide a light `ThemeData` with readable contrast on light backgrounds, preserving the existing brand palette (orange primary swatch, yellow `#FFF50A` accent for selected navigation and primary actions).

#### Scenario: Light theme scaffold and app bar

- **WHEN** the app is running in light mode
- **THEN** the scaffold background, app bar background, and bottom navigation bar background SHALL use light-surface colors (not the dark `#062029` background)
- **AND** primary text and icons on those surfaces SHALL use dark foreground colors for sufficient contrast

#### Scenario: Dark theme unchanged as default appearance

- **WHEN** the app is running in dark mode
- **THEN** the visual appearance SHALL match the current dark theme (dark teal `#062029` background, white text/icons on chrome surfaces)

### Requirement: Centralized palette tokens

All raw brand and surface colors SHALL be defined in a single `theme_tokens.dart` file. Widgets and pages SHALL NOT import or reference raw hex color constants directly.

#### Scenario: Palette change in one file

- **WHEN** a developer changes a brand color (e.g., accent yellow) in `theme_tokens.dart`
- **THEN** both light and dark themes SHALL reflect the new color without editing individual widget files

#### Scenario: No scattered hex values in widgets

- **WHEN** the implementation is complete
- **THEN** no page or shared component file outside `lib/app/common/themes/` SHALL contain hardcoded `Color(0x...)` values or direct imports of palette constants

### Requirement: Theme-aware component colors

All user-facing screens and shared components SHALL derive text, icon, divider, and surface colors from `Theme.of(context)`, `ColorScheme`, or `AppThemeExtension` rather than hardcoded `Colors.white` / `Colors.black` / `appBackgroungColorDarkTheme`.

#### Scenario: Comment list in light mode

- **WHEN** the user views the video comments page in light mode
- **THEN** comment author names, body text, timestamps, and secondary labels SHALL be readable on the light background without relying on hardcoded white text

#### Scenario: Video and favorites lists in light mode

- **WHEN** the user views search results, favorites, or video widgets in light mode
- **THEN** titles, metadata, and icons SHALL use theme-appropriate foreground colors

#### Scenario: Buttons retain semantic colors

- **WHEN** any theme mode is active
- **THEN** `CustomButton` primary, success, cancel, and neutral variants SHALL retain their distinct semantic fill and label colors (yellow primary, blue success, red cancel) sourced from `AppThemeExtension`

### Requirement: Semantic color extensions

The theme layer SHALL expose shared semantic tokens (accent yellow, favorited icon color, button variant colors) via `AppThemeExtension` registered on both light and dark `ThemeData`.

#### Scenario: Favorited icon color

- **WHEN** a video or comment is marked as favorited
- **THEN** the favorite icon SHALL display in the accent yellow color in both light and dark modes

### Requirement: Centralized typography scale

The theme layer SHALL define a complete Poppins-based `textTheme` covering all text sizes currently hardcoded in widgets (10, 12, 13–16, 20, 25). Widgets and pages SHALL use named `textTheme` styles instead of inline `fontSize` or `fontFamily`.

#### Scenario: Typography change in one file

- **WHEN** a developer adjusts a text style (e.g., body metadata size) in `app_theme.dart` `textTheme` definitions
- **THEN** all widgets using that style SHALL update without editing individual widget files

#### Scenario: No scattered font declarations in widgets

- **WHEN** the implementation is complete
- **THEN** no page or shared component file outside `lib/app/common/themes/` SHALL contain inline `fontSize:` or `fontFamily:` declarations (weight overrides via `.copyWith(fontWeight: ...)` are permitted)

#### Scenario: Empty-state and section headers

- **WHEN** the user views empty states or section headers on favorites or comments pages
- **THEN** header text SHALL use a named `textTheme` style (e.g., `headlineSmall`) rather than hardcoded `fontSize: 25`
