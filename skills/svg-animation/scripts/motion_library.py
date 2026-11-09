#!/usr/bin/env python3
"""Offline private SVG motion reference library; no network, renderers or AI calls."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

MAX_BYTES = 64 * 1024 * 1024
VERSION = 1
MEDIA_TYPES = {
    ".svg": "svg", ".gif": "animated-media", ".mp4": "animated-media",
    ".webm": "animated-media", ".json": "lottie-json",
    ".png": "static-image", ".jpg": "static-image",
    ".jpeg": "static-image", ".webp": "static-image",
}
DISALLOWED_SVG_TAGS = {"script", "foreignobject", "iframe", "object", "embed", "a"}
URL_PATTERN = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE | re.DOTALL)


class InputError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def library_home(explicit: str | None = None) -> Path:
    value = explicit or os.environ.get("SVG_ANIMATION_HOME")
    return Path(value).expanduser().resolve() if value else Path.home() / ".svg-animation-skill"


def _private_dir(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name == "posix":
        directory.chmod(0o700)


def _atomic_json(path: Path, document: dict) -> None:
    _private_dir(path.parent)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=".pending-",
        suffix=".json", delete=False
    ) as handle:
        pending = Path(handle.name)
        json.dump(document, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    try:
        if os.name == "posix":
            pending.chmod(0o600)
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)


def load_index(home: Path) -> dict:
    target = home / "index.json"
    if not target.exists():
        return {"schema_version": VERSION, "references": []}
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InputError(f"Cannot read reference index: {exc}") from exc
    if (
        not isinstance(value, dict)
        or value.get("schema_version") != VERSION
        or not isinstance(value.get("references"), list)
    ):
        raise InputError("Invalid or unsupported reference index format")
    return value


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def inspect_svg(source: bytes) -> dict:
    """Reject common active/external SVG hazards. Not a complete sanitizer."""
    upper = source.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        raise InputError("DTD and XML entities are not accepted")
    try:
        root = ET.fromstring(source)
    except ET.ParseError as exc:
        raise InputError(f"Invalid SVG XML: {exc}") from exc
    if _local_name(root.tag) != "svg":
        raise InputError("Root element must be <svg>")
    names, ids = [], []
    for element in root.iter():
        tag = _local_name(element.tag)
        names.append(tag)
        if tag in DISALLOWED_SVG_TAGS:
            raise InputError(f"Active or risky SVG element <{tag}> is forbidden")
        for full_name, value in element.attrib.items():
            attr = _local_name(full_name)
            if attr.startswith("on"):
                raise InputError(f"SVG event handler '{attr}' is forbidden")
            if attr == "href" and value.strip() and not value.strip().startswith("#"):
                raise InputError("External SVG href is forbidden")
            for match in URL_PATTERN.finditer(value):
                if not match.group(2).strip().startswith("#"):
                    raise InputError("External SVG url() references are forbidden")
            if attr == "id":
                ids.append(value)
        if tag == "style":
            css = "".join(element.itertext())
            if re.search(r"@import\b", css, re.IGNORECASE):
                raise InputError("CSS @import is forbidden inside SVG")
            for match in URL_PATTERN.finditer(css):
                if not match.group(2).strip().startswith("#"):
                    raise InputError("External CSS url() references are forbidden")
    raw_text = source.decode("utf-8", errors="replace")
    return {
        "has_viewbox": "viewBox" in root.attrib,
        "has_title": "title" in names,
        "has_reduced_motion_css": "prefers-reduced-motion" in raw_text.lower(),
        "has_css_keyframes": "@keyframes" in raw_text.lower(),
        "smil_element_count": sum(name in {
            "animate", "animatetransform", "animatemotion", "set", "animatecolor"
        } for name in names),
        "path_count": names.count("path"),
        "filter_count": names.count("filter"),
        "id_count": len(ids),
        "duplicate_ids": sorted({item for item in ids if ids.count(item) > 1}),
        "decorative": root.attrib.get("aria-hidden") == "true",
    }


def _load_source(path: Path) -> tuple[bytes, str, dict]:
    if not path.is_file():
        raise InputError(f"Reference file does not exist: {path}")
    size = path.stat().st_size
    if not 0 < size <= MAX_BYTES:
        raise InputError("Reference must be non-empty and no larger than 64 MiB")
    suffix = path.suffix.lower()
    if suffix not in MEDIA_TYPES:
        raise InputError(f"Unsupported media format: {suffix}")
    data = path.read_bytes()
    kind = MEDIA_TYPES[suffix]
    detail: dict = {}
    if suffix == ".svg":
        detail = inspect_svg(data)
    elif suffix == ".json":
        try:
            item = json.loads(data)
        except (UnicodeError, ValueError) as exc:
            raise InputError(f"Invalid JSON: {exc}") from exc
        if not isinstance(item, dict) or not isinstance(item.get("layers"), list) or "v" not in item:
            raise InputError("Only Lottie-shaped JSON (v + layers) is supported")
    else:
        magic_ok = {
            ".gif": data.startswith((b"GIF87a", b"GIF89a")),
            ".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
            ".jpg": data.startswith(b"\xff\xd8\xff"),
            ".jpeg": data.startswith(b"\xff\xd8\xff"),
            ".webp": data.startswith(b"RIFF") and data[8:12] == b"WEBP",
            ".mp4": len(data) > 12 and data[4:8] == b"ftyp",
            ".webm": data.startswith(b"\x1a\x45\xdf\xa3"),
        }
        if not magic_ok[suffix]:
            raise InputError(f"File signature does not match {suffix}")
    return data, kind, detail


def _words(values: list[str] | None, lower: bool = False) -> list[str]:
    answer = []
    for original in values or []:
        for value in original.split(","):
            word = value.strip().lower() if lower else value.strip()
            if word and word not in answer:
                answer.append(word)
    return answer


def _merge(current: list[str], fresh: list[str]) -> list[str]:
    return current + [item for item in fresh if item not in current]


def _safe_media(home: Path, entry: dict) -> Path:
    base = (home / "media").resolve()
    relative = entry.get("media_path")
    if not isinstance(relative, str):
        raise InputError("Missing reference file path")
    target = (home / relative).resolve()
    if not target.is_relative_to(base) or not target.is_file():
        raise InputError(f"Unsafe or missing reference path for {entry.get('id')}")
    return target


def add_reference(
    home: Path, source: Path, *, title: str = "",
    use_cases: list[str] | None = None, tags: list[str] | None = None,
    likes: list[str] | None = None, avoids: list[str] | None = None,
    rating: int | None = None,
) -> dict:
    if rating is not None and rating not in range(1, 6):
        raise InputError("rating must be 1..5")
    data, kind, detail = _load_source(source.expanduser().resolve())
    digest = hashlib.sha256(data).hexdigest()
    ref_id = "ref-" + digest[:20]
    rel = f"media/{digest}{source.suffix.lower()}"
    _private_dir(home / "media")
    target = home / rel
    if not target.exists():
        with target.open("xb") as handle:
            handle.write(data)
        if os.name == "posix":
            target.chmod(0o600)
    index = load_index(home)
    record = next((r for r in index["references"] if r.get("id") == ref_id), None)
    if record is None:
        record = {
            "id": ref_id, "media_path": rel, "media_type": kind,
            "title": title.strip() or source.stem,
            "use_cases": [], "tags": [], "liked_for": [], "avoid_copying": [],
            "rating": 3, "size_bytes": len(data), "source_inspection": detail,
            "created_at": _now(),
        }
        index["references"].append(record)
    for key, values, lower in [
        ("use_cases", use_cases, True),
        ("tags", tags, True),
        ("liked_for", likes, False),
        ("avoid_copying", avoids, False),
    ]:
        record[key] = _merge(record.get(key, []), _words(values, lower))
    if title.strip():
        record["title"] = title.strip()
    if rating is not None:
        record["rating"] = rating
    record["updated_at"] = _now()
    _atomic_json(home / "index.json", index)
    return {**record, "absolute_path": str(target.resolve())}


def select_references(
    home: Path, *, use_case: str | None = None,
    tags: list[str] | None = None, top: int = 2,
) -> list[dict]:
    if not 1 <= top <= 3:
        raise InputError("top must be between 1 and 3")
    desired = set(_words(tags, lower=True))
    use = use_case.lower() if use_case else None
    matching = []
    for item in load_index(home)["references"]:
        if item.get("rating", 3) < 3:
            continue
        use_match = bool(use and use in item.get("use_cases", []))
        tag_matches = desired.intersection(item.get("tags", []))
        if use and not use_match:
            continue
        if desired and not tag_matches:
            continue
        score = 40 * use_match + 10 * len(tag_matches) + item.get("rating", 3) * 2
        matching.append({
            **item, "absolute_path": str(_safe_media(home, item)),
            "match_score": score, "matched_tags": sorted(tag_matches),
        })
    matching.sort(key=lambda x: (-x["match_score"], x["id"]))
    return matching[:top]


def prepare(
    home: Path, *, request: str, use_case: str | None,
    tags: list[str], top: int,
) -> dict:
    selected = select_references(home, use_case=use_case, tags=tags, top=top)
    return {
        "schema_version": "1.0",
        "workflow": "reference-first-web-motion",
        "request": request, "use_case": use_case,
        "references": [
            {
                "id": r["id"], "path": r["absolute_path"],
                "media_type": r["media_type"], "title": r["title"],
                "borrow": r.get("liked_for", []),
                "do_not_copy": r.get("avoid_copying", []),
                "source_inspection": r.get("source_inspection", {}),
            }
            for r in selected
        ],
        "must_open_media": True,
        "instructions": [
            "Actually open/play selected references with your available tools.",
            "A file path or metadata is NOT a video/motion inspection.",
            "Static images provide style only, not temporal evidence.",
            "Extract timing, stages, easing and hierarchy; never copy branded art.",
            "Generate original editable SVG/CSS/JS/Vue code.",
            "Check reduced motion, SSR constraints, responsiveness and real playback.",
        ],
        "warnings": [] if selected else [
            "No matching local reference. Original design is allowed; do not claim reference-derived motion."
        ],
    }


def feedback(home: Path, ref_id: str, *, rating: int | None, likes: list[str], avoids: list[str]) -> dict:
    if rating is not None and rating not in range(1, 6):
        raise InputError("rating must be 1..5")
    index = load_index(home)
    item = next((r for r in index["references"] if r.get("id") == ref_id), None)
    if item is None:
        raise InputError("Reference not found")
    item["liked_for"] = _merge(item.get("liked_for", []), _words(likes))
    item["avoid_copying"] = _merge(item.get("avoid_copying", []), _words(avoids))
    if rating is not None:
        item["rating"] = rating
    item["updated_at"] = _now()
    _atomic_json(home / "index.json", index)
    return item


def remove_reference(home: Path, ref_id: str) -> dict:
    index = load_index(home)
    item = next((r for r in index["references"] if r.get("id") == ref_id), None)
    if item is None:
        raise InputError("Reference not found")
    media = _safe_media(home, item)
    index["references"].remove(item)
    _atomic_json(home / "index.json", index)
    media.unlink(missing_ok=True)
    return {"removed": ref_id}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Override ~/.svg-animation-skill (or SVG_ANIMATION_HOME)")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Explicitly save an approved reference")
    add.add_argument("--file", type=Path, required=True)
    add.add_argument("--title", default="")
    add.add_argument("--use-case", action="append", default=[])
    add.add_argument("--tag", action="append", default=[])
    add.add_argument("--like", action="append", default=[])
    add.add_argument("--avoid", action="append", default=[])
    add.add_argument("--rating", type=int, choices=range(1, 6))
    sub.add_parser("list")
    select = sub.add_parser("select")
    select.add_argument("--use-case")
    select.add_argument("--tag", action="append", default=[])
    select.add_argument("--top", type=int, default=2)
    prep = sub.add_parser("prepare")
    prep.add_argument("--use-case")
    prep.add_argument("--tag", action="append", default=[])
    prep.add_argument("--request", required=True)
    prep.add_argument("--top", type=int, default=2)
    rate = sub.add_parser("feedback")
    rate.add_argument("--id", required=True)
    rate.add_argument("--like", action="append", default=[])
    rate.add_argument("--avoid", action="append", default=[])
    rate.add_argument("--rating", type=int, choices=range(1, 6))
    rm = sub.add_parser("remove")
    rm.add_argument("--id", required=True)
    args = parser.parse_args(argv)
    home = library_home(args.home)
    try:
        if args.command == "add":
            result = add_reference(home, args.file, title=args.title,
                use_cases=args.use_case, tags=args.tag, likes=args.like,
                avoids=args.avoid, rating=args.rating)
        elif args.command == "list":
            result = load_index(home)
        elif args.command == "select":
            result = select_references(home, use_case=args.use_case, tags=args.tag, top=args.top)
        elif args.command == "prepare":
            result = prepare(home, request=args.request, use_case=args.use_case,
                tags=args.tag, top=args.top)
        elif args.command == "feedback":
            result = feedback(home, args.id, rating=args.rating,
                likes=args.like, avoids=args.avoid)
        else:
            result = remove_reference(home, args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (InputError, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
