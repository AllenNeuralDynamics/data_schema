import os
import argparse
import json
import hashlib
import operator
import random
from jsf import JSF
from functools import reduce
from typing import Any, Dict, List, Optional
from jsf.schema_types.base import ProviderNotSetException
from jsf.schema_types.array import Array


def patch_generate(cls):
    __class__ = cls  # provide closure cell for super()

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
                       in range(random.randint(obj.minItems, obj.maxItems))])
            if obj.uniqueItems:
                output = [dict(s) for
                          s in set(frozenset(d.items()) for d in output)]
                while len(output) < obj.minItems:
                    output.append(obj.items.generate(context))
            return output
    cls.generate = generate


def patch_parse(cls):
    __class__ = cls  # provide closure cell for super()

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


patch_generate(Array)
patch_parse(JSF)


class FakeJsonGenerator:

    def random_examples(self, json_schemas, num_of_examples):
        for schema in json_schemas:
            for _ in list(range(num_of_examples)):
                yield self.random_example(schema)

    def random_example(self, schema):
        fake_data_object = JSF(schema)
        fake_json = fake_data_object.generate()
        self._handle_if_then(fake_json, schema)
        self._handle_dependant_schemas(fake_json, schema)
        return fake_json

    def _handle_dependant_schemas(self, fake_json, json_schema):
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


def json_contents_from_filepath(filepath):
    """Extracts the json contents from a file path"""
    with open(filepath) as f:
        json_contents = json.load(f)
        file_name = f.name
        json_info = (file_name, json_contents)
    return json_info


def json_contents_from_dir(json_dir):
    """Extracts the json contents from a file path"""
    for subdir, dirs, files in os.walk(json_dir):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(subdir, file)
                json_info = json_contents_from_filepath(filepath)
                yield json_info


def write_json_to_file(json_contents, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_contents, f, ensure_ascii=False, indent=4)


def write_json_iter_to_files(json_iterable, directory, num_of_examples):
    faker = FakeJsonGenerator()
    for json_stuff in json_iterable:
        file_name = json_stuff[0]
        json_schema = json_stuff[1]
        for _ in range(num_of_examples):
            random_example = faker.random_example(schema=json_schema)
            random_example_string = json.dumps(json_schema)
            hash_str = hashlib.md5(random_example_string.encode()).hexdigest()
            out_file_name = (file_name
                             .replace('.json', '-' + hash_str + '.json'))
            out_filepath = os.path.join(directory, out_file_name)
            write_json_to_file(random_example, out_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', default=1)
    parser.add_argument('-s', '--schemas', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    schemas_loc = args.schemas
    num = args.num
    output_dir = args.output
    if os.path.isfile(schemas_loc) and str(schemas_loc).endswith(".json"):
        json_iter = iter([json_contents_from_filepath(schemas_loc)])
    else:
        json_iter = json_contents_from_dir(schemas_loc)
    write_json_iter_to_files(json_iter, output_dir, num)
