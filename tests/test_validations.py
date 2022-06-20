import os
import unittest
import logging
from pathlib import Path

from jsonschema import validators, validate

from example_generator.generator import json_contents_from_filepath
from example_generator.generator import FakeJsonGenerator

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)
TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
SCHEMAS_DIR = TEST_DIR / ".." / "schemas"
EXAMPLES_DIR = TEST_DIR / ".." / "example"

EXAMPLES_AND_SCHEMAS = (
    [
        (os.path.join(EXAMPLES_DIR, "mouse_296929.json"),
         os.path.join(SCHEMAS_DIR, "Mouse Schema.json")
         ),
        (os.path.join(EXAMPLES_DIR, "surgery_HPC.json"),
         os.path.join(SCHEMAS_DIR, "Surgery Schema.json")
         ),
        (os.path.join(EXAMPLES_DIR, "surgery_injection.json"),
         os.path.join(SCHEMAS_DIR, "Surgery Schema.json")
         ),
        (os.path.join(EXAMPLES_DIR, "session_001.json"),
         os.path.join(SCHEMAS_DIR, "ephys", "Ephys Session Schema.json"))
    ])


class TestValidSchemas(unittest.TestCase):
    """
    Checks that the schemas are valid using the jsonschema and unittest
    packages.
    """

    def setUp(self):
        """Sets the log level based on an env variable"""
        logging.basicConfig(level=LOG_LEVEL)

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
                            json_contents_from_filepath(filepath))
                        cls = validators.validator_for(json_schema)
                        cls.check_schema(json_schema)
                    finally:
                        logging.debug(f"Validating file: {file}")

    def test_examples(self):
        """
        Goes through each of the files in the example directory and checks
        them against a schema definition
        """
        for example_and_schema in EXAMPLES_AND_SCHEMAS:
            schema = json_contents_from_filepath(example_and_schema[1])
            example = json_contents_from_filepath(example_and_schema[0])
            validate(instance=example, schema=schema)


class TestGenerators(unittest.TestCase):

    rng_seed = 10
    my_faker = FakeJsonGenerator(rng_seed)

    def test_random_examples(self):
        """
        Walks through the schema directory, generates 3 random examples,
        and validates the examples against the original schema
        """
        for subdir, dirs, files in os.walk(SCHEMAS_DIR):
            for file in files:
                if file.endswith('.json'):
                    try:
                        filepath = os.path.join(subdir, file)
                        schema = json_contents_from_filepath(filepath)
                        for _ in range(3):
                            fake_example = self.my_faker.random_example(schema)
                            validate(instance=fake_example, schema=schema)
                    finally:
                        logging.debug(f"Validating file: {file}")


if __name__ == '__main__':
    unittest.main()
