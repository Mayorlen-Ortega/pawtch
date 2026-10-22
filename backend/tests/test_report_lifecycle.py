import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app import main


class ReportLifecycleApiTests(unittest.TestCase):
    def test_legacy_report_defaults_to_active(self):
        report = main.public_report({"id": "report-1", "photoPath": "private.jpg"})

        self.assertEqual(report["status"], "active")
        self.assertNotIn("photoPath", report)

    def test_resolve_report_records_timestamp_and_status(self):
        updated = {"id": "report-1", "status": "resolved", "resolvedAt": "2026-10-22T12:00:00+00:00"}
        with (
            patch("app.main.read_reports", return_value=[{"id": "report-1"}]),
            patch("app.main.update_report", return_value=updated) as update_report,
        ):
            result = main.resolve_report("report-1")

        self.assertEqual(result["status"], "resolved")
        self.assertIn("resolvedAt", result)
        update_report.assert_called_once()

    def test_resolved_report_has_no_possible_matches(self):
        reports = [
            {"id": "lost", "type": "lost"},
            {"id": "resolved-found", "type": "found", "status": "resolved"},
            {"id": "active-found", "type": "found"},
        ]
        matches = [
            {"id": "match-resolved", "lostReportId": "lost", "foundReportId": "resolved-found"},
            {"id": "match-active", "lostReportId": "lost", "foundReportId": "active-found"},
        ]
        with (
            patch("app.main.read_reports", return_value=reports),
            patch("app.main.read_matches", return_value=matches),
        ):
            result = main.matches("lost")

        self.assertEqual([match["id"] for match in result], ["match-active"])
        self.assertEqual(result[0]["otherReport"]["status"], "active")

    def test_match_detail_is_unavailable_after_either_report_is_resolved(self):
        match = {"id": "match-1", "lostReportId": "lost", "foundReportId": "found"}
        reports = [
            {"id": "lost", "status": "resolved"},
            {"id": "found"},
        ]
        with (
            patch("app.main.read_matches", return_value=[match]),
            patch("app.main.read_reports", return_value=reports),
        ):
            with self.assertRaises(HTTPException) as error:
                main.get_match("match-1")

        self.assertEqual(error.exception.status_code, 404)

    def test_delete_endpoint_returns_deleted_report_id(self):
        with patch("app.main.remove_report", return_value={"id": "report-1"}):
            result = main.delete_report_endpoint("report-1")

        self.assertEqual(result, {"id": "report-1", "deleted": True})


if __name__ == "__main__":
    unittest.main()