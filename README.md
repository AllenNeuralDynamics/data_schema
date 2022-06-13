# data_schema

A repository for acquisition metadata schemata. The formats follow the standards defined at [JSON Schema](https://json-schema.org/) and are validated using python.A

### Dependencies

* Tested against Python 3.8
* Python packages are listed in `requirements.txt`

### Validating the schemas

* If using conda, run:
 ```
conda create -n data-schema python=3.8
conda activate data-schema
pip install -r requirements.txt
python -m unittest
```
* Errors will be thrown if a schema is invalid
* For extra debugging, set the log level as an environment variable before running the unit tests: `export LOG_LEVEL=DEBUG`
