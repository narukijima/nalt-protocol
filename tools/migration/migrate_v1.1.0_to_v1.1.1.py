#!/usr/bin/env python3
"""
NALT Protocol Migration Tool: v1.1.0 to v1.1.1

This script migrates NALT Protocol documents from version 1.1.0 to version 1.1.1.
Main changes:
- Removes top-level 'timestamp' field
- Adds 'created_at' to entries if not present (using the removed timestamp)
- Updates spec_version to 'nalt-protocol/1.1.1'
"""

import json
import sys
from datetime import datetime

def migrate_entry(entry, doc_timestamp):
    """
    Migrate a single entry by adding created_at if missing.
    
    Args:
        entry: Entry object to migrate
        doc_timestamp: Document-level timestamp to use if entry lacks created_at
    
    Returns:
        Modified entry object
    """
    if 'created_at' not in entry and doc_timestamp:
        entry['created_at'] = doc_timestamp
    return entry

def migrate_document(old_doc):
    """
    Migrate a NALT Protocol document from v1.1.0 to v1.1.1.
    
    Args:
        old_doc: Document object in v1.1.0 format
    
    Returns:
        Document object in v1.1.1 format
    """
    new_doc = old_doc.copy()
    
    # Remove timestamp from top level and store it
    doc_timestamp = new_doc.pop('timestamp', None)

    # Migrate each entry
    entries = new_doc.get('entries', [])
    new_doc['entries'] = [migrate_entry(entry, doc_timestamp) for entry in entries]

    # Update version and add migration metadata
    new_doc['spec_version'] = 'nalt-protocol/1.1.1'
    new_doc['x_migrated_at'] = datetime.utcnow().isoformat() + 'Z'

    return new_doc

def main(filename):
    """
    Main migration function.
    
    Args:
        filename: Path to the JSON file to migrate
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            old_doc = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filename}': {e}")
        sys.exit(1)
    
    new_doc = migrate_document(old_doc)

    # Create output filename
    new_filename = f"migrated_{filename}"
    
    with open(new_filename, 'w', encoding='utf-8') as f:
        json.dump(new_doc, f, indent=2, ensure_ascii=False)
    
    print(f"Migration successful!")
    print(f"Output file: {new_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python migrate_v1.1.0_to_v1.1.1.py <filename>")
        print("Example: python migrate_v1.1.0_to_v1.1.1.py old_data.json")
        sys.exit(1)
    
    main(sys.argv[1])