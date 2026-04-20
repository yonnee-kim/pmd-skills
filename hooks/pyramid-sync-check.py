#!/usr/bin/env python3
"""Pyramid sync Stop hook. Silent unless mapped contract drift detected.

Posts at most one short line. Caller (Claude) then decides whether to run
/pyramid-sync. Does not analyze signatures — that's the skill's job.

Contract: see shared/mapping-spec.md.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=5)
        return r.stdout
    except Exception:
        return ""


def changed_files(root: Path) -> set[str]:
    files: set[str] = set()
    for args in (
        ["git", "-C", str(root), "diff", "--name-only"],
        ["git", "-C", str(root), "diff", "--name-only", "--cached"],
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
    ):
        for line in run(args).splitlines():
            line = line.strip()
            if line:
                files.add(line)
    return files


FM_SPLIT = re.compile(r"^---\s*$", re.M)
IMPL_BLOCK = re.compile(r"^implements:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)", re.M)
IMPL_INLINE = re.compile(r"^implements:\s*\[(.+?)\]\s*$", re.M)


def parse_implements(fm_text: str) -> list[str]:
    m = IMPL_BLOCK.search(fm_text)
    if m:
        return [
            ln.strip().lstrip("-").strip().strip("'\"")
            for ln in m.group(1).splitlines()
            if ln.strip()
        ]
    m = IMPL_INLINE.search(fm_text)
    if m:
        return [s.strip().strip("'\"") for s in m.group(1).split(",") if s.strip()]
    return []


def find_contract_docs(root: Path) -> list[Path]:
    # Override: user-supplied glob, trusted as-is
    override = os.environ.get("PYRAMID_CONTRACT_GLOB", "").strip()
    if override:
        return [p for p in root.glob(override) if p.is_file()]

    # Default: scan tracked .md files' frontmatter for `implements:` field
    # (respects .gitignore, layer-agnostic — SSOT is the field itself)
    tracked = [
        line.strip()
        for line in run(["git", "-C", str(root), "ls-files", "--", "*.md"]).splitlines()
        if line.strip()
    ]
    docs: list[Path] = []
    for rel in tracked:
        doc = root / rel
        try:
            head = doc.read_text(encoding="utf-8", errors="ignore")[:2048]
        except Exception:
            continue
        parts = FM_SPLIT.split(head, maxsplit=2)
        if len(parts) < 3:
            continue
        if parse_implements(parts[1]):
            docs.append(doc)
    return docs


def build_index(docs: list[Path]) -> dict[str, list[str]]:
    idx: dict[str, list[str]] = {}
    for doc in docs:
        try:
            text = doc.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        parts = FM_SPLIT.split(text, maxsplit=2)
        if len(parts) < 3:
            continue
        for path in parse_implements(parts[1]):
            idx.setdefault(path, []).append(str(doc))
    return idx


def _debug(msg: str) -> None:
    if os.environ.get("PYRAMID_SYNC_DEBUG", "").strip() in ("1", "true", "yes"):
        print(f"[pyramid-sync debug] {msg}", file=sys.stderr)


def main() -> None:
    if not run(["git", "rev-parse", "--git-dir"]).strip():
        _debug("not inside a git repo — exit")
        return
    root_s = run(["git", "rev-parse", "--show-toplevel"]).strip()
    if not root_s:
        _debug("git toplevel not found — exit")
        return
    root = Path(root_s)
    _debug(f"root={root}")

    changed = changed_files(root)
    _debug(f"changed files: {len(changed)} ({sorted(changed)[:5]}{'...' if len(changed) > 5 else ''})")
    if not changed:
        return

    docs = find_contract_docs(root)
    _debug(f"contract docs discovered: {len(docs)}")
    if not docs:
        return

    index = build_index(docs)
    _debug(f"index entries (code→doc): {len(index)}")
    if not index:
        return

    drift = [f for f in changed if f in index]
    _debug(f"drift: {len(drift)} ({drift})")
    if not drift:
        return

    n = len(drift)
    print(f"pyramid-sync: {n} changed file(s) mapped to contract doc(s) — run /pyramid-sync to review")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Silent on errors — hook must never break the session.
        pass
    sys.exit(0)
