#!/usr/bin/env python3
"""Pull the verbatim text of a Utah statute or administrative rule out of the local corpus.

This is the citation primitive for the research process: every claim about Utah law must be
backed by output from this tool, so that a citation in a finding can be mechanically checked
against the retrieved text rather than trusted.

A reference beginning with R is an administrative rule; anything else is a Code section. Both
layers matter -- the fishing-license probe found the identity requirement in the *rule*
(R657-45-2) after the statute turned out to have none.

Usage:
    python3 tools/cite.py 23A-4-601              # one Code section
    python3 tools/cite.py 63G-12                 # a whole Code chapter
    python3 tools/cite.py 63G-12-402 --raw       # keep XML markup
    python3 tools/cite.py R657-45                # a whole admin rule
    python3 tools/cite.py R657-45-2              # one rule section
    python3 tools/cite.py --grep 'penalty of perjury' --title 26B
    python3 tools/cite.py --grep 'verification of identity' --rules
"""

import argparse
import gzip
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "corpus"
CORPUS = BASE / "utah-code"
RULES = BASE / "admin-rules"


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


def load_rule(ref: str) -> tuple[str, str]:
    """Resolve an admin-rule reference to (rule number, text).

    R657-45-2 is a section of rule R657-45, so back off one dash at a time until a
    stored rule matches.
    """
    parts = ref.split("-")
    for cut in range(len(parts), 1, -1):
        candidate = "-".join(parts[:cut])
        path = RULES / f"{candidate}.txt.gz"
        if path.exists():
            return candidate, gzip.decompress(path.read_bytes()).decode("utf-8", "replace")
    raise SystemExit(
        f"no stored rule matches '{ref}'. Fetch it with:\n"
        f"    python3 tools/fetch-utah-admin-rules.py {parts[0]}"
    )


def rule_section(text: str, ref: str) -> str | None:
    """Slice one section (e.g. R657-45-2) out of a rule, up to the next section heading."""
    m = re.search(rf"^{re.escape(ref)}\.\s", text, re.M)
    if not m:
        return None
    rest = text[m.start():]
    nxt = re.search(r"^R\d+[A-Za-z]?-\d+[A-Za-z]?-\d+\w*\.\s", rest[1:], re.M)
    return rest[: nxt.start() + 1] if nxt else rest


def grep_rules(pattern: str, prefix: str | None) -> None:
    rx = re.compile(pattern, re.I)
    files = sorted(RULES.glob(f"{prefix.upper()}-*.txt.gz" if prefix else "*.txt.gz"))
    if not files:
        raise SystemExit(f"no rules in {RULES} (run tools/fetch-utah-admin-rules.py)")
    for f in files:
        text = gzip.decompress(f.read_bytes()).decode("utf-8", "replace")
        if not rx.search(text):
            continue
        # Report the rule section containing each hit, so the output is citable.
        heads = list(re.finditer(r"^(R\d+[A-Za-z]?-\d+[A-Za-z]?-\d+\w*)\.\s*(.*)$", text, re.M))
        for m in rx.finditer(text):
            here = [h for h in heads if h.start() <= m.start()]
            label = f"{here[-1].group(1)}\t{here[-1].group(2)[:60]}" if here else f.name
            snippet = re.sub(r"\s+", " ", text[max(0, m.start() - 90) : m.start() + 110])
            print(f"{label}\n    …{snippet}…")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", nargs="?", help="Code section (23A-4-601) or admin rule (R657-45-2)")
    ap.add_argument("--raw", action="store_true", help="emit XML instead of flattened text")
    ap.add_argument("--grep", metavar="PATTERN", help="search the corpus, printing section numbers")
    ap.add_argument("--title", help="restrict --grep to one title (26B) or rule prefix (R657)")
    ap.add_argument("--rules", action="store_true", help="search admin rules instead of the Code")
    args = ap.parse_args()

    if args.grep:
        if args.rules or (args.title or "").upper().startswith("R"):
            grep_rules(args.grep, args.title)
            return
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

    if ref.startswith("R") and re.match(r"R\d", ref):
        rule, text = load_rule(ref)
        if ref == rule:
            print(text)
            return
        section = rule_section(text, ref)
        if section is None:
            raise SystemExit(f"'{ref}' not found in rule {rule}")
        print(section)
        return

    frag = extract(load(title_of(ref)), ref)
    if frag is None:
        raise SystemExit(f"'{ref}' not found in Title {title_of(ref)}")
    print(frag if args.raw else plain(frag))


if __name__ == "__main__":
    main()
