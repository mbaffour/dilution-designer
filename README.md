# Dilution Designer — Molecular Biology Bench Toolkit

> *Built with passion for science and discovery*

A free, single-file, browser-based toolkit for everyday molecular-biology bench work: dilutions and molarity, reagent and buffer recipes, plate layouts, common calculators, step-by-step protocols, gel simulation and a lab notebook. No installation, no account, no server, and no data ever leaves your machine.

**Live tool:** [mbaffour.github.io/dilution-designer](https://mbaffour.github.io/dilution-designer)
**Blog post:** [mbaffour.github.io/dilution-designer/blog.html](https://mbaffour.github.io/dilution-designer/blog.html)

---

## The eight modules

| Module | What it does |
|---|---|
| **Home hub** | Launcher for everything below |
| **Plate Planner** | 96- and 384-well, multi-plate. Plasmid/induction and phage/MOI modes, master mix with overage, replicates, randomization, exclusions, bench-reality checks |
| **Reagent Prep** | 216 verified recipes across 13 categories — media, buffers, antibiotics, miniprep P1/P2/P3 and Buffer PE, CTAB, gel and protein reagents — scaled to whatever volume you need, with sources |
| **Dilution & Molarity** | C1V1 across molar and mass units, serial dilutions, molarity ⇄ mass, and weigh-outs |
| **Calculators** | 14 bench calculators: ng ⇄ pmol, A260 quant, ligation ratios, primer Tm and resuspension, OD₆₀₀ → cells, phage titer and MOI, % ⇄ molarity, RCF ⇄ RPM, doubling time, PCR/qPCR master mix |
| **Protocols** | 21 protocols — miniprep, CTAB gDNA, transformation, plaque assay, gels, MIC, Gibson and more — that **rescale as you change the numbers** |
| **Gel Simulator** | Predict an agarose or SDS-PAGE run before you pour it: 16 vendor ladders plus your own, band-resolution warnings, and a best-percentage suggestion |
| **Lab Notebook** | Pull results from any module into a dated entry, add your own notes, export to Markdown, HTML, PDF, Word (.docx), CSV or JSON |

---

## Why you might want it

- **Everything is local.** Every calculation runs in your browser. Nothing is uploaded, so it is fine for unpublished work.
- **It works offline.** Visit once and it keeps working with no network — usable in a cold room, a BSL suite, or on a plane. It is a PWA, so you can install it like an app.
- **The maths is checked.** A self-test harness (`?selftest=1`) asserts every formula — 43 assertions, anchored to published references rather than to the code's own output.
- **It is one file.** `index.html` plus a recipe library. No build step, no dependencies, no CDN.

---

## Quick start

Open the live URL, or serve the folder locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`. Opening `index.html` straight off disk mostly works, but browsers block local `file://` data requests, so the recipe library will not load — serve it instead.

---

## How to use

### Plate Planner — plasmid / induction

1. Pick **Plasmid / Induction** mode, choose 96- or 384-well
2. Enter compound name, stock concentration, and culture volume per well
3. Add conditions with **+ Add condition**, then paint or replicate across wells
4. Toggle controls (negative, blanks, positive) as needed
5. Read off the per-well volumes and the master mix table
6. Export **Save** (JSON), **CSV**, **PNG**, **Print**, or send it to the Notebook

### Plate Planner — phage infection

1. Pick **Phage Infection** mode
2. Enter bacterial concentration (CFU/mL), phage titer (PFU/mL), and infection volume per well
3. Use the **Serial Dilution Planner** to get from stock to working titer
4. Add MOI conditions, paint, and check the MOI panel for per-well and total phage volumes

### Gel Simulator

Choose DNA (agarose) or protein (SDS-PAGE), set the percentage, pick a ladder, and enter your expected fragment sizes per lane. It tells you which bands will not resolve, which run off or stick in the well, and which gel percentage would separate everything.

> The migration model is a planning aid, not a prediction: it approximates mobility as linear in log₁₀(size) over the gel's resolving range. Real migration also depends on buffer, voltage and conformation — supercoiled, nicked and linear plasmid of the same length run differently. Ladder band sizes are the manufacturers' published values; the image is drawn from those numbers.

### Notebook

Every module has a **＋ Notebook** button. It opens a picker so you choose exactly what to import — a plate image, a band table, a set of calculator results, a protocol with its tick state. Add free text in light markdown, then export.

---

## Keyboard and accessibility

- **Undo / Redo:** Ctrl+Z / Ctrl+Y, 30-step history
- Every control is reachable and operable by keyboard; dialogs trap focus and close on **Escape**
- All text meets WCAG AA contrast in all three themes (day, night, ambient), verified by a measured audit rather than by eye
- Gel images are canvas, so an equivalent band table is always rendered as real text for screen readers
- Respects `prefers-reduced-motion`

---

## Accuracy and sourcing

Recipes carry their sources and licences, weighted toward open references (PubChem, OpenWetWare, protocols.io, Addgene, Barrick Lab) and manufacturers' free technical sheets. Molecular weights cite a PubChem CID. Factual numbers — molecular weights, band sizes, concentrations — are used freely; vendor prose and artwork are never copied.

**This is a planning tool.** Check anything that matters against your own protocol before you pipette it.

---

## Supported browsers

Any modern browser (Chrome 99+, Firefox 112+, Safari 15.4+). PNG export uses the Canvas API with `roundRect`; offline support uses a service worker.

---

## Bugs & feature requests

[Open an issue on GitHub →](https://github.com/mbaffour/dilution-designer/issues)

Pull requests are welcome.

---

## Credits

- Typefaces: [DM Mono](https://fonts.google.com/specimen/DM+Mono) and [Syne](https://fonts.google.com/specimen/Syne), loaded as a progressive enhancement only — local stacks sit behind them so the offline experience is unchanged
- Plate layout inspired by Biotek Gen5 plate reader software

---

## License

MIT License — free to use, modify, and distribute.
