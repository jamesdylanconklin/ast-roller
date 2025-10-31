"""
Evaluator node classes for the dice rolling AST.
"""

import random
import re
from abc import ABC, abstractmethod
from .results import SequenceResultNode, ListResultNode, DiceResultNode, NumberResultNode, BinaryOpResultNode, ResultNode

### EVALUATOR NODES

class EvaluatorNode(ABC):
    """
    Base class for all evaluable nodes.
    Each evaluator node can evaluate itself to produce a ResultNode.
    """
    
    @abstractmethod
    def evaluate(self) -> ResultNode:
        """Evaluate this node and return a ResultNode containing the result."""
        pass

class SequenceEvaluatorNode(EvaluatorNode):
    """Handles sequences of expressions separated by commas."""

    def __init__(self, expr_nodes):
        self.expr_nodes = expr_nodes  # List of EvaluatorNode instances

    def evaluate(self) -> ListResultNode:
        results = [expr_node.evaluate() for expr_node in self.expr_nodes]
        return SequenceResultNode(results)

class ListEvaluatorNode(EvaluatorNode):
    """Handles list expressions - space-separated values with potential repetition."""
    
    def __init__(self, count_expr_node, loop_expr_node):
        self.count_expr_node = count_expr_node
        self.loop_expr_node = loop_expr_node
    
    def evaluate(self) -> ListResultNode:
        if self.count_expr_node is None:
            expr_result_node = self.loop_expr_node.evaluate()
            # Single expression case - just evaluate it
            return ListResultNode(NumberResultNode(1), [expr_result_node], int(expr_result_node.raw_result))

        # Two expression case - count and loop
        count_result = self.count_expr_node.evaluate()
        count = int(count_result.raw_result)
        
        # TODO: Consider error for negative count.
        if count <= 0:
            return ListResultNode(count_result, [],[])
        
        # Evaluate the loop expression count times
        loop_results = [self.loop_expr_node.evaluate() for _ in range(count)]
        
        # Extract raw results for the array
        raw_results = [r.raw_result for r in loop_results]

        # If we're dealing with leaf results, round.
        if isinstance(raw_results[0], (int, float)):
            for i in range(len(raw_results)):
                raw_results[i] = int(raw_results[i])

        return ListResultNode(count_result, loop_results, raw_results)


class BinaryOpEvaluatorNode(EvaluatorNode):
    """Handles arithmetic operations (+, -, *, /)."""
    
    def __init__(self, left, operator, right):
        if operator not in ['+', '-', '*', '/']:
            raise ValueError(f"Unknown binary operator: {operator}")
        
        self.left = left
        self.operator = operator  # Token like '+', '-', '*', '/'
        self.right = right

        if not all([hasattr(node, 'evaluate') for node in [left, right]]):
            raise ValueError("Left and right operands must expose evaluate functions")
    
    def evaluate(self) -> BinaryOpResultNode:
        left_result = self.left.evaluate()
        right_result = self.right.evaluate()
        
        if self.operator == '+':
            value = left_result.raw_result + right_result.raw_result
        elif self.operator == '-':
            value = left_result.raw_result - right_result.raw_result
        elif self.operator == '*':
            value = left_result.raw_result * right_result.raw_result
        elif self.operator == '/':
            value = left_result.raw_result / right_result.raw_result
        
        return BinaryOpResultNode(self.operator, left_result, right_result, value)


class DiceRollEvaluatorNode(EvaluatorNode):
    """Handles dice roll expressions like '3d6' or 'd20'."""
    
    def __init__(self, dice_token):
        self.dice_token = dice_token  # The DICE_ROLL token
        
        # Parse the dice token (e.g., "3d6", "d20", "4dF")
        match = re.match(r'(\d*)d(\d+|[Ff])', str(dice_token))
        if not match:
            raise ValueError(f"Invalid dice token: {dice_token}")
        
        count_str, sides_str = match.groups()
        self.num_dice = int(count_str) if count_str else 1

        if self.num_dice <= 0:
            raise ValueError(f"Number of dice must be positive, got {self.num_dice}")
        
        if sides_str.lower() == 'f':
            self.random_lower = -1
            self.random_upper = 1
        else:
            self.random_lower = 1
            self.random_upper = int(sides_str)

        if self.random_lower == self.random_upper:
            raise ValueError(f"Die must have more than one side, got {self.random_upper}")
    
    def evaluate(self) -> DiceResultNode:
        rolls = [random.randint(self.random_lower, self.random_upper) for _ in range(self.num_dice)]
        
        # Rolls aren't actually children - we'll need another init arg when we create the RollResultNode subclass
        return DiceResultNode(self.dice_token, sum(rolls), rolls)
    

class NumberEvaluatorNode(EvaluatorNode):
    """Handles numeric literals (integers, floats, natural numbers)."""
    
    def __init__(self, number_token, number_type):
        self.number_token = number_token
        self.number_type = number_type  # 'integer', 'float', 'natural_num'
    
    def evaluate(self) -> NumberResultNode:
        if self.number_type == 'float':
            value = float(self.number_token)
        elif self.number_type == 'integer':
            value = int(self.number_token)
        elif self.number_type == 'natural_num':
            value = int(self.number_token)
            if value <= 0:
                raise ValueError(f"Natural number must be positive, got {value}")
        else:
            raise ValueError(f"Unknown number type: {self.number_type}")
        
        return NumberResultNode(value)