#!/usr/bin/env python3
"""Check every PubChem accession this repo cites against PubChem itself.

Why this exists
---------------
The libraries state a molecular weight and, next to it, a PubChem CID. A wrong
CID is worse than no CID: it looks like provenance while pointing at an unrelated
molecule. That is not hypothetical — the first version of dye-library.json cited
CID 4632 for 7-AAD (it is oxybenzone), CID 5216 for DiBAC4(3) (simazine) and CID
4753 for phalloidin (phenacemide). Sixteen of twenty-six were wrong. The
molecular weights were right; only the accessions were invented.

What it checks
--------------
For every "PubChem CID <n> ... MW <m>" claim, it asks PUG-REST for that CID and
compares the molecular weight PubChem returns with the one stated alongside the
CID. Molecular weight is the discriminating test: an accession pointing at the
wrong molecule almost always carries a different mass, whereas a compound's
systematic title often will not textually resemble its common name (PubChem
calls calcofluor white "2,2'-(1,2-Ethenediyl)bis(...)").

Citations that deliberately reference a different form from the one sold — "CID
1464 is the free base (MW 452.55); the trihydrochloride trihydrate sold for
staining is MW 615.99" — are handled by comparing against the FIRST molecular
weight after the CID, which is the one belonging to that accession.

Usage
-----
    python3 tools/verify-citations.py            # check everything
    python3 tools/verify-citations.py --quiet    # only report failures

Exit status is non-zero if any accession disagrees, so it can gate a release.
Needs network access; skips cleanly (exit 0) if PubChem is unreachable, so it
never fails a build for the wrong reason.
"""
import json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUG = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/property/MolecularWeight,Title/JSON'
TOL_ABS, TOL_REL = 0.5, 0.002        # PubChem rounds to 1 dp; 0.2% covers the rest

# "PubChem CID 1464 is the free base (MW 452.55)" / "PubChem CID 6503 - tris..., MW 121.14"
# / "PubChem - Magnesium sulfate heptahydrate, CID 24843, MW 246.48"
CID_MW = re.compile(r'CID[\s:]*(\d+)(.{0,160}?)MW[\s:]*([\d.]+)', re.S | re.I)
CID_ANY = re.compile(r'CID[\s:]*(\d+)', re.I)


def claims_from(path, label):
    """Yield (source_label, item_name, cid, stated_mw_or_None) for one library."""
    with open(path) as fh:
        lib = json.load(fh)
    for cat in lib.get('categories', []):
        for item in cat.get('dyes', []) + cat.get('recipes', []):
            name = item.get('name', '?')
            blobs = [item.get('mwSource') or '']
            blobs += [c.get('mwSource') or '' for c in item.get('components', [])]
            blobs += [s.get('title') or '' for s in item.get('sources', [])]
            for blob in blobs:
                if not blob:
                    continue
                seen = set()
                for m in CID_MW.finditer(blob):
                    cid = int(m.group(1)); seen.add(cid)
                    yield (label, name, cid, float(m.group(3)))
                for m in CID_ANY.finditer(blob):      # CID with no MW beside it
                    cid = int(m.group(1))
                    if cid not in seen:
                        seen.add(cid)
                        yield (label, name, cid, None)


def fetch(cids):
    out = {}
    for i in range(0, len(cids), 100):
        chunk = cids[i:i + 100]
        url = PUG.format(','.join(map(str, chunk)))
        with urllib.request.urlopen(url, timeout=60) as r:
            for p in json.loads(r.read())['PropertyTable']['Properties']:
                out[p['CID']] = (float(p['MolecularWeight']), p.get('Title', ''))
    return out


def main():
    quiet = '--quiet' in sys.argv
    claims = []
    for fn, label in (('dye-library.json', 'dye'), ('reagent-library.json', 'reagent')):
        p = os.path.join(ROOT, fn)
        if os.path.exists(p):
            claims += list(claims_from(p, label))
    if not claims:
        print('no PubChem accessions found — nothing to check')
        return 0

    cids = sorted({c[2] for c in claims})
    try:
        props = fetch(cids)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        print(f'PubChem unreachable ({e}); skipping accession check')
        return 0

    bad, unchecked, ok = [], 0, 0
    for label, name, cid, mw in claims:
        got = props.get(cid)
        if got is None:
            bad.append((label, name, cid, mw, None, 'CID does not exist'))
            continue
        pmw, title = got
        if mw is None:
            unchecked += 1
            if not quiet:
                print(f'  ?  {label:8} {name[:34]:34} CID {cid:<9} no MW stated beside it — '
                      f'PubChem says {pmw:.2f} ({title[:30]})')
            continue
        if abs(pmw - mw) <= max(TOL_ABS, mw * TOL_REL):
            ok += 1
            if not quiet:
                print(f'  ok {label:8} {name[:34]:34} CID {cid:<9} {mw:>9.2f} == {pmw:.2f}')
        else:
            bad.append((label, name, cid, mw, pmw, title))

    print()
    print(f'{ok} accessions verified, {unchecked} stated without a molecular weight, {len(bad)} WRONG')
    if bad:
        print('\nAccessions that disagree with PubChem:')
        for label, name, cid, mw, pmw, title in bad:
            shown = f'{pmw:.2f}' if isinstance(pmw, float) else '—'
            print(f'  {label:8} {name[:40]:40} CID {cid}: cited MW {mw}, PubChem {shown}  {title}')
        print('\nFix the CID (or drop it) — do not adjust the molecular weight to match.')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
