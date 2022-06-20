import os
import glob
import ntpath
import argparse
import json
import hashlib
import operator
import random
from functools import reduce
from typing import Any, Dict, List, Optional

from jsf import JSF
from jsf.schema_types.base import ProviderNotSetException
from jsf.schema_types.array import Array


class FakeJsonGenerator:
    """
    Gives methods to create random examples for json schemas
    """

    def __init__(self, rng_seed=None):
        """Apply patches to jsf library. Optionally apply seed to rng."""
        if rng_seed is not None:
            random.seed(rng_seed)
        self.__patch_generate(Array)
        self.__patch_parse(JSF)

    def random_example(self, schema):
        """Create random example for given schema"""
        fake_data_object = JSF(schema)
        fake_json = fake_data_object.generate()
        self._handle_if_then(fake_json, schema)
        self._handle_dependant_schemas(fake_json, schema)
        return fake_json

    def _handle_dependant_schemas(self, fake_json, json_schema):
        """jsf library doesn't handle dependent schemas yet"""
        if 'dependentSchemas' in json_schema:
            dependencies = (set(fake_json.keys()).intersection(
                set(json_schema['dependentSchemas'])))
            for dep_schema_key in dependencies:
                dep_schema = (
                    json_schema['dependentSchemas'][dep_schema_key])
                dep_schema['type'] = 'object'
                dep_fake_json = self.random_example(dep_schema)
                fake_json.update(dep_fake_json)

    def _handle_if_then(self, fake_json, json_schema):
        """jsf library doesn't handle if then properties yet"""
        if 'allOf' in json_schema:
            for all_of_item in json_schema['allOf']:
                if 'if' in all_of_item:
                    item_key = list(all_of_item['if']['properties'].keys())[0]
                    item_value = (
                        all_of_item['if']['properties'][item_key]['const'])
                    if(item_key in fake_json and
                            fake_json[item_key] == item_value):
                        dep_schema = all_of_item['then']
                        dep_schema['type'] = 'object'
                        if '$defs' in json_schema:
                            dep_schema['$defs'] = json_schema['$defs']
                        dep_json = self.random_example(dep_schema)
                        self._handle_dep_refs(all_of_item,
                                              json_schema,
                                              dep_json)
                        fake_json.update(dep_json)
        return fake_json

    def _handle_dep_refs(self, all_of_item, json_schema, dep_json):
        """jsf library doesn't handle if then in array items"""
        for prop_key in all_of_item['then']['properties']:
            prop_value = all_of_item['then']['properties'][prop_key]
            if 'items' in prop_value and '$ref' in prop_value['items']:
                ref_key_str = prop_value['items']['$ref']
                ref_key = ref_key_str.replace('#/', '').split('/')
                dict_item = reduce(operator.getitem, ref_key, json_schema)
                if 'allOf' in dict_item:
                    new_array = []
                    for json_item in dep_json[prop_key]:
                        self._handle_if_then(json_item, dict_item)
                        new_array.append(json_item)
                    dep_json[prop_key] = new_array

    @staticmethod
    def __patch_generate(cls):
        """Monkey patches bug in jsf library"""
        __class__ = cls

        def generate(obj, context: Dict[str, Any]) -> Optional[List[Any]]:
            try:
                return super().generate(context)
            except ProviderNotSetException:

                if isinstance(obj.fixed, str):
                    obj.minItems = obj.maxItems = eval(obj.fixed, context)()
                elif isinstance(obj.fixed, int):
                    obj.minItems = obj.maxItems = obj.fixed

                output = ([obj.items.generate(context)
                           for _
                           in
                           range(random.randint(obj.minItems, obj.maxItems))])
                if obj.uniqueItems:
                    output = [dict(s) for
                              s in set(frozenset(d.items()) for d in output)]
                    while len(output) < obj.minItems:
                        output.append(obj.items.generate(context))
                return output

        cls.generate = generate

    @staticmethod
    def __patch_parse(cls):
        """Monkey patches bug in jsf library."""
        __class__ = cls

        def parse(obj, schema: Dict[str, Any]):
            for name, definition in schema.get("$defs", {}).items():
                item = obj._JSF__parse_definition(name,
                                                  path="#/$defs",
                                                  schema=definition)
                obj.definitions[f"#/$defs/{name}"] = item

            obj.root = obj._JSF__parse_definition(name="root",
                                                  path="#",
                                                  schema=schema)

        cls._parse = parse


def json_contents_from_filepath(filepath):
    """Extracts the json contents from a file path"""
    with open(filepath) as f:
        json_contents = json.load(f)
    return json_contents


def write_json_to_file(json_contents, filepath):
    """
    Writes json contents to a file
    ----------
    json_contents : Python dict to write out as json
    filepath : File to write contents to
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_contents, f, ensure_ascii=False, indent=4)


def write_json_iter_to_files(schema_location,
                             out_directory,
                             num_of_examples,
                             rng_seed=None):
    """
    Generates fake json contents for each schema in the json_iterable and
    writes them as json file in the directory. The contents are hashed to
    give unique file names.
    Parameters
    ----------
    schema_location : A file or directory to process
    out_directory : Where to write the files to
    num_of_examples : How many examples per schema to generate
    rng_seed : Optionally seed random number generator
    """
    if rng_seed is None:
        faker = FakeJsonGenerator()
    else:
        faker = FakeJsonGenerator(rng_seed)
    if (os.path.isfile(schema_location) and
            str(schema_location).endswith(".json")):
        json_files = glob.glob(schema_location)
    else:
        glob_path = os.path.join(schema_location, "**", "*.json")
        json_files = glob.glob(glob_path, recursive=True)
    for json_file in json_files:
        file_name = ntpath.basename(json_file)
        json_schema = json_contents_from_filepath(json_file)
        for _ in range(num_of_examples):
            random_example = faker.random_example(schema=json_schema)
            random_example_string = json.dumps(random_example)
            hash_str = hashlib.md5(random_example_string.encode()).hexdigest()
            out_file_name = (file_name
                             .replace('.json', '-' + hash_str + '.json'))
            out_filepath = os.path.join(out_directory, out_file_name)
            write_json_to_file(random_example, out_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', default=1, type=int)
    parser.add_argument('-s', '--schemas', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-r', '--rseed', required=False)
    args = parser.parse_args()
    write_json_iter_to_files(args.schemas, args.output, args.num, args.rseed)
