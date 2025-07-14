# Migration Guide: NALT Protocol v1.0.0 to v1.1.0

This guide helps you migrate your NALT Protocol data from v1.0.0 to v1.1.0.

## Breaking Changes

### 1. Required `document_id`
**v1.0.0**: `document_id` was recommended  
**v1.1.0**: `document_id` is **required** and must be a valid UUID v4

**Migration Action**:
```javascript
// If document_id is missing, generate a new UUID v4
if (!document.document_id) {
  document.document_id = crypto.randomUUID(); // or use uuid library
}
```

### 2. Content Format Restrictions
**v1.0.0**: `content_format` was free text  
**v1.1.0**: `content_format` must be one of: `text/plain`, `text/markdown`, `text/html`, `application/json`, `text/org`

**Migration Action**:
```javascript
// Map common formats to MIME types
const formatMapping = {
  'plain_text': 'text/plain',
  'markdown': 'text/markdown',
  'md': 'text/markdown',
  'html': 'text/html',
  'json': 'application/json',
  'org': 'text/org'
};

entries.forEach(entry => {
  entry.content_format = formatMapping[entry.content_format] || 'text/plain';
});
```

## New Features (Non-Breaking)

### 1. Strongly Recommended `timestamp`
While not required, `timestamp` is now strongly recommended. Consider adding it:

```javascript
if (!document.timestamp) {
  document.timestamp = new Date().toISOString();
}
```

### 2. New `end_date` Field
For entries spanning multiple days:

```javascript
// Example: A week-long vacation
{
  "date": "2025-07-01",
  "end_date": "2025-07-07",
  // ... other fields
}
```

### 3. Mood Intensity Precision
Intensity values should now use 0.01 precision:

```javascript
// Round to 2 decimal places
entry.moods.forEach(mood => {
  mood.intensity = Math.round(mood.intensity * 100) / 100;
});
```

### 4. UTC Offset for Performance
Add timezone offset for faster processing:

```javascript
// Calculate UTC offset in minutes
const date = new Date();
meta.x_utc_offset_minutes = -date.getTimezoneOffset();
```

### 5. Digital Signatures
Add signatures for data integrity:

```javascript
// Example signature object
{
  "signature": {
    "alg": "EdDSA",
    "sig": "BASE64URL_ENCODED_SIGNATURE",
    "public_key": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
  }
}
```

## Migration Script Example

```python
import json
import uuid
from datetime import datetime

def migrate_nalt_v1_0_to_v1_1(old_data):
    """Migrate NALT Protocol data from v1.0.0 to v1.1.0"""
    
    # Update spec version
    old_data['spec_version'] = 'nalt-protocol/1.1.0'
    
    # Add document_id if missing
    if 'document_id' not in old_data:
        old_data['document_id'] = str(uuid.uuid4())
    
    # Add timestamp if missing
    if 'timestamp' not in old_data:
        old_data['timestamp'] = datetime.now().isoformat() + 'Z'
    
    # Update content_format for all entries
    format_map = {
        'plain_text': 'text/plain',
        'markdown': 'text/markdown',
        'md': 'text/markdown',
        'html': 'text/html',
        'json': 'application/json'
    }
    
    for entry in old_data.get('entries', []):
        # Fix content_format
        old_format = entry.get('content_format', 'plain_text')
        entry['content_format'] = format_map.get(old_format, 'text/plain')
        
        # Round mood intensities
        if 'moods' in entry:
            for mood in entry['moods']:
                if 'intensity' in mood:
                    mood['intensity'] = round(mood['intensity'], 2)
    
    return old_data

# Usage
with open('old_data.json', 'r') as f:
    old_data = json.load(f)

new_data = migrate_nalt_v1_0_to_v1_1(old_data)

with open('migrated_data.json', 'w') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
```

## Validation After Migration

Use the updated validator to check your migrated data:

```bash
# Python
python tools/validator/python/validator.py migrated_data.json

# Node.js
node tools/validator/nodejs/validator.js migrated_data.json
```

## Rollback Strategy

If you need to rollback to v1.0.0:

1. Change `spec_version` back to `nalt-protocol/1.0.0`
2. Remove `end_date` fields if present
3. Remove `signature` objects if present
4. `document_id` can remain (it was recommended in v1.0.0)

## FAQ

**Q: What happens if I don't add document_id?**  
A: Validation will fail in v1.1.0. You must add a UUID v4.

**Q: Can I use custom content_format values?**  
A: No, you must use one of the allowed MIME types. For custom formats, use `application/json` and structure your content accordingly.

**Q: Is the signature field required?**  
A: No, signatures are optional but recommended for data integrity.

**Q: Do I need to update mood types?**  
A: The recommended mood types are suggestions. Your existing mood types remain valid.