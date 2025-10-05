"""
Evaluator node classes for the dice rolling AST.
"""

import random
import re
from abc import ABC, abstractmethod
from results import ResultNode


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

class ListEvaluatorNode(EvaluatorNode):
    """Handles list expressions - space-separated values with potential repetition."""
    
    def __init__(self, count_expr_node, loop_expr_node=None):
        self.count_expr_node = count_expr_node
        self.loop_expr_node = loop_expr_node
    
    def evaluate(self) -> ResultNode:
        if self.loop_expr_node is None:
            # Single expression case - just evaluate it
            result = self.count_expr_node.evaluate()
            return ResultNode(int(result.raw_result), result.children)

        # Two expression case - count and loop
        count_result = self.count_expr_node.evaluate()
        count = int(count_result.raw_result)
        
        # TODO: Consider error for negative count.
        if count <= 0:
            return ResultNode([], {'count_result': count_result})
        
        # Evaluate the loop expression count times
        loop_results = [self.loop_expr_node.evaluate() for _ in range(count)]
        
        
        
        # Extract raw results for the array
        raw_results = [r.raw_result for r in loop_results]

        # If we're dealing with leaf results, round.
        if isinstance(raw_results[0], (int, float)):
            for i in range(len(raw_results)):
                raw_results[i] = int(raw_results[i])


        # All child result nodes: count result + all loop results
        return ResultNode(raw_results, {
            'count_result': count_result,
            'loop_results': loop_results
        })


class BinaryOpEvaluatorNode(EvaluatorNode):
    """Handles arithmetic operations (+, -, *, /)."""
    
    def __init__(self, left, operator, right):
        if operator not in ['+', '-', '*', '/']:
            raise ValueError(f"Unknown binary operator: {operator}")
        
        self.left = left
        self.operator = operator  # Token like '+', '-', '*', '/'
        self.right = right
    
    def evaluate(self) -> ResultNode:
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
        
        return ResultNode(value, {
            'left': left_result,
            'right': right_result
        })


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
        
        if sides_str.lower() == 'f':
            self.random_lower = -1
            self.random_upper = 1
        else:
            self.random_lower = 1
            self.random_upper = int(sides_str)
    
    def evaluate(self) -> ResultNode:
        rolls = [random.randint(self.random_lower, self.random_upper) for _ in range(self.num_dice)]
        
        # Rolls aren't actually children - we'll need another init arg when we create the RollResultNode subclass
        return ResultNode(sum(rolls), {}) 
    

class NumberEvaluatorNode(EvaluatorNode):
    """Handles numeric literals (integers, floats, natural numbers)."""
    
    def __init__(self, number_token, number_type):
        self.number_token = number_token
        self.number_type = number_type  # 'integer', 'float', 'natural_num'
    
    def evaluate(self) -> ResultNode:
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
        
        return ResultNode(value, {})