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

SNAPSHOT_CASES = {
    "basic_dice": [
        '3d6',
        'd20',
        '4dF',
    ],
    "arithmetic_operations": [
        '3 * 4',
        '4+2',
        '0 - 10',
        '20 / 5',
        '29',
    ],

    "list_expressions": [
        '1d6',
        '6 3d6',
        '4 0 d8',
        '5 5 d5',
        '5 5', # Forcing NumberResult.pretty_print, mostly.
    ],

    "complex_expressions": [
        '3 * (4 + 5)',
        '1d4 + 2 6 2d6+6',
        '2 (1d4 + 2) * 3',
        '2 2 1.5*(d8 + 4 + 2d6)',
        '(d8 + 4 + 2d6) / 2'

    ],
}
