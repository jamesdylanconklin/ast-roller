from lark import Tree, Token

"""
Test cases for the dice rolling grammar.
Contains test data separated from test logic for easier maintenance.
"""

def integer_tree(value):
    """Helper to create an integer parse tree."""
    return Tree('integer', [Token('INTEGER', str(value))])

def die_tree(count, sides, capitalize=False):
    """Helper to create a dice roll parse tree."""
    count_str = count if count is not None else ''

    return Tree('dice_roll', [(Token('DICE_ROLL', f'{count_str}d{sides}'))])

def tree_root(children):
    """Helper to create a root parse tree."""
    return Tree('start', [list_tree(children)])

def list_tree(elements):
    """Helper to create a list expression parse tree."""
        
    if len(elements) == 1:
        return Tree('list_expression', elements)
    return Tree('list_expression', [elements[0], Token('LIST_SEP', ' '), list_tree(elements[1:])])
    

def binary_op_as_tree(op_name, left, right):
    """Helper for addition/subtraction binary operations."""
    return Tree('binary_op_as', [left, Token('OPERATOR_AS', op_name), right])

def binary_op_md_tree(op_name, left, right):
    """Helper for multiplication/division binary operations."""
    return Tree('binary_op_md', [left, Token('OPERATOR_MD', op_name), right])


def parens_tree(inner):
    """Helper for parentheses trees."""
    return Tree('parens', [inner])


# Basic parsing test cases
BASIC_PARSING_CASES = {
    "integers": [
        ("867", tree_root([integer_tree(867)])),
        ("-530", tree_root([integer_tree(-530)])),
        ("9", tree_root([integer_tree(9)]))
    ],

    "dice_rolls": [
      ("d6", tree_root([die_tree(None, 6)])),
      ("3d6", tree_root([die_tree(3, 6)])),
      ("1d20", tree_root([die_tree(1, 20)])),
      ("dF", tree_root([die_tree(None, 'F')])),
      ("4df", tree_root([die_tree(4, 'f')])), 
    ],

    "basic_arithmetic": [
        ("3+4", tree_root([binary_op_as_tree("+", integer_tree(3), integer_tree(4))])),
        ("10-2", tree_root([binary_op_as_tree("-", integer_tree(10), integer_tree(2))])),
        ("5*6", tree_root([binary_op_md_tree("*", integer_tree(5), integer_tree(6))])),
        ("8/2", tree_root([binary_op_md_tree("/", integer_tree(8), integer_tree(2))])),
    ],

    "parentheses": [
        ("(5+(4+(3)))", tree_root([
            parens_tree(
                binary_op_as_tree(
                    '+',
                    integer_tree(5),
                    parens_tree(
                        binary_op_as_tree(
                            '+',
                            integer_tree(4),
                            parens_tree(integer_tree(3))   
                            
                        )
                    )
                  )
            ) 
        ])),
        ("(5)", tree_root([parens_tree(integer_tree(5))])),
        ("(3+4)", tree_root([parens_tree(binary_op_as_tree('+', integer_tree(3), integer_tree(4)))])),
    ]
}

# List expression test cases
LIST_EXPRESSION_CASES = [
    ("3", tree_root([integer_tree(3)])),
    ("3 4 5", tree_root([integer_tree(3), integer_tree(4), integer_tree(5)])),
    ("d6 d8", tree_root([die_tree(None, 6), die_tree(None, 8)])),
    ("1d4 2d6 3d8", tree_root([die_tree(1, 4), die_tree(2, 6), die_tree(3, 8)])),
    ("5 2d6", tree_root([integer_tree(5), die_tree(2, 6)])),
    ("d20 15 3d4", tree_root([die_tree(None, 20), integer_tree(15), die_tree(3, 4)]))
]

# Operator precedence test cases
PRECEDENCE_CASES = [
    # Multiplication before addition - should parse as 2+(3*4)
    ("2+3*4", tree_root([
        binary_op_as_tree("+", 
            integer_tree(2), 
            binary_op_md_tree("*", integer_tree(3), integer_tree(4))
        )
    ])),
    
    # Addition after multiplication - should parse as (3*4)+5
    ("3*4+5", tree_root([
        binary_op_as_tree("+", 
            binary_op_md_tree("*", integer_tree(3), integer_tree(4)),
            integer_tree(5)
        )
    ])),
    
    # Division before subtraction - should parse as 10-(6/2)
    ("10-6/2", tree_root([
        binary_op_as_tree("-", 
            integer_tree(10), 
            binary_op_md_tree("/", integer_tree(6), integer_tree(2))
        )
    ])),
    
    # Subtraction after division - should parse as (8/2)-1
    ("8/2-1", tree_root([
        binary_op_as_tree("-", 
            binary_op_md_tree("/", integer_tree(8), integer_tree(2)),
            integer_tree(1)
        )
    ])),
    
    # Parentheses override precedence - should parse as (2+3)*4
    ("(2+3)*4", tree_root([
        binary_op_md_tree("*", 
            parens_tree(binary_op_as_tree("+", integer_tree(2), integer_tree(3))),
            integer_tree(4)
        )
    ])),
    
    # Parentheses override precedence - should parse as 2*(3+4)
    ("2*(3+4)", tree_root([
        binary_op_md_tree("*", 
            integer_tree(2),
            parens_tree(binary_op_as_tree("+", integer_tree(3), integer_tree(4)))
        )
    ])),
]

# Complex expression test cases
COMPLEX_CASES = [
    # Dice with arithmetic
    ("2d6+3", tree_root([
        binary_op_as_tree("+", die_tree(2, 6), integer_tree(3))
    ])),
    ("1d20-5", tree_root([
        binary_op_as_tree("-", die_tree(1, 20), integer_tree(5))
    ])), 
    ("3d4*2", tree_root([
        binary_op_md_tree("*", die_tree(3, 4), integer_tree(2))
    ])),
    ("4d6/2", tree_root([
        binary_op_md_tree("/", die_tree(4, 6), integer_tree(2))
    ])),
    
    # Arithmetic with dice
    ("5+2d8", tree_root([
        binary_op_as_tree("+", integer_tree(5), die_tree(2, 8))
    ])),
    ("10-1d6", tree_root([
        binary_op_as_tree("-", integer_tree(10), die_tree(1, 6))
    ])),
    
    # Multiple dice in expression
    ("2d6+1d8", tree_root([
        binary_op_as_tree("+", die_tree(2, 6), die_tree(1, 8))
    ])),
    ("3d4-2d6", tree_root([
        binary_op_as_tree("-", die_tree(3, 4), die_tree(2, 6))
    ])),
    
    # Complex combinations
    ("(2d6+3)*4", tree_root([
        binary_op_md_tree("*", 
            parens_tree(binary_op_as_tree("+", die_tree(2, 6), integer_tree(3))),
            integer_tree(4)
        )
    ])),
    ("1d20+5-2", tree_root([
        binary_op_as_tree("-", 
            binary_op_as_tree("+", die_tree(1, 20), integer_tree(5)),
            integer_tree(2)
        )
    ])),
]

# Edge cases and error conditions
EDGE_CASES = [
    # Should parse successfully
    ("d1", tree_root([die_tree(None, 1)])),
    ("100d100", tree_root([die_tree(100, 100)])),
    ("  3d6  ", tree_root([die_tree(3, 6)])),
    
    # Complex list expressions
    ("6 2d6+3", tree_root([
        integer_tree(6), 
        binary_op_as_tree("+", die_tree(2, 6), integer_tree(3))
    ])),
    ("3 (1d4+2)", tree_root([
        integer_tree(3), 
        parens_tree(binary_op_as_tree("+", die_tree(1, 4), integer_tree(2)))
    ])),
]

# Cases that should fail to parse
SHOULD_FAIL_CASES = [
    "",  # Empty string fails parse, but should have a configurable default
    "d",  # Incomplete dice
    "3d",  # Missing die size
    "d+3",  # Invalid die format
    "3++4",  # Double operator
    "3d6)",  # Unmatched parenthesis
    "(3d6",  # Unmatched parenthesis
    "3 d 6",  # Spaces in dice
    "-3d6", # Negative dice. Consider allowing as implicit subtraction from zero.
    "+4", # leading plus
]