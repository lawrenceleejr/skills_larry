# Font pairings & type scale (all Google Fonts, all free)

## Go-to pairings
| Heading | Body | Mood | Notes |
|---------|------|------|-------|
| Fraunces | Inter | Editorial, warm | Characterful serif display + neutral sans body |
| Playfair Display | Source Sans 3 | Elegant, high-contrast | Classic magazine feel; keep Playfair large |
| Space Grotesk | Inter | Modern, techy | Geometric headline, clean body |
| Archivo | Libre Franklin | Confident, editorial | Grotesque pairing, strong hierarchy |
| Libre Baskerville | Source Sans 3 | Literary | Traditional serif for reading-heavy pages |
| IBM Plex Serif | IBM Plex Sans | Cohesive, safe | Superfamily — pairs by design; add Plex Mono for code |
| Source Serif 4 | Source Sans 3 | Neutral, versatile | Superfamily; great for docs/reports |
| Newsreader | Inter | Journalistic | Optical serif for long text |

## Single-family (superfamily) defaults
When unsure, use one superfamily and vary weight/style: **Inter** (UI/sans),
**Source** (Serif 4 + Sans 3 + Mono), **IBM Plex** (Sans/Serif/Mono), **Noto**
(widest language coverage). Pairs by construction; minimal risk.

## Mono (code / tabular)
JetBrains Mono, IBM Plex Mono, Source Code Pro, Space Mono.

## Modular type scale
Pick a ratio and stick to it. Common ratios: 1.2 (minor third), 1.25 (major
third), 1.333 (perfect fourth).

Example at 1.25 from a 16px base:
```
caption  12.8  (0.8em)
body     16    (1em)     line-height 1.5
lead     20    (1.25em)
h3       25
h2       31.25
h1       39   (tighter line-height ~1.15)
display  48.8+
```
CSS custom properties:
```css
:root {
  --ratio: 1.25; --f0: 1rem;
  --f-1: calc(var(--f0) / var(--ratio));
  --f1: calc(var(--f0) * var(--ratio));
  --f2: calc(var(--f1) * var(--ratio));
  --f3: calc(var(--f2) * var(--ratio));
}
body { font-family: 'Inter', system-ui, sans-serif; font-size: var(--f0); line-height: 1.5; }
h1 { font-family: 'Fraunces', Georgia, serif; font-size: var(--f3); line-height: 1.15; }
```

## Hierarchy do/don't
- **Do** separate levels by size *and* weight; add whitespace to group.
- **Do** keep line length 45–75 characters (`max-width: 65ch`).
- **Don't** use more than ~3 weights, or rely on color alone for rank.
- **Don't** center long body text; reserve centering for short display lines.

## Weights to request
Request only what you use (smaller download): typically body 400/500, headings
600/700/900. For self-hosting, pass exactly those to `get_fonts.py`
(`"Inter:wght@400;500;700"`).
