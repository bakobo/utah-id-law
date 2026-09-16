#!/usr/bin/env python3
"""Derive the shared-schema (`id-law-kit`) manifests from this repo's corpus.

This repo predates `id-law-kit`. Its three fetchers each grew a manifest shaped to what that
fetcher happened to know -- `MANIFEST-utah-code.tsv` carries six columns, `MANIFEST-court-rules.tsv`
eight, `MANIFEST-admin-rules.tsv` ten, and they share only `retrieved`. None of them is readable by
`lawcorpus.manifest.Manifest.read`, so the repo that invented quote-or-drop was the one repo the
method's own tooling could not quote.

Three ways to fix that were available. This is a note of why the other two were refused.

**Migration is not possible.** `python -m lawcorpus.migrate` brings a manifest written against the
kit's own previous schema onto the current one, by supplying the two columns that schema lacked. It
refuses these files, correctly and by name:

    [e.input.format.migration.f] ... carries columns this migration does not know how to read:
    title, version, url, retrieved, bytes, sha256.

**Hand-editing is not possible either, because the bytes to write are not in the old manifests.**
`MANIFEST-admin-rules.tsv` has no digest of the text it stores. Its `html_sha256` column is the
digest of the *source HTML* the fetcher downloaded, not of the plain text it extracted and wrote to
disk -- so for 2,294 of this corpus's 3,051 items, the one field that makes a corpus worth more than
a web search had to be computed from the corpus rather than copied from a manifest. `tools/cite.py`
never checked a digest, so nothing surfaced it.

So: regeneration. The bespoke manifests stay, because they are the fetchers' own output and carry
columns the shared schema has no home for -- an administrative rule's `agency` and `program`, a
court rule's `set`. The shared manifests are derived from them plus the corpus itself, and every
`bytes` and `sha256` written here is computed from the stored file, never copied. Re-run this script
after any fetch.

One shared manifest per layer, not one for the repo. `lawcorpus.store.CorpusStore` turns an
`item_id` into a filename and refuses a path separator in it, so a single `corpus/MANIFEST.tsv`
could not reach `corpus/utah-code/`. Each layer is a corpus in its own right -- its own source, its
own fetcher, its own authority tier -- which is the same shape the sibling repos use
(`eidas-eudi/corpus-arf/`, `ccpa/corpus-regs/`, `aadhaar/corpus-judgments/`).

Usage:
    python3 tools/build-kit-manifests.py            # write all three
    python3 tools/build-kit-manifests.py --check    # verify, write nothing
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import re
import sys
from pathlib import Path

try:
    from lawcorpus.manifest import Manifest, ManifestItem
except ImportError:  # pragma: no cover - environment, not logic
    sys.exit(
        "This script needs `lawcorpus`, from the sibling bakobo/id-law-kit repo, so that the\n"
        "shared schema is imported rather than restated here and allowed to drift from it.\n"
        "Install it with:\n"
        "    pip install -e ../id-law-kit\n"
        "or run this script with that repo's interpreter:\n"
        "    ../id-law-kit/.venv/bin/python tools/build-kit-manifests.py"
    )

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpus"

LANG = "eng"

# Every layer is original-language primary text published by the body that enacted it: the
# Legislature's own Code, the agencies' own rules, the courts' own rules. Nothing here is a
# rendering of a text that binds somewhere else, which is what `translation_status` asks about.
TRANSLATION_STATUS = "authoritative"


def digest(path: Path) -> tuple[int, str]:
    """The size and SHA-256 of the *uncompressed* stored text.

    Computed, never copied from a manifest. `MANIFEST-admin-rules.tsv` records the digest of the
    HTML its fetcher downloaded rather than of the text it wrote, and a manifest that attests to
    bytes nobody stored is worse than one that attests to nothing.
    """
    raw = gzip.decompress(path.read_bytes())
    return len(raw), hashlib.sha256(raw).hexdigest()


def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def iso_date(american: str) -> str:
    """'5/18/2021' -> '2021-05-18'. Returns '' for anything that is not that shape."""
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", american.strip())
    if not m:
        return ""
    month, day, year = m.groups()
    return f"{year}-{int(month):02d}-{int(day):02d}"


def title_metadata(path: Path) -> tuple[str, str]:
    """The title's catchline, and a note about any date the Code records against the title itself.

    Only the element's own prefix is read -- everything before the first `<chapter` -- because
    `<effdate>` and `<enddate>` appear at chapter, part and section level throughout the corpus,
    and picking up a descendant's date would attribute it to the whole title.
    """
    xml = gzip.decompress(path.read_bytes()).decode("utf-8", "replace")
    prefix = xml.split("<chapter", 1)[0]

    catchline = re.search(r"<catchline>(.*?)</catchline>", prefix, re.S)
    name = re.sub(r"<[^>]+>", "", catchline.group(1)).strip() if catchline else ""

    notes = []
    for tag in ("effdate", "enddate"):
        m = re.search(rf"<{tag}[^>]*>([^<]*)</{tag}>", prefix)
        if m:
            notes.append(f"title-level <{tag}> {m.group(1).strip()}")
    # An in-force item may still carry a note. `validity_note` is only *required* when validity is
    # not `in-force`, and a title whose own text records a date is worth saying so about.
    return name, ("the Code records " + "; ".join(notes) if notes else "")


def utah_code() -> Manifest:
    rows = read_tsv(CORPUS / "MANIFEST-utah-code.tsv")
    items = []
    for row in rows:
        stamp = row["version"]
        path = CORPUS / "utah-code" / f"{stamp}.xml.gz"
        size, sha = digest(path)
        name, note = title_metadata(path)
        items.append(
            ManifestItem(
                # The stored filename is the version stamp, and `CorpusStore` resolves an item_id
                # to a filename, so the stamp is the item_id whether or not it is pretty. The
                # readable handle is `citation`, which `Corpus.resolve` matches on equally.
                item_id=stamp,
                citation=f"Utah Code Title {row['title']}",
                title=name or f"Utah Code Title {row['title']}",
                authority_tier="legislative",
                validity="in-force",
                validity_note=note,
                translation_status=TRANSLATION_STATUS,
                version_id=stamp,
                lang=LANG,
                source_url=row["url"],
                retrieved=row["retrieved"],
                media_type="application/xml",
                bytes=size,
                sha256=sha,
            )
        )
    return Manifest(items)


def admin_rules() -> Manifest:
    rows = read_tsv(CORPUS / "MANIFEST-admin-rules.tsv")
    items = []
    for row in rows:
        rule = row["rule"]
        path = CORPUS / "admin-rules" / f"{rule}.txt.gz"
        size, sha = digest(path)
        items.append(
            ManifestItem(
                item_id=rule,
                citation=f"Utah Admin. Code {rule}",
                title=row["name"],
                # Made by an agency under authority the Legislature delegated to it, through the
                # Utah Administrative Rulemaking Act. The textbook case for this tier.
                authority_tier="delegated",
                validity="in-force",
                validity_note="",
                translation_status=TRANSLATION_STATUS,
                # The rule's own effective date is the only version the Administrative Code
                # publishes; there is no stamp equivalent to the Code's.
                version_id=iso_date(row["effective"]),
                lang=LANG,
                source_url=row["url"],
                retrieved=row["retrieved"],
                media_type="text/plain",
                bytes=size,
                sha256=sha,
            )
        )
    return Manifest(items)


# What utcourts.gov puts on the page of a rule that is no longer operative. Matched on the whole
# sentence rather than on the word, because the word alone is a false-positive generator: three
# live rules say "repealed" in their own text -- URE-502 (Husband - Wife.), URCrP-1, UCJA-2-207 --
# and a bare `\brepealed\b` marks all three as dead law. The corresponding check over the
# administrative rules matches 129 of 2,294 on `repealed|expired|superseded` and none of them is
# repealed either; they are rules *about* repeal procedure, expired fuel cards and expired filing
# deadlines. This repo has twice been burned by a regex that did not mean what it looked like
# (findings/second-sweep.md), so the pattern is narrow and the residue is counted, not assumed.
LIFECYCLE = (
    ("This Rule has been repealed.", "repealed"),
    ("This Rule has been renumbered.", "amended"),
    ("This Rule number is reserved.", "not-yet-applicable"),
)

_REPEALED_ON = re.compile(r"This Rule was repealed on ([\d/]+)")
_RENUMBERED_AS = re.compile(r"RENUMBERED AS (.+?)\s*$", re.M)
# "(Rule 3-306.05. Interpreter removal, discipline, and formal complaints.)" -- a repealed rule's
# page keeps its old heading in parentheses, which is the only surviving record of what it said.
_OLD_HEADING = re.compile(r"\(Rule [\w.\-]+\.\s*(.+?)\)", re.S)
# "URCP Rule 69 (Rules of Civil Procedure) - Utah Courts", "UCJA Appendix A (...)"
_PAGE_TITLE = re.compile(r"^\w+\s+(Rule|Appendix)\s+(\S+)\s*\(")


def court_status(text: str) -> tuple[str, str]:
    """The rule's validity and the note that has to travel with it.

    utcourts.gov serves a page for every rule number it has ever used, so a repealed rule and a
    live one are the same kind of object on disk -- roughly 800 bytes of site navigation is all
    that distinguishes the dead ones by size. Reading the page's own sentence is the only way to
    tell, and until this manifest existed nothing in the repo did.
    """
    for marker, validity in LIFECYCLE:
        if marker not in text:
            continue
        note = f"the Utah Courts rule page states “{marker}”"
        when = _REPEALED_ON.search(text)
        if when:
            note += f", repealed on {when.group(1)}"
        target = _RENUMBERED_AS.search(text)
        if target:
            note += f"; renumbered as {target.group(1).strip()}"
        return validity, note
    return "in-force", ""


def court_title(row: dict, text: str) -> str:
    """The rule's heading, from the manifest if the fetcher caught one and from the page if not."""
    if row["heading"].strip():
        return row["heading"].strip()
    old = _OLD_HEADING.search(text)
    if old:
        heading = re.sub(r"\s+", " ", old.group(1)).strip()
        if heading and not heading.upper().startswith("REPEALED"):
            return heading
    page = _PAGE_TITLE.match(text.strip())
    if page:
        return f"{page.group(1)} {page.group(2)}"
    return row["rule"]


def court_rules() -> Manifest:
    rows = read_tsv(CORPUS / "MANIFEST-court-rules.tsv")
    items = []
    for row in rows:
        rule = row["rule"]
        path = CORPUS / "court-rules" / f"{rule}.txt.gz"
        size, sha = digest(path)
        text = gzip.decompress(path.read_bytes()).decode("utf-8", "replace")
        number = rule[len(row["set"]) + 1 :] if rule.startswith(row["set"] + "-") else rule
        validity, note = court_status(text)
        effective = re.search(r"Effective:\s*([\d/]+)", text)
        items.append(
            ManifestItem(
                item_id=rule,
                citation=f"Utah {row['set_name']} {number}",
                title=court_title(row, text),
                # `delegated`, not `judicial`. The ladder's `judicial` rung is for binding court
                # *decisions* (docs/taxonomy.md in id-law-kit), and a rule of procedure is not a
                # decision -- it is a prospective general rule made under a grant of rulemaking
                # power, which is the same kind of document as an agency rule. Filing it at
                # `judicial` would also rank it *below* an agency rule, and a Utah Rule of Civil
                # Procedure does not yield to one. The grant here is constitutional rather than
                # statutory (Utah Const. art. VIII, sec. 4), which is an argument for a higher
                # rung; the ladder has none between `constitutional` and `legislative`, and it
                # orders documents by kind rather than by how hard they are to amend.
                authority_tier="delegated",
                validity=validity,
                validity_note=note,
                translation_status=TRANSLATION_STATUS,
                # The rule text carries its own effective date on 498 of 661 pages; there is no
                # version stamp equivalent to the Code's.
                version_id=iso_date(effective.group(1)) if effective else "",
                lang=LANG,
                source_url=row["url"],
                retrieved=row["retrieved"],
                media_type="text/plain",
                bytes=size,
                sha256=sha,
            )
        )
    return Manifest(items)


LAYERS = {
    "utah-code": utah_code,
    "admin-rules": admin_rules,
    "court-rules": court_rules,
}


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="rebuild in memory and compare against what is on disk, writing nothing",
    )
    args = ap.parse_args()

    stale = False
    for layer, build in LAYERS.items():
        manifest = build()
        dest = CORPUS / layer / "MANIFEST.tsv"
        if args.check:
            if not dest.exists():
                print(f"{layer}: MANIFEST.tsv is missing")
                stale = True
                continue
            same = Manifest.read(dest) == manifest
            print(f"{layer}: {len(manifest)} items, {'up to date' if same else 'STALE'}")
            stale = stale or not same
        else:
            manifest.write(dest)
            print(f"{layer}: wrote {len(manifest)} items to {dest.relative_to(ROOT)}")

    if args.check and stale:
        print("\nRe-run without --check to rebuild.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
