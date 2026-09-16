#!/usr/bin/env python3
"""Fetch the Utah Code as per-title XML from le.utah.gov.

le.utah.gov serves the Code through a JS shell, but the underlying content sits at
stable, version-stamped URLs. The master index (`/xcode/code.html` -> `C_<stamp>.html`)
links every title with its current version stamp:

    href="Title23A/23A.html?v=C23A_2023050320230701"

which maps directly to the whole-title XML:

    https://le.utah.gov/xcode/Title23A/C23A_2023050320230701.xml

The stamp pins the exact version of the text we retrieved, which is what a citation
needs. It is opaque, and this docstring used to describe it as
<effective-start><effective-end> in YYYYMMDD form -- which the corpus refutes. 73 of
the 96 titles carry the sentinel `1800010118000101`; Title 75A's stamp runs `20240901`
then `20240501`, so it cannot be a range; and where a title records an `<effdate>` the
stamp's halves match it inconsistently. The index serves each title's *current*
version, so the text is current as of the retrieval date rather than bounded by the
stamp -- Title 23A is stamped 2023 and carries 2025 amendments.

Titles are stored gzipped (they compress ~10x and `rg -z` searches them transparently)
alongside a manifest recording URL, stamp, retrieval date, uncompressed size, and
SHA-256 for provenance.

Usage:
    python3 tools/fetch-utah-code.py                 # fetch all titles
    python3 tools/fetch-utah-code.py 23A 63G 53      # fetch specific titles
"""

import gzip
import hashlib
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

BASE = "https://le.utah.gov/xcode"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "utah-code"
MANIFEST = ROOT / "corpus" / "MANIFEST-utah-code.tsv"
UA = "bakobo-utah-id-law-research/1.0 (+https://github.com/bakobo/utah-id-law)"
DELAY = 0.5  # be polite to a public .gov server


def get(url: str, tries: int = 3) -> bytes:
    """Fetch a URL, retrying on transient failure."""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - retry anything transient
            if attempt == tries - 1:
                raise
            print(f"    retry {attempt + 1}/{tries - 1} after {exc}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def index_stamp() -> str:
    """Resolve the master index shell to its current version file."""
    shell = get(f"{BASE}/code.html").decode("utf-8", "replace")
    m = re.search(r"\['(C_\d+)\.html'", shell)
    if not m:
        raise SystemExit("could not find the master index version in /xcode/code.html")
    return m.group(1)


def titles(index_html: str) -> list[tuple[str, str]]:
    """Extract (title number, version stamp) for every title in the Code."""
    found = re.findall(r'href="Title([0-9A-Z]+)/[^"]*\?v=(C[0-9A-Z]+_\d+)"', index_html)
    # The index lists each title once, but dedupe defensively and keep document order.
    seen, out = set(), []
    for num, stamp in found:
        if num not in seen:
            seen.add(num)
            out.append((num, stamp))
    return out


def main() -> None:
    wanted = {t.upper() for t in sys.argv[1:]}
    OUT.mkdir(parents=True, exist_ok=True)

    index_html = get(f"{BASE}/{index_stamp()}.html").decode("utf-8", "replace")
    all_titles = titles(index_html)
    todo = [t for t in all_titles if not wanted or t[0] in wanted]
    if wanted:
        missing = wanted - {t[0] for t in all_titles}
        if missing:
            print(f"warning: no such title(s): {', '.join(sorted(missing))}", file=sys.stderr)
    print(f"{len(todo)} of {len(all_titles)} titles to fetch -> {OUT}")

    retrieved = date.today().isoformat()
    rows, total = [], 0
    for i, (num, stamp) in enumerate(todo, 1):
        url = f"{BASE}/Title{num}/{stamp}.xml"
        dest = OUT / f"{stamp}.xml.gz"
        try:
            raw = get(url)
        except Exception as exc:  # noqa: BLE001 - record the gap, keep going
            print(f"[{i}/{len(todo)}] Title {num}: FAILED ({exc})", file=sys.stderr)
            rows.append((num, stamp, url, retrieved, "0", "FETCH-FAILED"))
            continue
        # A 404 from this host is a 25KB HTML error page, not XML.
        if not raw.lstrip().startswith(b"<title"):
            print(f"[{i}/{len(todo)}] Title {num}: NOT XML ({len(raw)} bytes)", file=sys.stderr)
            rows.append((num, stamp, url, retrieved, str(len(raw)), "NOT-XML"))
            continue
        dest.write_bytes(gzip.compress(raw, 9))
        digest = hashlib.sha256(raw).hexdigest()
        rows.append((num, stamp, url, retrieved, str(len(raw)), digest))
        total += len(raw)
        print(f"[{i}/{len(todo)}] Title {num}: {len(raw):,} bytes -> {dest.name}")
        time.sleep(DELAY)

    # Merge with any existing manifest so partial runs accumulate rather than truncate.
    header = "title\tversion\turl\tretrieved\tbytes\tsha256"
    existing = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines()[1:]:
            if line.strip():
                existing[line.split("\t")[0]] = line
    for row in rows:
        existing[row[0]] = "\t".join(row)

    def sort_key(title: str) -> tuple[int, str]:
        m = re.match(r"(\d+)([A-Z]*)", title)
        return (int(m.group(1)), m.group(2)) if m else (999, title)

    ordered = [existing[k] for k in sorted(existing, key=sort_key)]
    MANIFEST.write_text(header + "\n" + "\n".join(ordered) + "\n")
    print(f"\n{total:,} bytes of XML this run; manifest has {len(ordered)} titles")


if __name__ == "__main__":
    main()
