#!/usr/bin/env python3
"""Sweep all three corpora for identity-duty language, bucketed by the kind of duty imposed.

The point is to answer "where in Utah law does an identity duty exist at all?" without
pre-selecting domains -- earlier work sampled three rule families and inherited their
narrowness.

Three buckets, because they are legally different duties (see docs/research-strategy.md §1):

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
    "PROOFING": [
        r"proof of identity",
        r"verif\w*\s+(?:the\s+|his\s+|her\s+|their\s+|an?\s+)?identity",
        r"identity\s+verification",
        r"establish\w*\s+the\s+identity",
        r"satisfactory evidence of identity",
        r"confirm\w*\s+(?:the\s+)?(?:individual's\s+|person's\s+)?identity",
        r"identity of the (?:applicant|signer|individual|person) ",
    ],
    "DOCUMENT": [
        r"photo(?:graphic)? identification",
        r"valid\s+(?:government[- ]issued\s+)?identification",
        r"government[- ]issued\s+(?:photo\s+)?(?:identification|id\b)",
        r"present\w*\s+(?:a\s+)?(?:valid\s+)?(?:driver\W{0,3}s? licen[cs]e|identification card)",
        r"proof of age",
        r"documentary evidence",
    ],
    "COLLECTION": [
        r"social security number",
        r"date of birth",
        r"driver\W{0,3}s? licen[cs]e number",
    ],
    # The competing design: deter false assertion afterward instead of verifying up front.
    "ATTESTATION": [
        r"under penalty of perjury",
        r"oath or affirmation",
        r"unsworn declaration",
        r"sworn statement",
        r"affidavit",
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
            if group.upper() != target and not label.upper().startswith(target):
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
    print(f"{'GROUP':<10} {'PROOF':>6} {'DOC':>6} {'COLLECT':>8} {'ATTEST':>7}  WHO")
    for group, c in rows:
        if not (c["PROOFING"] or c["DOCUMENT"]):
            continue
        print(
            f"{group:<10} {c['PROOFING']:>6} {c['DOCUMENT']:>6} {c['COLLECTION']:>8} "
            f"{c['ATTESTATION']:>7}  {agy.get(group, '')}"
        )


if __name__ == "__main__":
    main()
