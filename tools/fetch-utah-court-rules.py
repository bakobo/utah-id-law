#!/usr/bin/env python3
"""Fetch the Utah court rules from utcourts.gov.

The third body of Utah law. Statutes come from the legislature and administrative rules from
agencies; **court rules are promulgated by the Utah Supreme Court** under its constitutional
rulemaking power, and they govern procedure in the courts. Neither of the other corpora contains
them, which is why questions about filing, bail, and testimony were previously unresolvable.

Six rule sets:

    URCP   Rules of Civil Procedure          URAP   Rules of Appellate Procedure
    URCrP  Rules of Criminal Procedure       URJP   Rules of Juvenile Procedure
    URE    Rules of Evidence                 UCJA   Code of Judicial Administration

**Do not use `viewall.php`.** It looks like a one-request bulk download and silently truncates:
measured against the per-set indexes it returned 106 of 152 URCP rules and 14 of 295 UCJA rules.
This instead enumerates rule ids from each set's index page and fetches them individually.

`www.utcourts.gov` returns 406 to scripted clients; `legacy.utcourts.gov` serves the same current
text (rules carry effective dates into 2026).

Ids ending in `S` are rules superseded in 2011; they are skipped so the corpus holds current law
only. Every rule page also carries a "Rule printed on <date> at <time>" line whose timestamp would
change the SHA-256 on every refetch, defeating the manifest's purpose, so it is stripped.

Usage:
    python3 tools/fetch-utah-court-rules.py           # all six sets
    python3 tools/fetch-utah-court-rules.py urcp ure  # named sets only
"""

import gzip
import hashlib
import html as html_mod
import re
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

HOST = "https://legacy.utcourts.gov/rules"
SETS = {
    "urcp": ("URCP", "Rules of Civil Procedure"),
    "urcrp": ("URCrP", "Rules of Criminal Procedure"),
    "ure": ("URE", "Rules of Evidence"),
    "urap": ("URAP", "Rules of Appellate Procedure"),
    "urjp": ("URJP", "Rules of Juvenile Procedure"),
    "ucja": ("UCJA", "Code of Judicial Administration"),
}

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "corpus" / "court-rules"
MANIFEST = ROOT / "corpus" / "MANIFEST-court-rules.tsv"
UA = "bakobo-utah-id-law-research/1.0 (+https://github.com/bakobo/utah-id-law)"
DELAY = 0.35

PRINTED = re.compile(r"Rule printed on [^.]*\.\s*(?:Go to \S+ for current rules\.)?\s*", re.I)


def get(url: str, tries: int = 3) -> bytes:
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


def to_text(raw: bytes) -> str:
    doc = raw.decode("utf-8", "replace")
    doc = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", doc, flags=re.S | re.I)
    doc = re.sub(r"</(div|p|tr|h[1-6]|li)>", "\n", doc, flags=re.I)
    doc = re.sub(r"<br\s*/?>", "\n", doc, flags=re.I)
    doc = re.sub(r"<[^>]+>", "", doc)
    doc = html_mod.unescape(doc).replace("\xa0", " ")
    doc = PRINTED.sub("", doc)
    doc = re.sub(r"[ \t]+", " ", doc)
    return re.sub(r"\n\s*\n+", "\n", doc).strip()


def body_of(text: str, rule_id: str) -> tuple[str, str]:
    """Trim site chrome to the rule itself; return (heading, body).

    Every page wraps the rule in ~15 lines of site navigation. The rule proper starts at the
    "Rule <id>." heading -- which the page indents, so the match must tolerate leading space.
    """
    m = re.search(rf"^[ \t]*Rule {re.escape(rule_id)}\.[ \t]*(.*)$", text, re.M | re.I)
    if not m:
        return "", text
    body = text[m.start():].lstrip()
    # Drop the trailing navigation block that follows every rule.
    cut = re.search(
        r"\n[ \t]*(?:Utah Courts|Contact Us|Website Links|Related Information|"
        r"Utah State Courts|<< Previous Rule)\b",
        body,
    )
    if cut:
        body = body[: cut.start()]
    return m.group(1).strip(), body.strip()


def rule_ids(key: str) -> list[str]:
    html = get(f"{HOST}/{key}.php").decode("utf-8", "replace")
    ids = re.findall(r"rule=([0-9A-Za-z_.-]+)", html)
    # The index lists some rules twice differing only in case (64D and 64d). Fetching both
    # produced 29 duplicate files and inflated every per-corpus denominator, so dedupe
    # case-insensitively, preferring the first spelling seen.
    seen, out = {}, []
    for r in ids:
        if re.fullmatch(r"\d+[A-Za-z]?S", r):  # drop rules superseded in 2011
            continue
        if r.casefold() not in seen:
            seen[r.casefold()] = r
            out.append(r)
    return sorted(out, key=str.casefold)


def main() -> None:
    wanted = {a.lower() for a in sys.argv[1:]} or set(SETS)
    unknown = wanted - set(SETS)
    if unknown:
        raise SystemExit(f"unknown rule set(s): {', '.join(sorted(unknown))}")
    OUT.mkdir(parents=True, exist_ok=True)

    retrieved = date.today().isoformat()
    rows, total, failed = [], 0, 0
    for key in [k for k in SETS if k in wanted]:
        label, name = SETS[key]
        ids = rule_ids(key)
        print(f"{label:6} {name:34} {len(ids)} rules")
        for i, rid in enumerate(ids, 1):
            url = f"{HOST}/view.php?type={key}&rule={rid}"
            try:
                text = to_text(get(url))
            except Exception as exc:  # noqa: BLE001 - record the gap, keep going
                print(f"  {label}-{rid}: FAILED ({exc})", file=sys.stderr)
                failed += 1
                continue
            heading, body = body_of(text, rid)
            if len(body) < 80:
                print(f"  {label}-{rid}: empty/short, skipped", file=sys.stderr)
                failed += 1
                continue
            blob = body.encode("utf-8")
            (OUT / f"{label}-{rid}.txt.gz").write_bytes(gzip.compress(blob, 9))
            rows.append(
                (f"{label}-{rid}", heading.replace("\t", " ")[:120], label, name, url,
                 retrieved, str(len(blob)), hashlib.sha256(blob).hexdigest())
            )
            total += len(blob)
            if i % 50 == 0:
                print(f"  …{i}/{len(ids)}", flush=True)
            time.sleep(DELAY)

    header = "rule\theading\tset\tset_name\turl\tretrieved\tbytes\tsha256"
    existing = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines()[1:]:
            if line.strip():
                existing[line.split("\t")[0]] = line
    for row in rows:
        existing[row[0]] = "\t".join(row)

    def sort_key(cite: str) -> tuple:
        m = re.match(r"([A-Za-z]+)-(.*)", cite)
        if not m:
            return (cite,)
        parts = [int(p) if p.isdigit() else p for p in re.split(r"[-.]", m.group(2))]
        return (m.group(1), *[(0, p) if isinstance(p, int) else (1, p) for p in parts])

    MANIFEST.write_text(
        header + "\n" + "\n".join(existing[k] for k in sorted(existing, key=sort_key)) + "\n"
    )
    print(f"\n{total:,} bytes stored, {failed} skipped; manifest has {len(existing)} rules")


if __name__ == "__main__":
    main()
