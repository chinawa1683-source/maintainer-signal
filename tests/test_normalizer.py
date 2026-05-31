from datetime import timezone
import unittest

from maintainer_signal.normalizer import normalize_item


class NormalizeItemTest(unittest.TestCase):
    def test_normalizes_github_cli_shape(self):
        item = normalize_item(
            {
                "number": "7",
                "title": "Bug report",
                "body": None,
                "labels": [{"name": "bug"}, "needs-triage"],
                "url": "https://github.com/example/project/issues/7",
                "comments": "3",
                "createdAt": "2026-05-01T12:00:00Z",
                "updatedAt": "2026-05-02T12:00:00Z",
                "authorAssociation": "CONTRIBUTOR",
                "assignees": [{"login": "alice"}],
            }
        )

        self.assertEqual(item.number, 7)
        self.assertEqual(item.labels, ("bug", "needs-triage"))
        self.assertEqual(item.comments, 3)
        self.assertEqual(item.updated_at.tzinfo, timezone.utc)
        self.assertEqual(item.assignees, ("alice",))

    def test_detects_pull_request(self):
        item = normalize_item({"title": "Patch", "pull_request": {"url": "x"}})

        self.assertTrue(item.is_pull_request)


if __name__ == "__main__":
    unittest.main()
