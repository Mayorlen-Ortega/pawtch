from pathlib import Path
import unittest

from app.matching import calculate_match


class MatchingPolicyTests(unittest.TestCase):
    image_dir = Path("data/images")
    lost = {
        "species": "dog",
        "color": "brown and white",
        "markings": "white chest",
        "size": "medium",
        "locationId": "coquimbo-centro",
        "date": "2026-09-20",
        "photoPath": "unused.png",
    }

    def test_compatible_reports_surface_possible_match(self):
        found = {**self.lost, "date": "2026-09-22"}
        result = calculate_match(self.lost, found, self.image_dir, visual_score_override=85)
        self.assertTrue(result["isPossibleMatch"])
        self.assertEqual(result["weightedIndication"], 94)
        self.assertEqual(set(result) & {"visualScore", "physicalScore", "geographicScore", "dateScore"}, {
            "visualScore", "physicalScore", "geographicScore", "dateScore"
        })

    def test_incompatible_species_cannot_surface_match(self):
        found = {**self.lost, "species": "cat", "date": "2026-09-22"}
        result = calculate_match(self.lost, found, self.image_dir, visual_score_override=99)
        self.assertFalse(result["isPossibleMatch"])

    def test_found_before_lost_cannot_surface_match(self):
        found = {**self.lost, "date": "2026-09-19"}
        result = calculate_match(self.lost, found, self.image_dir, visual_score_override=99)
        self.assertFalse(result["isPossibleMatch"])

    def test_distance_remains_visible_in_evidence(self):
        found = {**self.lost, "locationId": "tongoy", "date": "2026-09-22"}
        result = calculate_match(self.lost, found, self.image_dir, visual_score_override=70)
        self.assertLess(result["geographicScore"], 100)
        self.assertTrue(any("locations" in explanation for explanation in result["explanations"]))


if __name__ == "__main__":
    unittest.main()
