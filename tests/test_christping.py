import unittest

from fbsc.christping import ChristPing
from fbsc.models import Phase


class ChristPingTests(unittest.TestCase):
    def test_no_trigger_within_tolerance(self):
        result = ChristPing(0.7).evaluate(0.6)
        self.assertFalse(result.triggered)
        self.assertIsNone(result.reentry_phase)

    def test_trigger_preserves_conflicts_and_reentry(self):
        conflicts = ["Evidence A supports claim", "Evidence B disputes claim"]
        result = ChristPing(0.5).evaluate(
            0.9, earliest_failed_phase=Phase.POLARITY, conflicts=conflicts
        )
        self.assertTrue(result.triggered)
        self.assertEqual(result.reentry_phase, Phase.POLARITY)
        self.assertEqual(result.preserved_conflicts, tuple(conflicts))

    def test_cannot_reenter_after_grace(self):
        result = ChristPing().evaluate(0.9, earliest_failed_phase=Phase.NAMING)
        self.assertEqual(result.reentry_phase, Phase.FRICTION)


if __name__ == "__main__":
    unittest.main()
