# Probe: does Utah law require "strong identification" to get a fishing license?

**Question.** A software architect asserted that *any time a citizen interacts with the state of Utah
to receive an entitlement, the state is legally required to strongly identify them*, offering a
fishing license as the example, and adding that observed agency practice to the contrary is mere
non-compliance rather than evidence about the requirement.

**Status.** Answered against the assertion, on primary sources, for the specific example given.
The general claim is not yet fully tested — see [Scope](#scope-of-this-probe) at the bottom.

**Sources.** Utah Code Title 23A and Title 63G as retrieved 2026-07-28 from le.utah.gov
(`corpus/utah-code/`, see `corpus/MANIFEST-utah-code.tsv` for version stamps and hashes);
8 U.S.C. § 1621 via Cornell LII.

---

## 1. The fishing-license statute imposes no identity requirement at all

**§23A-4-601** (Fishing license), in full on the operative point:

> (1) A person 12 years old or older shall purchase a fishing license before engaging in a regulated
> fishing activity.
> (2) **Upon paying the fee prescribed by the Wildlife Board, a person may obtain a license to fish**
> and engage in a regulated fishing activity in accordance with the rules, proclamations, and orders
> of the Wildlife Board.

The condition precedent is *payment of a fee*. There is no identity element — no document
presentation, no verification, no proofing, no authentication.

The surrounding chapter confirms this is deliberate rather than an oversight. **§23A-4-202** tells
the Wildlife Board to prescribe the *form* of the license (paper or electronic) and says nothing
about verifying the applicant. The identity-adjacent constraints that do exist are:

- **Age** (12+ needs a license; §23A-4-601(1), (3)) — asserted, not verified.
- **Residency**, which affects price (resident vs. nonresident licenses, §23A-4-401).
- **§23A-4-1101**, which makes it a class B misdemeanor to "obtain or attempt to obtain a license
  ... by fraud, deceit, or misrepresentation," including a resident/nonresident mismatch, and voids
  a license so obtained.

That last one is the tell. Utah addressed the risk of a lying applicant with an **after-the-fact
criminal penalty**, not with **front-door verification**. §23A-4-1101 would be largely redundant if
the state were already required to verify the facts being asserted. A statute that both verifies
identity *and* criminalizes misrepresentation is possible; a statute that only criminalizes
misrepresentation is strong evidence that verification was not the chosen design.

## 2. The general benefits-verification statute does not reach a fishing license

The nearest thing Utah has to a general identity duty at the benefits counter is
**§63G-12-402** (in the Utah Immigration Accountability and Enforcement Act — note this is *not* an
"identity documents" act; the label matters when reasoning about its scope):

> (1)(a) Except as provided in Subsection (3) or when exempted by federal law, an agency or political
> subdivision of the state shall **verify the lawful presence in the United States** of an individual
> **at least 18 years old** who applies for: (i) a state or local public benefit **as defined in
> 8 U.S.C. Sec. 1621**; or (ii) a federal public benefit as defined in 8 U.S.C. Sec. 1611 ...

Three independent reasons a recreational fishing license falls outside it:

**(a) It is not a "state or local public benefit."** 8 U.S.C. § 1621(c)(1) defines the term as:

> (A) any grant, contract, loan, **professional license, or commercial license** provided by an agency
> of a State or local government ...; and
> (B) any retirement, welfare, health, disability, public or assisted housing, postsecondary
> education, food assistance, unemployment benefit, or any other similar benefit **for which payments
> or assistance are provided to an individual** ... by an agency of a State or local government.

A recreational fishing license is neither professional nor commercial, so (A) does not reach it.
And under (B) the applicant *pays the state* — no payments or assistance flow to the individual — so
it is not a "similar benefit" either.

**(b) The age floor.** The duty attaches only to applicants **18 or older**. Utah requires a fishing
license from age **12**. Even if a fishing license were a public benefit, 12–17-year-old licensees
would be categorically outside the verification duty — which no "the state must always strongly
identify" reading can accommodate.

**(c) The catch-all exemption.** §63G-12-402(3)(a) removes "any purpose for which lawful presence in
the United States is not restricted by law, ordinance, or regulation." Nothing restricts fishing to
the lawfully present.

## 3. The decisive point: even where the duty *does* apply, the method is attestation

This is the finding that generalizes furthest, and it is where the assertion goes wrong most deeply.

§63G-12-402 does bind real programs — Medicaid, food assistance, unemployment, housing,
postsecondary education, professional licensing. For those, the statute prescribes its own method:

> (4)(a) An agency or political subdivision required to verify the lawful presence in the United
> States of an applicant under this section shall require the applicant to **certify under penalty of
> perjury** that: (i) the applicant is a United States citizen; or (ii) the applicant is (A) a
> qualified alien ... and (B) lawfully present ...
>
> (5) An agency or political subdivision shall verify a certification required under **Subsection
> (4)(a)(ii)** through the federal SAVE program.

Read the cross-reference carefully. The SAVE check in (5) is triggered only by
**(4)(a)(ii)** — the *qualified alien* branch. **For an applicant who certifies U.S. citizenship
under (4)(a)(i), signing the form is the complete statutory procedure.** No document check, no
database lookup, no biometric, nothing resembling NIST IAL2 proofing.

So for the overwhelming majority of applicants — citizens — Utah's most general
verification mandate is satisfied by a signature backed by a perjury warning. The pattern from
§23A-4-1101 recurs: **the enforcement mechanism is a criminal penalty for lying, not a verification
gate.** That is a complete and internally coherent legal design, not a weak approximation of
proofing.

Note also what is being verified: **lawful presence**, a *status*. Even the SAVE branch does not
establish that the applicant is who they say they are — it checks an immigration record for an
identity the applicant has asserted.

## 4. The exemption list contradicts the universal claim on its own terms

§63G-12-402(3) exempts, among others: emergency medical treatment; short-term noncash disaster
relief; **immunizations and testing/treatment of communicable disease symptoms**; soup kitchens,
crisis counseling, and short-term shelter; state retirement benefits under Title 49; certain home
loans; and several named scholarships and grants (Opportunity, New Century, promise grants).

These are unambiguously "citizens interacting with the state to receive an entitlement," and the
legislature wrote express carve-outs saying no verification is required. A statute containing a
list of entitlements exempt from verification is direct textual refutation of a claim that all
entitlements require it.

## 5. On the compliance argument

The architect's reasoning — non-compliance does not negate a requirement — is sound in the abstract,
and the retention analogy is a fair illustration of the general principle. But it does no work here,
because the question was never whether agencies comply. **The requirement is absent from the text**,
and §23A-4-601 affirmatively specifies a *different* condition (pay the fee). An agency issuing a
fishing license on payment alone is not out of compliance; it is doing exactly what the statute says.

Two further cautions on that line of argument:

- It shifts the burden the wrong way. "A requirement exists somewhere in the code, and what you
  observe is non-compliance" is unfalsifiable unless the provision is cited. The provision should be
  produced.
- The retention analogy may not survive its own scrutiny. Utah retention schedules are generally
  **minimums** with litigation-hold and archival exceptions; "retains longer than the schedule" is
  often permitted rather than violative. Worth a separate probe before relying on it —
  see the backlog.

## 6. The rules layer — where the architect is partly right

§23A-4-601(2) issues licenses "in accordance with the rules… of the Wildlife Board," so the statute
alone was never the whole answer. All 64 current **R657** (Wildlife Resources) rules have now been
retrieved and searched. The result refines the finding rather than overturning it, and it vindicates
one part of the architect's description.

**Collection is mandatory, and it is more than a name.** R657-45 ("Wildlife License, Permit, and
Certificate of Registration Forms and Terms"), issued under §23A-4-202:

> **R657-45-2(2)** The license, permit, and certificate of registration forms **shall include** the
> licensee's customer identification number, name, date of birth, address, height, weight, eye color,
> hair color, gender, and any other information the Division of Wildlife Resources may request.

R657-45-2(1) applies this to licenses "issued for hunting **or fishing**." So a Utah fishing license
does carry a real identity record — name, DOB, address, and a physical description. Anyone assuming
the state merely takes a name is understating it, and the "they write down a person's name" half of
the architect's characterization is **correct, and required by rule**.

**Verification is still absent.** Nothing in R657-45 — or anywhere in the 64 R657 rules — directs
the division to check any of it against evidence. R657-45-3(1)(a) keeps the statutory posture:
issuance follows "**paying the prescribed fee and satisfying the criteria for issuance**."
**R657-13** ("Taking Fish and Crayfish"), the operative fishing rule, contains **zero** occurrences
of *identity*, *proof*, *verif-*, *photo identification*, or *driver license* across 34,561
characters.

Searching all 64 R657 rules for identity language turns up exactly **one** verification requirement,
and its placement is telling:

> **R657-17-8(1)** If a **lifetime** hunting and fishing license is lost or stolen, a duplicate may be
> obtained from any division office by: (a) providing **verification of identity**; and (b) paying a
> lifetime hunting and fishing license duplication fee.

Utah requires identity verification to *replace a lost lifetime license* — an anti-fraud control on a
high-value, non-expiring credential — but not to *obtain* a fishing license in the first place. If a
general duty to strongly identify existed, this provision would be unnecessary.

The other hits are collection or record-linking, not proofing: R657-19 requires a certificate-of-
registration application to *include* SSN, driver-license number, DOB, and physical description;
R657-62 tracks bonus and preference points "using social security numbers or division-issued customer
identification numbers." Each asks the applicant to *supply* an identifier. None asks the division to
*validate* one.

**The distinction that survives:** the rules mandate **identity assertion** — a substantial dossier of
self-reported attributes, on a prescribed form. They do not mandate **identity proofing**. Those are
different duties (see the table in `docs/research-strategy.md` §1), and only the first is imposed.

## 7. First read across the whole Code — directional, not conclusive

With all 96 titles retrieved, a keyword sweep gives a preliminary read on the general claim:

| Phrase | Occurrences in the Utah Code |
|---|---|
| "under penalty of perjury" | **89** |
| "verif… the identity" | 17 |
| "identity verification" | 10 |
| "proof of identity" | 4 |
| "valid photo identification" | 0 |
| "strongly identif…" | 0 |

Attestation language outnumbers all identity-verification phrasings combined by roughly 3:1 — the
same design preference the two statutes above showed, visible at the scale of the whole code.

Where the identity-verification language *does* appear is equally suggestive. By title:
Title 59 (Revenue and Taxation) 9 · Title 78B (Judicial Code) 6 · Title 20A (Election Code) 5 ·
Title 63A (Government Operations) 4 · Title 53 (Public Safety) 2 · Titles 13, 17, 26B, 63G, 76 one
each. **Title 23A (Wildlife Resources): zero.**

The clustering is in tax administration, courts, elections, and driver licensing — fraud-sensitive
and franchise contexts — rather than in benefits delivery. Most striking: **Title 26B (Health and
Human Services)**, the title under which Utah administers Medicaid, food assistance, and child
welfare, contains exactly **one** occurrence, and it is not a mandate to identify recipients:

> **§26B-1-202(2)(pp)** — [the department may] establish methods or measures for health care
> providers, public health entities, and health care insurers **to coordinate among themselves** to
> verify the identity of the individuals the providers serve

That is a grant of rulemaking authority about provider coordination, not a duty to strongly identify
benefit applicants. The Title 63A hits are similar in kind: §63A-12-117 concerns electronic-record
notarization, and §63A-20-204 is SEDI itself, listing prospective use cases.

**Treat this as directional.** Keyword frequency is not a proof of absence: a statute can impose a
verification duty without using any of these phrases ("shall present a valid driver license,"
"documentary evidence of," "shall establish the applicant's identity"). Closing that gap is exactly
what the phrase-family sweep in `docs/research-strategy.md` is for.

## 8. Where the claim does hold — Medicaid and child care

With all ~2,294 current rules retrieved, the honest answer needs its other half. For **means-tested
benefit programs, Utah really does require identity verification**, including documentary evidence.

**Medicaid** (R414):

> **R414-308-4(4)** If an applicant's citizenship and identity do not match through the **Social
> Security electronic match process** and the eligibility agency cannot resolve the inconsistency,
> the eligibility agency shall require the applicant to provide **verification of his citizenship and
> identity** in accordance with 42 U.S.C. 1396a(ee)(1)(B). (a) The individual must provide
> verification to resolve the inconsistency or provide **original documentation** … within 90 days.

R414-302-3 implements 42 C.F.R. §435.406, requiring citizenship/lawful-status verification.

**Child care assistance** (R986-700-702(3)): "**A client must verify identity**," with the
Department verifying the SSN where provided and requesting "further verification to confirm an
individual's identity if a Social Security Number cannot be verified."

Three observations that keep this in proportion:

1. **The source is federal, not Utah.** Both regimes cite federal authority — 42 C.F.R. §435.406/407,
   42 U.S.C. §1396a(ee). These are conditions attached to federally funded programs, which is exactly
   why they reach Medicaid and child care but not fishing licenses. This is the layer flagged in
   `docs/research-strategy.md` §1 as the most common source of confusion, and it cuts *against*
   universality: a duty that attaches to specific federally funded programs is by construction not a
   duty that attaches to every interaction with the state.
2. **The design is risk-based, not gate-based.** The default path is an *electronic match* against
   SSA records; documentary proofing is the **exception**, triggered only by a mismatch. Even here,
   Utah is not front-door-verifying every applicant.
3. **It is program-specific, and the programs are enumerable.** That is the opposite of a general
   rule with scattered non-compliance.

So the fair summary of the disagreement: **the architect is right that some entitlements carry real
identity-verification duties, and wrong that this is a general requirement.** The dividing line is
not compliance — it is whether a given program is a federally funded means-tested benefit. Fishing
licenses, state park entry, immunizations, and the whole §63G-12-402(3) exemption list sit on the
other side of it.

## Scope of this probe

Answered: the fishing-license example, and the content and method of Utah's most general
benefits-verification duty.

**Not** answered with finality: the universal claim across all 96 titles. Section 7 is a keyword
sweep of the statutes, not the systematic phrase-family search described in
`docs/research-strategy.md` §3, and §§6 and 8 sample the rules layer by family (R657, R414, R986)
rather than sweeping all ~2,294 rules. Both corpora are now local, so that sweep is available work
rather than a blocked gap.

One limit remains genuinely open: **the federal layer is not archived.** The Medicaid and child care
duties in §8 cite 42 C.F.R. §435.406/407 and 42 U.S.C. §1396a(ee); those texts, plus 7 C.F.R. §273.2
(SNAP) and 6 C.F.R. Part 37 (REAL ID), have not been retrieved and were read only through the Utah
rules that implement them.

What the probe establishes: the best candidate for a general mandate (§63G-12-402) is bounded by a
defined term, an age floor, and a long exemption list and prescribes attestation rather than
proofing; the fishing example fails outright; and the genuine verification duties that do exist are
program-specific and federally sourced.

## Bottom line

| Claim | Verdict |
|---|---|
| A fishing license requires strong identification | **False.** §23A-4-601 requires payment of a fee. R657-45-2 requires the *form* to collect name, DOB, address, and physical description — collection, not verification. |
| The state writes down identifying information | **True, and required** — by rule (R657-45-2), not by statute. Credit where due; this is the accurate half of the characterization. |
| A fishing license is an "entitlement" triggering verification duties | **False.** Not a public benefit under 8 U.S.C. §1621(c); the applicant pays the state. |
| Utah law generally requires strong identification for entitlements | **Not supported as a general rule.** §63G-12-402 is bounded by a defined term, an 18+ floor, and an exemption list. But **specific programs do require it** — Medicaid (R414-308-4) and child care assistance (R986-700-702) both mandate identity verification, under federal authority. |
| Where verification *is* required, it means strong identification | **False.** §63G-12-402(4)–(5): certification under penalty of perjury; SAVE only for the non-citizen branch. |
| Observed practice is non-compliance, not evidence | **Not applicable here.** The statute specifies a different condition; issuing on payment alone complies. |

Two conflations drive the disagreement. The first is between **identity proofing** and **status
verification backed by perjury liability** — Utah's general design deters false assertion with
criminal penalty rather than preventing it with verification. The second is between **a general
requirement observed unevenly** and **a set of program-specific federal requirements**. §8 shows
the latter is what actually exists: real, enforceable identity verification in Medicaid and child
care, absent in recreational licensing, and expressly waived across the §63G-12-402(3) list.

For SEDI purposes the practical upshot is that Utah has **no general identity-assurance baseline**
to inherit. Assurance today is set program by program, mostly by federal funding conditions, and
ranges from nothing (fishing) through attestation (§63G-12-402(4)) to electronic match with
documentary fallback (Medicaid). Anything asserting a uniform statewide floor is describing a
future state, not the current legal landscape.
