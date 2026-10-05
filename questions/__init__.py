"""
Questions package for JavaScript Decorators and Call/Apply Mastery Test.
Provides a unified registry of all 10 progressive questions.
"""

from .q1_caching import Q1
from .q2_spy import Q2
from .q3_method_borrowing import Q3
from .q4_debounce_throttle import Q4
from .q5_composition import Q5
from .q6_properties import Q6
from .q7_factory import Q7
from .q8_bug_hunt import Q8
from .q9_rate_limit import Q9
from .q10_diagnostic import Q10

ALL_QUESTIONS = [
    Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10
]

def get_question(qid: int):
    for q in ALL_QUESTIONS:
        if q["id"] == qid:
            return q
    return None
