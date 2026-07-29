# Probe: court filings, bail, testifying, and jail visits

Resolves the question left open by earlier findings — filing a court petition — and extends to
posting bail, appearing as a witness, and visiting someone in custody. Answerable now because the
**court rules** corpus was added (661 rules across six sets; see `tools/fetch-utah-court-rules.py`).

**Court rules** are the third body of Utah law: promulgated by the **Utah Supreme Court** under its
constitutional rulemaking power, not by the legislature or an agency. They govern procedure in the
courts and appear in neither the Utah Code nor the Administrative Code.

## The headline number

> **Corrected 2026-07-29.** This section previously claimed *zero* identity-proofing requirements
> across *690* court rules. Both numbers were wrong. An adversarial review of the sweep tool found
> that its `verif…identity` pattern could not see a possessive noun (`verify the victim's identity`)
> and that its document-presentation pattern matched **nothing at all** corpus-wide. The corpus also
> contained 29 duplicate files — the index lists some rules twice differing only in case, and the
> fetcher stored both. The true count is **661 rules**, and nine of them impose identity duties. The
> corrected finding below is narrower, and better.

Across all **661 court rules**, using repaired patterns:

| | PROOFING | DOCUMENT | ATTESTATION |
|---|---|---|---|
| URCP (Civil Procedure) | **0** | **0** | 109 |
| URE (Evidence) | **0** | **0** | 11 |
| URAP (Appellate) | **0** | **0** | 23 |
| URCrP (Criminal Procedure) | 0 | 1 | 31 |
| URJP (Juvenile) | 0 | 3 | 18 |
| UCJA (Judicial Administration) | 3 | 14 | 29 |

The nine rules carrying identity duties, and where they cluster:

| Rule | Duty |
|---|---|
| UCJA-4-202.12(1)(A)(ii) | "*other documentation sufficient to **verify the victim's identity***" |
| UCJA-4-202.03(2) | "*presentation of **positive identification***" for adoption and expungement records |
| UCJA-4-202.04(1)(B) | requester of a non-public record "*must **present identification***" |
| UCJA-4-202.05(1) | requester "*shall **present identification***" |
| UCJA-3-414(8)(B) | officer "***presents valid picture identification***" — courthouse weapons |
| UCJA-4-609 | mandatory **fingerprinting** and offence-tracking number for unbooked defendants |
| URCrP-16(f) | court-ordered lineup, **fingerprinting**, bodily impressions |
| URJP-27(a) | motion to **photograph or fingerprint** a child under 14 |
| UCJA-4-907(6)(A) | "*valid form of **photo identification***" for the divorce/parenting class |

**The corrected claim.** No Utah court rule requires a party to prove identity in order to **file,
testify, or post bail** — URCP, URE and URAP are genuinely at zero on both proofing and document
presentation. The identity duties that exist attach to three things instead: **records access**
(4-202.03/.04/.05/.12), **courthouse security** (3-414), and **compulsory process against
defendants** (4-609, URCrP-16, URJP-27). Against that, **192** occurrences of oath, affirmation,
unsworn declaration, affidavit or penalty of perjury — the published 217 double-counted the
duplicate files.

That pattern is more informative than the "zero" it replaces: the courts demand identity to let you
**read a sealed record** or **carry a weapon into a courthouse**, and to fingerprint a defendant —
but never to invoke the court's jurisdiction in the first place.

## Filing a court petition — no identification required

**URCP-11(a)(2)** is dispositive:

> A person may sign a paper using any form of signature recognized by law as binding. **Unless
> required by statute, a paper need not be accompanied by affidavit or have a notarized, verified or
> acknowledged signature.** If a rule requires an affidavit or a notarized, verified or acknowledged
> signature, **the person may submit an unsworn declaration** as described in Title 78B, Chapter 18a,
> Uniform Unsworn Declarations Act.

So the default is expressly *no* notarisation — and even where a rule would demand one, an unsworn
declaration substitutes. The enforcement mechanism is URCP-11(b): by presenting a paper, the signer
makes representations to the court, sanctionable under URCP-11(c). The familiar pattern — deter the
lie afterward rather than verify the person up front.

The only identity-ish requirements in URCP concern *other* people or *disclosure*, not proofing the
filer: URCP-26.2(b)(3) makes a personal-injury plaintiff disclose their own SSN and date of birth
(to satisfy Medicare reporting under 42 U.S.C. §1395y(b)(8)); URCP-64D(d) makes a garnishing
plaintiff supply the *defendant's* identifiers.

**No photo ID is required to file.** The contrast that survives correction: UCJA-4-907(6)(A)
requires a person attending the mandatory divorce/parenting orientation course to "*present a valid
form of photo identification and pay the course fee.*" You can file the divorce petition without
showing ID; you must show ID to attend the class it triggers. (This is one of five
ID-presentation rules in the corpus, not the only one — see the corrected table above.)

## Posting bail — depends entirely on the instrument

Three different answers, and the split is instructive.

**Cash bail: nothing.** §77-20-401(1) lets an individual post bail with the county jail official
"*in money, by cash, certified or cashier's check, personal check with check guarantee card, money
order, or credit card … or by a bail bond issued by a surety.*" The statute enumerates payment
methods. It imposes no identity requirement on whoever hands over the money.

**A real property bond: notarised.** URCP-72(a) requires such a bond to "*be signed by all owners of
record*," to contain the legal description and property tax identification number, and — decisively
— to "*be acknowledged before a notary public.*" That routes back to §46-1-2(25)'s "satisfactory
evidence of identity," i.e. unexpired photo ID. Strong proofing, delegated to a notary.

**A surety bond: licensed intermediary.** The bond must be issued by a surety, and bail bond
producers are licensed under Title 31A with **fingerprint background checks**. Identity assurance
sits in the licensing of the intermediary, not in the transaction.

**The defendant, separately, is identified thoroughly** — but not as a voluntary interaction.
§77-20-202(1)(a) requires jail staff to submit to the court the arrestee's legal name and known
aliases, date of birth, **state identification number** (the criminal-history identifier established
by fingerprinting), and immigration status if not a citizen. And URCrP-16(f)(1) lets the court, on
good cause, order a defendant to "*appear in a lineup; speak for identification; submit to
fingerprinting or the making of other bodily impressions.*" This is the strongest identity process
anywhere in the survey — and it is compulsory and adversarial, the opposite of an entitlement
interaction.

Worth noting how far the other way the criminal rules bend: **URCrP-4(b)(1)(A)** provides that "*if
the name of the defendant is not known, the prosecution must identify the defendant as John or Jane
Doe.*" Utah's criminal process explicitly proceeds against people it cannot identify.

## Appearing as a witness — an oath, not an ID

**URE-601(a)**: "*Every person is competent to be a witness unless these rules provide otherwise.*"

**URE-603**: "*Before testifying, a witness must give an oath or affirmation to testify truthfully.
It must be in a form designed to impress that duty on the witness's conscience.*"

That is the whole of it. No rule requires a witness to prove who they are; the control is the oath,
backed by perjury liability. A subpoenaed witness who appears and swears has satisfied every
identity-related requirement in the Rules of Evidence.

## Visiting someone in custody — permissive, not mandatory

**R251-305(11)–(12)** (Visiting at Community Correctional Centers) draws the distinction in one
breath:

> (11) visitors **shall** be required to sign a visitor log when entering and leaving the Center;
> (12) visitors **may** be required to present picture identification prior to visiting.

Signing the log is mandatory — self-asserted collection. Presenting photo ID is **discretionary**. A
facility that never asked for ID would not be out of compliance, because the rule confers a power
rather than imposing a duty. This is the sharpest may/shall contrast found anywhere in the corpora.

A stricter regime applies to **sponsors** (people who take an offender into the community):
R251-306 requires "*positive identification*," defined as "*a document or documents containing a
photograph and date of birth, including driver's license, federal identification card or passport;
does not include credit cards, social security card, or similar document*," plus a Bureau of
Criminal Identification background check.

**Caveat:** these are Department of Corrections rules for state facilities. **County jails** are run
by county sheriffs, and their visitor ID policies are local operational policy — not in any of the
three corpora, and not state law.

## What this adds to the overall picture

Every one of these interactions falls on the *no-proofing* side, with three telling exceptions that
all follow the same pattern already seen: the duty attaches to a **notary** (property bond), a
**licensed intermediary** (surety), or a **discrete ancillary service** (the parenting class). The
courts themselves — the branch with the most at stake in knowing who is before it — impose no
identity proofing at all.
