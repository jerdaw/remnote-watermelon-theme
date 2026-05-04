"""
build_theme.py — Correctly combines light.css + dark.css into theme.css

For dark mode:
  1. Variable blocks (:root, .dark { }) → .dark { }  (no :root bleed)
  2. The html/body/#root global selector → .dark, .dark .rn-app, ... 
     (since .dark is ON body in RemNote, not a parent of it)
  3. All other component selectors → prefixed with ".dark "
"""
import re

with open("light.css") as f:
    light = f.read().rstrip()

with open("dark.css") as f:
    dark = f.read()

# ── 1. Fix variable blocks ────────────────────────────────────────────────────
# :root, .dark { ... }  →  .dark { ... }
dark = re.sub(r':root\s*,\s*\n\s*\.dark\s*\{', '.dark {', dark)
# bare :root { (shouldn't be any after the above, but safe)
dark = re.sub(r'(?<![.\w]):root\s*\{', '.dark {', dark)

# ── 2. Fix the global html/body/#root background selector ─────────────────────
dark = dark.replace(
    "html,\nbody,\n#root,\n.dark,\n.rn-app,\n.rn-pane,\n.rn-pane__body,\n"
    ".rn-clr-background,\n.rn-clr-background-primary {",
    ".dark,\n.dark .rn-app,\n.dark .rn-pane,\n.dark .rn-pane__body,\n"
    ".dark .rn-clr-background,\n.dark .rn-clr-background-primary {"
)

# ── 3. Prefix all remaining component selector blocks with .dark ───────────────
def prefix_component_selectors(css):
    """
    Walk the CSS token by token. For every rule block that is NOT a
    CSS custom-property (variable) block, prefix each selector with .dark.
    Variable blocks are identified by their first declaration starting with --.
    """
    # We'll use a simple state machine on the text
    out = []
    pos = 0
    n = len(css)

    while pos < n:
        # Skip whitespace / newlines
        ws_match = re.match(r'\s+', css[pos:])
        if ws_match:
            out.append(ws_match.group())
            pos += ws_match.end()
            continue

        # Comments
        if css[pos:pos+2] == '/*':
            end = css.find('*/', pos+2)
            if end == -1:
                out.append(css[pos:])
                break
            end += 2
            out.append(css[pos:end])
            pos = end
            continue

        # At-rules (pass through)
        if css[pos] == '@':
            end = css.find('{', pos)
            if end == -1:
                out.append(css[pos:])
                break
            # collect block
            depth = 1
            i = end + 1
            while i < n and depth:
                if css[i] == '{': depth += 1
                elif css[i] == '}': depth -= 1
                i += 1
            out.append(css[pos:i])
            pos = i
            continue

        # Try to match a selector block: selector(s) { ... }
        # Selector ends at the first { not inside () or []
        brace = -1
        depth_p = depth_b = 0
        i = pos
        while i < n:
            c = css[i]
            if c == '(' : depth_p += 1
            elif c == ')': depth_p -= 1
            elif c == '[': depth_b += 1
            elif c == ']': depth_b -= 1
            elif c == '{' and depth_p == 0 and depth_b == 0:
                brace = i
                break
            i += 1

        if brace == -1:
            # No more blocks
            out.append(css[pos:])
            break

        selector_text = css[pos:brace].strip()
        # Find matching closing brace
        depth = 1
        j = brace + 1
        while j < n and depth:
            if css[j] == '{': depth += 1
            elif css[j] == '}': depth -= 1
            j += 1
        block_body = css[brace:j]  # includes { ... }

        # Is this a variable block? Check if first real declaration starts with --
        inner = block_body[1:-1].strip()
        first_decl_match = re.search(r'[^\s*/]', inner)
        is_var_block = first_decl_match and inner[first_decl_match.start():].startswith('--')

        if is_var_block or not selector_text:
            # Variable block or empty — pass through as-is
            out.append(css[pos:j])
        else:
            # Prefix each selector with .dark
            # Split on comma + optional whitespace (but respect :is(), :not() etc.)
            raw_selectors = re.split(r',\s*(?=\n|[^\s])', selector_text)
            prefixed_parts = []
            for p in raw_selectors:
                p = p.strip()
                if not p:
                    continue
                if (p.startswith('.dark') or p.startswith('::') or
                        p.startswith(':root') or p == '*' or
                        p.startswith('*::')):
                    prefixed_parts.append(p)
                elif p.startswith('body div#hierarchy-editor') or p.startswith('body div#hierarchy-editor'.rstrip()):
                    # body is an ancestor qualifier; .dark is on #root (inside body).
                    # Rewrite: body div#hierarchy-editor ... → body .dark div#hierarchy-editor ...
                    prefixed_parts.append(p.replace('body div#hierarchy-editor', 'body .dark div#hierarchy-editor', 1))
                else:
                    prefixed_parts.append('.dark ' + p)
            new_sel = ',\n'.join(prefixed_parts)
            out.append(new_sel + ' ' + block_body)

        pos = j

    return ''.join(out)


dark_transformed = prefix_component_selectors(dark)

# ── Assemble ──────────────────────────────────────────────────────────────────
header = """\
/* =========================================
   Surprising Watermelon — RemNote Theme
   Light & Dark Mode

   Author: Jeremy Dawson <jeremyjdawson@gmail.com>
   Repo:   https://github.com/jerdaw/remnote-watermelon-theme

   Color palette adapted from:
   "Bearded Theme Surprising Watermelon" by BeardedBear
   https://github.com/BeardedBear/bearded-theme

   Light: v0.2.0  |  Dark: v0.4.0
   ========================================= */
"""

combined = (
    header
    + "\n\n/* ─────────────────────────────────────────\n"
    + "   LIGHT MODE (default — no class needed)\n"
    + "   ───────────────────────────────────────── */\n"
    + light
    + "\n\n\n/* ─────────────────────────────────────────\n"
    + "   DARK MODE (active when RemNote adds .dark to body/html)\n"
    + "   ───────────────────────────────────────── */\n"
    + dark_transformed
    + "\n"
)

with open("theme.css", "w") as f:
    f.write(combined)

# ── Sanity checks ─────────────────────────────────────────────────────────────
c = open("theme.css").read()
lines = c.count('\n')
dark_start = c.find("DARK MODE")
dark_section = c[dark_start:] if dark_start != -1 else ""

root_leaks = len(re.findall(r':root\s*\{', dark_section))
bad_sel = re.findall(r'\.dark\s+(html|body|#root)\b', dark_section)
dark_vars = len(re.findall(r'\.dark\s*\{', dark_section))

print(f"theme.css: {lines} lines, {len(c)} bytes")
print(f"':root {{' leaks in dark section: {root_leaks}")
print(f"Bad .dark html/body/#root selectors: {set(bad_sel) or 'none'}")
print(f"'.dark {{' variable blocks in dark section: {dark_vars}")
print("Done." if not root_leaks and not bad_sel else "ISSUES FOUND — review output.")
