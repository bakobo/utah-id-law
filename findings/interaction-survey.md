# Survey: which interactions with Utah actually require identification?

Answers the objection that earlier findings were too narrow — they sampled three rule families
(R657, R414, R986) and generalised from them. This sweeps **both corpora without pre-selecting
domains** (`tools/sweep-identity.py`), then reads the hits for the specific interaction types a
person is likely to have with the state.

The sweep buckets language into three legally distinct duties: **PROOFING** (validate a claimed
identity against authoritative evidence), **DOCUMENT** (present a specific credential), and
**COLLECTION** (supply attributes, with no duty on anyone to check them).

## Where the identity duties actually concentrate

Statutes, ranked by proofing language:

| Title | Proof | Doc | Subject |
|---|---|---|---|
| **46** — Notaries Public | 17 | 0 | Notarial acts (gateway to real property) |
| **59** — Revenue and Taxation | 9 | 2 | Tax administration |
| **63A** — Government Operations | 9 | 5 | Records, notarisation, **SEDI** |
| **20A** — Election Code | 7 | 7 | Voter registration |
| **26B** — Health and Human Services | 6 | 31 | Benefits, vital records |
| **78B** — Judicial Code | 6 | 4 | *(mostly false positives — see below)* |
| **53** — Public Safety | 4 | 20 | Driver licensing |
| **32B** — Alcoholic Beverages | 0 | **64** | Proof of age |
| **76** — Criminal Code | 2 | 20 | Proof-of-age offences, fraud |
| **48** — LLCs / partnerships | **0** | **0** | Entity formation |
| **54** — Public Utilities | **0** | **0** | Utility service |
| **10** — Cities and Towns | **0** | **0** | Municipal services |

## Interaction by interaction

### Strong identification required

**Buying or selling real property.** Not by the recorder, but by the **notary** whose acknowledgment
the deed requires. §46-1-2(1) defines an acknowledgment as certifying that a signer's identity is
"*personally known to the notary or proven on the basis of satisfactory evidence*," and §46-1-2(25)
defines "**satisfactory evidence of identity**" as "*unexpired personal identification that includes
the individual's photograph, signature, and physical description.*" The county-recorder rules adopt
that definition by reference (R255-30(27)). This is genuine documentary proofing — but the duty sits
on a **commissioned private notary**, not on a state agency.

**Registering to vote / party affiliation.** §20A-1-102(20) defines "**documentary proof of United
States citizenship**" as a Utah driver licence number or state ID card number "*that verifies United
States citizenship*," among other documents; the registration form also collects the last four SSN
digits (§20A-2-104).

**Buying alcohol or tobacco.** §32B-1-102(100) defines "**proof of age**" as an identification card
or equivalent — expressly *including* a State-Endorsed Digital Identity under Title 63A Ch. 20, and
expressly *excluding* a driving privilege card. §32B-1-407 governs "*verification of proof of age by
applicable licensees*"; tobacco has a parallel regime at §76-9-1117. Again the duty falls on the
**licensed retailer**, not the state.

**Enrolling a child in school.** §53G-6-603 requires the enroller to provide "*a certified copy of
the student's birth certificate*" or "*other reliable proof*" of identity. Documentary, and the duty
is on the parent.

**Medicaid and child care assistance.** As previously found: R414-308-4(4), R986-700-702(3)(a).

### No identification required

**Creating an LLC.** Title 48 contains **zero** occurrences of *proof of identity*, *identification*,
or *social security number*. A Utah LLC can be formed without anyone verifying who the organiser is.

**Filing a GRAMA (public records) request.** §63G-2-204(1)(a) requires only "*the person's name;
mailing address; email address*." Pure self-asserted collection — the closest analogue to the fishing
licence.

**Turning on utilities / paying a city water bill.** Title 54 (Public Utilities) and Title 10 (Cities
and Towns) contain no identity-proofing or SSN language at all. Whatever a utility asks for is its
own credit policy, not a state legal requirement.

**Filing a complaint with a state ombudsman.** Effectively nothing across the corpus.

**Fishing licence.** §23A-4-601(2) — fee only; R657-45-2(2) mandates *collection* of name, DOB,
address and physical description without any duty to verify.

### Genuinely uncertain

**Filing a court petition.** The Title 78B proofing hits are **false positives**: §78B-3-112 is a
blockchain-definitions section that happens to define "proof of identity," and §78B-6-817 concerns
law enforcement identifying trespassers. Neither is about filing. But civil procedure in Utah is set
by the **Utah Rules of Civil Procedure**, promulgated by the Utah Supreme Court — a third body of law
in **neither corpus**. Treat court filing as unresolved.

## Two corrections to the earlier framing

1. **The locus of the duty matters as much as its existence.** In the strongest cases — real
   property, alcohol, tobacco, school enrolment — the verification duty falls on a **notary, licensed
   retailer, or parent**, not on a state agency. "The state requires strong identification" and "a
   state agency must strongly identify you" are different propositions, and the second is rarer than
   the first.
2. **Keyword hits require reading.** Title 78B looked like the fourth-strongest proofing title until
   the hits turned out to be about blockchain. Any count in the table above is a pointer to read, not
   a finding.

## Methodological gap

Three bodies of law bear on these questions; this repo holds two. Missing: **Utah Rules of Civil
Procedure / Rules of Evidence** (Supreme Court), and the **federal** conditions (42 C.F.R. §435.406,
7 C.F.R. §273.2, 6 C.F.R. Part 37) read here only through the Utah rules implementing them.
