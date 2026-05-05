import pytest
from auth import authenticate_user



def test_missing_credentials():
    db = {}
    assert authenticate_user("", "pass", db) == "Missing credentials"
    assert authenticate_user("user", "", db) == "Missing credentials"


def test_user_not_found():
    db = {}
    assert authenticate_user("user", "pass", db) == "User not found"


def test_account_locked():
    db = {"user": {"password": "pass", "attempts": 3}}
    assert authenticate_user("user", "pass", db) == "Account locked"


def test_invalid_password():
    db = {"user": {"password": "pass", "attempts": 0}}
    assert authenticate_user("user", "wrong", db) == "Invalid password"
    assert db["user"]["attempts"] == 1


def test_success():
    db = {"user": {"password": "pass", "attempts": 1}}
    assert authenticate_user("user", "pass", db) == "Authenticated"
    assert db["user"]["attempts"] == 0



class TestBranchCoverage:
    def test_empty_username_only(self):
        """not username → True (short-circuit, password not checked)."""
        assert authenticate_user("", "secret", {}) == "Missing credentials"

    def test_empty_password_only(self):
        """not username → False, not password → True."""
        assert authenticate_user("alice", "", {}) == "Missing credentials"

    def test_both_credentials_present_user_missing(self):
        """username and password present, but username not in db."""
        assert authenticate_user("alice", "pass", {}) == "User not found"

    def test_attempts_exactly_3_locked(self):
        """attempts >= 3 → Account locked."""
        db = {"alice": {"password": "secret", "attempts": 3}}
        assert authenticate_user("alice", "secret", db) == "Account locked"

    def test_attempts_more_than_3_locked(self):
        """attempts > 3 → also locked."""
        db = {"alice": {"password": "secret", "attempts": 10}}
        assert authenticate_user("alice", "secret", db) == "Account locked"

    def test_attempts_less_than_3_not_locked(self):
        """attempts < 3 → not locked, proceed to password check."""
        db = {"alice": {"password": "secret", "attempts": 2}}
        assert authenticate_user("alice", "secret", db) == "Authenticated"

    def test_wrong_password_increments_attempts(self):
        db = {"alice": {"password": "secret", "attempts": 2}}
        result = authenticate_user("alice", "wrong", db)
        assert result == "Invalid password"
        assert db["alice"]["attempts"] == 3

    def test_correct_password_resets_attempts(self):
        db = {"alice": {"password": "secret", "attempts": 2}}
        result = authenticate_user("alice", "secret", db)
        assert result == "Authenticated"
        assert db["alice"]["attempts"] == 0



class TestConditionCoverageOr:
    def test_A_true_short_circuit(self):
        """A=True → short-circuit (B not evaluated)."""
        assert authenticate_user("", "anything", {}) == "Missing credentials"

    def test_A_false_B_true(self):
        """A=False, B=True → still missing."""
        assert authenticate_user("alice", "", {}) == "Missing credentials"

    def test_A_false_B_false(self):
        """A=False, B=False → not missing credentials, next check."""
        db = {"alice": {"password": "x", "attempts": 0}}
        result = authenticate_user("alice", "x", db)
        assert result == "Authenticated"


MCDC_TESTS = [
    ("alice", "x",  {"alice": {"password": "x", "attempts": 0}}, "Authenticated"),
    ("",      "x",  {},                                           "Missing credentials"),
    ("alice", "",   {},                                           "Missing credentials"),
    ("alice", "x",  {},                                           "User not found"),
    ("alice", "x",  {"alice": {"password": "x", "attempts": 3}}, "Account locked"),
    ("alice", "y",  {"alice": {"password": "x", "attempts": 0}}, "Invalid password"),
]


@pytest.mark.parametrize("username,password,db,expected", MCDC_TESTS)
def test_mcdc(username, password, db, expected):
    assert authenticate_user(username, password, db) == expected


class TestPathCoverage:
    def test_path1_missing_creds(self):
        assert authenticate_user("", "pass", {}) == "Missing credentials"

    def test_path2_user_not_found(self):
        assert authenticate_user("bob", "pass", {}) == "User not found"

    def test_path3_account_locked(self):
        db = {"bob": {"password": "pass", "attempts": 5}}
        assert authenticate_user("bob", "pass", db) == "Account locked"

    def test_path4_invalid_password(self):
        db = {"bob": {"password": "pass", "attempts": 1}}
        assert authenticate_user("bob", "wrong", db) == "Invalid password"

    def test_path5_authenticated(self):
        db = {"bob": {"password": "pass", "attempts": 0}}
        assert authenticate_user("bob", "pass", db) == "Authenticated"


class TestDataFlow:
    def test_attempts_default_zero_when_key_missing(self):
        """attempts uses .get(..., 0) → default 0 when key absent."""
        db = {"bob": {"password": "pass"}}
        assert authenticate_user("bob", "pass", db) == "Authenticated"
        assert db["bob"]["attempts"] == 0

    def test_attempts_incremented_correctly(self):
        db = {"bob": {"password": "pass", "attempts": 1}}
        authenticate_user("bob", "wrong", db)
        assert db["bob"]["attempts"] == 2

    def test_attempts_reset_on_success(self):
        db = {"bob": {"password": "pass", "attempts": 2}}
        authenticate_user("bob", "pass", db)
        assert db["bob"]["attempts"] == 0
