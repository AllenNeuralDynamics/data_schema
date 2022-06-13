import os
import json
import unittest
import logging
from pathlib import Path
from jsonschema import validators, validate

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)
TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
SCHEMAS_DIR = TEST_DIR / ".." / "schemas"
EXAMPLES_DIR = TEST_DIR / ".." / "example"


class TestValidSchemas(unittest.TestCase):
    """
    Checks that the schemas are valid using the jsonschema and unittest
    packages.
    """

    def setUp(self):
        """Sets the log level based on an env variable"""
        logging.basicConfig(level=LOG_LEVEL)

    @staticmethod
    def json_contents_from_filepath(filepath):
        """Extracts the json contents from a file path"""
        with open(filepath) as f:
            json_contents = json.load(f)
        return json_contents

    def test_schemas(self):
        """
        Walks through the schemas directory and validates each of the json
        files
        """
        for subdir, dirs, files in os.walk(SCHEMAS_DIR):
            for file in files:
                if file.endswith('.json'):
                    try:
                        filepath = os.path.join(subdir, file)
                        json_schema = (
                            self.json_contents_from_filepath(filepath))
                        cls = validators.validator_for(json_schema)
                        cls.check_schema(json_schema)
                    finally:
                        logging.debug(f"Validating file: {file}")

    def test_examples(self):
        """
        Goes through each of the files in the example directory and checks
        them against a schema definition
        """
        # Mouse example
        mouse_example_path = os.path.join(EXAMPLES_DIR, "mouse_296929.json")
        mouse_schema_path = os.path.join(SCHEMAS_DIR, "Mouse Schema.json")
        mouse_example = self.json_contents_from_filepath(mouse_example_path)
        mouse_schema = self.json_contents_from_filepath(mouse_schema_path)
        validate(instance=mouse_example, schema=mouse_schema)
        # Surgery HPC example
        surgery_example_hpc_path = (
            os.path.join(EXAMPLES_DIR, "surgery_HPC.json"))
        surgery_schema_path = os.path.join(SCHEMAS_DIR, "Surgery Schema.json")
        surgery_hpc_example = (
            self.json_contents_from_filepath(surgery_example_hpc_path))
        surgery_schema = self.json_contents_from_filepath(surgery_schema_path)
        validate(instance=surgery_hpc_example, schema=surgery_schema)
        # Surgery injection example
        surgery_example_inj_path = (
            os.path.join(EXAMPLES_DIR, "surgery_injection.json"))
        surgery_injection_example = (
            self.json_contents_from_filepath(surgery_example_inj_path))
        validate(instance=surgery_injection_example, schema=surgery_schema)
        # Session example
        session_001_path = (
            os.path.join(EXAMPLES_DIR, "session_001.json"))
        session_schema_path = (
            os.path.join(SCHEMAS_DIR, "ephys", "Ephys Session Schema.json"))
        session_example = (
            self.json_contents_from_filepath(session_001_path))
        session_schema = self.json_contents_from_filepath(session_schema_path)
        validate(instance=session_example, schema=session_schema)


if __name__ == '__main__':
    unittest.main()
