"""
Test cases for output formatting and pretty-printing.
Contains test data for snapshot testing and output verification.
"""

import random

# Seed configurations for reproducible test runs
RANDOM_SEEDS = {
    "basic_dice": 42,
    "complex_expressions": 123,
    "list_operations": 456,
    "nested_operations": 789,
}

# Test cases for snapshot testing - input expressions and expected output structure
SNAPSHOT_CASES = {
    "basic_dice_rolls": [
        # "expression_string": "expected_snapshot_filename"
        # TODO: Add basic dice roll expressions
    ],
    
    "arithmetic_operations": [
        # TODO: Add arithmetic with dice expressions
    ],
    
    "list_expressions": [
        # TODO: Add list/repetition expressions
    ],
    
    "complex_nested": [
        # TODO: Add complex nested expressions
    ]
}

# Pretty-print formatting test cases
PRETTY_PRINT_CASES = {
    # TODO: Add test cases for different pretty-print formats
    # "format_style": [(result_node, expected_output), ...]
}


def setup_seed_for_case(case_name):
    """Helper to set up deterministic random seed for test case."""
    if case_name in RANDOM_SEEDS:
        random.seed(RANDOM_SEEDS[case_name])
    else:
        random.seed(42)  # Default seed