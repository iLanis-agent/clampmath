# Clamp Math

Fluid text size arithmetic for CSS `clamp()`. Text that grows from 16px at 400px wide to 24px at 1200px wide is `clamp(1rem, 0.75rem + 1vw, 1.5rem)`.

## What it computes

All inputs are whole numbers. Sizes are 1 to 200px, page widths 200 to 4000px, the root size 8 to 32px.

- **The formula truth** - the `clamp()` value for a straight-line change between two sizes over two widths, with the numbers rounded to 4 places and 1rem counted as the root size you enter.
- **The size truth** - the exact text size (to hundredths of a pixel) at a page width, or the smallest or largest size outside the range.
- **The reach truth** - the page width (to a tenth of a pixel) where the text reaches a size inside the range.

## Boundary

Arithmetic only. It has not seen any page, font or visitor setting. It does not know how browser zoom, a visitor's own text size or other CSS will change what people see, or whether the text is easy to read, and it gives no verdict that a size is right. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers).
- `oracle.py` - the Python mirror (Fractions, solves the line from its two points, bisects for the width) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (299 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/clampmath/
Repo: https://github.com/iLanis-agent/clampmath
