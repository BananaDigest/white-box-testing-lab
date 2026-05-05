import pytest
from task1 import process_data

class TestStatementCoverage:
    """Every executable line must be reached at least once."""

    def test_all_statements_executed(self):
        assert process_data([-1, 3]) == 2

class TestBranchCoverage:
    """Every branch (True/False) of every decision node must be exercised."""

    def test_outer_loop_not_entered(self):
        """Outer-loop condition → False (zero iterations)."""
        assert process_data([]) == 0

    def test_data_negative_continue(self):
        """data[i] < 0 → True  →  continue."""
        assert process_data([-1]) == 0

    def test_data_zero_inner_loop_skipped(self):
        """data[i] < 0 → False, data[i]=0 → inner loop never entered."""
        assert process_data([0]) == 0

    def test_inner_loop_even_branch(self):
        """j % 2 == 0 → True (j=0,2) and False (j=1) in one run."""
        assert process_data([3]) == 2

class TestConditionCoverage:
    """Each atomic condition must evaluate both True and False."""

    def test_cond_data_i_negative_true(self):
        assert process_data([-5]) == 0

    def test_cond_data_i_negative_false(self):
        assert process_data([2]) == 0

    def test_cond_j_even_true(self):
        """j % 2 == 0 evaluates to True (j=0)."""
        assert process_data([1]) == 0

    def test_cond_j_even_false(self):
        """j % 2 == 0 evaluates to False (j=1)."""
        assert process_data([2]) == 0 


class TestPathCoverage:

    def test_p1_empty(self):
        assert process_data([]) == 0

    def test_p2_negative(self):
        assert process_data([-1]) == 0

    def test_p3_zero_inner(self):
        assert process_data([0]) == 0

    def test_p4_j_even_only(self):
        """data[i]=1 → inner loop: j=0 (even) only."""
        assert process_data([1]) == 0

    def test_p5_mixed_j(self):
        """data[i]=3 → j=0(even), j=1(odd), j=2(even)."""
        assert process_data([3]) == 2


class TestLoopCoverage:

    # Outer loop
    def test_outer_zero(self):
        assert process_data([]) == 0

    def test_outer_one(self):
        assert process_data([0]) == 0

    def test_outer_many(self):
        assert process_data([-1, 0, 3]) == 2

    # Inner loop
    def test_inner_zero(self):
        """Inner loop: 0 iterations (data[i]=0, outer loop entered)."""
        assert process_data([0]) == 0

    def test_inner_one(self):
        """Inner loop: 1 iteration (data[i]=1, j=0 only)."""
        assert process_data([1]) == 0

    def test_inner_many(self):
        """Inner loop: many iterations (data[i]=5)."""
        assert process_data([5]) == 6


class TestDefUsePairs:
    """
    Def-use pairs:
      total : def @total=0        → use @total+=j, @return total
      i     : def @for i …        → use @data[i] (condition + range)
      j     : def @for j …        → use @j%2==0, @total+=j
      data[i]: (external def)     → use @data[i]<0, @range(data[i])
    """

    def test_total_def_then_used_in_return(self):
        """total defined at 0 and used at return without modification."""
        assert process_data([]) == 0

    def test_total_def_then_modified_and_returned(self):
        """total defined, modified (total+=j), returned."""
        assert process_data([3]) == 2

    def test_i_used_as_index(self):
        """i defined by outer loop, used as index into data."""
        assert process_data([0, 1, 3]) == 2

    def test_j_used_in_condition(self):
        """j defined by inner loop, used in j%2==0."""
        assert process_data([4]) == 2

    def test_j_used_in_addition(self):
        """j defined by inner loop, used in total+=j."""
        assert process_data([5]) == 6

    def test_data_i_used_in_condition_and_range(self):
        """data[i] used both in <0 check and as range() argument."""
        assert process_data([-1, 0, 4]) == 2
