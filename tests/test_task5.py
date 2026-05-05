import pytest
from task5 import update_task_status


def make_task(status):
    return {"status": status}


class TestStatementCoverage:
    def test_no_change(self):
        assert update_task_status(make_task("open"), "open", "user") == "No change"

    def test_invalid_transition(self):
        assert update_task_status(make_task("closed"), "open", "user") == "Invalid transition"

    def test_permission_denied(self):
        assert update_task_status(make_task("open"), "closed", "user") == "Permission denied"

    def test_updated(self):
        t = make_task("open")
        assert update_task_status(t, "in_progress", "user") == "Updated"
        assert t["status"] == "in_progress"


class TestBranchCoverage:
    def test_same_status(self):
        assert update_task_status(make_task("open"), "open", "admin") == "No change"

    def test_invalid_transition_closed_has_no_targets(self):
        assert update_task_status(make_task("closed"), "open", "user") == "Invalid transition"

    def test_invalid_transition_on_hold_cannot_close(self):
        assert update_task_status(make_task("on_hold"), "closed", "admin") == "Invalid transition"

    def test_permission_denied_user_tries_to_close(self):
        assert update_task_status(make_task("open"), "closed", "user") == "Permission denied"

    def test_updated_admin_closes(self):
        t = make_task("open")
        assert update_task_status(t, "closed", "admin") == "Updated"
        assert t["status"] == "closed"

    def test_updated_user_non_close(self):
        t = make_task("open")
        assert update_task_status(t, "in_progress", "user") == "Updated"
        assert t["status"] == "in_progress"

    def test_updated_manager_closes(self):
        t = make_task("in_progress")
        assert update_task_status(t, "closed", "manager") == "Updated"

    def test_updated_on_hold_to_in_progress(self):
        t = make_task("on_hold")
        assert update_task_status(t, "in_progress", "user") == "Updated"


class TestConditionCoverage:
    def test_cond_A_false_B_true(self):
        """A=False (admin), B=True (closing) → condition False → Updated."""
        t = make_task("open")
        assert update_task_status(t, "closed", "admin") == "Updated"

    def test_cond_A_true_B_false(self):
        """A=True (user), B=False (not closing) → condition False → Updated."""
        t = make_task("open")
        assert update_task_status(t, "in_progress", "user") == "Updated"

    def test_cond_A_true_B_true(self):
        """A=True (user), B=True (closing) → condition True → Permission denied."""
        assert update_task_status(make_task("open"), "closed", "user") == "Permission denied"


MCDC_TESTS = [
    ("open", "open",        "user",    "No change"         ),
    ("closed","open",       "user",    "Invalid transition"),
    ("open", "closed",      "admin",   "Updated"           ),
    ("open", "in_progress", "user",    "Updated"           ),
    ("open", "closed",      "user",    "Permission denied" ),
]


@pytest.mark.parametrize("status,new_status,role,expected", MCDC_TESTS)
def test_mcdc(status, new_status, role, expected):
    t = make_task(status)
    assert update_task_status(t, new_status, role) == expected


class TestValidTransitions:
    def test_open_to_in_progress(self):
        t = make_task("open")
        assert update_task_status(t, "in_progress", "user") == "Updated"

    def test_open_to_closed_by_admin(self):
        t = make_task("open")
        assert update_task_status(t, "closed", "admin") == "Updated"

    def test_in_progress_to_closed_by_manager(self):
        t = make_task("in_progress")
        assert update_task_status(t, "closed", "manager") == "Updated"

    def test_in_progress_to_on_hold(self):
        t = make_task("in_progress")
        assert update_task_status(t, "on_hold", "user") == "Updated"

    def test_on_hold_to_in_progress(self):
        t = make_task("on_hold")
        assert update_task_status(t, "in_progress", "user") == "Updated"


class TestInvalidTransitions:
    def test_closed_to_anything(self):
        for target in ["open", "in_progress", "on_hold"]:
            assert update_task_status(make_task("closed"), target, "admin") == "Invalid transition"

    def test_open_to_on_hold(self):
        assert update_task_status(make_task("open"), "on_hold", "admin") == "Invalid transition"

    def test_on_hold_to_closed(self):
        assert update_task_status(make_task("on_hold"), "closed", "admin") == "Invalid transition"
