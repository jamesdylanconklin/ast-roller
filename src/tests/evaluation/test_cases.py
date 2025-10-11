"""
Test cases for evaluator classes.
Contains test data and mock configurations for evaluation testing.
"""

# Test cases for DiceRollEvaluatorNode
DICE_ROLL_CASES = {
    "single_die": [
        ("d6", {"result": 6, "calls": [(1, 6)], "raw_results": [6]}),
        ("1d8", {"result": 8, "calls": [(1, 8)], "raw_results": [8]}),
        ("d20", {"result": 20, "calls": [(1, 20)], "raw_results": [20]}),
        ("1d100", {"result": 100, "calls": [(1, 100)], "raw_results": [100]}),
    ],
    "multiple_dice": [
        ("3d6", {"result": 18, "calls": [(1, 6), (1, 6), (1, 6)], "raw_results": [6, 6, 6]}),
        ("5d8", {"result": 40, "calls": [(1, 8), (1, 8), (1, 8), (1, 8), (1, 8)], "raw_results": [8, 8, 8, 8, 8]}),
        ("6d10", {"result": 60, "calls": [(1, 10), (1, 10), (1, 10), (1, 10), (1, 10), (1, 10)], "raw_results": [10, 10, 10, 10, 10, 10]}),
    ],
    "fudge_dice": [
        ("df", {"result": 1, "calls": [(-1, 1)], "raw_results": [1]}),
        ("4dF", {"result": 4, "calls": [(-1, 1), (-1, 1), (-1, 1), (-1, 1)], "raw_results": [1, 1, 1, 1]}),
    ],
    "invalid_dice": [
        "3d1",     # y = 1 (invalid die size)  
        "0d6",     # x = 0 (zero dice)
        "3dx",     # y not number or F (invalid die type)
        "ad6",     # x not number (invalid count)
        "2d",      # missing die size
        "d",       # incomplete dice format
    ]
}

# Test cases for NumberEvaluatorNode
NUMBER_EVALUATOR_CASES = {
    # "test_category": [(token, number_type, expected_result), ...]
}

# Test cases for BinaryOpEvaluatorNode  
BINARY_OP_CASES = {
    # "operator": [(left_result, right_result, expected_result), ...]
}

# Test cases for ListEvaluatorNode
LIST_EVALUATOR_CASES = {
    # "test_scenario": [(count_result, loop_results, expected_result), ...]
}