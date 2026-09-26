from __future__ import annotations

import math
from datetime import date
from pathlib import Path

from .config import DATE_DECAY_DAYS, MATCH_THRESHOLD, MATCH_WEIGHTS
from .embeddings import visual_similarity
from .locations import get_location


def _terms(value: str) -> set[str]:
    return {term.strip().lower() for term in value.replace(",", " ").split() if len(term.strip()) > 2}


def physical_score(lost: dict, found: dict) -> tuple[float, list[str]]:
    if lost["species"].lower() != found["species"].lower():
        return 0.0, ["The species are different, so physical compatibility is low."]
    score = 40.0
    reasons = ["The species is compatible."]
    if lost["color"].lower() == found["color"].lower():
        score += 35.0
        reasons.append("The main color is compatible.")
    elif _terms(lost["color"]) & _terms(found["color"]):
        score += 20.0
        reasons.append("The color descriptions partially overlap.")
    marking_overlap = _terms(lost.get("markings", "")) & _terms(found.get("markings", ""))
    description_overlap = _terms(lost.get("description", "")) & _terms(found.get("description", ""))
    if marking_overlap or description_overlap:
        score += 25.0
        reasons.append("The markings or descriptions share visible characteristics.")
    if lost.get("size") and found.get("size") and lost["size"].lower() == found["size"].lower():
        score = min(100.0, score + 10.0)
        reasons.append("The approximate size is compatible.")
    return min(100.0, score), reasons


def geographic_score(lost: dict, found: dict) -> tuple[float, str]:
    first = get_location(lost["locationId"])
    second = get_location(found["locationId"])
    if not first or not second:
        return 0.0, "The locations could not be compared."
    distance = math.hypot(first["latitude"] - second["latitude"], first["longitude"] - second["longitude"]) * 111
    score = max(0.0, min(100.0, 100.0 - distance * 10.0))
    if distance < 3:
        message = "The selected locations are nearby."
    elif distance < 10:
        message = "The selected locations are in the same broader area."
    else:
        message = "The selected locations are relatively far apart."
    return score, message


def date_score(lost: dict, found: dict) -> tuple[float, bool, str]:
    lost_date = date.fromisoformat(lost["date"])
    found_date = date.fromisoformat(found["date"])
    days = (found_date - lost_date).days
    if days < 0:
        return 0.0, False, "The found date is before the lost date, so the dates are incompatible."
    if days <= DATE_DECAY_DAYS[1]:
        return 100.0, True, "The found date is shortly after the lost date."
    if days <= DATE_DECAY_DAYS[2]:
        return 80.0, True, "The found date is after the lost date and remains compatible."
    if days <= DATE_DECAY_DAYS[3]:
        return 55.0, True, "The found date is after the lost date, with a wider time gap."
    return 25.0, True, "The found date is after the lost date but much later."


def calculate_match(lost: dict, found: dict, image_dir: Path, visual_score_override: float | None = None) -> dict:
    visual = visual_score_override if visual_score_override is not None else visual_similarity(image_dir / lost["photoPath"], image_dir / found["photoPath"])
    physical, physical_reasons = physical_score(lost, found)
    geographic, geographic_reason = geographic_score(lost, found)
    temporal, date_compatible, date_reason = date_score(lost, found)
    weighted = sum((visual * MATCH_WEIGHTS["visual"], physical * MATCH_WEIGHTS["physical"], geographic * MATCH_WEIGHTS["geographic"], temporal * MATCH_WEIGHTS["date"]))
    possible = date_compatible and weighted >= MATCH_THRESHOLD and physical > 0
    explanations = [
        "The photos have similar visual characteristics." if visual >= 60 else "The photos have limited visual similarity.",
        *physical_reasons,
        geographic_reason,
        date_reason,
    ]
    return {
        "visualScore": round(visual),
        "physicalScore": round(physical),
        "geographicScore": round(geographic),
        "dateScore": round(temporal),
        "weightedIndication": round(weighted),
        "isPossibleMatch": possible,
        "explanations": explanations,
    }
