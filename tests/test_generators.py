import unittest
import json
import os
from pathlib import Path
import logging
from jsonschema import validate
from example_generator.generator import FakeJsonGenerator

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)
TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
SCHEMAS_DIR = TEST_DIR / ".." / "schemas"
EXAMPLES_DIR = TEST_DIR / ".." / "example"


class TestGenerators(unittest.TestCase):

    my_faker = FakeJsonGenerator()

    @staticmethod
    def json_contents_from_filepath(filepath):
        """Extracts the json contents from a file path"""
        with open(filepath) as f:
            json_contents = json.load(f)
        return json_contents

    def test_gen1(self):
        schema_path = os.path.join(SCHEMAS_DIR, "Mouse Schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None

    def test_gen2(self):
        schema_path = os.path.join(SCHEMAS_DIR, "Surgery Schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None

    def test_gen3(self):
        schema_path = os.path.join(SCHEMAS_DIR,
                                    "ephys",
                                    "Ephys Rig Schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None

    def test_gen4(self):
        schema_path = os.path.join(SCHEMAS_DIR,
                                    "ephys",
                                    "Ephys Session alternate schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None

    def test_gen5(self):
        schema_path = os.path.join(SCHEMAS_DIR,
                                    "ephys",
                                    "Ephys Session Schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None

    def test_gen6(self):
        schema_path = os.path.join(SCHEMAS_DIR,
                                    "imaging",
                                    "Instrument Schema.json")
        schema = self.json_contents_from_filepath(schema_path)
        fake_example = self.my_faker.random_example(schema)
        validate(instance=fake_example, schema=schema)
        return None


if __name__ == '__main__':
    unittest.main()
