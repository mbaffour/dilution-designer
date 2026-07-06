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
