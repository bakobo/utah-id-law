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
| **Utah Administrative Code** (agency rules) | ✅ all ~2,295 current rules, `corpus/admin-rules/` |
| **Federal conditions** (PRWORA, CFR program rules) | ◐ 8 U.S.C. §1621 only |
| **Agency practice** (manuals, forms) | ❌ GRAMA-request territory, not corpus-searchable |

The rules layer matters disproportionately, because statutes routinely delegate — and in the fishing
probe it changed the answer. The statute imposes no identity requirement at all; the *rule*
(R657-45-2) requires the license form to collect name, date of birth, address, and a physical
description. Never conclude from statute alone.

### Admin rules — how the API was cracked (2026-07-28)

There is **no official bulk download and no documented API**. `adminrules.utah.gov` is a React SPA
(built by Tecuity); `rules.utah.gov/publications/utah-administrative-code/` links to the SPA rather
than to files, and the Office's own guidance is to phone or email. The working endpoints below were
recovered by reading the SPA's JS bundle, `/static/js/main.*.chunk.js`.

Two quirks made this hard, and neither is guessable:

1. **Missing path parameters are sent as the literal string `"undefined"`,** not omitted. Every
   attempt with real-looking values returned 400; `undefined` in the id slot returns 200.
2. **`searchRuleDataTotal` takes (searchTerm, ruleType), not (query, page).** Passing a page number
   as the second argument silently returns the agency/program skeleton with `rules: []`, which
   reads like an empty result set rather than a wrong call. The correct second argument is a rule
   type such as `Current Rules`.

The pipeline, two calls deep:

```sh
# 1. Enumerate the entire code. Any single-letter search term returns all ~2,295 rules,
#    each with its agency, program, effective date, and htmlDownload path.
curl 'https://adminrules.utah.gov/api/public/searchRuleDataTotal/a/Current%20Rules'

# 2. Fetch one rule's full text using the htmlDownload path from the index.
curl 'https://adminrules.utah.gov/api/public/getHTML/uac-html/<guid>.html'

# Rule metadata by reference number, if you have the number but not the index:
curl 'https://adminrules.utah.gov/api/public/rule/R657-13/undefined/Current%20Rules'
```

Implemented in `tools/fetch-utah-admin-rules.py`. Endpoints that do **not** work publicly:
`/api/program/{id}/currentrules` → 500 (authenticated), and `/api/public/getfile/` → 404 for the
`uac-pdf` paths.

### Alternative bulk sources (researched, rejected)

- **`rules.utah.gov/publicat/code_zip/r{NNN}.zip`** — per-title RTF archives, still live and
  returning 200 (r657.zip = 960 KB, 59 RTF files). **But the contents are dated April 2020**, a
  stale snapshot from before the eRules migration. Useful only for enumerating historical rule
  numbers or diffing against 2020. Do not quote current law from these.
- **`rules.utah.gov/publications/code-updates/`** — monthly ZIPs of *changed* rules as `.docx`
  plus `.xlsx` change reports, archived back to 2010, each with an MD5. This is the best source
  for **change tracking over time**, and the natural basis for a periodic re-fetch, but it is
  incremental rather than a full snapshot.
- **Directory listings** (`/publicat/code/`, `/publicat/code_zip/`) — 403, no index.
- **An official XML/JSON export** — none found; the Office suggests contacting them
  (`rulesonline@utah.gov`) if one is needed.

Codification cadence: the Code is updated by the 10th of each month with filings effective through
the 1st. Re-fetch monthly if currency matters; the manifest's SHA-256 column makes the diff cheap.

## 6. Provenance discipline

- `corpus/MANIFEST-utah-code.tsv` records URL, version stamp, retrieval date, byte count, and
  SHA-256 for every title. Re-running the fetcher and diffing hashes shows exactly what changed.
- The version stamp (`C63A_2021050520210701`) is an opaque version identifier from le.utah.gov's
  master index. It pins a *version*, which is what a citation needs. It does **not** encode an
  effective-date range, which this line claimed until 2026-09-16: 73 of the 96 titles carry the
  sentinel `1800010118000101`, Title 75A's stamp runs `20240901` then `20240501`, and Title 23A is
  stamped 2023 while its text carries 2025 amendments. The stored text is the current consolidated
  version **as of the retrieval date**, and the retrieval date is what bounds it.
- `corpus/<layer>/MANIFEST.tsv` restates the same corpus in the schema shared with the sibling
  repos, so `lawcite` can quote it with a validity banner and a digest check. Rebuild it with
  `tools/build-kit-manifests.py` after any fetch; the `MANIFEST-*.tsv` files remain the harvest log.
- `sources/registry.md` follows the `../sedi` convention: live URL ⇄ local copy ⇄ retrieval date.
- Corpus files are stored gzipped (86 MB → 15 MB) and stay searchable via `rg -z`.

## 7. Standing cautions

- **Not legal advice.** This is textual research. For a specific program the binding answer often
  lives in an agency manual or unpublished policy, reachable by GRAMA request rather than search.
- **Statutes change.** Findings cite retrieval dates and version stamps for this reason. Re-fetch
  before relying on an old finding.
- **Scope guard.** This repo is Utah identity-verification law *generally*. SEDI-specific statutory
  analysis belongs in `../sedi`, which is deliberately scoped to SEDI only. Cross-link; do not merge.
  **The guard is about the programme, not about the chapter, and reading it the other way cost this
  repo a chapter.** Title 63A Ch. 20 went uncited for seven weeks because its title says
  *State-Endorsed Digital Identity* and that was taken as enough to send all eighteen sections away —
  including §63A-20-303, the corpus's only strict identity-proofing duty, and §63A-20-302(7)(a), its
  clearest minimisation ceiling. Both bear directly on the question at the top of this document. A
  provision belongs to `../sedi` when the answer it gives is *about the programme*: its governance,
  its wallet and verifier obligations, its rollout. It belongs here when the answer it gives is about
  what Utah law demands of a person's identity, whatever instrument happens to carry it. When in
  doubt, read it here and cross-link. See [`../findings/digital-identity-chapter-probe.md`](../findings/digital-identity-chapter-probe.md).
- **Duties run in two directions, and the tooling only sees one.** The four-way table in §1 and all
  five buckets in `tools/sweep-identity.py` describe ways of *requiring* identification. A provision
  that forbids collecting or retaining it — the `prohibited-identification` direction — matches none
  of them and cannot surface from any sweep at any threshold. Ten such provisions are now known, in
  titles 13, 26B, 34 and 63A; there is no reason to think that list is complete, because nothing
  systematic has ever looked for them.
