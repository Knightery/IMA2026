# Slide Assets

This folder now contains both the legacy Marp theme assets and the primary PPTX-native deck builder.

## Primary Deck Build
- `build_case_deck_pptx.py`: builds the full 40-slide PowerPoint deck directly from the existing analysis outputs
- `case-deck.pptx`: generated PowerPoint deck

Build the deck with:

```powershell
python slides/build_case_deck_pptx.py
```

## Legacy Marp Assets
The Marp files are still useful for style reference and fast HTML/PDF iteration, but they are no longer the main deck output path.

## Files
- `executive-avocado.css`: reusable Marp theme with palette, typography, layout, and slide classes
- `style-preview.md`: preview deck showing the theme on representative case-slide patterns

## Slide Classes
- `lead`: title and closing slides
- `section`: main section divider slides
- `appendix`: divider before backup material

## Utility Classes
- `pill-row` and `pill`: compact tags for scenarios and labels
- `kpi-grid`, `card`, and `metric`: executive summary and recommendation cards
- `columns`, `columns equal`, and `col`: two-column layouts
- `timeline` and `timeline-step`: implementation roadmap layout
- `caption`, `muted`, `small`, and `tiny`: text helpers

## Suggested Marp Command
Use a local theme set and allow local image files so the preview can load charts from `../outputs/`.

```powershell
npx @marp-team/marp-cli slides/style-preview.md --theme-set slides/executive-avocado.css --allow-local-files --pdf
```

If you prefer HTML output while iterating:

```powershell
npx @marp-team/marp-cli slides/style-preview.md --theme-set slides/executive-avocado.css --allow-local-files --html
```
