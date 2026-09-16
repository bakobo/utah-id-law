# Title 63A Chapter 20: the chapter in our own corpus that no finding cited

A comparative pass across nine identity-law corpora asked each one whether its jurisdiction has a
general identity-assurance baseline, and in passing noticed that this repo holds a whole chapter of
the Utah Code about identity proofing which none of its findings cites. That is right, and it is
worth saying plainly how a chapter sitting in `corpus/utah-code/` for seven weeks went unread.

> **Recorded 2026-09-16.** This was not a sampling gap. Every earlier sweep *saw* Title 63A — the
> interaction survey ranks it with 11 proofing hits and names SEDI in the same table row, and
> `sources/registry.md` cites §63A-20-204 by number. Three things then kept it from being read.
> **First, a scope guard sent it away**: `docs/research-strategy.md` §7 says "SEDI-specific statutory
> analysis belongs in `../sedi`", the chapter is titled *State-Endorsed Digital Identity*, and that
> was enough to file the whole of it elsewhere. The guard is defensible for the *programme* and wrong
> for the chapter, because the chapter also contains general duty text bearing on this repo's own
> headline question. **Second, the repo had no way to ask the question §63A-20-302(7)(a) answers.**
> Its framing is "when does Utah law require identifying a person?", and its sweep tool's five
> buckets — PROOFING, DOCUMENT, ATTRIBUTE, COLLECTION, ATTESTATION — are all ways of requiring
> identification. A duty *forbidding* collection matches none of them, so no sweep could have
> surfaced it at any threshold. **Third, the drill-down was broken.** `tools/sweep-identity.py
> --detail 63A` printed nothing at all for every statute title until it was fixed today, because a
> title is labelled `Title 63A` and cited `63A`. Silence read as absence. That is the third time this
> repo has published from a tool that could not see what it was asked about, after the possessive-noun
> and document-presentation failures recorded in
> [`second-sweep.md`](second-sweep.md).

The chapter is new law. All eighteen of its sections carry the history *Enacted by Chapter 436, 2026
General Session*, and none carries an `<effdate>` — where the Code holds text that is not yet
operative it says so, as Title 16 does for the five chapters it marks `<effdate>10/1/2026`. On the
corpus's own convention the chapter was in force when it was retrieved on 2026-07-28.

## What §63A-20-303 actually requires

**§63A-20-303** (Identity proofing), on the operative point:

> (1)(a) The department shall establish and maintain identity proofing requirements for the issuance
> of a state-endorsed digital identity that:
> (1)(a)(i) follow a **generally accepted identity proofing standard**;
> (1)(a)(ii) are commensurate with the risks of impersonation, fraud, and misuse associated with the
> credential; and
> (1)(a)(iii) are consistent with the privacy, civil liberties, and security requirements of this
> chapter.
> (1)(b) The identity proofing process shall be designed to establish, at a minimum, that:
> (1)(b)(i) **the applicant is a real individual**;
> (1)(b)(ii) **the applicant is the individual the applicant claims to be**;
> (1)(b)(iii) the applicant's birth date is the date the applicant claims it to be; and
> (1)(b)(iv) the applicant meets the eligibility requirements of Section 63A-20-302.

Against the four duties in [`docs/research-strategy.md`](../docs/research-strategy.md) §1 this is
unusually clean, because it imposes three of them in three consecutive clauses:

| Duty | Where | What it demands |
|---|---|---|
| **Identity proofing** | §63A-20-303(1)(b)(i)–(ii) | that the applicant is real and is who they claim — the definition, not an approximation of it |
| **Status verification** | §63A-20-303(1)(b)(iv) → §63A-20-302(6)(a)–(b) | lawful presence in the United States, and Utah residency |
| **Identity assertion** | §63A-20-302(7)(b)(i)–(iii) | true and full legal name, date of birth, Utah residence address |
| **Authentication** | *not imposed here* | §63A-20-303(1)(d)(i) says the endorsement "reflects verification at a point in time" |

This is the first provision in the corpus that demands **proofing** in the taxonomy's strict sense.
The fishing-licence probe's finding was that rule R657-45-2 requires a form to *collect* attributes
and requires no one to check them; §63A-20-303(1)(b) is the opposite, and the chapter's own
definition draws the same line the taxonomy does:

> **§63A-20-201(12):** "Identity proofing" means the process of **collecting, validating, and
> verifying** information about an individual to establish confidence in the individual's claimed
> identity.

### The "IAL2-shaped" characterisation is not supported by the text

The comparative finding describes §63A-20-303 as IAL2-shaped. The substance is proofing-shaped, but
the statute adopts no assurance level and names no standard. Searched across all 96 titles:

| Phrase | Sections in the Utah Code |
|---|---|
| `identity assurance`, `assurance level`, `level of assurance` | **0** |
| `IAL`, `AAL` (as words) | **0** |
| `multifactor`, `multi-factor` | **0** |
| `NIST` (as a word) | 2 — both §78B-4-701 and §78B-4-703, cybersecurity affirmative defence, nothing to do with identity |
| `generally accepted identity proofing` | 1 — §63A-20-303(1)(a)(i) |

A positive control on that last row: a case-insensitive search for `NIST` without word boundaries
returns 6,485 sections, every one of them the word *administer*. The statute delegates the actual
standard rather than setting one — **§63A-20-303(4)(a)** requires the department to "define by rule
… the identity proofing standards and processes required for issuance" — so the assurance level, if
Utah ever has one, will be in the administrative rules, and no such rule is in this corpus. Calling
the provision IAL2 imports a number the legislature did not write.

## The more interesting half: a duty running the other way

**§63A-20-302(7)(a)**, in full:

> The department **may not require collection of information that is not necessary** to verify
> identity or eligibility.

This is a ceiling, not a floor. It is the first provision this repo has recorded that constrains
identification rather than compelling it — what the shared taxonomy calls the
`prohibited-identification` direction — and the original framing of this repo, "when does Utah law
require identifying a person?", was not built to notice it. It does not stand alone. The chapter
repeats the construction against every actor it binds:

> **§63A-20-301(3):** A state-endorsed digital identity **may not include a mechanism that allows
> the department to monitor, surveil, or track** the presentation of a state-endorsed digital
> identity to another entity.

> **§63A-20-501(1)(d)** (verifiers) and **§63A-20-601(1)(d)** (relying parties): process **only the
> minimum identity attributes reasonably necessary** to achieve a specified purpose.

> **§63A-20-303(1)(d):** Identity proofing processes shall be designed so that the state's
> endorsement (i) reflects verification at a point in time; and (ii) **does not require** (A)
> continuous monitoring; or (B) tracking.

### And the direction is unsearched outside this chapter too

Having built a ceiling sweep, the honest next step was to run it across all 96 titles rather than
stop at the chapter that prompted it. Ceiling language is genuinely sparse, and most of what exists
is in Title 63A — but not all of it, and none of it has ever been cited in a finding here:

| Provision | The ceiling |
|---|---|
| **§63A-20-302(7)(a)** | department may not require collection not necessary to verify identity or eligibility |
| **§63A-19-402.5** | "A governmental entity may not collect user data on a government website unless" the notice requirements are met |
| **§63A-19-401** | a governmental entity shall "obtain and process only the minimum amount of personal data reasonably necessary" |
| **§13-61-503** | a motor vehicle manufacturer "collects only the minimum personal data necessary to accomplish the purpose" |
| **§26B-2-709** | the department is to encourage a complainant to disclose "the minimum personal identifying information necessary" |
| **§34-46-203** | "an employer may not retain the information described in Subsection (1) more than two years" |

One result here is a true zero rather than a broken search: **no provision in the Utah Code says the
state may not require identification.** The pattern `may not require … identification|identity|proof
of identity` returns nothing across all 96 titles. Utah's ceilings bound *how much* may be collected
once a programme is identifying someone; none of them bounds *whether* it may.

Note that §63A-19-401 and §63A-19-402.5 sit in the chapter immediately before this one, in the same
title, and were missed by the same scope guard for the same reason.

## Does the headline claim survive?

The README says **Utah has no general identity-assurance baseline.** It survives, and the chapter
sharpens rather than threatens it, because the credential is voluntary in the statute's own words:

> **§63A-20-302(5):** An individual is **not required to apply for or obtain** a state-endorsed
> digital identity.

> **§63A-20-101(4):** An individual has a right to **not be compelled by the state** to possess,
> use, or rely upon a digital form of identity assertion in place of a physical form of identity
> assertion that is endorsed by the state.

> **§63A-20-101(9):** An individual has the right to any service or benefit to which the individual
> is otherwise lawfully entitled **based on the individual's choice of a lawful format or means of
> identity assertion** without denial, diminishment, or condition.

A proofing standard that binds one department, for one optional credential, that nobody must hold,
and that no one may be disadvantaged for declining, is not a baseline. It is the strongest
identity-proofing duty in the corpus and it reaches exactly the people who volunteer for it.

What does change is the shape of the claim. Before this chapter, "no general baseline" meant Utah
had never legislated an assurance standard at all. It now has legislated one — and made it opt-in,
and paired it with a bill of rights whose first clause is that identity is "innate to the
individual's existence and independent of the state" (§63A-20-101(1)). The README is qualified
accordingly.

## Bottom line

| Claim | Verdict |
|---|---|
| A whole chapter on identity proofing sat uncited in our own corpus | **True**, and for three separate reasons, all recorded above |
| §63A-20-303 imposes identity proofing in the strict sense | **True** — the only provision in the corpus that does |
| §63A-20-303 is IAL2-shaped | **Not supported.** No assurance level, standard, or NIST reference appears anywhere in the Utah Code; the standard is delegated to rulemaking |
| §63A-20-302(7)(a) is a minimisation ceiling | **True**, and one of a family of at least ten across four titles |
| Utah now has a general identity-assurance baseline | **False.** The credential is voluntary, and refusing it may not be held against anyone |
| Utah law anywhere forbids requiring identification | **False**, as a true zero across 96 titles rather than a failed search |

## Scope of this probe

**Searched:** the Utah Code, all 96 titles, for the assurance vocabulary and the ceiling
constructions tabulated above, and Title 63A Chapter 20 in full.

**Not searched, and each could change an answer here:**

- **The administrative rules.** This is the load-bearing gap. §63A-20-302(4) and §63A-20-303(4)
  both require the department to make rules, and §63A-20-303(4)(b) says those rules shall specify
  "the acceptable methods of identity proofing" and "minimum evidence requirements and validation
  methods". The actual Utah assurance standard will be an R-rule, the chapter was enacted in the
  2026 session, and this corpus was retrieved in July 2026 — so it is unlikely any such rule exists
  yet, and certain that none is held here. Re-fetch `R21` and the Department of Government
  Operations families before concluding anything about what proofing Utah actually demands.
- **The court rules.** Nothing in this probe touched them; a digital credential's evidentiary
  treatment would live there.
- **Federal conditions and case law**, per the standing gaps in the README.
- **The SEDI programme itself**, which remains scoped to the sibling dossier. This probe deliberately
  reads Chapter 20 only for what it says about Utah's general identity-duty landscape, and does not
  analyse the programme, its governance, or its wallet and verifier obligations beyond quoting the
  minimisation clauses.

Every quotation above is reproducible from the corpus in this repo:
`python3 tools/cite.py 63A-20-303`, and likewise for each section cited.
