# theme-preference

User theme mode selection, persistence, and UI controls.

## Requirements

### Requirement: Theme mode selection

The app SHALL allow the user to choose among three theme modes: **Light**, **Dark**, and **System** (follow OS appearance).

#### Scenario: User selects light mode

- **WHEN** the user selects Light theme mode
- **THEN** the app SHALL immediately apply the light theme across all visible screens

#### Scenario: User selects dark mode

- **WHEN** the user selects Dark theme mode
- **THEN** the app SHALL immediately apply the dark theme across all visible screens

#### Scenario: User selects system mode

- **WHEN** the user selects System theme mode
- **THEN** the app SHALL use the platform's current brightness setting (light or dark) to choose the active theme
- **AND** the app SHALL update automatically when the OS appearance changes while the app is running

### Requirement: Theme preference persistence

The selected theme mode SHALL persist across app restarts using local device storage (`shared_preferences` via the existing `CachePackage` or equivalent).

#### Scenario: Preference restored on launch

- **WHEN** the user previously selected a theme mode and relaunches the app
- **THEN** the app SHALL start with that same theme mode applied before the first frame is painted (or as early as possible during startup)

#### Scenario: Default on first launch

- **WHEN** no theme preference has been stored
- **THEN** the app SHALL default to **System** mode

### Requirement: Theme mode UI control

The app SHALL expose an accessible control for changing theme mode without requiring a separate settings screen rebuild.

#### Scenario: Toggle reachable from main navigation

- **WHEN** the user is on any primary screen (search, comments, favorites)
- **THEN** the user SHALL be able to open or act on a theme mode control (e.g., app bar action or settings affordance) to switch between Light, Dark, and System

#### Scenario: Current mode is indicated

- **WHEN** the theme mode control is displayed
- **THEN** the currently active mode SHALL be visually indicated (selected state, icon, or label)
