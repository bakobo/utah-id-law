#!/usr/bin/env python3
"""Pull the verbatim text of a Utah Code section out of the local corpus.

This is the citation primitive for the research process: every claim about Utah law must be
backed by output from this tool, so that a section number in a finding can be mechanically
checked against the retrieved text rather than trusted.

Usage:
    python3 tools/cite.py 23A-4-601              # one section
    python3 tools/cite.py 63G-12-402 --raw       # keep XML markup
    python3 tools/cite.py 63G-12                 # a whole chapter
    python3 tools/cite.py --grep 'penalty of perjury' --title 26B
"""

import argparse
import gzip
import re
import sys
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus" / "utah-code"


def title_of(ref: str) -> str:
    """'63G-12-402' -> '63G'. Titles may carry a letter suffix (23A, 53G, 70A)."""
    m = re.match(r"(\d+[A-Z]?)", ref.upper())
    if not m:
        raise SystemExit(f"cannot parse a title out of '{ref}'")
    return m.group(1)


def load(title: str) -> str:
    hits = sorted(CORPUS.glob(f"C{title}_*.xml.gz"))
    if not hits:
        raise SystemExit(
            f"Title {title} is not in the corpus. Fetch it with:\n"
            f"    python3 tools/fetch-utah-code.py {title}"
        )
    return gzip.decompress(hits[0].read_bytes()).decode("utf-8", "replace")


def plain(xml: str) -> str:
    """Flatten the Code's nested <subsection> markup into readable, numbered text."""
    xml = re.sub(r"<histories>.*?</histories>", "", xml, flags=re.S)
    xml = re.sub(r"<subsection number=\"([^\"]+)\">", r"\n[\1] ", xml)
    xml = re.sub(r"<section number=\"([^\"]+)\">", r"\n\n## \1\n", xml)
    xml = re.sub(r"<catchline>(.*?)</catchline>", r"\1\n", xml)
    xml = re.sub(r"<[^>]+>", "", xml)
    return re.sub(r"\n\s*\n+", "\n", xml).strip()


def extract(xml: str, ref: str) -> str | None:
    """Return the XML fragment for a section or chapter reference."""
    for tag in ("section", "chapter"):
        m = re.search(
            rf'<{tag} number="{re.escape(ref)}">(.*?)(?=<{tag} number="|</{tag}>)', xml, re.S
        )
        if m:
            return m.group(1)
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", nargs="?", help="section or chapter, e.g. 23A-4-601 or 63G-12")
    ap.add_argument("--raw", action="store_true", help="emit XML instead of flattened text")
    ap.add_argument("--grep", metavar="PATTERN", help="search the corpus, printing section numbers")
    ap.add_argument("--title", help="restrict --grep to one title, e.g. 26B")
    args = ap.parse_args()

    if args.grep:
        titles = [args.title.upper()] if args.title else None
        files = (
            [f for t in titles for f in CORPUS.glob(f"C{t}_*.xml.gz")]
            if titles
            else sorted(CORPUS.glob("*.xml.gz"))
        )
        rx = re.compile(args.grep, re.I)
        for f in files:
            xml = gzip.decompress(f.read_bytes()).decode("utf-8", "replace")
            # Walk sections so every hit can be reported with the section that contains it.
            for m in re.finditer(r'<section number="([^"]+)">(.*?)(?=<section number="|</part>)', xml, re.S):
                num, body = m.group(1), m.group(2)
                if rx.search(re.sub(r"<[^>]+>", " ", body)):
                    cat = re.search(r"<catchline>(.*?)</catchline>", body)
                    print(f"{num}\t{re.sub('<[^>]+>', '', cat.group(1)) if cat else ''}")
        return

    if not args.ref:
        ap.error("give a section/chapter reference, or use --grep")

    ref = args.ref.upper()
    frag = extract(load(title_of(ref)), ref)
    if frag is None:
        raise SystemExit(f"'{ref}' not found in Title {title_of(ref)}")
    print(frag if args.raw else plain(frag))


if __name__ == "__main__":
    main()
