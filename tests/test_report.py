import unittest

from maintainer_signal.models import Item, Signal
from maintainer_signal.report import render_report


class ReportTest(unittest.TestCase):
    def test_renders_summary_and_item(self):
        report = render_report(
            [
                Signal(
                    item=Item(number=1, title="Security bug", body="", url="https://example.com/1"),
                    priority="critical",
                    score=90,
                    suggested_labels=("security", "bug"),
                    signals=("security keywords",),
                    next_action="confirm impact",
                )
            ]
        )

        self.assertIn("# Maintainer Signal Report", report)
        self.assertIn("- Total items: 1", report)
        self.assertIn("## Critical", report)
        self.assertIn("[Security bug](https://example.com/1)", report)


if __name__ == "__main__":
    unittest.main()
