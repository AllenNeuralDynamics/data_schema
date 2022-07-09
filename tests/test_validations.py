import json
import logging
import os
import unittest
from pathlib import Path

from aind_data_schemas.ephys_schemas import EphysRigSchema, EphysSessionSchema
from aind_data_schemas.mouse_schema import MouseSchema
from aind_data_schemas.surgery_schema import SurgerySchema

LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)
TEST_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
SCHEMAS_DIR = TEST_DIR / ".." / "aind_data_schemas"
EXAMPLES_DIR = TEST_DIR / ".." / "example"


class TestValidSchemas(unittest.TestCase):
    """
    Checks that the aind_data_schemas are valid using the jsonschema and
    unittest packages.
    """

    def setUp(self):
        """Sets the log level based on an env variable"""
        logging.basicConfig(level=LOG_LEVEL)

    def _test_example_against_schema(self, example_path, schema):
        with open(example_path) as f:
            data = json.load(f)
        errs = schema.validate(data)
        self.assertFalse(
            errs,
            msg=(
                f"\n on instance: \n \t {data} \n from "
                f"file: \n \t {example_path}"
            ),
        )

    def test_mouse_examples(self):
        """
        Goes through each of the files in the example directory and checks
        them against a schema definition
        """
        example = os.path.join(EXAMPLES_DIR, "mouse_296929.json")
        schema = MouseSchema()
        self._test_example_against_schema(example, schema)

    def test_surgery_examples(self):
        surgery_hpc_example = os.path.join(EXAMPLES_DIR, "surgery_HPC.json")
        surgery_inj_example = os.path.join(
            EXAMPLES_DIR, "surgery_injection.json"
        )
        schema = SurgerySchema()
        self._test_example_against_schema(surgery_hpc_example, schema)
        self._test_example_against_schema(surgery_inj_example, schema)

    def test_ephys_rig_examples(self):
        example = os.path.join(EXAMPLES_DIR, "ephys_rig_2_0_3.json")
        schema = EphysRigSchema()
        self._test_example_against_schema(example, schema)

    def test_ephys_session_examples(self):
        example = os.path.join(EXAMPLES_DIR, "session_001.json")
        schema = EphysSessionSchema()
        self._test_example_against_schema(example, schema)


if __name__ == "__main__":
    unittest.main()
