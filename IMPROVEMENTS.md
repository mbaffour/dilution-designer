# Improvements

This document summarizes the changes on branch `claude/tool-improvements`.

## Fixes

### ⚠️ Correctness fix — delivered concentration now equals the target (BREAKING: results change)

**This changes computed numbers. Please confirm the intended convention before merging.**

**Before:** In `calcWellData` (plasmid mode), the compound volume `iv` was *added on top of* a
full `cultureVol` aliquot:

```
iv        = (targetConc / src) * cultureVol
finalVol  = cultureVol + iv          // volume grows past the intended per-well volume
```

Because `iv` was added rather than accounted for inside the well volume, the concentration
**actually delivered** was

```
deliveredConc = iv * src / finalVol = targetConc * cultureVol / (cultureVol + iv)
```

which is **lower than requested**. The error is negligible for high-potency stocks but large for
low-potency stocks:

| Target vs. stock | Old delivered conc | Error |
|---|---|---|
| target = 0.4% of stock | 99.6% of target | −0.4% |
| target = 20% of stock  | 83.3% of target | **−16.7%** |
| target = 50% of stock  | 66.7% of target | **−33.3%** |

**After (volume-conserving):** the well's final volume is held at `cultureVol`, and the compound
volume is taken **out of** the aliquot instead of added on top:

```
iv       = (targetConc / src) * cultureVol
cultVol  = max(0, cultureVol - iv)   // (or media aliquot for blanks)
finalVol = cultVol + iv = cultureVol
deliveredConc = iv * src / finalVol = targetConc   ✓ exact
```

Delivered concentration now equals the requested target in every case (verified numerically).

Changed in `index.html`:
- `calcWellData()` — the plasmid branch (compound volume subtracted from the culture/media aliquot; a
  comment explaining the corrected relationship was added).
- `buildCalcBreakdown()` — the hover tooltip now shows the culture aliquot as `cultureVol − iv` and the
  correct final volume, so the tooltip matches the table/master-mix math.

Downstream views (per-well table, master mix with 10% overage, bench steps, CSV export) read
`cultVol`/`indVol`/`finalVol` from `calcWellData`, so they update automatically and stay internally
consistent.

**Note on convention:** this implements the *volume-conserving* interpretation (final well volume =
your stated "volume per well"). If instead you intend "add cells at exactly `cultureVol`, then spike
compound on top" (final volume slightly larger), that is a different bench convention and the fix
should be revisited. Phage (MOI) mode was **not** changed — please confirm whether the same
volume-conservation should apply there before altering it.

### Added missing MIT LICENSE

The README states the project is MIT-licensed but no license file existed. Added a standard
`LICENSE` (MIT) with `Copyright (c) 2026 Michael Baffour Awuah`. No existing license file was
present, so nothing was overwritten.

## New features

All features are client-side, additive, and do not change existing behavior.

### 1. Serial-dilution condition generator (plasmid / induction mode)

A new **"Serial-dilution series"** panel in the Conditions sidebar. Enter a top concentration, a
dilution factor, and a number of points, then click **+ Generate series** to create that many
`condition` entries stepped down by the factor (e.g. 10000 → 5000 → 2500 → …). This lets you set up a
full dose-response gradient in one click instead of adding each condition by hand; existing
conditions and controls are preserved, and the action is undoable (Ctrl+Z).

- UI: `#serialGenPanel` (inputs `#sgTop`, `#sgFactor`, `#sgPoints`) in the conditions sidebar,
  shown only in plasmid mode.
- Handler: `generateSerialConditions()` in `index.html`; wired for visibility in `setMode()` and for
  the units hint in `update()`.

(Note: a phage-mode *serial-dilution planner* that computes transfer/diluent volumes already existed
and is unchanged. The existing well-level "Auto-fill from conditions" helper is also unchanged — the
new generator populates the condition list that auto-fill then paints from.)

### 2. Named layout save / load (multiple slots, beyond autosave)

The app already had single-slot autosave (localStorage) and file-based JSON export/import. Added a
**named-layout** manager in the header so several plate layouts can be kept in the browser under
names of your choosing:

- **＋ Save layout** — prompts for a name and stores the full experiment payload.
- **Saved layouts…** dropdown + **Open** — restores a saved layout.
- **🗑** — deletes the selected layout.

Layouts are stored under the `dd_layouts` localStorage key as a `{name: payload}` map; the payload is
the same structure produced by `_mkPayload()` used by JSON export, so file export/import and named
layouts are interoperable. Loading a named layout reuses the shared `_applyState()` helper (extracted
from `loadJSON()` so both paths behave identically) and is undoable.

- UI: header controls (`#layoutSelect`, Open / ＋ Save layout / 🗑 buttons).
- Handlers: `saveNamedLayout()`, `loadNamedLayout()`, `deleteNamedLayout()`, `refreshLayoutSelect()`,
  and the `_applyState()` refactor in `index.html`. `refreshLayoutSelect()` is called on init.

### CSV export — already present

The originally-suggested "CSV export of the pipetting plan" already exists (`downloadCSV()` /
`downloadMinimalCSV()`, wired to the **CSV** and **Minimal CSV** header buttons). It was **not**
duplicated. Its numbers now reflect the corrected volume math automatically.

## Verification

- Extracted the single inline `<script>` block and ran `node --check` — passes.
- Numerically verified old-vs-new delivered concentration (see table above): the new math delivers
  the exact target in every tested case.

---

# Microscopy workflows & dye directions

## What was added

Imaging was the one area of everyday bench work the toolkit did not touch. Before this change the
whole codebase contained exactly **two** excitation/emission numbers, both buried in free-text
`notes[]` strings in `reagent-library.json` (ethidium bromide and SYBR Safe). There was no
fluorophore, spectra, laser, filter or channel data structure anywhere.

### 1. `dye-library.json` — a new data file (79 dyes, 10 categories)

Same shape and the same load discipline as `reagent-library.json`. Each record carries what you
actually need at the scope: Ex/Em maxima and band widths, extinction coefficient and quantum yield,
cell permeability, stock and working concentrations with solvent and storage, an `applications[]`
table of *what to use it for and at what concentration*, tickable `directions[]`, hazards, and a
citation. Categories cover nucleic-acid/nuclear stains, viability, membrane, organelle,
cytoskeleton, bacterial cell-wall probes, antibody labels, fluorescent proteins, histology
brightfield stains and EM negative stains.

### 2. Microscopy module (`mic`) in `index.html`

Follows the `phg` module pattern exactly — mode string, view div, five `setMode()` edits, a
`window.MIC` global, a hub card with a live count, and a notebook provider. Two views: a per-dye
sheet (spectra strip, channel/cube/laser assignment, working-dilution solver, stock reconstitution,
directions) and a panel builder that checks a whole dye set against a chosen scope configuration.

### 3. Shared spectral and dilution maths

`dyeWorking()`, `micPanelCheck()`, `micChannelFor()`, `micOverlapIndex()`, `micEmFrac()` and the
unit converters are **top-level functions**, so the Microscopy module, the new `dyedil` calculator
entry and the self-test all call one implementation and cannot drift apart — the arrangement
`planInfection()` already uses across three surfaces. When a working dilution needs a volume below
the pipetting floor, `dyeWorking()` builds the intermediate ladder with the existing
`sizeDilutionSeries()` rather than a second implementation of the same idea.

The spectral model deserves an explicit caveat, and carries one in the UI: it approximates each band
as a Gaussian through the published maximum, with an asymmetric split-normal emission (narrower
below the maximum, wider above) because the red tail is what actually bleeds into the next channel.
It catches channel collisions, bleed-through and cross-excitation. It is not a substitute for real
overlap integrals or linear unmixing, and the app does not ship spectral curves.

### 4. Ten new protocols and 27 new recipes

A `Microscopy & staining` protocol group (immunofluorescence on coverslips and in 96-well plates,
phalloidin F-actin, live-cell staining, bacterial live/dead, agarose pads for time-lapse, H&E,
simple/negative smear stains, Schaeffer–Fulton endospore, and TEM negative staining of phage), plus
a `microscopy` recipe category (permeabilisation and blocking buffers, antibody diluent, quench and
retrieval buffers, Mowiol–DABCO and glycerol–NPG antifade mountants, dye stocks, histology stains,
imaging pads and VALAP). Recipes already in the library — PBS, TBS-T, 4% PFA, the Gram reagents,
Loeffler's methylene blue and the four TEM negative stains — are cross-referenced, not duplicated.

## One real error caught along the way

The DAPI record originally said to dilute the 1 mg/mL stock **1:3300** for 300 nM. Working the
arithmetic through for the self-test showed that is wrong: 1 mg/mL DAPI is 2.855 mM, so 300 nM is a
1:9517 dilution. 1:3300 delivers ~865 nM. The published protocols people actually follow say
1:10,000 → 0.1 µg/mL, which is the ~286 nM everyone calls "300 nM DAPI". Fixed, and the corrected
number is now pinned by an assertion.

## Verification

- Extracted the inline `<script>` block and ran `node --check` — passes.
- `?selftest=1` goes from **102/102 to 126/126**, with 24 new assertions covering the dilution
  solver (including the sub-pipettable intermediate case), mass ⇄ molar conversion for DAPI,
  Hoechst 33342 and propidium iodide, stock reconstitution, channel assignment, panel collision and
  bleed-through detection, overlap-index ordering, and the normalisation and red-tail asymmetry of
  the emission model. Every expectation is hand-computed or taken from a vendor spec.
- Driven headless in the pre-installed Chromium: zero page errors, all eleven mode tabs render, the
  dye list loads 79 records, the working dilution rescales live with sample count, the panel builder
  flags a deliberate FITC + Alexa Fluor 488 collision, and notebook capture returns blocks.
- `sw.js` `CACHE` bumped to `dd-v1.7.0` and `./dye-library.json` added to `CORE`, so the new module
  works offline.

---

# Citation audit: 20 wrong PubChem accessions, and a guard against the next one

## What went wrong

The dye and microscopy-recipe records shipped with molecular weights that were
right and PubChem accessions that frequently were not. Cross-checking every
asserted CID against PUG-REST found **16 of 26 wrong in `dye-library.json`** and
**4 more in the microscopy recipes**. They did not point at a near neighbour or a
different salt — they pointed at unrelated molecules:

| Cited for | CID | What that CID actually is |
|---|---|---|
| 7-AAD | 4632 | oxybenzone (a sunscreen) |
| DiBAC4(3) | 5216 | simazine (a herbicide) |
| Phalloidin (×3) | 4753 | phenacemide (an anticonvulsant) |
| JC-1 | 5497144 | bilirubin |
| Fluorescein diacetate | 21100 | metanephrine |
| DiI | 6438393 | 24,25-dihydroxyvitamin D2 |
| Trypan blue | 5904 | penicillin G |
| Calcofluor white | 2724304 | 4-maleimido-TEMPO |
| DABCO | 9270 | ethynodiol diacetate (a progestin) |

The cause was straightforward: the records were written from memory and cited
generic landing pages, and no individual accession was ever fetched to confirm
it. A wrong CID is worse than no CID — it wears the appearance of provenance.

## What held up

Everything a user actually pipettes with:

- **Molecular weights** — all 20 checkable values confirmed against PubChem,
  including the salt and hydrate forms (DAPI dihydrochloride 350.25, Hoechst
  33342 trihydrochloride trihydrate 615.99, acridine orange HCl, resazurin
  sodium salt).
- **Fluorescent protein spectra** — 6/6 exact against the FPbase API: excitation,
  emission, extinction coefficient and quantum yield.
- **Dye spectra** — 9/9 exact against Thermo's own product pages, wherever the
  vendor publishes Ex/Em.
- **Vendor catalogue numbers** — all 14 resolve to the product claimed.
- **Stock concentrations** — confirmed verbatim from the Molecular Probes
  manuals, e.g. MP21486 states "Hoechst 33342 ... (MW 615.99) ... 10 mg/mL
  (16.2 mM)" and MP07510 states the 1 mM anhydrous DMSO stock.

## Corrections made

1. **20 accessions replaced** with CIDs re-queried by name and confirmed by both
   returned title and molecular weight. Where PubChem indexes a different form
   from the one sold, the citation now says so explicitly rather than implying
   the accession matches the stated mass (uranyl acetate, Hoechst 33258, sodium
   citrate dihydrate, potash alum dodecahydrate).
2. **Three working concentrations corrected against the vendor manuals:**
   - LysoTracker range 50–200 nM → **50–75 nM** (MP07525's recommendation).
   - MitoTracker Green FM / Deep Red no longer carry a blanket "serum-free"
     instruction — MP07510's serum caution applies to the *reduced* probe forms,
     which these are not.
   - Calcein AM / EthD-1 are presented as figures to titrate rather than as
     vendor-fixed numbers, since MP03224 gives different values for suspensions
     and says to use the lowest concentration that labels distinctly.
3. **Provenance marked where it is convention, not vendor guidance** — the
   300 nM / 5 min DAPI counterstain and the BacLight 3 µL/mL timing.

## The guard

`tools/verify-citations.py` re-queries PubChem for every accession either library
asserts and compares the returned molecular weight with the one stated beside the
CID. Molecular weight is the discriminating test: a wrong accession nearly always
carries a different mass, whereas a correct one often has a systematic title that
does not textually resemble the common name. It exits non-zero on disagreement so
it can gate a release, and exits 0 when PubChem is unreachable so it never fails a
build for the wrong reason.

    $ python3 tools/verify-citations.py --quiet
    211 accessions verified, 496 stated without a molecular weight, 0 WRONG

It found the four recipe-side errors on its first run, which is the point of it.

## Still unverified

Working concentrations for DAPI and the BacLight kit could not be confirmed from
a primary vendor document — the DAPI manual is image-based and the BacLight PDF
is access-restricted. Sigma-Aldrich blocks automated access entirely, so the
vendor cross-check is single-sourced to Thermo. Those figures are conventional and
now labelled as such.

## Verification

- `tools/verify-citations.py` — 211 accessions verified, 0 wrong, exit 0.
- `?selftest=1` — still **126/126**; this was a data and provenance change with no
  effect on any formula.
- Headless Chromium run: 79 dyes load, filter chips narrow 79 → 5, protocols
  rescale, 243 recipes load, the shared dilution maths still agrees across the
  module and the calculator, and the module still works offline.
