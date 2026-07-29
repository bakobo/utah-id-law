# utah-id-law — when does Utah law require identifying a person?

**This is a share of research findings and the primary sources behind them. Nothing more.**

It is offered **without warranty of any kind** and **without any claim of legal gravitas**. It was
produced by non-lawyers doing textual research, with substantial AI assistance. It is not legal
advice, not an authoritative statement of Utah law, and not a substitute for a lawyer. If something
here matters to a decision you are making, verify it against the authoritative sources — which are
linked from every claim — and talk to someone qualified.

What it *is*: a searchable local copy of three bodies of Utah law, a small set of tools for quoting
and searching them, and a handful of written-up questions with every assertion tied to a citation you
can check yourself. The value is in the sources and the traceability, not in our authority. We have
none.

## The question

Which interactions between a person and the state of Utah carry a legal requirement to verify
identity, what "verify" means in each, and which carry no such requirement at all.

The short answer: **Utah has no general identity-assurance baseline.** Requirements are set
interaction by interaction and range from nothing, through attestation, to documentary proof. See
[`findings/identity-duties-summary.md`](findings/identity-duties-summary.md).

## Three layers, and why all three matter

| Corpus | Made by | Size |
|---|---|---|
| **Utah Code** (statute) | The legislature | 96 titles |
| **Utah Administrative Code** (rules) | Agencies, under authority delegated in statute | 2,294 rules |
| **Utah court rules** | The Utah Supreme Court, under its rulemaking power | 661 rules |

Checking one layer is not enough, and this was learned the hard way twice. The fishing-licence
identity requirements turned out to exist **only** in the administrative rules, with nothing in the
statute. The court-filing question was simply unanswerable until the court rules were added.

## Layout

```
corpus/utah-code/                 96 titles, version-stamped XML, gzipped (86 MB → 15 MB)
corpus/admin-rules/               2,294 current rules, extracted text, gzipped (36 MB → 16 MB)
corpus/court-rules/               661 rules across six sets (URCP, URCrP, URE, URAP, URJP, UCJA)
corpus/MANIFEST-*.tsv             source URL, retrieval date, bytes, SHA-256 per item
tools/fetch-utah-code.py          refetch statutes (all titles, or named)
tools/fetch-utah-admin-rules.py   refetch admin rules (all, or named prefixes)
tools/fetch-utah-court-rules.py   refetch court rules (all, or named sets)
tools/cite.py                     quote a section or rule; search any layer
tools/sweep-identity.py           map identity-duty language across all three corpora
docs/research-strategy.md         how the research is done — read before adding to it
findings/                         written-up questions, each citing the corpus
sources/registry.md               live URL ⇄ local copy ⇄ retrieval date
```

## Using it

```sh
python3 tools/cite.py 23A-4-601                       # a Utah Code section
python3 tools/cite.py 63G-12                          # a whole chapter
python3 tools/cite.py R657-45-2                       # an administrative rule section
python3 tools/cite.py URCP-11                         # a court rule
python3 tools/cite.py --grep 'lawful presence'        # Code sections matching a pattern
python3 tools/cite.py --grep 'identity' --title R657  # ...across one rule family
python3 tools/cite.py --grep 'oath' --courts          # ...across the court rules
python3 tools/sweep-identity.py                       # where identity duties concentrate

rg -z 'proof of identity' corpus/                     # raw search; rg -z reads gzip directly
```

## The one working rule

**Quote-or-drop.** Every claim about Utah law must carry a citation *and* a verbatim quote
retrievable from `corpus/`. Language models fabricate statute citations fluently and confidently; the
corpus exists so that any citation can be checked mechanically rather than trusted. If a quote cannot
be reproduced from a local file, the claim is deleted rather than softened. See
[`docs/research-strategy.md`](docs/research-strategy.md).

Two worked examples of why. Title 78B once ranked among the top identity-proofing titles in a keyword
sweep — until the hits turned out to be a *blockchain* definitions section. And an adversarial review
of the sweep tool itself (2026-07-29) found its patterns could not see `verify the victim's identity`
(a possessive noun) and that its document-presentation pattern matched *nothing at all*, which had
produced a published "zero requirements" claim that was false. Counts are pointers to read, never
findings — including our own. Corrections are marked inline in the affected files.

## Findings

- [**Summary: when does Utah law require identifying a person?**](findings/identity-duties-summary.md)
  — the overview, with citations.
- [**Fishing licence probe**](findings/fishing-license-probe.md) — the origin question. §23A-4-601
  conditions a licence on paying a fee; rule R657-45-2 requires the form to *collect* name, date of
  birth, address and physical description without requiring anyone to *verify* it.
- [**Survey across interaction types**](findings/interaction-survey.md) — LLC formation, records
  requests, utilities, real property, voter registration, alcohol and tobacco, school enrolment.
- [**Courts, bail, testimony, jail visits**](findings/courts-bail-jail-probe.md) — no court rule
  requires proving identity to file, testify or post bail; the nine rules that do impose identity
  duties attach to records access, courthouse security, and compulsory process against defendants.
- [**Traffic stops and parking tickets**](findings/traffic-stop-parking-probe.md) — the sharpest
  contrast in the repo. A lawful stop compels disclosure of name or date of birth (§76-8-301.5,
  class B misdemeanour) and a driver must display a licence (§53-3-217); paying a parking ticket
  has no identity requirement in state law at all.

## Known gaps

State law is covered; these are not, and no "Utah law nowhere requires X" claim is complete without
them:

1. **Federal program conditions** — 42 C.F.R. §435.406/407 and §435.940 (Medicaid), 7 C.F.R. §273.2
   (SNAP), 6 C.F.R. Part 37 (REAL ID). These bind specific federally funded programs regardless of
   what Utah's own law says, and several of the strongest requirements found here originate there.
2. **Agency practice** — manuals, forms, and unpublished policy, reachable by a GRAMA request rather
   than by search.
3. **Local government** — county and municipal policy. County jail visitor rules, utility connection
   requirements, and parking ordinances are local operational policy and appear in none of these
   corpora.
4. **Case law** — no judicial decisions are held here. For most questions the statutory text carries
   the answer, but not all: what a traffic-stop identification duty means in practice turns on
   Fourth and Fifth Amendment doctrine and on Utah appellate decisions construing the statute.

The findings are also **samples, not an exhaustive reading** of ~3,100 instruments. Absence of a
requirement in an unexamined corner cannot be excluded.

## Provenance and currency

Every manifest records the source URL, retrieval date, byte count, and SHA-256 for each item, so a
refetch can be diffed to see exactly what changed. Statute files carry a version stamp encoding the
text's effective-date range, so a citation pins a *version*, not just a section. The Administrative
Code is recodified monthly; court rules and statutes change on their own schedules. **Everything here
was retrieved in late July 2026** — re-fetch before relying on it.

## Licence

The **original work** — findings, research strategy, source registry, and the tooling under
`tools/` — is licensed **[CC BY 4.0](LICENSE)**. Attribution appreciated: Bakobo, *utah-id-law*.

The **corpora under `corpus/` are not covered by that licence and are not ours to license.** They are
the text of Utah statutes, administrative rules, and court rules — edicts of government, which carry
no copyright. They are redistributed as retrieved, with provenance in the manifests. The
authoritative sources remain [le.utah.gov](https://le.utah.gov/xcode/code.html),
[adminrules.utah.gov](https://adminrules.utah.gov/public/home), and
[utcourts.gov](https://www.utcourts.gov/rules).

The admin-rules and court-rules corpora store **extracted text** rather than the served HTML, for the
size reasons documented in each fetcher. Quote from them freely — but for anything load-bearing,
verify against the live source. The manifests tell you exactly where to look.
