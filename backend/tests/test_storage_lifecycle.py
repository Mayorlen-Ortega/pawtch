from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from app import storage


class StorageLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.images_dir = self.root / "images"
        self.images_dir.mkdir()
        self.reports_file = self.root / "reports.json"
        self.matches_file = self.root / "matches.json"
        self.reports_file.write_text("[]", encoding="utf-8")
        self.matches_file.write_text("[]", encoding="utf-8")

        patches = (
            patch.object(storage, "DATA_DIR", self.root),
            patch.object(storage, "IMAGES_DIR", self.images_dir),
            patch.object(storage, "REPORTS_FILE", self.reports_file),
            patch.object(storage, "MATCHES_FILE", self.matches_file),
        )
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def test_update_report_keeps_photo_and_sets_status(self):
        photo = self.images_dir / "pet.jpg"
        photo.write_bytes(b"image")
        storage.write_json(self.reports_file, [{"id": "report-1", "photo": photo.name}])

        updated = storage.update_report("report-1", {"status": "resolved"})

        self.assertEqual(updated["status"], "resolved")
        self.assertTrue(photo.exists())

    def test_delete_report_removes_its_photo_and_matches_only(self):
        deleted_photo = self.images_dir / "deleted.jpg"
        retained_photo = self.images_dir / "retained.jpg"
        deleted_photo.write_bytes(b"deleted")
        retained_photo.write_bytes(b"retained")
        storage.write_json(self.reports_file, [
            {"id": "report-1", "photoPath": deleted_photo.name},
            {"id": "report-2", "photoPath": retained_photo.name},
        ])
        storage.write_json(self.matches_file, [
            {"id": "match-1", "lostReportId": "report-1", "foundReportId": "report-2"},
            {"id": "match-2", "lostReportId": "report-2", "foundReportId": "report-3"},
        ])

        deleted = storage.delete_report("report-1")

        self.assertEqual(deleted["id"], "report-1")
        self.assertEqual([report["id"] for report in storage.read_reports()], ["report-2"])
        self.assertEqual([match["id"] for match in storage.read_matches()], ["match-2"])
        self.assertFalse(deleted_photo.exists())
        self.assertTrue(retained_photo.exists())

    def test_delete_report_does_not_delete_outside_image_directory(self):
        outside_photo = self.root / "keep.jpg"
        outside_photo.write_bytes(b"keep")
        storage.write_json(self.reports_file, [{"id": "report-1", "photo": "../keep.jpg"}])

        storage.delete_report("report-1")

        self.assertTrue(outside_photo.exists())


if __name__ == "__main__":
    unittest.main()