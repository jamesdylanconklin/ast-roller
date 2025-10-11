"""
Tests for evaluator node classes.
"""

import pytest
from unittest.mock import patch, call

from ast_roller.evaluators import DiceRollEvaluatorNode
from test_cases import DICE_ROLL_CASES

mock_random_fn = lambda _, max_val: max_val  # Always return max for testing

class TestNumberEvaluatorNode:
    """Test NumberEvaluatorNode evaluation."""
    
    def test_integer_evaluation(self):
        """Test integer number evaluation."""
        # TODO: Implement
        pass
    
    def test_float_evaluation(self):
        """Test float number evaluation."""
        # TODO: Implement
        pass
    
    def test_natural_number_validation(self):
        """Test natural number validation (must be positive)."""
        # TODO: Implement
        pass


class TestBinaryOpEvaluatorNode:
    """Test BinaryOpEvaluatorNode evaluation."""
    
    def test_addition(self):
        """Test addition operation."""
        # TODO: Implement
        pass
    
    def test_subtraction(self):
        """Test subtraction operation."""
        # TODO: Implement
        pass
    
    def test_multiplication(self):
        """Test multiplication operation."""
        # TODO: Implement  
        pass
    
    def test_division(self):
        """Test division operation."""
        # TODO: Implement
        pass
    
    def test_invalid_operator(self):
        """Test invalid operator raises ValueError."""
        # TODO: Implement
        pass


class TestDiceRollEvaluatorNode:
    """Test DiceRollEvaluatorNode evaluation with mocked random."""

    @pytest.mark.parametrize("die_str,case_config", DICE_ROLL_CASES['single_die'])
    @patch('random.randint', side_effect=mock_random_fn)
    def test_single_die_roll(self, mock_randint, die_str, case_config):
        """Test single die roll (d6, d20, etc.)."""
        node = DiceRollEvaluatorNode(die_str)
        result_node = node.evaluate()
        assert result_node.raw_result == case_config["result"]
        mock_randint.assert_has_calls([call(*args) for args in case_config["calls"]])
        # TODO: Add assertions for individual die results when ResultsNode Dice subclass ready.
    
    @pytest.mark.parametrize("die_str,case_config", DICE_ROLL_CASES['multiple_dice'])
    @patch('random.randint', side_effect=mock_random_fn)
    def test_multiple_dice_roll(self, mock_randint, die_str, case_config):
        """Test multiple dice roll (3d6, 4d8, etc.)."""
        node = DiceRollEvaluatorNode(die_str)
        result_node = node.evaluate()
        assert result_node.raw_result == case_config["result"]
        mock_randint.assert_has_calls([call(*args) for args in case_config["calls"]])
    
    @pytest.mark.parametrize("die_str,case_config", DICE_ROLL_CASES['fudge_dice'])
    @patch('random.randint', side_effect=mock_random_fn)
    def test_fate_dice_roll(self, mock_randint, die_str, case_config):
        """Test Fate dice roll (dF, 4dF, etc.)."""
        node = DiceRollEvaluatorNode(die_str)
        result_node = node.evaluate()
        assert result_node.raw_result == case_config["result"]
        mock_randint.assert_has_calls([call(*args) for args in case_config["calls"]])
    
    @pytest.mark.parametrize("die_str", DICE_ROLL_CASES['invalid_dice'])
    def test_invalid_dice_token(self, die_str):
        """Test invalid dice token raises ValueError."""
        with pytest.raises(ValueError):
            DiceRollEvaluatorNode(die_str)


class TestListEvaluatorNode:
    """Test ListEvaluatorNode evaluation."""
    
    def test_single_expression(self):
        """Test single expression (no loop)."""
        # TODO: Implement
        pass
    
    def test_count_and_loop_expression(self):
        """Test count and loop expression."""
        # TODO: Implement
        pass
    
    def test_zero_count(self):
        """Test zero count returns empty list."""
        # TODO: Implement
        pass
    
    def test_negative_count(self):
        """Test negative count behavior."""
        # TODO: Implement
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])