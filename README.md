# Dilution Designer — Molecular Biology Bench Toolkit

> *Built with passion for science and discovery*

A free, single-file, browser-based toolkit for everyday molecular-biology bench work: dilutions and molarity, reagent and buffer recipes, plate layouts, common calculators, step-by-step protocols, gel simulation and a lab notebook. No installation, no account, no server, and no data ever leaves your machine.

**Live tool:** [mbaffour.github.io/dilution-designer](https://mbaffour.github.io/dilution-designer)
**Blog post:** [mbaffour.github.io/dilution-designer/blog.html](https://mbaffour.github.io/dilution-designer/blog.html)

---

## The ten modules

| Module | What it does |
|---|---|
| **Home hub** | Launcher for everything below |
| **Plate Planner** | 96- and 384-well, multi-plate. Plasmid/induction and phage/MOI modes, master mix with overage, replicates, randomization, exclusions, bench-reality checks |
| **Phage Planner** | A saved library of lysates and their titers, then the volume for an infection — by MOI, total PFU or final PFU/mL — plus the dilution to make when that volume is too small to pipette |
| **Reagent Prep** | 243 verified recipes across 14 categories — media, buffers, antibiotics, miniprep P1/P2/P3 and Buffer PE, CTAB, gel and protein reagents, fixatives, stains and mountants — scaled to whatever volume you need, with sources |
| **Dilution & Molarity** | C1V1 across molar and mass units, serial dilutions, molarity ⇄ mass, and weigh-outs |
| **Calculators** | 16 bench calculators: ng ⇄ pmol, A260 quant, ligation ratios, primer Tm and resuspension, OD₆₀₀ → cells, phage titer, MOI, lysate → infection volume, % ⇄ molarity, RCF ⇄ RPM, doubling time, dye working dilution, PCR/qPCR master mix |
| **Protocols** | 31 protocols — miniprep, CTAB gDNA, transformation, plaque assay, gels, MIC, Gibson, immunofluorescence, H&E, live/dead and more — that **rescale as you change the numbers** |
| **Microscopy & Dyes** | 79 dyes and stains — what to use for what, at what concentration, and in which channel. Ex/Em maxima, filter-cube and laser matching, a panel builder that flags channel collisions and bleed-through, working-dilution volumes for your sample count, and step-by-step staining directions |
| **Gels & Blots** | Simulate a DNA gel, a protein gel or a Western blot before you run it: 18 vendor ladders plus your own, load-aware band width and brightness per stain, uncut plasmid (supercoiled / nicked / linear), transfer efficiency by protein size, exposure and saturation, a Ponceau view, where to cut the membrane and how much antibody each strip needs |
| **Lab Notebook** | Pull results from any module into a dated entry, add your own notes, export to Markdown, HTML, PDF, Word (.docx), CSV or JSON |

---

## Why you might want it

- **Everything is local.** Every calculation runs in your browser. Nothing is uploaded, so it is fine for unpublished work.
- **It works offline.** Visit once and it keeps working with no network — usable in a cold room, a BSL suite, or on a plane. It is a PWA, so you can install it like an app.
- **The maths is checked.** A self-test harness (`?selftest=1`) asserts every formula — 360 assertions, anchored to published references rather than to the code's own output.
- **It is one file.** `index.html` plus a recipe library and a dye library. No build step, no dependencies, no CDN.

---

## Quick start

Open the live URL, or serve the folder locally:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`. Opening `index.html` straight off disk mostly works, but browsers block local `file://` data requests, so the recipe and dye libraries will not load — serve it instead.

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

### Phage Planner

1. **＋ Add lysate** — name, titer, volume on hand, propagating host and the date you titered it. If you only have a plate count, open *Calculate titer from a plaque assay* and it fills the titer in for you. Lysates are saved in your browser and survive reloads; **Export / Import JSON** moves them between machines, and **Pull from plate** copies the stocks off your current plate layout
2. Pick a lysate on the left — or skip that and just type a titer
3. Choose what you want to deliver: **a target MOI** (with the host density), **a total number of PFU**, or **a final PFU/mL** in the infection
4. Set the volume per infection, how many infections, and whether the phage goes *on top of* the culture or *comes out of* the stated volume
5. Read off the volume to pipette. If the neat volume is too small for your pipettes, it tells you which dilution to make, gives you the recipe (take X µL + Y µL diluent), and shows every rung of the ladder with its verdict so you can override the choice
6. **→ Send to Plate Planner** turns the selected lysate into a phage stock for a plate layout

The same solver is available as a calculator (*Calculators → Phage lysate → infection volume*) and the Plate Planner's phage-stock editor can load from and save to the same library.

> Delivered MOI, final volume and PFU/mL are computed from the volume you will **actually pipette**, not from the neat-equivalent volume — those two differ whenever a dilution is involved.

### Microscopy & Dyes

1. Start from **what you are staining** — the chips down the left filter the library by target (nucleus, membrane, mitochondria, actin, viability, cell wall, antibody label, brightfield, EM) and by sample type (live cells, fixed cells, bacteria, tissue, EM grid)
2. Open a dye. The sheet gives you Ex/Em maxima on a wavelength axis, the filter cube and laser line it belongs on, how well that line actually excites it, and which other dyes in the library are too close to share a panel with
3. **What to use it for** lists the assays that dye is good for, each with a concentration and an incubation time
4. **Working dilution** takes your target concentration, sample count and volume per sample and gives you the exact volumes — and when the neat stock draw falls below what you can pipette, it builds the intermediate dilution ladder for you rather than telling you to take 0.1 µL
5. **Making the stock** turns a vial mass into the volume of solvent to add
6. **Directions** are tickable staining steps that rescale with the numbers above
7. **＋ Add to panel**, then **🎛 Panel builder**: pick your scope configuration and it assigns every dye to a channel and flags the three things that ruin a multi-colour experiment — two dyes in one channel, emission bleeding into the next collection band, and one dye lighting up on another's laser line

The working-dilution solver is also available on its own as *Calculators → Fluorophore / stain working dilution*, and **＋ Add a dye** stores your own reagents in the browser alongside the library.

> The panel checks are modelled from published excitation and emission **maxima** and their band widths — the app does not ship full spectral curves. They catch the obvious clashes; they are not a substitute for real overlap integrals or for linear unmixing on your own instrument. Working concentrations are starting points from published protocols and must be titrated on your own sample.

### Gels & Blots

Three tabs share one engine.

**DNA gel** — pick an agarose %, a stain and a ladder, and type band sizes per lane. Add an amount after `@` to make it load-aware (`3000@150` is 150 ng of 3 kb): bands below the stain's detection limit disappear, overloaded ones broaden and smear, and fat bands stop resolving. Add `sc` or `oc` for supercoiled or nicked plasmid (`4000sc@300`), or use **＋ Uncut** to draw a typical miniprep. A restriction digest sent from *Sequences* arrives with equimolar masses, so short fragments are faint, as on a real gel.

**Protein gel** — Tris-glycine gels from 7.5% to 15%, a 4–20% gradient, and a 16% Tris-Tricine gel for peptides, with Coomassie, colloidal Coomassie, silver or SYPRO Ruby. Give a lane a lysate amount to see what a whole-cell lysate looks like behind your protein. The separation ranges are the same table the SDS-PAGE protocol quotes, so the two can no longer disagree.

**Western blot** — lanes are total protein loaded; targets are antibodies with an apparent MW, an abundance, a relative level per lane and a host species. Add loading controls from a preset list. Then set the transfer (method, time, membrane, methanol, SDS) and the detection (ECL on an imager or film, exposure, or two-colour near-IR). It shows:
1. The blot as it would image — saturated bands in red, as imagers show them — or a **Ponceau S** view of total protein, dimmed by how well each size transferred
2. Transfer efficiency against protein size for your settings, with each target marked and specific fixes when one will not transfer
3. Saturation and detection per lane, the longest exposure before a band saturates, and the classic trap — a loading control that saturates long before your target is visible
4. Targets that co-migrate, and whether two-colour detection rescues them (it needs primaries from different species)
5. Where to cut the membrane, named by the ladder bands either side, and the primary and secondary antibody volume each strip needs

Any ORF in *Sequences* can be sent to the protein gel or the Western at its computed mass.

> These are planning aids, not predictions. Mobility is a smooth sigmoid in log₁₀(size) — steepest mid-gel and compressing toward the well and dye front — and real mobility also depends on buffer, voltage and temperature; glycosylated, very basic and membrane proteins often run away from their true mass. Plasmid conformations use rules of thumb for a ~1% gel. Western transfer and signal are heuristic curves that encode published rules of thumb, and abundances are order-of-magnitude. Ladder band sizes are the manufacturers' published values; the image is drawn from those numbers.

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
