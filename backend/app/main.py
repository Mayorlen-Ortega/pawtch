from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .locations import LOCATIONS, get_location
from .matching import calculate_match
from .storage import IMAGES_DIR, ensure_storage, read_matches, read_reports, save_image, write_match, write_report

app = FastAPI(title="Huella Cerca API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ensure_storage()
app.mount("/media", StaticFiles(directory=IMAGES_DIR), name="media")

REQUIRED_FIELDS = ("type", "species", "color", "markings", "locationId", "date")


def public_report(report: dict) -> dict:
    return {key: value for key, value in report.items() if key != "photoPath"}


@app.get("/api/locations")
def locations() -> list[dict]:
    return [{"id": item["id"], "name": item["name"]} for item in LOCATIONS]


@app.get("/api/reports")
def reports() -> list[dict]:
    return [public_report(report) for report in read_reports()]


@app.post("/api/reports")
async def create_report(report: str = Form(...), photo: UploadFile = File(...)) -> dict:
    try:
        payload = json.loads(report)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail={"form": "The report details could not be read."}) from exc

    missing = [field for field in REQUIRED_FIELDS if not str(payload.get(field, "")).strip()]
    if missing:
        raise HTTPException(status_code=422, detail={field: "This field is required." for field in missing})
    if payload["type"] not in {"lost", "found"}:
        raise HTTPException(status_code=422, detail={"type": "Choose lost or found."})
    if not photo.content_type or not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail={"photo": "Please choose an image file."})
    location = get_location(payload["locationId"])
    if location is None:
        raise HTTPException(status_code=422, detail={"locationId": "Choose a listed location."})

    report_id = f"report-{len(read_reports()) + 1:03d}"
    image_name = save_image(photo.filename or "pet-photo", await photo.read())
    saved = {
        "id": report_id,
        "type": payload["type"],
        "photo": image_name,
        "photoPath": image_name,
        "species": payload["species"],
        "color": payload["color"],
        "markings": payload["markings"],
        "name": payload.get("name", ""),
        "sex": payload.get("sex", ""),
        "size": payload.get("size", ""),
        "description": payload.get("description", ""),
        "locationId": location["id"],
        "locationName": location["name"],
        "date": payload["date"],
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    pending_matches = []
    if saved["type"] == "found":
        for lost in (item for item in read_reports() if item["type"] == "lost"):
            result = calculate_match(lost, saved, IMAGES_DIR)
            if result["isPossibleMatch"]:
                pending_matches.append({
                    "id": f"match-{len(read_matches()) + 1:03d}",
                    "lostReportId": lost["id"],
                    "foundReportId": saved["id"],
                    **result,
                    "createdAt": datetime.now(timezone.utc).isoformat(),
                })
    write_report(saved)
    first_match_number = len(read_matches()) + 1
    for offset, match in enumerate(pending_matches):
        match["id"] = f"match-{first_match_number + offset:03d}"
        write_match(match)
    return public_report(saved)


@app.get("/api/reports/{report_id}")
def get_report(report_id: str) -> dict:
    report = next((item for item in read_reports() if item["id"] == report_id), None)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return public_report(report)


@app.get("/api/reports/{report_id}/matches")
def matches(report_id: str) -> list[dict]:
    reports_by_id = {item["id"]: item for item in read_reports()}
    if report_id not in reports_by_id:
        raise HTTPException(status_code=404, detail="Report not found.")
    result = []
    for item in read_matches():
        if item.get("lostReportId") != report_id and item.get("foundReportId") != report_id:
            continue
        other_id = item["foundReportId"] if item["lostReportId"] == report_id else item["lostReportId"]
        other = reports_by_id[other_id]
        result.append({**item, "otherReport": public_report(other)})
    return result
