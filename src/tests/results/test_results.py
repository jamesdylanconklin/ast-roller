"""
Tests for output formatting and pretty-printing functionality.
Includes snapshot testing for consistent output verification.
"""

import pytest
import random
import json
from results_test_cases import SNAPSHOT_CASES
from ast_roller.grammar import parser, transformer
from pathlib import Path

class TestPrettyPrinting:
    def run_test(self, roll_string, seed):
        random.seed(seed)
        result = transformer.transform(parser.parse(roll_string)).evaluate()
        return result.pretty_print(depth=0, indent=0)
    
    def validate_output(self, roll_string, snapshot, result):
        try:
            snapshot.assert_match(result, 'output.txt')
        except AssertionError as e:
            error_str = f"Snapshot mismatch for roll string: {roll_string}"
            error_str += (f"\tGenerated Output:\n{result}")
            error_str += (f"\tSnapshot: {snapshot}")
            raise AssertionError(error_str) from e

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['basic_dice'])
    def test_basic_dice_outputs(self, roll_string, snapshot):
        suite_seed = 42
        output = self.run_test(roll_string, suite_seed)
        snapshot.assert_match(output, 'output.txt')


    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['arithmetic_operations'])
    def test_arithmetic_operations_outputs(self, roll_string, snapshot):
        suite_seed = 24752
        output = self.run_test(roll_string, suite_seed)
        snapshot.assert_match(output, 'output.txt')

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['sequence_expressions'])
    def test_sequence_expression_outputs(self,roll_string, snapshot):
        suite_seed = 90210
        output = self.run_test(roll_string, suite_seed)
        snapshot.assert_match(output, 'output.txt')

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['list_expressions'])
    def test_list_expressions_outputs(self, roll_string, snapshot):
        suite_seed = 13579
        output = self.run_test(roll_string, suite_seed)
        snapshot.assert_match(output, 'output.txt')

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['complex_expressions'])
    def test_complex_expressions_outputs(self, roll_string, snapshot):
        suite_seed = 24886
        output = self.run_test(roll_string, suite_seed)
        snapshot.assert_match(output, 'output.txt')


class TestJSONOutput:
    """Test JSON output functionality with snapshot testing and JSON validation."""
    
    def run_test(self, roll_string, seed):
        """Generate JSON output for a roll string with a fixed seed."""
        random.seed(seed)
        result = transformer.transform(parser.parse(roll_string)).evaluate()
        # TODO: Replace with result.to_json() once implemented
        return result.to_json()
    
    def validate_json_output(self, roll_string, snapshot, output):
        """Validate that output is valid JSON and matches snapshot."""
        try:
            # Validate that the output is valid JSON
            json.loads(output)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Invalid JSON output for roll string '{roll_string}': {e}")
        
        try:
            snapshot.assert_match(output, 'output.json')
        except AssertionError as e:
            error_str = f"JSON snapshot mismatch for roll string: {roll_string}"
            error_str += f"\tGenerated Output:\n{output}"
            error_str += f"\tSnapshot: {snapshot}"
            raise AssertionError(error_str) from e

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['basic_dice'])
    def test_basic_dice_json_outputs(self, roll_string, snapshot):
        suite_seed = 42
        output = self.run_test(roll_string, suite_seed)
        self.validate_json_output(roll_string, snapshot, output)

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['arithmetic_operations'])
    def test_arithmetic_operations_json_outputs(self, roll_string, snapshot):
        suite_seed = 24752
        output = self.run_test(roll_string, suite_seed)
        self.validate_json_output(roll_string, snapshot, output)

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['sequence_expressions'])
    def test_sequence_expression_json_outputs(self, roll_string, snapshot):
        suite_seed = 90210
        output = self.run_test(roll_string, suite_seed)
        self.validate_json_output(roll_string, snapshot, output)

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['list_expressions'])
    def test_list_expressions_json_outputs(self, roll_string, snapshot):
        suite_seed = 13579
        output = self.run_test(roll_string, suite_seed)
        self.validate_json_output(roll_string, snapshot, output)

    @pytest.mark.parametrize("roll_string", SNAPSHOT_CASES['complex_expressions'])
    def test_complex_expressions_json_outputs(self, roll_string, snapshot):
        suite_seed = 24886
        output = self.run_test(roll_string, suite_seed)
        self.validate_json_output(roll_string, snapshot, output)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])