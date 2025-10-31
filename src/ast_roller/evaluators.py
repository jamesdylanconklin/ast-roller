"""
Evaluator node classes for the dice rolling AST.
"""

import random
import re
from abc import ABC, abstractmethod
from collections import defaultdict
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
        if len(expr_nodes) < 2:
            raise ValueError("SequenceEvaluatorNode requires at least two expressions")
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
    
    def __init__(self, dice_token, directives):
        self.dice_token = str(dice_token)
        self.directive_tokens = [str(d) for d in directives]
        self.directives = self.parse_directives() 

        # Parse the dice token (e.g., "3d6", "d20", "4dF")
        match = re.match(r'(\d*)d(\d+|[Ff])', self.dice_token)
        if not match:
            raise ValueError(f"Invalid dice token: {self.dice_token}")

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

    def combined_token(self):
        return f"{' '.join([self.dice_token, *self.directive_tokens])}"

    def parse_directives(self):
        directives = { 'drop': {}, 'keep': {} }
        directive_pattern = re.compile(r'^(?P<keep_drop>[kd])(?P<high_low>[hl])(?P<count>\d+)')

        for token in self.directive_tokens:
            match = directive_pattern.match(token)
            if not match:
                raise ValueError(f"Invalid dice roll directive: {token}")
            keep_drop = { 'k': 'keep', 'd': 'drop' }[match.group('keep_drop').lower()]
            high_low = {'h': 'high', 'l': 'low' }[match.group('high_low').lower()]
            count = int(match.group('count'))

            directives[keep_drop][high_low] = count

        if len(directives['keep']) > 1:
            raise ValueError("Cannot have both keep high and keep low directives")

        return directives
    
    def apply_directives(self, rolls):
        to_keep, to_drop = defaultdict(int), defaultdict(int)

        sorted_rolls = sorted(rolls)

        left_idx = 0
        right_idx = len(sorted_rolls)

        for high_low, count in self.directives['drop'].items():
            if high_low == 'high':
                for roll in sorted_rolls[-count:]:
                    to_drop[roll] += 1
                right_idx -= count
            else:
                for roll in sorted_rolls[:count]:
                    to_drop[roll] += 1
                left_idx += count
        # Should only be one of these, but the unpacking and parallels to above is friendlier.
        for high_low, count in self.directives['keep'].items():
            if high_low == 'high':
                for roll in sorted_rolls[right_idx - count : right_idx]:
                    to_keep[roll] += 1
            else:
                for roll in sorted_rolls[left_idx : left_idx + count]:
                    to_keep[roll] += 1

        result = sum(sorted_rolls[left_idx:right_idx])
        if to_keep:
            result = sum([die * count for die, count in to_keep.items()])

        return result, to_keep, to_drop

    def evaluate(self) -> DiceResultNode:
        rolls = [random.randint(self.random_lower, self.random_upper) for _ in range(self.num_dice)]
        
        # Apply directives
        result, to_keep, to_drop = self.apply_directives(rolls)

        return DiceResultNode(self.combined_token(), result, rolls, to_keep=to_keep, to_drop=to_drop)


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