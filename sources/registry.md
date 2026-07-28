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

## 3. Utah Administrative Code (primary — archived in full)

| Live | Local | Note |
|---|---|---|
| https://adminrules.utah.gov/public/home | `../corpus/admin-rules/*.txt.gz` | **All ~2,295 current rules**, retrieved 2026-07-28 via the undocumented SPA API. Stored as extracted text (~44 MB → ~12 MB); the manifest records each rule's source URL and the **SHA-256 of the original HTML**. Refetch with `tools/fetch-utah-admin-rules.py`; read with `tools/cite.py R657-45-2`. |

There is **no official bulk download and no documented API** — the endpoints were recovered from the
SPA's JS bundle. Recipe, quirks, and rejected alternatives: `../docs/research-strategy.md` §5.
The Code is recodified monthly (by the 10th, for filings effective through the 1st), so a refetch
plus a manifest hash-diff is the currency check.

Rules load-bearing so far:

- **R657-45-2** — Wildlife license/permit forms **shall include** customer ID number, name, date of
  birth, address, height, weight, eye color, hair color, gender. Applies to hunting *and fishing*.
  Mandates identity **collection**; imposes no verification.
- **R657-13** — Taking Fish and Crayfish. The operative fishing rule; zero identity content.
- **R657-17-8** — Lost/stolen **lifetime** license: duplicate requires "providing verification of
  identity." The only genuine identity-verification requirement in the 64 R657 rules.
- **R657-19**, **R657-62** — Application contents (SSN, driver-license number, DOB) and
  point-tracking identifiers. Collection and record-linking, not proofing.

Other rule families of interest, now retrievable: **R986-** (Workforce Services / public
assistance), **R414-** (Medicaid), **R156-** (professional licensing / DOPL).

Other publication channels:

- Utah State Bulletin (semi-monthly PDFs): https://rules.utah.gov/publications/utah-state-bulletin/
- Monthly code-update ZIPs (changed rules as `.docx`, plus `.xlsx` change reports, back to 2010,
  each with an MD5) — the right source for **change tracking**:
  https://rules.utah.gov/publications/code-updates/
- ⚠️ **Stale trap:** `https://rules.utah.gov/publicat/code_zip/r{NNN}.zip` still returns 200 with
  per-title RTF archives, but the contents are an **April 2020 snapshot** predating the eRules
  migration. Do not quote current law from these.

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
3. **"The statute settles it."** ❌ It usually doesn't. In the fishing probe the statute imposed no
   identity requirement at all, while the *rule* (R657-45-2) required the license form to collect
   name, date of birth, address, and a physical description. Always check both layers before
   concluding. What survived the rules layer was the narrower distinction: **collection is mandated,
   proofing is not.**
4. **Rule text can lag statutory recodification.** R657-13 still cross-references "Section 23-19-18"
   — the pre-2023 Title 23 numbering, since recodified to Title 23A. Do not assume a rule's internal
   citations match current Code numbering.
