"""
Result node classes for the dice rolling evaluation system.
"""


class ResultNode:
    """
    Base class for all evaluation result nodes.
    Stores the computed result and provides interface for pretty printing.
    """
    def __init__(self, raw_result, children=None):
        self.raw_result = raw_result
        self.children = children or {}
    
    # TODO: Add node type-specific subclasses. Implement indented pretty-printing.