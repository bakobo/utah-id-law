# Source registry — Utah identity-verification law

Live URL ⇄ local copy ⇄ retrieval date, following the `../sedi/sources/registry.md` convention.
**Trust order:** statute and CFR text > official agency publication > case law > commentary.

## 1. Utah Code (primary — archived in full)

| Live | Local | Note |
|---|---|---|
| https://le.utah.gov/xcode/code.html | `../corpus/utah-code/*.xml.gz` | **All 96 titles**, whole-title XML, retrieved 2026-07-28. 86 MB raw / 15 MB gzipped. Per-title URL, version stamp, byte count, and SHA-256 in `../corpus/MANIFEST-utah-code.tsv`. Refetch with `tools/fetch-utah-code.py`; read with `tools/cite.py`. |

Version stamps encode the effective-date range (`C63G-12_1800010118000101`), so a citation pins a
specific version of the text. Sections load-bearing so far:

- **§23A-4-601** — Fishing license. Requires payment of a fee; no identity element.
- **§23A-4-202** — License form prescribed by Wildlife Board (delegation to rules).
- **§23A-4-1101** — Fraud in obtaining a license; class B misdemeanor.
- **§63G-12-402** — Receipt of public benefits: verification, exceptions, penalties. The general
  provision. Verifies *lawful presence*, not identity; method is certification under penalty of
  perjury, with SAVE only for the non-citizen branch.
- **§26B-1-202(2)(pp)** — Department authority re: provider identity coordination. The sole
  identity-verification reference in the Health and Human Services title.
- **§63A-12-117** — Electronic records / notarization-grade identity verification.
- **§63A-20-204** — SEDI use cases. (SEDI analysis proper lives in `../../sedi`.)

## 2. Federal law

| Live | Local | Note |
|---|---|---|
| https://www.law.cornell.edu/uscode/text/8/1621 | *(not archived — quoted in findings)* | **8 U.S.C. §1621**, definition of "state or local public benefit" at (c)(1). The hinge for whether a given interaction triggers §63G-12-402. Retrieved 2026-07-28. |
| https://www.law.cornell.edu/uscode/text/8/1611 | — | §1611, "federal public benefit". Not yet pulled. |
| https://www.law.cornell.edu/uscode/text/8/1641 | — | §1641, "qualified alien". Not yet pulled. |

⚠️ **Gap.** Program-level federal identity/eligibility rules are not yet retrieved and are needed
before any claim about Medicaid/SNAP/UI identity duties: 42 C.F.R. §435.940 et seq. (Medicaid
citizenship/identity), 7 C.F.R. §273.2 (SNAP), 6 C.F.R. Part 37 (REAL ID).

## 3. Utah Administrative Code — **NOT YET RETRIEVED**

The rules layer is missing and matters: statutes delegate heavily (§23A-4-601 issues licenses
"in accordance with the rules… of the Wildlife Board").

- Browse UI: https://adminrules.utah.gov/public/home
- Publications page (links to the SPA, no bulk files): https://rules.utah.gov/publications/utah-administrative-code/
- Utah State Bulletin: https://rules.utah.gov/publications/utah-state-bulletin/
- Working API primitives and the specific blocker: see `../docs/research-strategy.md` §5.
- Rules of interest when access is solved: **R657-** (Wildlife Resources), **R986-** (Workforce
  Services / public assistance), **R414-** (Medicaid).

## 4. Cross-references

- `../../sedi/` — SEDI dossier (Title 63A Ch. 20). Scoped to SEDI only; this repo holds the
  general Utah identity-law baseline SEDI is layered onto.
- `../../landscape/` — competitive and standards-landscape research.

## ⚠ Verification flags

1. **"63G-12 is the Identity Documents and Verification Act."** ❌ Wrong — an assumption made and
   corrected during the 2026-07-28 probe. Title 63G Chapter 12 is the **Utah Immigration
   Accountability and Enforcement Act**. The benefits-verification provision is §63G-12-402, inside
   that act. The label matters when reasoning about the provision's purpose and scope.
2. **Keyword counts are directional, not dispositive.** The §7 sweep in
   `../findings/fishing-license-probe.md` counts phrases, not duties. A statute can impose
   verification without using any searched phrase. Do not cite the counts as proof of absence.
3. **Corpus is statute-only.** Any claim of the form "Utah law nowhere requires X" is unproven until
   the Administrative Code layer is retrieved.
