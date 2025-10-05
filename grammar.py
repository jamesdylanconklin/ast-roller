"""
Grammar definition for AST parsing using Lark.
"""

from lark import Transformer, Lark, v_args

# Lark grammar definition
# This will be populated with the actual grammar rules

GRAMMAR = """
start: list_expression | seq_expression -> root_result
seq_expression: (list_expression SEQ_SEP)+ list_expression -> seq_result
list_expression: expression | expression LIST_SEP list_expression -> list_expression
expression: "(" expression ")" -> parens
          | expression OPERATOR_AS expression -> binary_op_as
          | expression OPERATOR_MD expression -> binary_op_md
          | DICE_ROLL -> dice_roll
          | FLOAT -> float_num
          | INTEGER -> integer
          | WHOLE_NUM -> whole_num

DICE_ROLL: /([1-9]\d*)?d([1-9]\d*|[Ff])/i
OPERATOR_AS: "+" | "-"
OPERATOR_MD: "*" | "/"
FLOAT: /-?\d*\.\d+/
INTEGER: /-?\d+/
WHOLE_NUM: /\d+/
SEQ_SEP: ","
LIST_SEP: /\s+/

%import common.WS_INLINE
%ignore WS_INLINE  # Only ignore inline whitespace in expressions

"""

@v_args(inline=True)
class CalculateTree(Transformer):
    """
    Transforms the parse tree into an evaluable structure.
    """
    pass
            
parser = Lark(GRAMMAR, parser='earley')