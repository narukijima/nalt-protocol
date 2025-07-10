import json
import jsonschema
import sys
import os

def validate_personal_data_protocol(file_path):
    """
    Validates a JSON file against the Personal Data Protocol (PDP) v1.0.0 schema.
    """
    # Construct the absolute path to the schema file
    script_dir = os.path.dirname(__file__)
    schema_path = os.path.join(script_dir, '../../../schema/v1.0.0/schema.json')

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            instance = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file {file_path}")
        sys.exit(1)

    try:
        jsonschema.validate(instance=instance, schema=schema)
        print(f"✅ Validation successful: '{file_path}' conforms to Personal Data Protocol (PDP) v1.0.0.")
    except jsonschema.exceptions.ValidationError as err:
        print(f"❌ Validation failed: '{file_path}' does not conform to the schema.")
        print("Error details:")
        print(f"  Message: {err.message}")
        print(f"  Path: {list(err.path)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validator.py <path_to_json_file>")
        sys.exit(1)
    
    file_to_validate = sys.argv[1]
    validate_personal_data_protocol(file_to_validate)