import unittest
from datetime import datetime, timezone

from studio.errors import TransitionError
from studio.status import LIFECYCLE, Status, apply_transition, new_status, parse_status, validate_status_data

NOW = datetime(2026, 11, 20, 9, 0, tzinfo=timezone.utc)


class StatusTests(unittest.TestCase):
    def test_lifecycle_order_matches_claude_md(self) -> None:
        self.assertEqual(
            [s.value for s in LIFECYCLE],
            ["RESEARCHED", "APPROVED_TOPIC", "SCRIPT_READY", "ASSETS_READY", "RENDERED", "QA_PASSED", "READY_FOR_HUMAN_REVIEW"],
        )

    def test_published_is_forbidden(self) -> None:
        for bad in ("PUBLISHED", "published", "SCHEDULED", "UPLOADED"):
            with self.assertRaisesRegex(TransitionError, "forbidden"):
                parse_status(bad)

    def test_full_forward_walk(self) -> None:
        data = new_status("2026-11-20-demo", NOW)
        for target in LIFECYCLE[1:]:
            data = apply_transition(data, target, now=NOW)
        self.assertEqual(data["status"], "READY_FOR_HUMAN_REVIEW")
        self.assertEqual(len(data["history"]), len(LIFECYCLE))
        self.assertFalse(data["published"])
        self.assertEqual(validate_status_data(data), [])

    def test_cannot_skip_stages(self) -> None:
        data = new_status("2026-11-20-demo", NOW)
        with self.assertRaisesRegex(TransitionError, "skip"):
            apply_transition(data, Status.RENDERED, now=NOW)

    def test_backward_requires_note(self) -> None:
        data = apply_transition(new_status("2026-11-20-demo", NOW), Status.APPROVED_TOPIC, now=NOW)
        with self.assertRaisesRegex(TransitionError, "note"):
            apply_transition(data, Status.RESEARCHED, now=NOW)
        back = apply_transition(data, Status.RESEARCHED, note="weak sources", now=NOW)
        self.assertEqual(back["status"], "RESEARCHED")

    def test_transition_is_pure(self) -> None:
        data = new_status("2026-11-20-demo", NOW)
        apply_transition(data, Status.APPROVED_TOPIC, now=NOW)
        self.assertEqual(data["status"], "RESEARCHED")
        self.assertEqual(len(data["history"]), 1)

    def test_validation_flags_published_true(self) -> None:
        data = new_status("x", NOW) | {"published": True}
        self.assertTrue(any("published" in p for p in validate_status_data(data)))

    def test_timestamps_are_deterministic(self) -> None:
        self.assertEqual(new_status("x", NOW)["updated_at"], "2026-11-20T09:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
