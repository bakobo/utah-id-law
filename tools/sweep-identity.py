#!/usr/bin/env python3
"""Sweep all three corpora for identity-duty language, bucketed by the kind of duty imposed.

The point is to answer "where in Utah law does an identity duty exist at all?" without
pre-selecting domains -- earlier work sampled three rule families and inherited their
narrowness.

Five buckets, because they are legally different duties (see docs/research-strategy.md §1):

  PROOFING   - validate a claimed identity against authoritative evidence
  DOCUMENT   - present a specific credential (driver licence, photo ID)
  COLLECTION - supply attributes (name, DOB, SSN) with no duty on anyone to check them

Usage:
    python3 tools/sweep-identity.py               # all three corpora, grouped
    python3 tools/sweep-identity.py --rules       # admin rules only
    python3 tools/sweep-identity.py --code        # statutes only
    python3 tools/sweep-identity.py --courts      # court rules only
    python3 tools/sweep-identity.py --detail R81  # quote every hit in one family/title/set
"""

import argparse
import collections
import gzip
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "corpus"

PATTERNS = {
    # A possessive noun between the verb and "identity" is the commonest phrasing in Utah
    # drafting ("verify the applicant's identity"), and the original pattern -- which allowed
    # only an article or pronoun -- missed all of it, undercounting the Code roughly 4x.
    "PROOFING": [
        r"(?:verif|confirm|establish|ascertain|authenticat|validat|substantiat)\w*"
        r"\s+(?:(?:the|a|an|his|her|their|its|each|any|that|this|such|said)\s+)?"
        r"(?:\w+[\u2019'`]s\s+|\w+s[\u2019']\s+|\w+\s+){0,3}identit\w+",
        r"(?:verification|confirmation|validation|authentication)\s+of\s+"
        r"(?:(?:the|a|an|his|her|their|its)\s+)?(?:\w+[\u2019'`]s\s+|\w+\s+){0,3}identit\w+",
        r"identit\w+\s+(?:\w+\s+){0,3}(?:is|are|be|been|was|were)\s+"
        r"(?:\w+\s+){0,2}(?:verified|confirmed|established|ascertained|authenticated|validated)",
        r"proof of identity",
        r"positive identification",
        r"satisfactory evidence of\s+(?:\w+\s+){0,2}identit\w+",
        r"personally known to the notary",
    ],
    # "present a valid driver license" never matched anything corpus-wide: Utah drafting
    # almost always puts a word between the verb and the noun ("present a currently valid
    # Utah driver license"). Broadened, and given the document vocabulary it lacked.
    "DOCUMENT": [
        r"(?:present|produce|exhibit|display|show|furnish|surrender|tender)\w*"
        r"\s+(?:\w+[\u2019'`]?s?\s+){0,5}"
        r"(?:identification|identity document|photo\s?ID\b|driver\W{0,3}s? licen[cs]e)\b",
        r"(?:photo|picture|photographic)[- ]?(?:identification|ID\b)",
        r"(?:valid|current(?:ly valid)?|unexpired)\s+(?:\w+[- ]?){0,3}identification",
        r"government[- ]issued\s+(?:\w+\s+){0,2}(?:identification|id\b)",
        r"(?:identification|identity) document",
        r"certified copy of\s+(?:\w+\s+){0,3}birth certificate",
        r"birth certificate",
        r"\bpassport\b",
        r"documentary proof",
        r"documentary evidence of\s+(?:\w+\s+){0,2}(?:identit|age|citizenship|birth|residenc)",
        r"(?:finger|thumb)print",
        r"\bbiometric",
    ],
    # Proving an attribute (age, residency, citizenship) is legally distinct from proving
    # identity -- the 63G-12-402 "lawful presence, a status, not an identity" distinction --
    # so it gets its own bucket rather than being folded into DOCUMENT.
    "ATTRIBUTE": [
        r"proof of (?:age|residency|residence|citizenship|lawful presence)",
        r"documentary proof of (?:United States )?citizenship",
        r"evidence of (?:age|residency|citizenship|lawful presence)",
    ],
    "COLLECTION": [
        r"social security number",
        r"date of birth",
        r"driver\W{0,3}s? licen[cs]e number",
    ],
    # The competing design: deter false assertion afterward instead of verifying up front.
    "ATTESTATION": [
        r"under (?:the )?penalt(?:y|ies) of perjury",
        r"\bunder oath\b",
        r"oath or affirmation",
        r"unsworn declaration",
        r"sworn statement",
        r"\baffidavit",
        r"notarized",
        r"acknowledged before a notary",
    ],
}
COMPILED = {b: [re.compile(p, re.I) for p in ps] for b, ps in PATTERNS.items()}


def texts(which: str):
    """Yield (label, group, plain text) for each instrument in the requested corpora."""
    if which in ("both", "code"):
        for f in sorted((BASE / "utah-code").glob("*.xml.gz")):
            title = re.match(r"C([0-9A-Z]+)_", f.name).group(1)
            xml = gzip.decompress(f.read_bytes()).decode("utf-8", "replace")
            yield f"Title {title}", f"Title {title}", re.sub(r"<[^>]+>", " ", xml)
    if which in ("both", "rules"):
        for f in sorted((BASE / "admin-rules").glob("*.txt.gz")):
            ref = f.name[:-7]
            fam = re.match(r"(R\d+[A-Za-z]?)", ref)
            yield ref, (fam.group(1) if fam else ref), gzip.decompress(f.read_bytes()).decode(
                "utf-8", "replace"
            )
    if which in ("both", "courts"):
        for f in sorted((BASE / "court-rules").glob("*.txt.gz")):
            ref = f.name[:-7]
            yield ref, ref.split("-")[0], gzip.decompress(f.read_bytes()).decode("utf-8", "replace")


def agencies() -> dict[str, str]:
    """Map rule family -> agency/program, from the admin-rules manifest."""
    out = {}
    man = BASE / "MANIFEST-admin-rules.tsv"
    if man.exists():
        for line in man.read_text().splitlines()[1:]:
            parts = line.split("\t")
            fam = re.match(r"(R\d+[A-Za-z]?)", parts[0])
            if fam and fam.group(1) not in out:
                out[fam.group(1)] = f"{parts[2]} / {parts[3]}"
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--code", action="store_true")
    ap.add_argument("--courts", action="store_true")
    ap.add_argument("--detail", metavar="GROUP", help="quote every hit in one title/rule family")
    args = ap.parse_args()
    which = (
        "rules" if args.rules else "code" if args.code else "courts" if args.courts else "both"
    )

    if args.detail:
        target = args.detail.upper()
        for label, group, text in texts(which):
            up = label.upper()
            # A statute title is labelled "Title 63A" and cited "63A", so the documented
            # `--detail 63A` matched nothing for the whole Code layer -- and printed nothing
            # rather than saying so, which reads as "no identity language in Title 63A" when
            # there are 204 hits in it. Both spellings resolve now. A zero is a question.
            names = {up, group.upper()}
            if up.startswith("TITLE "):
                names.add(up[len("TITLE ") :])
            if not (
                target in names
                or any(re.match(rf"{re.escape(target)}[-. ]", n) for n in names)
            ):
                continue
            for bucket, rxs in COMPILED.items():
                for rx in rxs:
                    for m in rx.finditer(text):
                        ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 170) : m.start() + 170])
                        print(f"[{bucket}] {label}\n    …{ctx}…\n")
        return

    counts: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for _label, group, text in texts(which):
        for bucket, rxs in COMPILED.items():
            n = sum(len(rx.findall(text)) for rx in rxs)
            if n:
                counts[group][bucket] += n

    agy = agencies()
    rows = sorted(counts.items(), key=lambda kv: -kv[1]["PROOFING"])
    print(f"{'GROUP':<10} {'PROOF':>6} {'DOC':>6} {'ATTRIB':>7} {'COLLECT':>8} {'ATTEST':>7}  WHO")
    for group, c in rows:
        if not sum(c.values()):
            continue
        print(
            f"{group:<10} {c['PROOFING']:>6} {c['DOCUMENT']:>6} {c['ATTRIBUTE']:>7} "
            f"{c['COLLECTION']:>8} {c['ATTESTATION']:>7}  {agy.get(group, '')}"
        )


if __name__ == "__main__":
    main()
