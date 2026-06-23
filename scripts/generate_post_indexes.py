#!/usr/bin/env python3
"""
generate_post_indexes.py

Scan the `_posts` folder recursively, parse front-matter, and rewrite:
- all_posts.md (all posts grouped by Month Year)
- personal_notes.md (posts in `_personal` or type: personal)
- engineering_thoughts.md (posts in `_coding` or type: coding)

Usage:
  python scripts/generate_post_indexes.py

This script makes minimal assumptions about front-matter: it parses simple
`key: value` lines from the YAML front-matter to extract `title` and `date`.
If a `title` is missing it falls back to the filename slug. Links are built
using the filename slug portion after the date (e.g. `YYYY-MM-DD-Slug.md` ->
`/YYYY/MM/DD/Slug/`).
"""
from __future__ import annotations

import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"

TARGET_ALL = ROOT / "all_posts.md"
TARGET_PERSONAL = ROOT / "personal_notes.md"
TARGET_CODING = ROOT / "engineering_thoughts.md"

POST_FILE_RE = re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(?P<slug>.+)\.(md|markdown)$")


def parse_front_matter(text: str) -> Dict[str, str]:
    fm: Dict[str, str] = {}
    if not text.startswith("---"):
        return fm
    parts = text.split("---")
    if len(parts) < 3:
        return fm
    body = parts[1]
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        fm[key] = val
    return fm


def scan_posts() -> List[Dict]:
    posts = []
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if not f.lower().endswith((".md", ".markdown")):
                continue
            path = Path(root) / f
            m = POST_FILE_RE.match(f)
            rel = path.relative_to(ROOT)
            with path.open("r", encoding="utf-8") as fh:
                txt = fh.read()
            fm = parse_front_matter(txt)
            title = fm.get("title")
            # derive date from front-matter or filename
            date_str = fm.get("date")
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str)
                except Exception:
                    try:
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
                    except Exception:
                        date = None
            else:
                date = None
            if not date and m:
                year, month, day = int(m.group("year")), int(m.group("month")), int(m.group("day"))
                date = datetime(year, month, day)
            slug = None
            if m:
                slug = m.group("slug")
            else:
                slug = path.stem

            if not title:
                # prettify slug
                t = slug.replace("-", " ")
                title = t.replace("_", " ").strip().title()

            # category by folder name or front-matter 'type' or 'categories'
            kind = None
            p = str(rel).replace("\\", "/")
            if "/_personal/" in p or p.startswith("_posts/_personal") or fm.get("type") == "personal":
                kind = "personal"
            elif "/_coding/" in p or p.startswith("_posts/_coding") or fm.get("type") == "coding":
                kind = "coding"

            # Build URL: /YYYY/MM/DD/Slug/
            if m and date:
                url = f"/{date.year}/{date.month:02d}/{date.day:02d}/{slug}/"
            elif date:
                url = f"/{date.year}/{date.month:02d}/{date.day:02d}/{slug}/"
            else:
                url = f"/{slug}/"

            posts.append({
                "path": str(rel),
                "title": title,
                "date": date,
                "url": url,
                "kind": kind,
            })
    # sort by date descending (None at end)
    posts.sort(key=lambda p: p["date"] or datetime.min, reverse=True)
    return posts


def group_by_month(posts: List[Dict]) -> List[Tuple[str, List[Dict]]]:
    groups = defaultdict(list)
    order = []
    for p in posts:
        d = p["date"]
        if d:
            key = f"{d.strftime('%B')} {d.year}"
        else:
            key = "Undated"
        if key not in groups:
            order.append(key)
        groups[key].append(p)
    return [(k, groups[k]) for k in order]


def write_index(target: Path, header_front_matter: str, groups: List[Tuple[str, List[Dict]]]):
    lines = []
    lines.append(header_front_matter.rstrip())
    lines.append("")
    for month, items in groups:
        lines.append("--------")
        lines.append("")
        lines.append(month)
        lines.append("")
        for it in items:
            lines.append(f"[{it['title']}]({it['url']})")
            lines.append("")
    content = "\n".join(lines).rstrip() + "\n"
    target.write_text(content, encoding="utf-8")


def read_front_matter_block(path: Path) -> str:
    txt = path.read_text(encoding="utf-8")
    if txt.startswith("---"):
        parts = txt.split("---", 2)
        if len(parts) >= 2:
            return "---\n" + parts[1] + "---\n"
    # fallback minimal front-matter
    return "---\nlayout: page\n---\n"


def main():
    posts = scan_posts()
    groups = group_by_month(posts)

    # write all_posts.md
    header = read_front_matter_block(TARGET_ALL) if TARGET_ALL.exists() else "---\nlayout: page\ntitle: Index\n---\n"
    write_index(TARGET_ALL, header, groups)

    # personal
    personal_posts = [p for p in posts if p["kind"] == "personal"]
    header_p = read_front_matter_block(TARGET_PERSONAL) if TARGET_PERSONAL.exists() else "---\nlayout: page\ntitle: Personal Notes\n---\n"
    write_index(TARGET_PERSONAL, header_p, group_by_month(personal_posts))

    # coding
    coding_posts = [p for p in posts if p["kind"] == "coding"]
    header_c = read_front_matter_block(TARGET_CODING) if TARGET_CODING.exists() else "---\nlayout: page\ntitle: Engineering Thoughts\n---\n"
    write_index(TARGET_CODING, header_c, group_by_month(coding_posts))

    print(f"Wrote: {TARGET_ALL}\nWrote: {TARGET_PERSONAL}\nWrote: {TARGET_CODING}")


if __name__ == "__main__":
    main()
