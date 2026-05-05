import itertools
import pytest
from task2 import check_access

ALL_COMBINATIONS = [
    ("guest", False, False, False),
    ("guest", False, True,  True ),
    ("guest", True,  False, False),
    ("guest", True,  True,  True ),
    ("user",  False, False, False),
    ("user",  False, True,  True ),
    ("user",  True,  False, True ),
    ("user",  True,  True,  True ),
]


@pytest.mark.parametrize("role,is_active,is_admin,expected", ALL_COMBINATIONS)
def test_condition_combination_coverage(role, is_active, is_admin, expected):
    """Condition Combination Coverage: all 2^3 = 8 combinations."""
    assert check_access(role, is_active, is_admin) == expected


MCDC_TESTS = [
    ("user",  False, False, False),
    ("user",  True,  False, True ),
    ("guest", True,  False, False),
    ("guest", True,  True,  True ),
]


@pytest.mark.parametrize("role,is_active,is_admin,expected", MCDC_TESTS)
def test_mcdc(role, is_active, is_admin, expected):
    """MC/DC: each condition independently affects the outcome."""
    assert check_access(role, is_active, is_admin) == expected


def test_branch_if_true_via_admin():
    """Branch: if-condition True via is_admin only."""
    assert check_access("guest", False, True) is True


def test_branch_if_true_via_user_active():
    """Branch: if-condition True via (role='user' and is_active)."""
    assert check_access("user", True, False) is True


def test_branch_if_false():
    """Branch: if-condition False → return False."""
    assert check_access("guest", False, False) is False
