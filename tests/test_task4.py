import itertools
import pytest
from task4 import validate_input


class TestStatementCoverage:
    def test_all_returns_reached(self):
        assert validate_input("", "pass") == "Missing user"
        assert validate_input("a", "short") == "Weak password"
        assert validate_input("a", "abcdefgh") == "Invalid"
        assert validate_input("a", "Abcdefg1") == "Valid"


class TestBranchCoverage:
    def test_missing_user_branch_true(self):
        assert validate_input("", "password") == "Missing user"

    def test_missing_user_branch_false(self):
        assert validate_input("a", "password") != "Missing user"

    def test_weak_password_branch_true(self):
        assert validate_input("a", "short") == "Weak password"

    def test_weak_password_branch_false(self):
        assert validate_input("a", "longpassword") != "Weak password"

    def test_valid_branch_true(self):
        assert validate_input("a", "Abcdefg1") == "Valid"

    def test_valid_branch_false(self):
        assert validate_input("a", "abcdefgh") == "Invalid"


FULL_COMBINATIONS = [
    ("",  "Abcdefg1",  True,  False, True,  True,  "Missing user" ),
    ("a", "abc",       False, True,  True,  True,  "Weak password"), 
    ("a", "abcdefgh",  False, False, False, False, "Invalid"      ),
    ("a", "abcdefgH",  False, False, False, True,  "Invalid"      ),
    ("a", "abcdefg1",  False, False, True,  False, "Invalid"      ),
    ("a", "Abcdefg1",  False, False, True,  True,  "Valid"        ),
]


@pytest.mark.parametrize(
    "user,password,c1,c2,c3a,c3b,expected", FULL_COMBINATIONS
)
def test_full_condition_combinations(user, password, c1, c2, c3a, c3b, expected):
    assert validate_input(user, password) == expected


MCDC_TESTS = [
    ("",  "Abcdefg1", "Missing user" ),
    ("a", "abc",      "Weak password"), 
    ("a", "abcdefgH", "Invalid"      ), 
    ("a", "abcdefg1", "Invalid"      ),  
    ("a", "Abcdefg1", "Valid"        ),  
]


@pytest.mark.parametrize("user,password,expected", MCDC_TESTS)
def test_mcdc(user, password, expected):
    """
    MC/DC pairs:
      C1  : T1 vs T5  (C1 F→T, outcome MissingUser↔Valid)
      C2  : T2 vs T5  (C2 T→F, outcome WeakPassword↔Valid)
      C3a : T3 vs T5  (C3a F→T, C3b=T fixed, outcome Invalid↔Valid)
      C3b : T4 vs T5  (C3b F→T, C3a=T fixed, outcome Invalid↔Valid)
    """
    assert validate_input(user, password) == expected


class TestPathCoverage:
    def test_path_missing_user(self):
        assert validate_input("", "anything") == "Missing user"

    def test_path_weak_password(self):
        assert validate_input("diana", "abc") == "Weak password"

    def test_path_no_digit_no_upper(self):
        assert validate_input("diana", "abcdefgh") == "Invalid"

    def test_path_no_digit_has_upper(self):
        assert validate_input("diana", "abcdefgH") == "Invalid"

    def test_path_has_digit_no_upper(self):
        assert validate_input("diana", "abcdefg1") == "Invalid"

    def test_path_has_digit_has_upper(self):
        assert validate_input("diana", "Abcdefg1") == "Valid"
