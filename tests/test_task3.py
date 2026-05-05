"""
Task 3: White-box tests for process_matrix()
Covers: Statement, Branch, Condition, Path, Loop (3 nested loops)
Cyclomatic complexity M = 4 + 1 = 5
"""
import pytest
from task3 import process_matrix


# ── Statement Coverage ────────────────────────────────────────────────────────
class TestStatementCoverage:
    def test_all_statements(self):
        """
        matrix=[[3,-1],[0,2]] exercises every statement:
          count=0, outer loop, middle loop, if>0 True, inner loop,
          count+=k%3, if>0 False, return count
        """
        # (0,0)=3>0: k=0→0,k=1→1,k=2→2 → +3
        # (0,1)=-1>0 False
        # (1,0)=0>0  False
        # (1,1)=2>0: k=0→0,k=1→1 → +1
        # total = 4
        assert process_matrix([[3, -1], [0, 2]]) == 4


# ── Branch Coverage ───────────────────────────────────────────────────────────
class TestBranchCoverage:
    def test_outer_loop_not_entered(self):
        """Outer loop: 0 iterations."""
        assert process_matrix([]) == 0

    def test_middle_loop_not_entered(self):
        """Outer=1 iter, middle=0 iters (empty row)."""
        assert process_matrix([[]]) == 0

    def test_condition_false_zero(self):
        """matrix[i][j]=0 → condition 0>0 False."""
        assert process_matrix([[0]]) == 0

    def test_condition_false_negative(self):
        """matrix[i][j]<0 → condition False."""
        assert process_matrix([[-3]]) == 0

    def test_condition_true_inner_one(self):
        """matrix[i][j]=1>0 True, inner loop: 1 iteration (k=0)."""
        assert process_matrix([[1]]) == 0  # k=0: 0%3=0

    def test_condition_true_inner_many(self):
        """matrix[i][j]=3>0 True, inner loop: 3 iterations."""
        # k=0→0, k=1→1, k=2→2 → count=3
        assert process_matrix([[3]]) == 3


# ── Condition Coverage ────────────────────────────────────────────────────────
class TestConditionCoverage:
    def test_cond_positive_true(self):
        assert process_matrix([[4]]) == 3   # 0+1+2+0(4%3=1 for k=3? wait)
        # k=0:0%3=0, k=1:1%3=1, k=2:2%3=2, k=3:3%3=0 → 0+1+2+0=3

    def test_cond_positive_false(self):
        assert process_matrix([[-1]]) == 0


# ── Path Coverage (M=5 basis paths) ──────────────────────────────────────────
class TestPathCoverage:
    """
    P1: outer_loop_false
    P2: outer + middle_loop_false
    P3: outer + middle + condition_false
    P4: outer + middle + condition_true + inner_one_iter
    P5: outer + middle + condition_true + inner_many_iters
    """
    def test_p1(self):
        assert process_matrix([]) == 0

    def test_p2(self):
        assert process_matrix([[]]) == 0

    def test_p3(self):
        assert process_matrix([[0]]) == 0

    def test_p4(self):
        assert process_matrix([[1]]) == 0

    def test_p5(self):
        assert process_matrix([[3]]) == 3


# ── Loop Coverage (0 / 1 / many) ─────────────────────────────────────────────
class TestLoopCoverage:
    # Outer loop
    def test_outer_zero(self):
        assert process_matrix([]) == 0

    def test_outer_one(self):
        assert process_matrix([[0]]) == 0

    def test_outer_many(self):
        assert process_matrix([[0], [3]]) == 3

    # Middle loop
    def test_middle_zero(self):
        assert process_matrix([[]]) == 0

    def test_middle_one(self):
        assert process_matrix([[3]]) == 3

    def test_middle_many(self):
        # [[0, 3]]: j=0→0>0 F, j=1→3>0 T → k=0,1,2 → count=3
        assert process_matrix([[0, 3]]) == 3

    # Inner loop
    def test_inner_zero_via_condition_false(self):
        """inner loop effectively 0 iters when condition=False."""
        assert process_matrix([[0]]) == 0

    def test_inner_one(self):
        assert process_matrix([[1]]) == 0

    def test_inner_many(self):
        assert process_matrix([[5]]) == 4  # 0+1+2+0+1=4? let's verify
        # k=0:0%3=0, k=1:1, k=2:2, k=3:0, k=4:1 → 0+1+2+0+1=4


# ── Integration ───────────────────────────────────────────────────────────────
class TestIntegration:
    def test_mixed_matrix(self):
        matrix = [[3, -1], [0, 2]]
        assert process_matrix(matrix) == 4

    def test_all_positive(self):
        # [[1,2],[3]]: only inner lists need equal-length check
        # (0,0)=1: k=0→0; (0,1)=2: k=0→0,k=1→1; (1,0)=3: k=0,1,2→0+1+2
        assert process_matrix([[1, 2], [3]]) == 4   # 0 + (0+1) + (0+1+2) = 4

    def test_all_non_positive(self):
        assert process_matrix([[-1, 0], [0, -2]]) == 0
