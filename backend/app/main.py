from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .locations import LOCATIONS, get_location
from .matching import calculate_match
from .storage import IMAGES_DIR, delete_image, delete_report as remove_report, ensure_storage, read_matches, read_reports, save_image, update_report, write_match, write_report

app = FastAPI(title="Pawtch API")
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
    result = {key: value for key, value in report.items() if key != "photoPath"}
    result.setdefault("status", "active")
    return result


def report_is_active(report: dict) -> bool:
    return report.get("status", "active") == "active"


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

    report_id = f"report-{uuid4().hex}"
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
        "status": "active",
    }
    pending_matches = []
    try:
        if saved["type"] == "found":
            for lost in (item for item in read_reports() if item["type"] == "lost" and report_is_active(item)):
                result = calculate_match(lost, saved, IMAGES_DIR)
                if result["isPossibleMatch"]:
                    pending_matches.append({
                        "id": f"match-{uuid4().hex}",
                        "lostReportId": lost["id"],
                        "foundReportId": saved["id"],
                        **result,
                        "createdAt": datetime.now(timezone.utc).isoformat(),
                    })
    except Exception as exc:
        delete_image(image_name)
        raise HTTPException(status_code=503, detail="We could not analyze that photo locally. Please try another image or check the local model setup.") from exc
    write_report(saved)
    for match in pending_matches:
        write_match(match)
    return public_report(saved)


@app.get("/api/reports/{report_id}")
def get_report(report_id: str) -> dict:
    report = next((item for item in read_reports() if item["id"] == report_id), None)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return public_report(report)


@app.post("/api/reports/{report_id}/resolve")
def resolve_report(report_id: str) -> dict:
    report = next((item for item in read_reports() if item.get("id") == report_id), None)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    if not report_is_active(report):
        return public_report(report)
    updated = update_report(report_id, {
        "status": "resolved",
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
    })
    if updated is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return public_report(updated)


@app.delete("/api/reports/{report_id}")
def delete_report_endpoint(report_id: str) -> dict:
    report = remove_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found.")
    return {"id": report_id, "deleted": True}


@app.get("/api/reports/{report_id}/matches")
def matches(report_id: str) -> list[dict]:
    reports_by_id = {item["id"]: item for item in read_reports()}
    if report_id not in reports_by_id:
        raise HTTPException(status_code=404, detail="Report not found.")
    if not report_is_active(reports_by_id[report_id]):
        return []
    result = []
    for item in read_matches():
        if item.get("lostReportId") != report_id and item.get("foundReportId") != report_id:
            continue
        lost = reports_by_id.get(item.get("lostReportId"))
        found = reports_by_id.get(item.get("foundReportId"))
        if lost is None or found is None or not report_is_active(lost) or not report_is_active(found):
            continue
        other_id = item["foundReportId"] if item["lostReportId"] == report_id else item["lostReportId"]
        other = reports_by_id[other_id]
        result.append({**item, "otherReport": public_report(other)})
    return result


@app.get("/api/matches/{match_id}")
def get_match(match_id: str) -> dict:
    match = next((item for item in read_matches() if item.get("id") == match_id), None)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found.")
    reports_by_id = {item["id"]: item for item in read_reports()}
    lost = reports_by_id.get(match["lostReportId"])
    found = reports_by_id.get(match["foundReportId"])
    if lost is None or found is None:
        raise HTTPException(status_code=404, detail="Reports for this match were not found.")
    if not report_is_active(lost) or not report_is_active(found):
        raise HTTPException(status_code=404, detail="This possible match is no longer active.")
    return {**match, "lostReport": public_report(lost), "foundReport": public_report(found)}
