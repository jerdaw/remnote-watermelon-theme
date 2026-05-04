# Surprising Watermelon — RemNote Theme

A coordinated light and dark mode theme for [RemNote](https://www.remnote.com/), adapted from the [Bearded Theme "Surprising Watermelon"](https://github.com/BeardedBear/bearded-theme) color palette by BeardedBear.

The canonical marketplace stylesheet is the single combined [`theme.css`](./theme.css). Light mode is the default token set; dark mode overrides the same shared tokens when RemNote applies `.dark`.

---

## Preview

**Dark Mode** — Deep teal backgrounds, coral accents, and a warm watermelon-red highlight system.

**Light Mode** — Soft sage greens with matching coral accents, designed to be easier on the eyes than a bright white theme.

> Before marketplace submission, add real RemNote screenshots to `screenshots/` and reference them here. Recommended files:
>
> - `screenshots/light-editor.png`
> - `screenshots/dark-editor.png`
> - `screenshots/light-headings-quotes.png`
> - `screenshots/dark-headings-quotes.png`

---

## Features

- Single combined `theme.css` with coordinated **light and dark mode** support
- Shared variable-driven rule set to reduce light/dark selector leakage
- Custom **heading styles**: H1 accent fill, H2 top border, H3 left rail
- **Inline code** styling with monospace chip treatment
- **Quote chips**: tight, text-hugging, no left rail
- **Highlight colors** with contrast fixes for red, orange, yellow, green, blue, and purple
- **Cloze** card styling
- **KaTeX** math rendering support
- **Scrollbar** theming
- **Demo Tabs** plugin compatibility
- **Bold, italic, underline, link, caret, search, and form-control** polish

---

## Installation

### From the Theme Marketplace

Search for **Surprising Watermelon** in RemNote's Theme Marketplace and click **Install**.

### Manual Install / Local Test

1. Download or clone this repository.
2. In RemNote, open **Settings → Plugins and Themes → Build**.
3. Upload a zip of this repository folder, or use the packaging instructions in [`PACKAGING.md`](./PACKAGING.md).
4. Test in both RemNote light mode and dark mode.

---

## Repository Structure

```text
remnote-watermelon-theme/
  theme.css        # Canonical combined marketplace stylesheet
  manifest.json    # RemNote theme metadata
  README.md        # Marketplace/readme description
  LICENSE          # MIT license
  PACKAGING.md     # Human packaging instructions
  AGENTS.md        # Instructions for AI agents/editing assistants
  build_theme.py   # Validation + optional packaging helper
  light.css        # Historical/reference light-only source
  dark.css         # Historical/reference dark-only source
  screenshots/     # Add real screenshots before marketplace submission
  reference/       # Original palette reference
```

`theme.css` is the source of truth. Do not regenerate it by concatenating `light.css` and `dark.css`.

---

## Development

Validate the theme before packaging:

```bash
python build_theme.py
```

Create a marketplace upload zip from the main repo without maintaining a second directory:

```bash
python build_theme.py --package
```

This creates `remnote-watermelon-theme.zip` while excluding `.git/`, cache files, generated zips, and other local artifacts.

---

## Privacy and Permissions

This is a CSS-only RemNote theme.

- No JavaScript
- No network requests
- No native access
- No requested RemNote permission scopes

`manifest.json` uses:

```json
"requestNative": false,
"requiredScopes": []
```

---

## Color Palette Reference

The theme is adapted from the Bearded Theme "Surprising Watermelon" VS Code palette. An unaltered copy of the original VS Code color definitions is preserved in [`reference/bearded-theme-surprising-watermelon.json`](./reference/bearded-theme-surprising-watermelon.json) for reference.

Key colors:

| Role | Dark Mode | Light Mode |
|---|---:|---:|
| Background | `#142326` | `#f1f6f4` |
| Foreground | `#c1d9de` | `#263f46` |
| Accent / Coral | `#da6c62` | `#da6c62` |
| Cyan | `#00B3BD` | `#008c98` |
| Green | `#a9dc76` | `#7eaf4f` |
| Purple | `#c47cbf` | `#a45ea0` |

---

## Credits

Color palette by [BeardedBear](https://github.com/BeardedBear) — [Bearded Theme](https://github.com/BeardedBear/bearded-theme).

---

## License

MIT. See [`LICENSE`](./LICENSE).
