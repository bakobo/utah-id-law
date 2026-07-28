#!/usr/bin/env python3
"""Fetch the Utah Administrative Code from adminrules.utah.gov.

There is no bulk download and no documented API. The site is a React SPA; these endpoints
were recovered by reading its JS bundle (`/static/js/main.*.chunk.js`). Two quirks matter,
and neither is guessable:

  * Missing path parameters are sent as the *literal string* "undefined", not omitted.
  * `searchRuleDataTotal` takes (searchTerm, ruleType) -- the second argument is a rule
    type such as "Current Rules", not a page number. Any single-letter search term returns
    the complete set, so one request enumerates the whole code.

Pipeline:
    GET /api/public/searchRuleDataTotal/a/Current%20Rules   -> all rules + metadata
    GET /api/public/getHTML/{htmlDownload}                  -> one rule's full text

The index already carries each rule's `htmlDownload` path, so no per-rule metadata call is
needed.

**Storage: extracted text, not the served HTML.** The rules are RTF-converted to HTML with
per-span absolute positioning (`<div class="awdiv" style="top:279.42pt; z-index:2;">`), which
carries no legal content and does not compress -- measured over the full code, storing HTML
costs 182 MB against 12.5 MB for the text it contains (text is 8% of the HTML characters).
Provenance is preserved instead by recording each rule's source URL and the **SHA-256 of the
original HTML** in the manifest, so any stored text can be checked against a refetch.

Historical note: `https://rules.utah.gov/publicat/code_zip/r{NNN}.zip` still serves per-title
RTF archives, but they are a **stale April-2020 snapshot** -- usable for enumerating old rule
numbers, not for current text. This tool uses the live API instead.

Usage:
    python3 tools/fetch-utah-admin-rules.py            # all current rules
    python3 tools/fetch-utah-admin-rules.py R657 R414  # only these rule prefixes
"""

import gzip
import hashlib
import html as html_mod
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

API = "https://adminrules.utah.gov/api/public"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "admin-rules"
MANIFEST = ROOT / "corpus" / "MANIFEST-admin-rules.tsv"
UA = "bakobo-utah-id-law-research/1.0 (+https://github.com/bakobo/utah-id-law)"
DELAY = 0.3


def get(url: str, tries: int = 3) -> bytes:
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - retry anything transient
            if attempt == tries - 1:
                raise
            print(f"    retry {attempt + 1}/{tries - 1} after {exc}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    raise AssertionError("unreachable")


def to_text(raw: bytes) -> str:
    """Strip the RTF-derived markup, keeping block boundaries as newlines."""
    doc = raw.decode("utf-8", "replace")
    doc = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", doc, flags=re.S | re.I)
    doc = re.sub(r"</(div|p|tr|h[1-6]|li)>", "\n", doc, flags=re.I)
    doc = re.sub(r"<br\s*/?>", "\n", doc, flags=re.I)
    doc = re.sub(r"<[^>]+>", "", doc)
    doc = html_mod.unescape(doc)
    doc = doc.replace("\xa0", " ")
    doc = re.sub(r"[ \t]+", " ", doc)
    return re.sub(r"\n\s*\n+", "\n", doc).strip()


def index() -> list[dict]:
    """Enumerate every current rule. The search term is arbitrary; 'a' returns all."""
    raw = get(f"{API}/searchRuleDataTotal/a/{urllib.parse.quote('Current Rules')}")
    agencies = json.loads(raw)
    rules = []
    for agency in agencies:
        for program in agency.get("programs", []):
            for rule in program.get("rules", []):
                rule["_agency"] = agency.get("name", "")
                rule["_program"] = program.get("name", "")
                rules.append(rule)
    return rules


def main() -> None:
    wanted = {p.upper().rstrip("-") for p in sys.argv[1:]}
    OUT.mkdir(parents=True, exist_ok=True)

    rules = index()
    print(f"{len(rules)} current rules in the index")
    if wanted:
        rules = [r for r in rules if r["referenceNumber"].split("-")[0].upper() in wanted]
        print(f"{len(rules)} match {', '.join(sorted(wanted))}")

    retrieved = date.today().isoformat()
    rows, total, failed = [], 0, 0
    for i, rule in enumerate(rules, 1):
        ref = rule["referenceNumber"]
        path = rule.get("htmlDownload")
        if not path:
            print(f"[{i}/{len(rules)}] {ref}: no htmlDownload in index", file=sys.stderr)
            failed += 1
            continue
        url = f"{API}/getHTML/{path}"
        try:
            raw = get(url)
        except Exception as exc:  # noqa: BLE001 - record the gap, keep going
            print(f"[{i}/{len(rules)}] {ref}: FAILED ({exc})", file=sys.stderr)
            failed += 1
            continue

        text = to_text(raw).encode("utf-8")
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", ref)
        (OUT / f"{safe}.txt.gz").write_bytes(gzip.compress(text, 9))
        rows.append(
            (
                ref,
                rule.get("name", "").replace("\t", " "),
                rule.get("_agency", "").replace("\t", " "),
                rule.get("_program", "").replace("\t", " "),
                str(rule.get("effectiveDate", "")),
                url,
                retrieved,
                str(len(text)),
                str(len(raw)),
                hashlib.sha256(raw).hexdigest(),
            )
        )
        total += len(text)
        if i % 50 == 0 or i == len(rules):
            print(f"[{i}/{len(rules)}] {ref} ({total:,} bytes so far)", flush=True)
        time.sleep(DELAY)

    # html_bytes/html_sha256 describe the ORIGINAL served HTML, not the stored text, so a
    # refetch can be verified against what we actually retrieved.
    header = (
        "rule\tname\tagency\tprogram\teffective\turl\tretrieved\t"
        "text_bytes\thtml_bytes\thtml_sha256"
    )
    existing = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines()[1:]:
            if line.strip():
                existing[line.split("\t")[0]] = line
    for row in rows:
        existing[row[0]] = "\t".join(row)

    def sort_key(ref: str) -> tuple[int, int, str]:
        m = re.match(r"R(\d+)-(\d+)", ref)
        return (int(m.group(1)), int(m.group(2)), ref) if m else (10**9, 0, ref)

    MANIFEST.write_text(
        header + "\n" + "\n".join(existing[k] for k in sorted(existing, key=sort_key)) + "\n"
    )
    print(f"\n{total:,} bytes fetched, {failed} failed; manifest has {len(existing)} rules")


if __name__ == "__main__":
    main()
