"""
Grammar definition for AST parsing using Lark.
"""

from lark import Transformer, Lark, v_args
from .evaluators import (
    ListEvaluatorNode, 
    BinaryOpEvaluatorNode, 
    DiceRollEvaluatorNode, 
    NumberEvaluatorNode
)

# Lark grammar definition
# This will be populated with the actual grammar rules

# TODO: Support comma separated expression sequences

GRAMMAR = """
start: list_expression -> root_result
list_expression: expression | expression LIST_SEP list_expression -> list_expression
expression: "(" expression ")" -> parens
          | expression OPERATOR_AS expression -> binary_op_as
          | expression OPERATOR_MD expression -> binary_op_md
          | DICE_ROLL -> dice_roll
          | FLOAT -> float
          | NATURAL_NUM -> natural_num
          | INTEGER -> integer

DICE_ROLL: /([1-9]\d*)?d([1-9]\d*|[Ff])/i
OPERATOR_AS: "+" | "-"
OPERATOR_MD: "*" | "/"
FLOAT: /-?\d*\.\d+/
INTEGER: /-?\d+/
NATURAL_NUM: /[1-9]\d*/
LIST_SEP: /\s+/

%import common.WS_INLINE
%ignore WS_INLINE  # Only ignore inline whitespace in expressions

"""


### TRANSFORMER

@v_args(inline=True)
class CalculateTree(Transformer):
    """
    Transforms the parse tree into an evaluable structure.
    """
    
    def root_result(self, child):
        """Transform root expression."""
        # We pruned single-element list results. 
        # We actually want one at the root.
        if isinstance(child, ListEvaluatorNode):
            return child

        return ListEvaluatorNode(None, child)
    
    def list_expression(self, *args):
        """Transform list expression - either single or count+loop."""
        if len(args) == 1:
            # Single expression
            return args[0]
        else:
            # Count + loop expression (args[1] is LIST_SEP token, args[2] is loop expr)
            return ListEvaluatorNode(args[0], args[2])
    
    def parens(self, inner):
        """Transform parentheses - just return inner expression (prune)."""
        return inner
    
    def binary_op_as(self, left, op_token, right):
        """Transform addition/subtraction operations."""
        return BinaryOpEvaluatorNode(left, str(op_token), right)
    
    # Alias for multiplication/division 
    binary_op_md = binary_op_as
    
    def dice_roll(self, dice_token):
        """Transform dice roll."""
        return DiceRollEvaluatorNode(dice_token)
    
    def float(self, token):
        """Transform float number."""
        return NumberEvaluatorNode(token, 'float')
    
    def integer(self, token):
        """Transform integer."""
        return NumberEvaluatorNode(token, 'integer')
    
    def natural_num(self, token):
        """Transform natural number."""
        return NumberEvaluatorNode(token, 'natural_num')


parser = Lark(GRAMMAR, parser='earley')
transformer = CalculateTree()