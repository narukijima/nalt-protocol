#!/usr/bin/env python3
"""
Migration tool for NALT Protocol v1.1.1 to v1.2.0
Removes non-core fields as part of the slim-core initiative.
"""

import json
import sys
import os
from datetime import datetime
from copy import deepcopy


def migrate_document(old_doc):
    """
    Migrate a NALT Protocol document from v1.1.1 to v1.2.0.
    Removes all non-core fields to create a slim-core document.
    """
    new_doc = deepcopy(old_doc)
    removed_fields = {
        'top_level': [],
        'meta': [],
        'entries': {}
    }
    
    # Remove top-level fields
    if 'signature' in new_doc:
        del new_doc['signature']
        removed_fields['top_level'].append('signature')
    
    if 'timestamp' in new_doc:  # Should already be gone in v1.1.1, but check anyway
        del new_doc['timestamp']
        removed_fields['top_level'].append('timestamp')
    
    # Remove meta fields
    if 'meta' in new_doc and 'x_utc_offset_minutes' in new_doc['meta']:
        del new_doc['meta']['x_utc_offset_minutes']
        removed_fields['meta'].append('x_utc_offset_minutes')
    
    # Remove x_ fields from meta that are in our removal list
    meta_x_fields_to_remove = ['x_processed_by', 'x_ai_processing', 'x_statistics', 
                               'x_migration', 'x_encryption', 'x_merged_from']
    if 'meta' in new_doc:
        for field in list(new_doc['meta'].keys()):
            if field in meta_x_fields_to_remove:
                del new_doc['meta'][field]
                removed_fields['meta'].append(field)
    
    # Remove entry fields
    entry_fields_to_remove = ['summary', 'moods', 'tags', 'entities', 'end_date', 
                              'created_at', 'x_relations', 'x_due_date']
    
    for i, entry in enumerate(new_doc.get('entries', [])):
        removed_fields['entries'][i] = []
        for field in entry_fields_to_remove:
            if field in entry:
                del entry[field]
                removed_fields['entries'][i].append(field)
    
    # Update version
    new_doc['spec_version'] = 'nalt-protocol/1.2.0'
    
    # Add migration metadata as extension field
    new_doc['x_migrated_at'] = datetime.utcnow().isoformat() + 'Z'
    
    return new_doc, removed_fields


def summarize_migration(removed_fields):
    """Generate a summary of removed fields."""
    summary = []
    
    if removed_fields['top_level']:
        summary.append(f"Top-level fields removed: {', '.join(removed_fields['top_level'])}")
    
    if removed_fields['meta']:
        summary.append(f"Meta fields removed: {', '.join(removed_fields['meta'])}")
    
    # Count entry field removals
    entry_field_counts = {}
    for entry_idx, fields in removed_fields['entries'].items():
        for field in fields:
            entry_field_counts[field] = entry_field_counts.get(field, 0) + 1
    
    if entry_field_counts:
        entry_summary = []
        for field, count in sorted(entry_field_counts.items()):
            entry_summary.append(f"{field} ({count} entries)")
        summary.append(f"Entry fields removed: {', '.join(entry_summary)}")
    
    return '\n'.join(summary)


def main():
    if len(sys.argv) != 2:
        print("Usage: python migrate_v1.1.1_to_v1.2.0.py <input_file.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            old_doc = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{input_file}': {e}")
        sys.exit(1)
    
    # Check version
    if not old_doc.get('spec_version', '').startswith('nalt-protocol/1.1'):
        print(f"Warning: Document version is '{old_doc.get('spec_version', 'unknown')}', expected 'nalt-protocol/1.1.x'")
    
    # Migrate the document
    new_doc, removed_fields = migrate_document(old_doc)
    
    # Generate output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"migrated_{os.path.basename(base_name)}.json"
    
    # Write the migrated document
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_doc, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"✅ Migration complete: {input_file} → {output_file}")
    print(f"   Version: {old_doc.get('spec_version', 'unknown')} → {new_doc['spec_version']}")
    print("\n📊 Migration Summary:")
    print(summarize_migration(removed_fields))
    print(f"\n   Output file: {output_file}")


if __name__ == "__main__":
    main()