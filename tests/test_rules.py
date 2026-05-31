from datetime import datetime, timezone
import unittest

from maintainer_signal.models import Item
from maintainer_signal.rules import analyze_item, analyze_items


NOW = datetime(2026, 5, 31, tzinfo=timezone.utc)


class RulesTest(unittest.TestCase):
    def test_security_issue_is_critical(self):
        signal = analyze_item(
            Item(
                number=42,
                title="Security: token leak in logs",
                body="The debug logger prints a credential.",
            ),
            now=NOW,
        )

        self.assertEqual(signal.priority, "critical")
        self.assertIn("security", signal.suggested_labels)
        self.assertIn("bug", signal.suggested_labels)

    def test_regression_issue_is_high(self):
        signal = analyze_item(
            Item(
                number=9,
                title="Regression in latest release",
                body="Import fails with traceback.",
            ),
            now=NOW,
        )

        self.assertEqual(signal.priority, "high")
        self.assertIn("bug", signal.suggested_labels)

    def test_stale_docs_issue_gets_triage_label(self):
        signal = analyze_item(
            Item(
                number=5,
                title="Docs typo in README",
                body="Small spelling fix.",
                updated_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
            ),
            now=NOW,
        )

        self.assertEqual(signal.stale_days, 60)
        self.assertIn("needs-triage", signal.suggested_labels)
        self.assertIn("documentation", signal.suggested_labels)

    def test_pull_request_without_assignee_gets_review_action(self):
        signal = analyze_item(
            Item(
                number=12,
                title="Fix parser edge case",
                body="",
                is_pull_request=True,
            ),
            now=NOW,
        )

        self.assertEqual(signal.priority, "normal")
        self.assertIn("pull request", signal.suggested_labels)
        self.assertEqual(signal.next_action, "assign a reviewer and check CI status")

    def test_analyze_items_sorts_critical_first(self):
        signals = analyze_items(
            [
                Item(number=1, title="Docs typo", body=""),
                Item(number=2, title="Security vulnerability", body="token leak"),
            ],
            now=NOW,
        )

        self.assertEqual(signals[0].item.number, 2)


if __name__ == "__main__":
    unittest.main()
