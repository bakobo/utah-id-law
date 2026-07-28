# utah-id-law — when does Utah law require identifying a person?

Primary-source research on **identity-verification duties in Utah law**: which interactions between a
person and the state carry a legal requirement to verify identity, what "verify" means in each, and
which do not.

This is the **baseline that SEDI is layered onto**, and it is a separate repo for a reason.
[`../sedi`](../sedi) is deliberately scoped to SEDI alone after a review found adjacent material
creeping in dressed as SEDI fact. General Utah identity law is adjacent, useful, and *not SEDI* —
so it lives here and is cross-linked, not merged.

## Layout

```
corpus/utah-code/          all 96 titles of the Utah Code as gzipped XML (86 MB → 15 MB)
corpus/admin-rules/        all ~2,295 current administrative rules as gzipped text (44 MB → 12 MB)
corpus/MANIFEST-*.tsv      source URL, retrieval date, bytes, SHA-256 per item
tools/fetch-utah-code.py   refetch the statutes (all titles, or named ones)
tools/fetch-utah-admin-rules.py  refetch the rules (all, or named prefixes)
tools/cite.py              pull verbatim text of a section or rule; search either layer
docs/research-strategy.md  how research here is done — read before starting
findings/                  answered questions, each citing the corpus
sources/registry.md        live URL ⇄ local copy ⇄ retrieval date
```

## Using the corpus

```sh
python3 tools/cite.py 23A-4-601                       # verbatim text of a Code section
python3 tools/cite.py 63G-12                          # a whole chapter
python3 tools/cite.py R657-45-2                       # an administrative rule section
python3 tools/cite.py --grep 'lawful presence'        # Code sections matching a pattern
python3 tools/cite.py --grep 'perjury' --title 26B    # ...within one title
python3 tools/cite.py --grep 'identity' --title R657  # ...across one rule family

rg -z 'proof of identity' corpus/                     # raw search (gzip is transparent to rg -z)
python3 tools/fetch-utah-code.py 23A 63G              # refresh specific titles
python3 tools/fetch-utah-admin-rules.py R657          # refresh a rule family
```

**Check both layers, always.** Statutes delegate heavily. In the fishing probe the statute imposed
no identity requirement at all, and the operative requirement — collect name, date of birth,
address, and physical description — was in the *rule*.

## The one rule

**Quote-or-drop.** Every claim about Utah law must carry a section number *and* a verbatim quote
retrievable from `corpus/`. Models fabricate statute citations fluently and confidently; the corpus
exists so that any citation can be mechanically checked. If the quote cannot be reproduced from a
local file, the claim is deleted rather than hedged. See
[`docs/research-strategy.md`](docs/research-strategy.md).

## Findings so far

- [**Does a Utah fishing license require strong identification?**](findings/fishing-license-probe.md)
  — No. §23A-4-601 conditions issuance on payment of a fee alone, and rule R657-45-2 requires the
  license form to *collect* name, date of birth, address, and a physical description without
  requiring anyone to *verify* it. Across all 64 Wildlife rules the only identity-verification
  requirement is for replacing a lost **lifetime** license (R657-17-8). More broadly, Utah's general
  benefits-verification provision (§63G-12-402) verifies *lawful presence* rather than identity,
  applies only to a defined class of public benefits for applicants 18+, carries a long exemption
  list, and is satisfied for citizens by **certification under penalty of perjury** — attestation
  backed by criminal penalty, not identity proofing.

## Known gaps

Both Utah layers are archived. Still missing, and needed before any "Utah law nowhere requires X"
claim is complete:

1. **Federal program conditions** — 42 C.F.R. §435.940 (Medicaid), 7 C.F.R. §273.2 (SNAP),
   6 C.F.R. Part 37 (REAL ID). These bind specific federally funded programs regardless of what
   Utah's own code says.
2. **Agency practice** — manuals, forms, and unpublished policy, reachable by GRAMA request rather
   than by search.

## Not legal advice

Textual research by non-lawyers. For any specific program the binding answer often sits in an agency
manual or unpublished policy, reachable by GRAMA request rather than by search.
