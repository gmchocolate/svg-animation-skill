#!/usr/bin/env python3
"""Static structure and motion-hygiene checks for standalone SVGs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from motion_library import InputError, _load_source


def check_file(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    details = {}
    try:
        if path.suffix.lower() != ".svg":
            raise InputError("Only standalone .svg files can be checked")
        _, _, details = _load_source(path)
    except (InputError, OSError, UnicodeError) as exc:
        errors.append(str(exc))
        return {"ok": False, "errors": errors, "warnings": warnings, "details": details}

    if not details["has_viewbox"]:
        warnings.append("Missing viewBox: scaling may be impaired")
    if not details["decorative"] and not details["has_title"]:
        warnings.append("Provide <title> for informative SVG or aria-hidden=true for decoration")
    if details["duplicate_ids"]:
        warnings.append("Duplicate SVG IDs: " + ", ".join(details["duplicate_ids"]))
    if (details["smil_element_count"] or details["has_css_keyframes"]) and not details["has_reduced_motion_css"]:
        warnings.append("No detectable prefers-reduced-motion CSS; verify manually")
    if details["filter_count"] > 3:
        warnings.append("Multiple filters: inspect GPU/paint cost on mobile")
    if details["path_count"] > 100:
        warnings.append("Many paths: inspect DOM/paint cost")
    return {"ok": True, "errors": errors, "warnings": warnings, "details": details}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("file", type=Path)
    args = parser.parse_args(argv)
    outcome = check_file(args.file)
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 1 if outcome["errors"] or (args.strict and outcome["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
