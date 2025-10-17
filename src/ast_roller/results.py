"""
Result node classes for the dice rolling evaluation system.
"""

from abc import ABC, abstractmethod

class ResultNode:
    """
    Base class for all evaluation result nodes.
    Stores the computed result and provides interface for pretty printing.
    """

    def __init__(self, raw_result, token, children=None):
        self.raw_result = raw_result
        self.token = token
        self.children = children or {}

    def compact_print(self):
        return f"{self.raw_result}"

    @abstractmethod
    def traverse(self):
        pass

    @abstractmethod
    def detailed_print(self, depth, indent):
        pass

class StructuralResultNode(ResultNode):
    """Result node for structural constructs like lists."""

    pass

class ListResultNode(StructuralResultNode):
    def __init__(self, count_result_node, expr_result_nodes, raw_result):
        expr_token = expr_result_nodes[0].token if expr_result_nodes else '[Expression Not Evaluated]'
        token = f'{count_result_node.token} {expr_token}'
        super().__init__(raw_result, token, {'count': count_result_node, 'expr_results': expr_result_nodes})
        self.count_result_node = count_result_node
        self.expr_result_nodes = expr_result_nodes

    def traverse(self, depth=0):
        yield (self, depth)
        yield from self.count_result_node.traverse(depth + 1)
        for expr_node in self.expr_result_nodes:
            yield from expr_node.traverse(depth + 1)
    
    def compact_print(self):
        """Compact print for list result node."""
        # Because of nesting, this can get complex quickly. Forgo
        # deep inspection.

        return f'{raw_results}'
    
    def detailed_print(self, depth=0, indent=0):
        lines = []
        lines.append(f"{indent * '  '}List Expansion: {self.token}")
        lines.append(f"{(indent + 1) * '  '}Count: {self.count_result_node.token} => {self.count_result_node.raw_result}")
        lines.append(f"{(indent + 1) * '  '}Expression: {self.expr_result_nodes[0].token}")

        # I think list expressions are the only one that really need to worry about depth cutoffs.

        for expr_node_idx in range(len(self.expr_result_nodes)):
            expr_node = self.expr_result_nodes[expr_node_idx]
            prefix = f"{(indent + 1) * '  '}{expr_node_idx}: "
            if depth > 0:
                lines.append(f"{prefix}{expr_node.raw_result}")
            else:
                lines.append(prefix)
                lines.append(f"{expr_node.detailed_print(depth + 1, len(prefix) // 2)}")

        return "\n".join(lines)


class BinaryOpResultNode(StructuralResultNode):
    """Result node for binary operations."""

    def __init__(self, operator, left_node, right_node, raw_result):
        token = f"{left_node.token} {operator} {right_node.token}"
        super().__init__(raw_result, token, {'left': left_node, 'right': right_node})
        self.left = left_node
        self.right = right_node
        self.operator = operator

    def compact_print(self):
        return f'{self.left.token} {self.operator} {self.right.token} = {self.raw_result}'
    
    def detailed_print(self, _, indent=0):
        raw_eq = f"({self.left.token} {self.operator} {self.right.token})"
        result_eq = f"{self.left.raw_result} {self.operator} {self.right.raw_result}"
        return (f"{indent * '  '}{raw_eq} => {result_eq} = {self.raw_result}")

    def traverse(self, depth=0):
        yield (self, depth)
        yield from self.children['left'].traverse(depth + 1)
        yield from self.children['right'].traverse(depth + 1)

    
class LeafResultNode(ResultNode):
    """Result node for leaf values like numbers and dice rolls."""

    def traverse(self, depth=0):
        yield (self, depth)

class DiceResultNode(LeafResultNode):
    """Result node for dice rolls, storing individual die results."""
    def __init__(self, roll_string, raw_result, die_results):
        super().__init__(raw_result, token=roll_string)
        self.die_results = die_results  # List of individual die roll results

    # Consider dropping if too verbose
    def compact_print(self):
        return f'{self.token} => {self.raw_result}'

    def detailed_print(self, _, indent):
        return f"{indent * '  '}{self.token} => {self.die_results} = {self.raw_result}"

class NumberResultNode(LeafResultNode):
    """Result node for numeric values."""

    def __init__(self, raw_result):
        super().__init__(raw_result, token=raw_result)

    def detailed_print(self, _, indent):
        return f"{indent * ''}{self.token} => {self.raw_result}"
    
    