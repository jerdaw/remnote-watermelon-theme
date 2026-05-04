# Instructions for AI Agents Working on This Repo

This repo contains a CSS-only RemNote theme. The goal is to keep the main repo directly marketplace-ready. Do not create or maintain a second source directory.

## Non-Negotiable Rules

1. `theme.css` is the source of truth.
2. Do not rebuild `theme.css` by concatenating `light.css` and `dark.css`.
3. `light.css` and `dark.css` are reference/history only.
4. Do not add JavaScript, remote imports, analytics, or network calls.
5. Keep `requestNative` false and `requiredScopes` empty unless the project explicitly stops being CSS-only.
6. Do not include `.git/`, caches, logs, generated zips, or local scratch files in upload packages.

## How to Make Theme Changes

Most changes should happen in `theme.css`.

Preferred pattern:

- Add or edit variables in the light token block under `:root, .light`.
- Add or edit corresponding variables in the `.dark` token block.
- Keep visual rules mode-neutral by using shared `--sw-*` variables.
- Only add explicit `.dark ...` selectors when a rule truly cannot be variable-driven.

Avoid these old regression patterns:

```css
--swl-*
body .dark div#hierarchy-editor
.light .dark\:bg-black, .dark\:bg-black
:is(.rn-rem-reference, .dark .rn-highlight-reference)
```

## Validation

Run:

```bash
python build_theme.py
```

Before packaging or committing, this should pass with no errors.

## Packaging

Run:

```bash
python build_theme.py --package
```

The package should contain a single top-level `remnote-watermelon-theme/` folder with the repo contents and no `.git/` directory.

## Marketplace Readiness Checklist

Before telling the user the repo is ready for upload, verify:

- `theme.css` exists and validates.
- `manifest.json` exists and has version/name/description appropriate for the release.
- `README.md` describes the theme and installation.
- `LICENSE` exists.
- `PACKAGING.md` exists.
- Real screenshots have been added or the user has been clearly told that screenshots are still the only missing manual asset.
- A zip produced by `python build_theme.py --package` does not include `.git/`.
