# Dilution Designer — 96-Well Plate Protocol Planner

> *Built with passion for science and discovery*

A free, single-file, browser-based tool for designing 96-well plate experiments. No installation, no account, no server — open `index.html` in any modern browser and start planning.

**Live tool:** [mbaffour.github.io/dilution-designer](https://mbaffour.github.io/dilution-designer)  
**Blog post:** [mbaffour.github.io/dilution-designer/blog.html](https://mbaffour.github.io/dilution-designer/blog.html)

---

## What it does

Dilution Designer calculates compound and culture volumes for every well in your 96-well plate, generates a master mix table with 10% overage, and produces step-by-step bench instructions — all in real time as you paint the plate.

Two experiment modes:

| Mode | Use case |
|---|---|
| **Plasmid / Induction** | Dose-response, MIC, reporter assays, dye uptake, any concentration gradient |
| **Phage Infection** | MOI-based infection assays, host range, dose-response with phage |

---

## Features

- **Interactive plate map** — Paint, Replicate (fill a row or column in one drag), Erase, and Exclude tools
- **Undo / Redo** — Ctrl+Z / Ctrl+Y, 30-step history
- **Auto-save** — State restored automatically on page reload (localStorage)
- **JSON save/load** — Export experiments as `.json` files and reload them on any device
- **PNG export** — Download a clean plate image for notebooks, slides, and reports
- **MOI calculator** — Per-well phage volume from bacterial concentration, phage titer, and desired MOI
- **Serial dilution planner** — Stock → working titer with minimum pipettable volume constraint
- **Input validation** — Red borders and inline errors for impossible values; warnings when stock or culture volume is insufficient
- **Calc breakdown tooltip** — Hover any filled well to see the exact formula used to calculate its volumes
- **Master mix table** — Grouped by condition with 10% overage, lists all well IDs
- **Per-well table** — Every well shown as an independent row (replicates are never summed)
- **Three themes** — Day (bright), Night (dark), Ambient (warm, low-contrast)
- **Print modes** — Full protocol report, or plate-map-only
- **CSV export** — Full or minimal (plate map + volumes only)
- **Gen5-style plate layout** — Large square wells, well IDs visible, inspired by Biotek Gen5 software

---

## How to use

### Plasmid / Induction experiments

1. Open `index.html` (or the live URL above) — select **Plasmid / Induction** mode
2. Enter your **compound name**, **stock concentration**, and **culture volume per well**
3. Add conditions in the sidebar with **+ Add condition** — enter concentration and pick a color
4. Select a condition in the palette, choose the **Paint** or **Replicate** tool, and click/drag wells
5. Toggle controls (negative, blanks, positive) as needed
6. Review the per-well volumes and master mix table
7. Export: **💾 Save** (JSON), **CSV**, **🖼 PNG**, or **Print all**

### Phage Infection experiments

1. Select **Phage Infection** mode
2. Enter **bacterial concentration** (CFU/mL), **phage titer** (PFU/mL), and **infection volume per well**
3. Use the **Serial Dilution Planner** in the sidebar to prepare working titer from stock
4. Add MOI conditions and paint the plate
5. Check the MOI calculator panel for per-well and total phage volumes

### Tips

- **Undo/Redo:** Ctrl+Z / Ctrl+Y (or the toolbar buttons) — works for painting, exclusion, and condition changes
- **Replicate tool:** Set n= and direction (row/col), then click any well to paint that many consecutive wells at once
- **Exclude tool:** Click or drag to mark wells as off-limits — they're removed from all calculations
- **Calc tooltip:** Hover any filled well to see the formula broken down with your actual numbers
- **Auto-save:** Your experiment is automatically saved to the browser. Reload the page and pick up where you left off.

---

## Screenshots

_Add screenshots here_

---

## Supported browsers

Any modern browser (Chrome 99+, Firefox 112+, Safari 15.4+). PNG export uses the Canvas API with `roundRect` — all supported in the above versions.

---

## Bugs & feature requests

[Open an issue on GitHub →](https://github.com/mbaffour/dilution-designer/issues)

Pull requests are welcome.

---

## Credits

- Typefaces: [DM Mono](https://fonts.google.com/specimen/DM+Mono) and [Syne](https://fonts.google.com/specimen/Syne) via Google Fonts
- Inspired by Biotek Gen5 plate reader software layout

---

## License

MIT License — free to use, modify, and distribute.
