import json
import jsonschema
import sys
import os
import argparse
from datetime import datetime

def validate_nalt_protocol(file_path, version='v1.1.0', check_strongly_recommended=True):
    """
    Validates a JSON file against the NALT Protocol schema.
    
    Args:
        file_path: Path to the JSON file to validate
        version: Schema version to validate against (default: v1.1.0)
        check_strongly_recommended: Whether to warn about missing strongly recommended fields
    """
    # Construct the absolute path to the schema file
    script_dir = os.path.dirname(__file__)
    schema_path = os.path.join(script_dir, f'../../../schema/{version}/schema.json')

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
        print(f"✅ Validation successful: '{file_path}' conforms to NALT Protocol {version}.")
        
        # Check for strongly recommended fields
        if check_strongly_recommended and version == 'v1.1.0':
            warnings = check_strongly_recommended_fields(instance)
            for warning in warnings:
                print(f"⚠️  Warning: {warning}")
    except jsonschema.exceptions.ValidationError as err:
        print(f"❌ Validation failed: '{file_path}' does not conform to the schema.")
        print("Error details:")
        print(f"  Message: {err.message}")
        print(f"  Path: {list(err.path)}")
        sys.exit(1)

def check_strongly_recommended_fields(instance):
    """Check for strongly recommended fields and return warnings."""
    warnings = []
    
    # Check for timestamp
    if 'timestamp' not in instance:
        warnings.append("'timestamp' field is strongly recommended but missing")
    
    # Check mood intensity precision
    for entry in instance.get('entries', []):
        if 'moods' in entry:
            for i, mood in enumerate(entry['moods']):
                intensity = mood.get('intensity', 0)
                if intensity != round(intensity, 2):
                    warnings.append(f"Mood intensity should use 0.01 precision (entry {i})")
    
    # Check for valid mood types (v1.1.0 enforces 20 predefined types)
    valid_moods = {
        # Positive moods
        'happy', 'excited', 'peaceful', 'content', 'grateful', 
        'calm', 'hopeful', 'proud', 'motivated',
        # Negative moods
        'sad', 'angry', 'anxious', 'frustrated', 'tired', 
        'confused', 'lonely',
        # Neutral moods
        'neutral', 'curious', 'nostalgic', 'surprised'
    }
    for entry in instance.get('entries', []):
        if 'moods' in entry:
            for mood in entry['moods']:
                mood_type = mood.get('type', '')
                if mood_type and mood_type not in valid_moods:
                    warnings.append(f"Mood type '{mood_type}' is not in the list of 20 predefined mood types")
                    break
    
    return warnings

def check_dates_consistency(instance):
    """Check that end_date >= date when present."""
    if 'end_date' in instance and 'date' in instance:
        try:
            start = datetime.fromisoformat(instance['date'])
            end = datetime.fromisoformat(instance['end_date'])
            if end < start:
                return False, "end_date must be greater than or equal to date"
        except:
            pass
    return True, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Validate NALT Protocol JSON files')
    parser.add_argument('file', help='Path to JSON file to validate')
    parser.add_argument('--version', default='v1.1.0', help='Schema version (default: v1.1.0)')
    parser.add_argument('--no-warnings', action='store_true', help='Disable strongly recommended field warnings')
    
    args = parser.parse_args()
    
    validate_nalt_protocol(args.file, args.version, not args.no_warnings)