"""
AstroBench - Open-source LLM benchmark using real astrophysics reasoning problems.
"""
__version__ = "0.1.0"

from astrobench.problems import load_problems
from astrobench.grader import grade_response
from astrobench.submit import run_benchmark

__all__ = ["load_problems", "grade_response", "run_benchmark"]
