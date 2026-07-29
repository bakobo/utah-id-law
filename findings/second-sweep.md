# Second sweep: new interactions, and the categories we were blind to

Two things prompted this pass. The sweep tool's regexes were repaired after an adversarial review
(see the corrections marked inline in the other findings), so the whole corpus needed re-reading.
And the earlier work had been shaped entirely by *asking about interactions we happened to think of*
— a survey of examples, not of the space.

## Part 1: what re-running the repaired sweep changed

**Old conclusions that hold.** The fishing-licence finding survives intact: R657's only
identity-*proofing* requirement is still R657-17-8 (replacing a lost lifetime licence). Title 23A is
still at zero. The §63G-12-402 analysis is a reading of statutory text and never depended on the
regexes at all.

**One addition to the wildlife family.** R657-42 was invisible before: transferring a wildlife
document from a decedent's estate requires the person administering the estate to provide "*(a)
picture identification; (b) letters testamentary, letters of administration, or such other evidence
establishing the person is legally entitled to administer the affairs*" of the deceased. Two
identities and the relationship between them — see Part 3.

**The largest miss: R708-41, Utah's REAL ID rule.** Entirely absent from the earlier tables, and it
is the most elaborate documentary identity regime in Utah law. It defines "*identity document*" as
"*an original, government-issued document that contains identifying information about the subject of
the document*," defines "*full legal name evidence*" as "*the name established on an identity
document*," and builds an "*exception process*" — "*a written, defined process for persons who are
unable to present the necessary documents and must rely on alternate documents to establish identity,
date of birth, or US citizenship.*"

That is the closest thing Utah has to a general identity-proofing standard. It sits in the driver
licence rules, and it applies to getting a licence — not to the interactions the licence is later
used for.

**Other families that were invisible and are not small:** R156 (professional licensing, 10 proofing /
41 document), R381 (child care centre licensing, 44 document), R436 (vital records, 39 document),
R430 (residential child care, 29 document), R501 (human services licensing, 25 document).

## Part 2: interactions probed but never written up

| Interaction | Duty | Citation |
|---|---|---|
| **Vehicle registration** | "*shall require that the applicant provide **valid government-issued identification***" | §41-1a-210.5 |
| **Marriage licence** | "*the age, legal name, and **identity of each applicant is verified***," plus both SSNs | §81-2-303(1)(g) |
| **Concealed firearm permit** | "*one recent dated **photograph***" and "*one set of **fingerprints***" | §53-5a-303(6) |
| **Driver licence / state ID** | Full documentary identity regime with an exception process | R708-41 |
| **Signing a petition** | Signatures verified against voter records; verification audits | §20A-1-1002, §20A-3a-402.5(4) |
| **Registering as a candidate** | Sworn declaration; **no identity check** | §20A-9-203(5)(a) |

**Candidate registration deserves its own note**, because it is the sharpest instance of the pattern
this whole project keeps finding. The declaration is sworn — "*I, (print name) ____, **being first
sworn and under penalty of perjury**, say that I reside at…*" For most offices the filing officer must
"*read to the individual the constitutional and statutory qualification requirements*" and then
"*require the individual to **state** whether the individual meets the requirements*" (§20A-9-201(3)(a)).
The officer recites; you assert.

For exactly three offices — county attorney, district attorney, county sheriff — the clerk "*shall
**ensure***" the filer is a citizen, a registered voter, a resident, and (for the attorneys) "*an
attorney licensed to practice law in the state who is an active member in good standing of the Utah
State Bar*," with a letter from the Utah Supreme Court to prove it. But note what is verified even
there: **qualifications, not identity**. Nobody confirms the person filing is the person named.

Meanwhile, if a candidate qualifies by gathering signatures, those signatures **are** checked against
voter records. **Utah correlates the people who sign for you to authoritative records, and takes your
own identity on a sworn statement.**

## Part 3: the categories we were blind to

The earlier surveys all shared a shape — a person walks up to a counter and asks for something. That
framing hid whole classes of interaction.

### Anonymity by design — the mirror image

The question "where must you identify yourself?" has an inverse: **where does Utah law deliberately
refuse to know who you are, or forbid disclosure?** This is not an absence of regulation; it is
regulation pointing the other way.

- **§81-5-708(3)** — gamete donation: "*a donor's request to **remain anonymous** shall be given full
  deference.*"
- **§53H-4-210(2)(a)(i)** — the SafeUT Crisis Line must provide "*a means for an individual to
  **anonymously report**…*"
- **§80-4-502** — safe-haven newborn relinquishment, which operates *around* the absence of a
  parental identity.
- **§20A-2-601** — voter records are disclosable "*without disclosing the identity of the voter.*"
- **Title 36** — whistleblower disclosures made "*on the condition that the identity of the person be
  protected.*"
- **§53G-9-605(5)** — a school "*may not permit formal disciplinary action that is based solely on an
  **anonymous** report*" — the balancing case, where anonymity is preserved but limited in effect.

**Why this matters more than another licensing probe.** A state digital identity system has to
accommodate interactions where the state is legally *forbidden* to know who you are. That is a design
constraint, not a coverage gap.

### Money flowing toward you — attestation, not proof

Intuition says the state tightens up when it is paying out. It does not.

**§67-4a-903(1)(b)** — unclaimed property: "*The claimant shall **verify the claim** as to its
completeness and accuracy.*" Read that carefully: what gets verified is *the claim*, by the claimant,
and "verify" here means **swear to** — attestation, not identity proofing. You assert your way to
money the state is holding for you.

**Title 59 (tax)** was the highest-signal unexamined title. Its proofing language turns out to
concern **disclosure**, not filing: information necessary "*to verify the identity of the taxpayer*"
appears where a taxpayer consents to releasing their records to a third party. Filing a return and
claiming a refund carry no identity-proofing duty in the statute.

### Identity of things, not people

**§4-24-201** and the brand-inspection provisions run a central **Brand Registry**, with
"*verification of ownership through brand inspection*" and a "*brand inspector may demand evidence of
ownership.*" Utah maintains more systematic verification machinery for **cattle ownership** than for
most human interactions in this repo. Same family: vehicle titles, water rights, mining claims.

### Acting for someone else

Two identities plus the relationship between them — the hardest case for any credential system, and
almost entirely unexamined here. Confirmed instance: **R657-42**, requiring picture identification
*and* letters testamentary. The wider set — power of attorney, guardianship, conservatorship,
personal representatives under Title 75 — remains open.

### Time-delayed identity

Matching a person to a record created decades earlier, possibly under a different name.
**UCJA-4-202.03(2)** requires "*presentation of positive identification*" to access **adoption
records** and certified copies of **expungement orders**. Note the inversion: these are the cases
where the state most wants certainty, and they are also the cases where a current credential is least
able to bridge to the old record.

## What this changes

Nothing in Part 1 overturns a previous conclusion; the fishing-licence and §63G-12-402 findings hold.
But Parts 2 and 3 shift the overall picture in one important way. The earlier surveys concluded that
identity duties were sparse. With repaired patterns and a wider frame, they are **not sparse — they
are concentrated**, in places the sampling missed: driver licensing, professional and facility
licensing, vital records, and the machinery around elections.

What remains true, and is the more precise claim, is that they are **absent from the ordinary
transactional interactions** a person has with the state — buying a licence, paying a fine, filing a
petition, requesting a record — and that where they exist, the mechanism is very often delegated to a
notary, a licensee, or a federal condition.
