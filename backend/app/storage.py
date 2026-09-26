from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
REPORTS_FILE = DATA_DIR / "reports.json"
MATCHES_FILE = DATA_DIR / "matches.json"


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    for path in (REPORTS_FILE, MATCHES_FILE):
        if not path.exists():
            path.write_text("[]", encoding="utf-8")


def read_json(path: Path) -> list[dict]:
    ensure_storage()
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else []
    except json.JSONDecodeError:
        return []


def write_json(path: Path, value: list[dict]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True), encoding="utf-8")


def read_reports() -> list[dict]:
    return read_json(REPORTS_FILE)


def write_report(report: dict) -> None:
    reports = read_reports()
    reports.append(report)
    write_json(REPORTS_FILE, reports)


def save_image(filename: str, contents: bytes) -> str:
    safe_name = f"{uuid4().hex}_{Path(filename).name}"
    (IMAGES_DIR / safe_name).write_bytes(contents)
    return safe_name


def delete_image(filename: str) -> None:
    (IMAGES_DIR / filename).unlink(missing_ok=True)


def read_matches() -> list[dict]:
    return read_json(MATCHES_FILE)


def write_match(match: dict) -> None:
    matches = read_matches()
    matches.append(match)
    write_json(MATCHES_FILE, matches)
