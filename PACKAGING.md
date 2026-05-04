# Packaging and Marketplace Checklist

This repository is intended to be the single source directory for the RemNote Marketplace upload. Do **not** maintain a second marketplace-only folder.

## Source of Truth

- `theme.css` is the canonical combined light/dark stylesheet.
- `light.css` and `dark.css` are historical/reference files only.
- Do not regenerate `theme.css` by concatenating `light.css` and `dark.css`.

## Validate

From the repository root:

```bash
python build_theme.py
```

The validator checks that:

- Required files are present.
- CSS braces are balanced outside comments.
- Custom properties used via `var(...)` are defined.
- Old merge-regression patterns are absent.
- `manifest.json` contains the expected marketplace metadata.

## Create an Upload Zip

Preferred command:

```bash
python build_theme.py --package
```

This creates:

```text
remnote-watermelon-theme.zip
```

The zip contains the repository folder and excludes:

- `.git/`
- Python caches
- editor/OS junk
- prior generated zip files
- logs

Alternative if the repo is committed to Git:

```bash
git archive --format=zip --output=remnote-watermelon-theme.zip --prefix=remnote-watermelon-theme/ HEAD
```

## Upload to RemNote

1. Open RemNote.
2. Go to **Settings → Plugins and Themes → Build**.
3. Use the Theme Marketplace upload flow.
4. Upload `remnote-watermelon-theme.zip`.
5. Test after upload in both light mode and dark mode.

## Final Manual QA

Before public submission, test:

- Light mode editor background, sidebar, menus, omnibar, headings, quotes, code, highlights, clozes, and KaTeX.
- Dark mode editor background, sidebar, menus, omnibar, headings, quotes, code, highlights, clozes, and KaTeX.
- Search highlighting and selection styling.
- At least one document with nested bullets/indents.
- At least one quote Rem containing bold, italic, links/references, inline code, and highlights.
- At least one flashcard/card delimiter to ensure delimiter symbols are not styled as code chips.

## Screenshots

RemNote's theme documentation asks theme authors to include pictures of the theme. Add real screenshots before marketplace submission, ideally:

```text
screenshots/light-editor.png
screenshots/dark-editor.png
screenshots/light-headings-quotes.png
screenshots/dark-headings-quotes.png
```

Then update the Preview section in `README.md` to embed the images.
