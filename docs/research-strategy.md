# Research strategy — Utah identity-verification law

How this repo answers questions of the form *"does Utah law require the state to identify a person
before doing X?"* The method matters more than any single answer, because the failure mode in
AI-assisted legal research is not sloppiness — it is **fluent, confident, fabricated citation**.

## 1. Decompose the claim before researching it

Most disputes here are definitional, and separating the terms often resolves them faster than
research does. Four distinctions do the work:

**"Entitlement" is not a legal term.** The operative terms are `state or local public benefit`
(8 U.S.C. §1621(c)) and `federal public benefit` (§1611(c)), both closed definitions. A thing that
feels like an entitlement may be neither — a recreational license is not, because the applicant pays
the state rather than receiving payments or assistance.

**"Strong identification" appears nowhere in the Utah Code** (0 hits). Four distinct duties get
conflated under it:

| Duty | What it establishes | Typical statutory phrasing |
|---|---|---|
| Identity assertion | A name is on record | "shall provide the applicant's name" |
| Identity proofing | The claimed identity is real and belongs to the claimant (~NIST IAL2) | "proof of identity", "documentary evidence" |
| Status verification | An attribute — lawful presence, age, residency — holds | "verify the lawful presence" |
| Authentication | A returning user is the same person as the record (~NIST AAL) | "credential", "multifactor" |

A statute demanding the third does not demand the second. §63G-12-402 demands the third, and even
then accepts attestation.

**State law vs. federal conditions.** Many real duties on Utah agencies arrive as conditions on
federal funds (Medicaid, SNAP, unemployment, REAL ID). They bind *those programs*, not "any
interaction with the state." A universal claim cannot rest on program-specific federal conditions —
and their program-specificity is itself evidence against universality.

**Quantifier asymmetry.** A universal claim ("any time…") is refuted by one well-sourced
counterexample; it is *established* only by a general provision. Whoever asserts the universal owes
the citation. Refutation is cheap, so do it first — then, if the question stays live, run the sweep.

## 2. Corpus first, model second

**Every claim about Utah law must be produced by `tools/cite.py`, not from memory.** A model asked
"what does Utah law require for X" will produce a plausible section number with a plausible
quotation, and both may be inventions. The corpus makes this mechanically checkable: a finding cites
`23A-4-601`, and anyone can run `python3 tools/cite.py 23A-4-601` and see whether the quoted words
are there.

Operational rule for any agent or panel working in this repo:

> **Quote-or-drop.** A claim about Utah law is admissible only with (a) a section number and (b) a
> verbatim quotation retrievable from `corpus/`. If the quote cannot be reproduced from the corpus,
> the claim is deleted — not hedged, not softened. "I recall that Utah requires…" is not evidence.

Retrieval is `rg -z` and `tools/cite.py --grep` over the corpus, never recall.

## 3. Searching well — the phrase-family problem

Keyword search under-detects, because statutes express the same duty many ways. Any sweep intended
to support a *negative* conclusion ("no such requirement exists") must run the whole family, not one
phrase:

- **Proofing:** `proof of identity`, `verif\w+ the identity`, `identity verification`,
  `establish the .{0,20}identity`, `documentary evidence`, `satisfactory evidence of identity`
- **Document presentation:** `present .{0,30}(driver license|identification card)`,
  `valid .{0,20}identification`, `government-issued`, `photo identification`
- **Attestation (the competing design):** `under penalty of perjury`, `certif\w+ under penalty`,
  `sworn statement`, `affidavit`, `attest`
- **Status checks:** `lawful presence`, `SAVE program`, `status verification system`, `E-verify`
- **Identifiers as proxies:** `social security number`, `date of birth`, `biometric`

Two search-design rules, both learned the hard way in §7 of the fishing probe:

1. **Search for the competing design too.** Finding 89 "penalty of perjury" against 17
   "verify the identity" is a stronger result than either count alone, because it shows the
   legislature had a verification option available and chose otherwise.
2. **Report where hits cluster, not just how many.** The distribution (tax, courts, elections) was
   more probative than the totals.

Negative results need an explicit caveat: absence of a phrase family is evidence of absence, not
proof of it.

## 4. Panel design — adversarial, not survey

Fan out only after the cheap probe. Structure:

- **Steelman** — build the strongest case *for* the claim under test. Broadest defensible reading,
  every provision that could support it. Run this first; if the steelman comes back thin, the
  question may be closed already.
- **Refuter** — hunt counterexamples, and hunt exemption lists specifically. §63G-12-402(3) was
  worth more than any amount of argument, because a legislature enumerating entitlements exempt from
  verification has refuted the universal claim in its own words.
- **Definitions** — resolve the terms of art against the four-way table in §1.
- **Domain probes, in parallel** — one per program family: recreational licensing (23A),
  professional licensing (58), health and human services (26B), education (53E–53H), motor vehicles
  (53), elections (20A), tax (59), vital records. Each answers: what duty, from which provision,
  with what scope conditions and exemptions.
- **Verifier** — one adversarial pass per surviving claim, prompted to *refute*, with corpus access.
  Its job is to break the quote-to-claim link, not to agree.
- **Cross-model check** — put the final conclusion to `codex exec` or `gemini -p`. Different model,
  genuine perspective variety on a reasoning question, and cheap.

Respect the machine limits in `~/.claude/CLAUDE.md`: at most 2 general-purpose subagents at once
(3–4 if the extras are read-only), and `nice -n 19` for anything heavy.

## 5. Layers — and which are still missing

A complete answer spans four layers. The corpus currently covers one and a half.

| Layer | Status |
|---|---|
| **Utah Code** (statute) | ✅ all 96 titles, `corpus/utah-code/` |
| **Utah Administrative Code** (agency rules) | ❌ **not retrieved** — see below |
| **Federal conditions** (PRWORA, CFR program rules) | ◐ 8 U.S.C. §1621 only |
| **Agency practice** (manuals, forms) | ❌ GRAMA-request territory, not corpus-searchable |

The rules layer matters disproportionately, because statutes routinely delegate. §23A-4-601 issues
licenses "in accordance with the rules… of the Wildlife Board." If a fishing-license identity
requirement exists, that is where it would be.

### Admin rules — what worked and what didn't (2026-07-28)

`adminrules.utah.gov` is a React SPA with no bulk download; `rules.utah.gov/publications/
utah-administrative-code/` links to the SPA rather than to files. Probing its API:

- ✅ `GET /api/public/agencies` → 48 agencies as JSON
- ✅ `GET /api/public/programs/{agencyId}` → programs (Natural Resources = 31 → Wildlife Resources
  = id 122, number 657)
- ⚠️ `GET /api/public/searchRuleDataTotal/{query}/{page}` → 200, but returns the agency/program
  skeleton with `rules: []` — it appears to serve counts, not rows
- ❌ `GET /api/public/rule/{a}/{b}/{c}` → 400 on every parameter shape tried (rule numbers,
  numeric ids, publication names); the route matches but the argument types are wrong
- ❌ `GET /api/program/{id}/currentrules` → 500 (likely authenticated, not public)
- ❓ `GET /api/public/getHTML/{id}` → needs a numeric rule id we could not yet enumerate

**Next step:** the missing piece is the rule-listing call. Either read the paginated-search code path
in `/static/js/main.*.chunk.js` more carefully, or capture the network trace from a real browser
session on a rule page and copy the exact request. Once a rule id is in hand, `getHTML` should give
the text. Do **not** treat the statute corpus as complete without this layer.

## 6. Provenance discipline

- `corpus/MANIFEST-utah-code.tsv` records URL, version stamp, retrieval date, byte count, and
  SHA-256 for every title. Re-running the fetcher and diffing hashes shows exactly what changed.
- The version stamp (`C63G-12_1800010118000101`) encodes the text's effective-date range, so a
  citation pins a *version*, not just a section.
- `sources/registry.md` follows the `../sedi` convention: live URL ⇄ local copy ⇄ retrieval date.
- Corpus files are stored gzipped (86 MB → 15 MB) and stay searchable via `rg -z`.

## 7. Standing cautions

- **Not legal advice.** This is textual research. For a specific program the binding answer often
  lives in an agency manual or unpublished policy, reachable by GRAMA request rather than search.
- **Statutes change.** Findings cite retrieval dates and version stamps for this reason. Re-fetch
  before relying on an old finding.
- **Scope guard.** This repo is Utah identity-verification law *generally*. SEDI-specific statutory
  analysis belongs in `../sedi`, which is deliberately scoped to SEDI only. Cross-link; do not merge.
