# NALT Protocol - AI Development Documentation

This comprehensive documentation contains all technical specifications, implementation details, and development guidelines for AI systems working with NALT Protocol v1.2.0. This document is optimized for AI consumption with complete technical details and structured information.

## Table of Contents

1. [Protocol Overview and Architecture](#1-protocol-overview-and-architecture)
2. [Complete Specification v1.2.0](#2-complete-specification-v120)
3. [JSON Schema and Validation Rules](#3-json-schema-and-validation-rules)
4. [Implementation Guidelines](#4-implementation-guidelines)
5. [Security Implementation](#5-security-implementation)
6. [Performance Optimization](#6-performance-optimization)
7. [Migration Procedures](#7-migration-procedures)
8. [Code Examples and Patterns](#8-code-examples-and-patterns)
9. [Testing and Quality Assurance](#9-testing-and-quality-assurance)
10. [Error Handling and Edge Cases](#10-error-handling-and-edge-cases)

## 1. Protocol Overview and Architecture

### 1.1 Core Concept

NALT Protocol is a JSON-based specification for structuring and preserving personal information in an AI-interpretable format. The protocol captures personality, values, thoughts, and behavioral patterns from individual-generated data.

### 1.2 Design Principles

- **Reproducibility**: Deterministic rules ensure consistent interpretation across environments
- **Contextuality**: Events and thoughts are connected as graphs with causal relationships
- **Extensibility**: Safe extension mechanisms maintain backward compatibility
- **Privacy**: Separation of personally identifiable information from content

### 1.3 Architecture Components

```
┌─────────────────────────────────────────────────────────┐
│                NALT Document v1.2.0                      │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────────────────┐   │
│ │   Top-Level      │  │        Entries Array        │   │
│ │   Metadata       │  │  ┌───────────────────────┐  │   │
│ │ - spec_version   │  │  │   Entry Object (Core) │  │   │
│ │ - document_id    │  │  │  - entry_id          │  │   │
│ │ - date           │  │  │  - type              │  │   │
│ │ - meta           │  │  │  - mode              │  │   │
│ │ - [x_* extensions]│ │  │  - content_format    │  │   │
│ └─────────────────┘  │  │  - content           │  │   │
│                      │  │  - [x_* extensions]   │  │   │
│                      │  └───────────────────────┘  │   │
│                      └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 2. Complete Specification v1.2.0 (Slim-Core)

### 2.1 File Requirements

- **Encoding**: UTF-8 (mandatory)
- **Extension**: `.json`
- **Structure**: Single root JSON object

### 2.2 Top-Level Object Schema

```typescript
interface NALTDocument {
  spec_version: string;      // Required: "nalt-protocol/1.2.0"
  document_id: string;       // Required: UUIDv4
  date: string;             // Required: YYYY-MM-DD
  meta: MetaObject;         // Required
  entries: Entry[];         // Required: min 1 entry
  [key: `x_${string}`]: any;  // Optional: Extension fields
}
```

### 2.3 Meta Object Schema

```typescript
interface MetaObject {
  language: string;              // Required: ISO 639-1
  timezone: string;              // Required: IANA timezone
  [key: `x_${string}`]: any;     // Optional: Extension fields
}
```

### 2.4 Entry Object Schema

```typescript
interface Entry {
  // Core fields (required) - v1.2.0 slim-core
  entry_id: string;          // UUIDv4 recommended
  type: EntryType;           // Enum: event|reflection|task|idea|log
  mode: TimeMode;            // Enum: morning|afternoon|evening|night|none
  content_format: ContentFormat; // Enum: text/plain|text/markdown|text/html|application/json|text/org
  content: string;           // Original user content
  
  // Extension fields (all optional with x_ prefix)
  [key: `x_${string}`]: any; // Custom extensions including:
  // x_summary?: string;      // AI-generated summary
  // x_moods?: Mood[];        // Mood tracking
  // x_tags?: string[];       // Categorization
  // x_entities?: Entities;   // Entity extraction
  // x_end_date?: string;     // Multi-day entries
  // x_created_at?: string;   // Creation timestamp
  // x_relations?: Relation[];// Entry relationships
  // x_due_date?: string;     // Task due dates
}

// v1.2.0 Note: These interfaces are for extension fields only
// Example extension field definitions:
/*
interface XMood {
  type: string;       // Mood type
  intensity: number;  // 0.00-1.00
}

interface XEntities {
  people?: string[];
  locations?: string[];
  organizations?: string[];
  [key: string]: string[] | undefined;
}

interface XRelation {
  type: string;      // Relationship type
  target_id: string; // Entry ID reference
}
*/
```

### 2.5 Enumeration Definitions (Core v1.2.0)

```typescript
enum EntryType {
  EVENT = "event",           // Real-world occurrences
  REFLECTION = "reflection", // Introspection and thoughts
  TASK = "task",            // To-do items
  IDEA = "idea",            // Creative concepts
  LOG = "log"               // Data records
}

enum TimeMode {
  MORNING = "morning",       // 05:00-11:59
  AFTERNOON = "afternoon",   // 12:00-17:59
  EVENING = "evening",       // 18:00-21:59
  NIGHT = "night",          // 22:00-04:59
  NONE = "none"             // Time-agnostic
}

enum ContentFormat {
  PLAIN = "text/plain",
  MARKDOWN = "text/markdown",
  HTML = "text/html",
  JSON = "application/json",
  ORG = "text/org"
}

// Extension field enumerations moved to implementation section
```

## 3. JSON Schema and Validation Rules

### 3.1 Schema Location

Official schema URL: `https://nalt-protocol.org/schemas/v1.2.0/schema.json`

**Note**: v1.2.0 schema reflects the slim-core design with only essential fields.

### 3.2 Validation Implementation

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

class NALTValidator {
  constructor() {
    this.ajv = new Ajv({ allErrors: true, strict: true });
    addFormats(this.ajv);
    this.schema = this.loadSchema();
  }

  loadSchema() {
    return {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "required": ["spec_version", "document_id", "date", "meta", "entries"],
      "additionalProperties": true,
      "properties": {
        "spec_version": {
          "type": "string",
          "pattern": "^nalt-protocol/1\\.1\\.1$"
        },
        "document_id": {
          "type": "string",
          "format": "uuid"
        },
        "date": {
          "type": "string",
          "format": "date"
        },
        "meta": {
          "type": "object",
          "required": ["language", "timezone"],
          "properties": {
            "language": {
              "type": "string",
              "pattern": "^[a-z]{2}$"
            },
            "timezone": {
              "type": "string"
            },
          },
          "additionalProperties": true
        },
        "entries": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/definitions/entry"
          }
        },
        "signature": {
          "$ref": "#/definitions/signature"
        }
      },
      "definitions": {
        "entry": {
          "type": "object",
          "required": ["entry_id", "type", "mode", "content_format", "content"],
          "properties": {
            "entry_id": {
              "type": "string"
            },
            "type": {
              "enum": ["event", "reflection", "task", "idea", "log"]
            },
            "mode": {
              "enum": ["morning", "afternoon", "evening", "night", "none"]
            },
            "created_at": {
              "type": "string",
              "format": "date-time"
            },
            "content_format": {
              "enum": ["text/plain", "text/markdown", "text/html", "application/json", "text/org"]
            },
            "content": {
              "type": "string"
            },
            "summary": {
              "type": "string",
              "maxLength": 140
            },
            "moods": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["type", "intensity"],
                "properties": {
                  "type": {
                    "type": "string"
                  },
                  "intensity": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "multipleOf": 0.01
                  }
                }
              }
            },
            "tags": {
              "type": "array",
              "minItems": 1,
              "maxItems": 6,
              "items": {
                "type": "string",
                "pattern": "^[a-z_]+$"
              }
            },
            "entities": {
              "type": "object",
              "properties": {
                "people": {
                  "type": "array",
                  "items": { "type": "string" }
                },
                "locations": {
                  "type": "array",
                  "items": { "type": "string" }
                },
                "organizations": {
                  "type": "array",
                  "items": { "type": "string" }
                }
              },
              "additionalProperties": {
                "type": "array",
                "items": { "type": "string" }
              }
            },
            "end_date": {
              "type": "string",
              "format": "date"
            },
            "x_relations": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["type", "target_id"],
                "properties": {
                  "type": {
                    "enum": ["caused_by", "led_to", "related_to", "explains", "contradicts"]
                  },
                  "target_id": {
                    "type": "string"
                  }
                }
              }
            },
            "x_due_date": {
              "type": "string",
              "format": "date"
            }
          },
          "additionalProperties": true
        },
        "signature": {
          "type": "object",
          "required": ["alg", "sig", "public_key"],
          "properties": {
            "alg": {
              "enum": ["EdDSA", "ES256", "RS256"]
            },
            "sig": {
              "type": "string"
            },
            "public_key": {
              "type": "string"
            }
          }
        }
      }
    };
  }

  validate(document) {
    const validate = this.ajv.compile(this.schema);
    const valid = validate(document);
    
    if (!valid) {
      return {
        valid: false,
        errors: validate.errors
      };
    }
    
    // v1.2.0: Custom validations simplified due to slim-core design
    const customErrors = this.customValidations(document);
    if (customErrors.length > 0) {
      return {
        valid: false,
        errors: customErrors
      };
    }
    
    return { valid: true };
  }

  customValidations(document) {
    const errors = [];
    
    // Validate date consistency
    if (document.end_date && document.end_date < document.date) {
      errors.push({
        path: '/end_date',
        message: 'end_date must be after or equal to date'
      });
    }
    
    // Validate entry references
    const entryIds = new Set(document.entries.map(e => e.entry_id));
    document.entries.forEach(entry => {
      if (entry.x_relations) {
        entry.x_relations.forEach(relation => {
          if (!entryIds.has(relation.target_id)) {
            errors.push({
              path: `/entries/${entry.entry_id}/x_relations`,
              message: `Invalid target_id reference: ${relation.target_id}`
            });
          }
        });
      }
    });
    
    return errors;
  }
}
```

## 4. Implementation Guidelines

### 4.1 Entry Segmentation Rules

1. **Time Period Change**: Create new entry when `mode` changes
2. **Topic Change**: Segment on significant topic shifts
3. **Type Change**: New entry when switching between event/reflection/task/etc
4. **Character Limit**: Consider segmentation around 400 chars (JP) or 240 tokens (EN)

### 4.2 Parser Implementation

```javascript
class NALTParser {
  constructor(options = {}) {
    this.maxEntryLength = options.maxEntryLength || 400;
    this.autoSegment = options.autoSegment !== false;
  }

  parseDocument(rawData) {
    const document = JSON.parse(rawData);
    
    if (this.autoSegment) {
      document.entries = this.segmentEntries(document.entries);
    }
    
    return this.enrichDocument(document);
  }

  segmentEntries(entries) {
    const segmented = [];
    
    entries.forEach(entry => {
      if (entry.content.length <= this.maxEntryLength) {
        segmented.push(entry);
        return;
      }
      
      const segments = this.intelligentSplit(entry);
      segments.forEach((segment, index) => {
        segmented.push({
          ...entry,
          entry_id: `${entry.entry_id}-${index + 1}`,
          content: segment.content,
          x_segment: {
            original_id: entry.entry_id,
            part: index + 1,
            total: segments.length
          }
        });
      });
    });
    
    return segmented;
  }

  intelligentSplit(entry) {
    const sentences = this.extractSentences(entry.content);
    const segments = [];
    let currentSegment = { content: '', sentences: [] };
    
    sentences.forEach(sentence => {
      if ((currentSegment.content + sentence).length > this.maxEntryLength && currentSegment.content) {
        segments.push(currentSegment);
        currentSegment = { content: '', sentences: [] };
      }
      currentSegment.content += sentence;
      currentSegment.sentences.push(sentence);
    });
    
    if (currentSegment.content) {
      segments.push(currentSegment);
    }
    
    return segments;
  }

  extractSentences(text) {
    // Language-aware sentence extraction
    const japanesePattern = /[^。！？\n]+[。！？]?/g;
    const englishPattern = /[^.!?\n]+[.!?]?/g;
    
    const hasJapanese = /[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9faf]/.test(text);
    const pattern = hasJapanese ? japanesePattern : englishPattern;
    
    return text.match(pattern) || [text];
  }

  enrichDocument(document) {
    // Add computed fields
    document.x_statistics = {
      entry_count: document.entries.length,
      mood_distribution: this.analyzeMoods(document.entries),
      type_distribution: this.analyzeTypes(document.entries),
      content_length_total: document.entries.reduce((sum, e) => sum + e.content.length, 0)
    };
    
    return document;
  }

  analyzeMoods(entries) {
    const moodStats = {};
    
    entries.forEach(entry => {
      if (entry.moods) {
        entry.moods.forEach(mood => {
          if (!moodStats[mood.type]) {
            moodStats[mood.type] = { count: 0, totalIntensity: 0 };
          }
          moodStats[mood.type].count++;
          moodStats[mood.type].totalIntensity += mood.intensity;
        });
      }
    });
    
    Object.keys(moodStats).forEach(type => {
      moodStats[type].averageIntensity = 
        moodStats[type].totalIntensity / moodStats[type].count;
    });
    
    return moodStats;
  }

  analyzeTypes(entries) {
    const typeCount = {};
    entries.forEach(entry => {
      typeCount[entry.type] = (typeCount[entry.type] || 0) + 1;
    });
    return typeCount;
  }
}
```

### 4.3 Extension Policy Implementation

**Important**: All custom/extension fields MUST be prefixed with `x_` to distinguish them from official fields. Parsers MUST ignore unknown fields without the `x_` prefix.

```javascript
class NALTExtensionHandler {
  constructor() {
    this.registeredExtensions = new Map();
    this.strictMode = true; // Enforce x_ prefix rule
  }

  registerExtension(prefix, handler) {
    if (!prefix.startsWith('x_')) {
      throw new Error('Extension prefix must start with x_');
    }
    this.registeredExtensions.set(prefix, handler);
  }

  processExtensions(document) {
    const processed = JSON.parse(JSON.stringify(document));
    
    // Process document-level extensions
    this.processObjectExtensions(processed);
    
    // Process meta extensions
    this.processObjectExtensions(processed.meta);
    
    // Process entry extensions
    processed.entries.forEach(entry => {
      this.processObjectExtensions(entry);
    });
    
    return processed;
  }

  processObjectExtensions(obj) {
    Object.keys(obj).forEach(key => {
      if (key.startsWith('x_')) {
        const handler = this.findHandler(key);
        if (handler) {
          obj[key] = handler(obj[key], obj);
        }
      } else if (this.strictMode && !this.isOfficialField(key)) {
        // In strict mode, warn about non-x_ prefixed unknown fields
        console.warn(`Unknown field '${key}' should be prefixed with 'x_'`);
      }
    });
  }
  
  isOfficialField(fieldName) {
    // List of official fields that don't require x_ prefix
    const officialFields = new Set([
      'spec_version', 'document_id', 'date', 'meta', 'entries', 'signature',
      'language', 'timezone', 'entry_id', 'type', 'mode', 'content_format',
      'content', 'summary', 'moods', 'tags', 'entities', 'end_date', 'created_at'
    ]);
    return officialFields.has(fieldName);
  }

  findHandler(key) {
    for (const [prefix, handler] of this.registeredExtensions) {
      if (key.startsWith(prefix)) {
        return handler;
      }
    }
    return null;
  }
}

// Example extension for AI processing metadata
const aiExtension = {
  prefix: 'x_ai_',
  handler: (value, context) => {
    if (typeof value === 'object' && value.model) {
      return {
        ...value,
        processed_at: new Date().toISOString(),
        context_type: context.type || 'unknown'
      };
    }
    return value;
  }
};
```

## 5. Security Implementation

### 5.1 Digital Signature Implementation (Extension)

**Note**: v1.2.0 removed signature from core spec. This implementation shows how to add signature support as an extension.

```javascript
const crypto = require('crypto');
const { canonicalize } = require('json-canonicalize');

class NALTSigner {
  constructor(privateKey, publicKeyDID) {
    this.privateKey = privateKey;
    this.publicKeyDID = publicKeyDID;
  }

  async signDocument(document) {
    // Remove existing x_signature extension
    const { x_signature, ...documentToSign } = document;
    
    // Canonicalize JSON (RFC 8785)
    const canonical = canonicalize(documentToSign);
    
    // Create signature
    const signer = crypto.createSign('SHA256');
    signer.update(canonical);
    const signature = signer.sign(this.privateKey, 'base64url');
    
    return {
      ...document,
      x_signature: {
        alg: 'EdDSA',
        sig: signature,
        public_key: this.publicKeyDID
      }
    };
  }

  async verifyDocument(document) {
    if (!document.x_signature) {
      return { valid: false, error: 'No signature present' };
    }
    
    const { x_signature, ...documentToVerify } = document;
    const canonical = canonicalize(documentToVerify);
    
    try {
      const verifier = crypto.createVerify('SHA256');
      verifier.update(canonical);
      
      // Extract public key from DID (implementation depends on DID method)
      const publicKey = await this.resolvePublicKey(x_signature.public_key);
      
      const valid = verifier.verify(publicKey, x_signature.sig, 'base64url');
      return { valid, error: valid ? null : 'Signature verification failed' };
    } catch (error) {
      return { valid: false, error: error.message };
    }
  }

  async resolvePublicKey(did) {
    // DID resolution implementation
    // This is a simplified example - use proper DID resolver in production
    if (did.startsWith('did:key:')) {
      // Extract key from did:key format
      const keyId = did.substring(8);
      // Convert multibase to public key
      return this.multibaseToPublicKey(keyId);
    }
    throw new Error('Unsupported DID method');
  }
}
```

### 5.2 Encryption Implementation

```javascript
class NALTEncryption {
  constructor() {
    this.algorithm = 'aes-256-gcm';
  }

  encryptDocument(document, key) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);
    
    // Encrypt entries individually for selective decryption
    const encryptedEntries = document.entries.map(entry => {
      const entryIv = crypto.randomBytes(16);
      const entryCipher = crypto.createCipheriv(this.algorithm, key, entryIv);
      
      const encrypted = Buffer.concat([
        entryCipher.update(JSON.stringify(entry), 'utf8'),
        entryCipher.final()
      ]);
      
      return {
        entry_id: entry.entry_id,
        encrypted_data: encrypted.toString('base64'),
        iv: entryIv.toString('base64'),
        auth_tag: entryCipher.getAuthTag().toString('base64')
      };
    });
    
    return {
      ...document,
      entries: encryptedEntries,
      x_encryption: {
        algorithm: this.algorithm,
        iv: iv.toString('base64'),
        encrypted_at: new Date().toISOString()
      }
    };
  }

  decryptDocument(encryptedDocument, key) {
    const entries = encryptedDocument.entries.map(encEntry => {
      const iv = Buffer.from(encEntry.iv, 'base64');
      const authTag = Buffer.from(encEntry.auth_tag, 'base64');
      const decipher = crypto.createDecipheriv(this.algorithm, key, iv);
      decipher.setAuthTag(authTag);
      
      const decrypted = Buffer.concat([
        decipher.update(Buffer.from(encEntry.encrypted_data, 'base64')),
        decipher.final()
      ]);
      
      return JSON.parse(decrypted.toString('utf8'));
    });
    
    const { x_encryption, ...documentData } = encryptedDocument;
    return {
      ...documentData,
      entries
    };
  }
}
```

### 5.3 Access Control Implementation

```javascript
class NALTAccessControl {
  constructor() {
    this.policies = new Map();
  }

  definePolicy(documentId, policy) {
    this.policies.set(documentId, policy);
  }

  async checkAccess(documentId, subject, action) {
    const policy = this.policies.get(documentId);
    if (!policy) {
      return { allowed: false, reason: 'No policy defined' };
    }
    
    if (policy.default === 'deny') {
      // Check explicit allow rules
      for (const rule of policy.rules) {
        if (this.matchesRule(rule, subject, action)) {
          return { allowed: true, rule: rule };
        }
      }
      return { allowed: false, reason: 'Default deny' };
    }
    
    // Default allow, check deny rules
    for (const rule of policy.rules) {
      if (rule.effect === 'deny' && this.matchesRule(rule, subject, action)) {
        return { allowed: false, reason: 'Explicit deny', rule: rule };
      }
    }
    
    return { allowed: true, reason: 'Default allow' };
  }

  matchesRule(rule, subject, action) {
    // Check subject match
    if (rule.subject !== '*' && rule.subject !== subject) {
      return false;
    }
    
    // Check action match
    if (!rule.actions.includes('*') && !rule.actions.includes(action)) {
      return false;
    }
    
    // Check conditions
    if (rule.conditions) {
      return this.evaluateConditions(rule.conditions);
    }
    
    return true;
  }

  evaluateConditions(conditions) {
    if (conditions.date_range) {
      const now = new Date();
      const from = new Date(conditions.date_range.from);
      const to = new Date(conditions.date_range.to);
      
      if (now < from || now > to) {
        return false;
      }
    }
    
    // Add more condition evaluations as needed
    
    return true;
  }
}
```

## 6. Performance Optimization

### 6.1 UTC Offset Optimization (Extension)

**Note**: v1.2.0 removed UTC offset from core spec. Applications can implement it as an extension.

```javascript
class TimeZoneOptimizer {
  constructor() {
    this.cache = new Map();
  }

  addUTCOffset(document) {
    const cacheKey = `${document.date}-${document.meta.timezone}`;
    
    if (this.cache.has(cacheKey)) {
      document.x_utc_offset_minutes = this.cache.get(cacheKey);
      return document;
    }
    
    const offset = this.calculateOffset(document.date, document.meta.timezone);
    this.cache.set(cacheKey, offset);
    
    document.x_utc_offset_minutes = offset;
    return document;
  }

  calculateOffset(date, timezone) {
    const d = new Date(date);
    const utcDate = new Date(d.toLocaleString('en-US', { timeZone: 'UTC' }));
    const tzDate = new Date(d.toLocaleString('en-US', { timeZone: timezone }));
    return (tzDate - utcDate) / 60000;
  }

  convertToLocalTime(timestamp, utcOffsetMinutes) {
    const date = new Date(timestamp);
    return new Date(date.getTime() + utcOffsetMinutes * 60000);
  }

  // v1.2.0: When reading documents, check for UTC offset in multiple locations
  getUTCOffset(document) {
    return document.x_utc_offset_minutes || 
           document.meta?.x_utc_offset_minutes || 
           this.calculateOffset(document.date, document.meta.timezone);
  }
}
```

### 6.2 Indexing System

```javascript
class NALTIndexer {
  constructor() {
    this.indices = {
      temporal: new BTree(),      // B-tree for date range queries
      textual: new InvertedIndex(), // Full-text search
      relational: new Graph(),     // Entry relationships
      categorical: new Map()       // Type/mood/tag indices
    };
  }

  indexDocument(document) {
    // Temporal index
    this.indices.temporal.insert(document.date, document.document_id);
    
    document.entries.forEach(entry => {
      // Textual index
      this.indexText(entry);
      
      // v1.2.0: Relational index for x_relations extension
      if (entry.x_relations) {
        entry.x_relations.forEach(relation => {
          this.indices.relational.addEdge(
            entry.entry_id,
            relation.target_id,
            relation.type
          );
        });
      }
      
      // Categorical indices
      this.indexCategorical(entry);
    });
  }

  indexText(entry) {
    const tokens = this.tokenize(entry.content);
    tokens.forEach(token => {
      this.indices.textual.addDocument(entry.entry_id, token);
    });
    
    // v1.2.0: Index x_summary if present
    if (entry.x_summary) {
      const summaryTokens = this.tokenize(entry.x_summary);
      summaryTokens.forEach(token => {
        this.indices.textual.addDocument(entry.entry_id, token, 1.5); // Higher weight
      });
    }
  }

  indexCategorical(entry) {
    // Type index
    this.addToCategoricalIndex('type', entry.type, entry.entry_id);
    
    // v1.2.0: Index extension fields if present
    // Mood index (x_moods)
    if (entry.x_moods) {
      entry.x_moods.forEach(mood => {
        const moodKey = `${mood.type}:${Math.round(mood.intensity * 100)}`;
        this.addToCategoricalIndex('mood', moodKey, entry.entry_id);
      });
    }
    
    // Tag index (x_tags)
    if (entry.x_tags) {
      entry.x_tags.forEach(tag => {
        this.addToCategoricalIndex('tag', tag, entry.entry_id);
      });
    }
  }

  addToCategoricalIndex(category, key, entryId) {
    if (!this.indices.categorical.has(category)) {
      this.indices.categorical.set(category, new Map());
    }
    
    const categoryIndex = this.indices.categorical.get(category);
    if (!categoryIndex.has(key)) {
      categoryIndex.set(key, new Set());
    }
    
    categoryIndex.get(key).add(entryId);
  }

  tokenize(text) {
    // Basic tokenization - enhance with NLP library for production
    return text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(token => token.length > 2);
  }

  search(query) {
    const results = new Map(); // entry_id -> score
    
    // Text search
    if (query.text) {
      const textResults = this.indices.textual.search(query.text);
      textResults.forEach(result => {
        results.set(result.id, (results.get(result.id) || 0) + result.score);
      });
    }
    
    // Date range search
    if (query.dateRange) {
      const dateResults = this.indices.temporal.range(
        query.dateRange.from,
        query.dateRange.to
      );
      dateResults.forEach(docId => {
        // Boost documents in date range
        const currentScore = results.get(docId) || 0;
        results.set(docId, currentScore + 10);
      });
    }
    
    // Filter by categories
    ['type', 'mood', 'tag'].forEach(category => {
      if (query[category]) {
        const categoryResults = this.getCategoricalResults(category, query[category]);
        
        if (query.filterMode === 'strict') {
          // Remove entries not in category results
          for (const [entryId] of results) {
            if (!categoryResults.has(entryId)) {
              results.delete(entryId);
            }
          }
        } else {
          // Boost entries in category results
          categoryResults.forEach(entryId => {
            results.set(entryId, (results.get(entryId) || 0) + 5);
          });
        }
      }
    });
    
    // Sort by score
    return Array.from(results.entries())
      .sort((a, b) => b[1] - a[1])
      .map(([id, score]) => ({ id, score }));
  }

  getCategoricalResults(category, value) {
    const categoryIndex = this.indices.categorical.get(category);
    if (!categoryIndex) return new Set();
    
    if (Array.isArray(value)) {
      const combined = new Set();
      value.forEach(v => {
        const entries = categoryIndex.get(v);
        if (entries) {
          entries.forEach(e => combined.add(e));
        }
      });
      return combined;
    }
    
    return categoryIndex.get(value) || new Set();
  }
}
```

### 6.3 Streaming Parser

```javascript
const { Transform } = require('stream');

class NALTStreamParser extends Transform {
  constructor(options = {}) {
    super({ objectMode: true });
    this.state = 'INIT';
    this.buffer = '';
    this.depth = 0;
    this.inString = false;
    this.escape = false;
    this.currentEntry = '';
    this.documentMeta = null;
  }

  _transform(chunk, encoding, callback) {
    this.buffer += chunk.toString();
    
    for (let i = 0; i < this.buffer.length; i++) {
      const char = this.buffer[i];
      const prevChar = i > 0 ? this.buffer[i - 1] : '';
      
      // Track string boundaries
      if (char === '"' && prevChar !== '\\') {
        this.inString = !this.inString;
      }
      
      if (!this.inString) {
        if (char === '{') {
          this.depth++;
          if (this.state === 'IN_ENTRIES' && this.depth === 2) {
            this.currentEntry = '{';
          }
        } else if (char === '}') {
          this.depth--;
          
          if (this.state === 'IN_ENTRIES' && this.depth === 1 && this.currentEntry) {
            this.currentEntry += '}';
            try {
              const entry = JSON.parse(this.currentEntry);
              this.push({ type: 'entry', data: entry });
              this.currentEntry = '';
            } catch (e) {
              // Invalid JSON, skip
            }
          }
        }
        
        // State transitions
        if (this.buffer.includes('"entries"') && this.state === 'INIT') {
          this.state = 'IN_ENTRIES';
          // Extract document metadata
          const metaMatch = this.buffer.match(/"meta"\s*:\s*(\{[^}]+\})/);
          if (metaMatch) {
            try {
              this.documentMeta = JSON.parse(metaMatch[1]);
              this.push({ type: 'meta', data: this.documentMeta });
            } catch (e) {}
          }
        }
      }
      
      if (this.currentEntry && this.state === 'IN_ENTRIES') {
        this.currentEntry += char;
      }
    }
    
    // Keep only unparsed tail in buffer
    if (this.buffer.length > 10000) {
      this.buffer = this.buffer.slice(-5000);
    }
    
    callback();
  }

  _flush(callback) {
    this.push({ type: 'end', data: null });
    callback();
  }
}

// Usage example
const parser = new NALTStreamParser();
const processor = new Transform({
  objectMode: true,
  transform(chunk, encoding, callback) {
    if (chunk.type === 'entry') {
      // Process individual entry
      const processed = processEntry(chunk.data);
      callback(null, processed);
    } else if (chunk.type === 'meta') {
      // Handle metadata
      console.log('Document metadata:', chunk.data);
      callback();
    } else {
      callback();
    }
  }
});

fs.createReadStream('large-nalt-file.json')
  .pipe(parser)
  .pipe(processor)
  .pipe(outputStream);
```

## 7. Migration Procedures

**Note**: This section shows migration to v1.2.0, which removes many fields to create a slim-core specification.

### 7.1 Version Detection and Migration

```javascript
class NALTMigrator {
  constructor() {
    this.migrations = {
      '1.0.0': this.migrateFrom_1_0_0.bind(this),
      '1.1.0': this.migrateFrom_1_1_0.bind(this),
      '1.1.1': this.migrateFrom_1_1_1.bind(this),
      '1.2.0': null // v1.2.0 is the current version
    };
  }

  async migrate(document) {
    const currentVersion = this.extractVersion(document.spec_version);
    const targetVersion = '1.1.1';
    
    if (currentVersion === targetVersion) {
      return { document, migrated: false };
    }
    
    let migratedDoc = { ...document };
    const migrationPath = this.getMigrationPath(currentVersion, targetVersion);
    
    for (const version of migrationPath) {
      const migrator = this.migrations[version];
      if (migrator) {
        migratedDoc = await migrator(migratedDoc);
      }
    }
    
    return { document: migratedDoc, migrated: true };
  }

  extractVersion(specVersion) {
    const match = specVersion.match(/(\d+\.\d+\.\d+)/);
    return match ? match[1] : null;
  }

  getMigrationPath(from, to) {
    // Simple linear migration for now
    const versions = ['1.0.0', '1.1.0', '1.1.1', '1.2.0'];
    const fromIndex = versions.indexOf(from);
    const toIndex = versions.indexOf(to);
    
    if (fromIndex === -1 || toIndex === -1 || fromIndex >= toIndex) {
      return [];
    }
    
    return versions.slice(fromIndex + 1, toIndex + 1);
  }

  async migrateFrom_1_0_0(document) {
    const migrated = { ...document };
    
    // Update spec version
    migrated.spec_version = 'nalt-protocol/1.2.0';
    
    // Add required document_id if missing
    if (!migrated.document_id) {
      migrated.document_id = this.generateUUID();
    }
    
    // Add timestamp if missing
    if (!migrated.timestamp) {
      migrated.timestamp = new Date().toISOString();
    }
    
    // Update content_format values
    const formatMap = {
      'plain_text': 'text/plain',
      'markdown': 'text/markdown',
      'md': 'text/markdown',
      'html': 'text/html',
      'json': 'application/json',
      'org': 'text/org'
    };
    
    migrated.entries = migrated.entries.map(entry => {
      const updated = { ...entry };
      
      // Update content format
      if (formatMap[entry.content_format]) {
        updated.content_format = formatMap[entry.content_format];
      } else if (!this.isValidMimeType(entry.content_format)) {
        updated.content_format = 'text/plain';
      }
      
      // v1.2.0: Handle mood data as extension if present
      if (updated.x_moods) {
        updated.x_moods = updated.x_moods.map(mood => ({
          ...mood,
          intensity: Math.round(mood.intensity * 100) / 100
        }));
      }
      
      return updated;
    });
    
    // v1.2.0: UTC offset removed from core spec
    // Applications can still add it as extension if needed
    
    // Add migration metadata
    migrated.x_migration = {
      from_version: '1.0.0',
      to_version: '1.2.0',
      migrated_at: new Date().toISOString()
    };
    
    return migrated;
  }

  async migrateFrom_1_1_0(document) {
    // First migrate to 1.1.1
    const v1_1_1 = await this.migrateFrom_1_1_0_to_1_1_1(document);
    // Then migrate to 1.2.0
    return this.migrateFrom_1_1_1(v1_1_1);
  }

  async migrateFrom_1_1_0_to_1_1_1(document) {
    // Remove top-level timestamp
    const { timestamp, ...documentWithoutTimestamp } = document;
    
    // Update spec version
    documentWithoutTimestamp.spec_version = 'nalt-protocol/1.1.1';
    
    // If timestamp exists, add to entries as created_at
    if (timestamp && documentWithoutTimestamp.entries) {
      documentWithoutTimestamp.entries = documentWithoutTimestamp.entries.map(entry => {
        if (!entry.created_at) {
          return { ...entry, created_at: timestamp };
        }
        return entry;
      });
    }
    
    return documentWithoutTimestamp;
  }

  async migrateFrom_1_1_1(document) {
    const migrated = { ...document };
    
    // Update spec version
    migrated.spec_version = 'nalt-protocol/1.2.0';
    
    // Migrate top-level signature to x_signature
    if (migrated.signature) {
      migrated.x_signature = migrated.signature;
      delete migrated.signature;
    }
    
    // Migrate meta.x_utc_offset_minutes to document level
    if (migrated.meta?.x_utc_offset_minutes !== undefined) {
      migrated.x_utc_offset_minutes = migrated.meta.x_utc_offset_minutes;
      delete migrated.meta.x_utc_offset_minutes;
    }
    
    // Migrate entries
    migrated.entries = migrated.entries.map(entry => {
      const newEntry = { ...entry };
      
      // Migrate fields to x_ extensions
      const fieldMappings = {
        'summary': 'x_summary',
        'moods': 'x_moods',
        'tags': 'x_tags',
        'entities': 'x_entities',
        'end_date': 'x_end_date',
        'created_at': 'x_created_at'
      };
      
      Object.entries(fieldMappings).forEach(([oldField, newField]) => {
        if (newEntry[oldField] !== undefined) {
          newEntry[newField] = newEntry[oldField];
          delete newEntry[oldField];
        }
      });
      
      return newEntry;
    });
    
    // Add migration metadata
    migrated.x_migration = {
      from_version: '1.1.1',
      to_version: '1.2.0',
      migrated_at: new Date().toISOString()
    };
    
    return migrated;
  }

  isValidMimeType(format) {
    const validTypes = [
      'text/plain',
      'text/markdown',
      'text/html',
      'application/json',
      'text/org'
    ];
    return validTypes.includes(format);
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  calculateUTCOffset(date, timezone) {
    try {
      const d = new Date(date);
      const utcDate = new Date(d.toLocaleString('en-US', { timeZone: 'UTC' }));
      const tzDate = new Date(d.toLocaleString('en-US', { timeZone: timezone }));
      return (tzDate - utcDate) / 60000;
    } catch (e) {
      return null;
    }
  }
}
```

### 7.2 Batch Migration Tool

```javascript
class NALTBatchMigrator {
  constructor(migrator) {
    this.migrator = migrator;
    this.stats = {
      total: 0,
      migrated: 0,
      failed: 0,
      errors: []
    };
  }

  async migrateDirectory(directory, options = {}) {
    const files = await this.findNALTFiles(directory);
    this.stats.total = files.length;
    
    const batchSize = options.batchSize || 10;
    const backup = options.backup !== false;
    
    for (let i = 0; i < files.length; i += batchSize) {
      const batch = files.slice(i, i + batchSize);
      await Promise.all(batch.map(file => this.migrateFile(file, backup)));
    }
    
    return this.stats;
  }

  async migrateFile(filePath, backup) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      const document = JSON.parse(content);
      
      const { document: migrated, migrated: changed } = 
        await this.migrator.migrate(document);
      
      if (changed) {
        if (backup) {
          await fs.copyFile(filePath, `${filePath}.bak`);
        }
        
        await fs.writeFile(
          filePath,
          JSON.stringify(migrated, null, 2),
          'utf8'
        );
        
        this.stats.migrated++;
      }
    } catch (error) {
      this.stats.failed++;
      this.stats.errors.push({
        file: filePath,
        error: error.message
      });
    }
  }

  async findNALTFiles(directory) {
    const files = [];
    const entries = await fs.readdir(directory, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(directory, entry.name);
      
      if (entry.isDirectory()) {
        files.push(...await this.findNALTFiles(fullPath));
      } else if (entry.name.endsWith('.json')) {
        // Quick check if it's likely a NALT file
        const content = await fs.readFile(fullPath, 'utf8');
        if (content.includes('spec_version') && content.includes('nalt-protocol')) {
          files.push(fullPath);
        }
      }
    }
    
    return files;
  }
}
```

## 8. Code Examples and Patterns

### 8.1 Document Creation Patterns

```javascript
class NALTDocumentBuilder {
  constructor() {
    this.reset();
  }

  reset() {
    this.document = {
      spec_version: 'nalt-protocol/1.2.0',
      document_id: this.generateUUID(),
      date: new Date().toISOString().split('T')[0],
      meta: {
        language: 'en',
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
      },
      entries: []
    };
    return this;
  }

  setDate(date) {
    this.document.date = date;
    return this;
  }

  setMeta(meta) {
    this.document.meta = { ...this.document.meta, ...meta };
    return this;
  }

  addEntry(entry) {
    const completeEntry = {
      entry_id: entry.entry_id || this.generateUUID(),
      type: entry.type || 'event',
      mode: entry.mode || this.detectMode(),
      content_format: entry.content_format || 'text/plain',
      content: entry.content || '',
      ...entry
    };
    
    this.document.entries.push(completeEntry);
    return this;
  }

  addRelatedEntry(entry, relationToLast, relationType = 'related_to') {
    if (this.document.entries.length === 0) {
      throw new Error('No entries to relate to');
    }
    
    const lastEntry = this.document.entries[this.document.entries.length - 1];
    const newEntry = {
      ...entry,
      x_relations: [
        ...(entry.x_relations || []),
        {
          type: relationType,
          target_id: lastEntry.entry_id
        }
      ]
    };
    
    return this.addEntry(newEntry);
  }

  detectMode() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) return 'morning';
    if (hour >= 12 && hour < 18) return 'afternoon';
    if (hour >= 18 && hour < 22) return 'evening';
    return 'night';
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  build() {
    if (this.document.entries.length === 0) {
      throw new Error('Document must have at least one entry');
    }
    
    // v1.2.0: UTC offset can be added as document-level extension
    const offset = this.calculateUTCOffset();
    if (offset !== null) {
      this.document.x_utc_offset_minutes = offset;
    }
    
    return this.document;
  }

  calculateUTCOffset() {
    try {
      const d = new Date();
      const utcDate = new Date(d.toLocaleString('en-US', { timeZone: 'UTC' }));
      const tzDate = new Date(d.toLocaleString('en-US', { timeZone: this.document.meta.timezone }));
      return (tzDate - utcDate) / 60000;
    } catch (e) {
      return null;
    }
  }
}

// Usage pattern
const builder = new NALTDocumentBuilder();
const document = builder
  .setDate('2025-01-15')
  .setMeta({ language: 'en', timezone: 'America/New_York' })
  .addEntry({
    type: 'event',
    content: 'Started working on new AI project',
    x_tags: ['work', 'ai', 'project_start']  // v1.2.0: tags as extension
  })
  .addRelatedEntry({
    type: 'reflection',
    content: 'Feeling excited about the possibilities this project could bring',
    x_moods: [{ type: 'excited', intensity: 0.85 }]  // v1.2.0: moods as extension
  }, 'caused_by')
  .build();
```

### 8.2 Query and Filter Patterns

```javascript
class NALTQueryEngine {
  constructor(documents) {
    this.documents = documents;
    this.buildIndices();
  }

  buildIndices() {
    this.indices = {
      byDate: new Map(),
      byType: new Map(),
      byMood: new Map(),
      byTag: new Map()
    };
    
    this.documents.forEach(doc => {
      this.indices.byDate.set(doc.date, doc);
      
      doc.entries.forEach(entry => {
        // Type index
        if (!this.indices.byType.has(entry.type)) {
          this.indices.byType.set(entry.type, []);
        }
        this.indices.byType.get(entry.type).push({ doc, entry });
        
        // v1.2.0: Index extension fields
        // Mood index (x_moods)
        if (entry.x_moods) {
          entry.x_moods.forEach(mood => {
            const key = mood.type;
            if (!this.indices.byMood.has(key)) {
              this.indices.byMood.set(key, []);
            }
            this.indices.byMood.get(key).push({ doc, entry, intensity: mood.intensity });
          });
        }
        
        // Tag index (x_tags)
        if (entry.x_tags) {
          entry.x_tags.forEach(tag => {
            if (!this.indices.byTag.has(tag)) {
              this.indices.byTag.set(tag, []);
            }
            this.indices.byTag.get(tag).push({ doc, entry });
          });
        }
      });
    });
  }

  query() {
    return new NALTQuery(this);
  }

  // Complex query example: Find related entry chains
  findRelationChains(startEntryId, maxDepth = 3) {
    const chains = [];
    const visited = new Set();
    
    const traverse = (entryId, chain, depth) => {
      if (depth > maxDepth || visited.has(entryId)) return;
      visited.add(entryId);
      
      // Find entry across all documents
      for (const doc of this.documents) {
        const entry = doc.entries.find(e => e.entry_id === entryId);
        if (entry) {
          chain.push({ entry, document_id: doc.document_id });
          
          if (entry.x_relations) {
            entry.x_relations.forEach(relation => {
              traverse(relation.target_id, [...chain], depth + 1);
            });
          } else {
            chains.push(chain);
          }
          break;
        }
      }
    };
    
    traverse(startEntryId, [], 0);
    return chains;
  }

  // Mood progression analysis
  analyzeMoodProgression(moodType, dateRange) {
    const progression = [];
    
    for (const [date, doc] of this.indices.byDate) {
      if (dateRange && (date < dateRange.from || date > dateRange.to)) {
        continue;
      }
      
      // v1.2.0: Check for moods in extension field
      const moodEntries = doc.entries.filter(entry => 
        entry.x_moods?.some(mood => mood.type === moodType)
      );
      
      if (moodEntries.length > 0) {
        const avgIntensity = moodEntries.reduce((sum, entry) => {
          const mood = entry.x_moods.find(m => m.type === moodType);
          return sum + (mood?.intensity || 0);
        }, 0) / moodEntries.length;
        
        progression.push({
          date,
          intensity: avgIntensity,
          count: moodEntries.length
        });
      }
    }
    
    return progression.sort((a, b) => a.date.localeCompare(b.date));
  }
}

class NALTQuery {
  constructor(engine) {
    this.engine = engine;
    this.filters = [];
  }

  whereType(type) {
    this.filters.push(result => result.entry.type === type);
    return this;
  }

  whereMood(moodType, minIntensity = 0) {
    this.filters.push(result => 
      result.entry.x_moods?.some(mood => 
        mood.type === moodType && mood.intensity >= minIntensity
      )
    );
    return this;
  }

  whereTag(tag) {
    this.filters.push(result => result.entry.x_tags?.includes(tag));
    return this;
  }

  whereDateBetween(from, to) {
    this.filters.push(result => 
      result.doc.date >= from && result.doc.date <= to
    );
    return this;
  }

  whereContent(searchText) {
    const lower = searchText.toLowerCase();
    this.filters.push(result => 
      result.entry.content.toLowerCase().includes(lower) ||
      result.entry.x_summary?.toLowerCase().includes(lower)
    );
    return this;
  }

  execute() {
    const results = [];
    
    this.engine.documents.forEach(doc => {
      doc.entries.forEach(entry => {
        const result = { doc, entry };
        
        if (this.filters.every(filter => filter(result))) {
          results.push(result);
        }
      });
    });
    
    return results;
  }
}
```

### 8.3 AI Processing Integration

```javascript
class NALTAIProcessor {
  constructor(aiService) {
    this.aiService = aiService;
  }

  async processDocument(document) {
    const processed = { ...document };
    
    // Process entries in parallel batches
    const batchSize = 5;
    for (let i = 0; i < processed.entries.length; i += batchSize) {
      const batch = processed.entries.slice(i, i + batchSize);
      
      await Promise.all(batch.map(async (entry, index) => {
        const actualIndex = i + index;
        
        // v1.2.0: AI enrichments should be stored as extension fields
        // Generate summary if needed
        if (!entry.x_summary) {
          processed.entries[actualIndex].x_summary = 
            await this.generateSummary(entry.content);
        }
        
        // Extract entities
        if (!entry.x_entities) {
          processed.entries[actualIndex].x_entities = 
            await this.extractEntities(entry.content);
        }
        
        // Detect moods if needed
        if (!entry.x_moods || entry.x_moods.length === 0) {
          processed.entries[actualIndex].x_moods = 
            await this.detectMoods(entry.content);
        }
        
        // Generate tags
        if (!entry.x_tags || entry.x_tags.length === 0) {
          processed.entries[actualIndex].x_tags = 
            await this.generateTags(entry);
        }
      }));
    }
    
    // Analyze relationships
    processed.entries = await this.analyzeRelationships(processed.entries);
    
    // Add processing metadata
    processed.x_ai_processing = {
      processor_version: '1.0.0',
      processed_at: new Date().toISOString(),
      model: this.aiService.getModelInfo()
    };
    
    return processed;
  }

  async generateSummary(content) {
    const response = await this.aiService.complete({
      prompt: `Summarize the following diary entry in 140 characters or less: ${content}`,
      maxTokens: 50
    });
    
    return response.text.trim();
  }

  async extractEntities(content) {
    const response = await this.aiService.complete({
      prompt: `Extract entities from this text. Return JSON with arrays for: people, locations, organizations.\n\nText: ${content}`,
      format: 'json'
    });
    
    const entities = JSON.parse(response.text);
    
    // Filter out empty arrays
    Object.keys(entities).forEach(key => {
      if (!entities[key] || entities[key].length === 0) {
        delete entities[key];
      }
    });
    
    // v1.2.0: Return as extension field structure
    return Object.keys(entities).length > 0 ? entities : undefined;
  }

  async detectMoods(content) {
    // v1.2.0: Mood types can be application-defined when using extensions
    const validMoodTypes = [
      // Positive moods
      'happy', 'excited', 'peaceful', 'content', 'grateful', 
      'calm', 'hopeful', 'proud', 'motivated',
      // Negative moods
      'sad', 'angry', 'anxious', 'frustrated', 'tired', 
      'confused', 'lonely',
      // Neutral moods
      'neutral', 'curious', 'nostalgic', 'surprised'
    ];
    
    const response = await this.aiService.complete({
      prompt: `Analyze the emotional content of this diary entry. Return JSON array of moods with type (must be one of: ${validMoodTypes.join(', ')}) and intensity (0-1).\n\nText: ${content}`,
      format: 'json'
    });
    
    const moods = JSON.parse(response.text);
    
    // Validate and ensure proper mood types and intensity values
    return moods
      .filter(mood => validMoodTypes.includes(mood.type))
      .map(mood => ({
        type: mood.type,
        intensity: Math.round(Math.max(0, Math.min(1, mood.intensity)) * 100) / 100
      }));
  }

  async generateTags(entry) {
    const context = {
      type: entry.type,
      content: entry.content,
      moods: entry.x_moods?.map(m => m.type).join(', ')
    };
    
    const response = await this.aiService.complete({
      prompt: `Generate 1-6 relevant tags for this diary entry. Return as JSON array of snake_case strings.\n\nContext: ${JSON.stringify(context)}`,
      format: 'json'
    });
    
    const tags = JSON.parse(response.text);
    
    // v1.2.0: Return tags for x_tags extension field
    return tags
      .slice(0, 6)
      .map(tag => tag.toLowerCase().replace(/\s+/g, '_'));
  }

  async analyzeRelationships(entries) {
    if (entries.length < 2) return entries;
    
    // Analyze pairs of entries for relationships
    const updatedEntries = [...entries];
    
    for (let i = 0; i < entries.length - 1; i++) {
      for (let j = i + 1; j < Math.min(i + 5, entries.length); j++) {
        const relation = await this.detectRelation(entries[i], entries[j]);
        
        if (relation) {
          // v1.2.0: x_relations is an extension field
          if (!updatedEntries[i].x_relations) {
            updatedEntries[i].x_relations = [];
          }
          
          updatedEntries[i].x_relations.push({
            type: relation,
            target_id: entries[j].entry_id
          });
        }
      }
    }
    
    return updatedEntries;
  }

  async detectRelation(entry1, entry2) {
    const response = await this.aiService.complete({
      prompt: `Analyze if these diary entries have a relationship. Return one of: caused_by, led_to, related_to, explains, contradicts, or null.

Entry 1: ${entry1.content}
Entry 2: ${entry2.content}`,
      format: 'json'
    });
    
    const result = JSON.parse(response.text);
    return result && result !== 'null' ? result : null;
  }
}
```

## 9. Testing and Quality Assurance

### 9.1 Comprehensive Test Suite

```javascript
class NALTTestSuite {
  constructor() {
    this.tests = [];
    this.results = [];
  }

  addTest(name, testFn) {
    this.tests.push({ name, testFn });
  }

  async runAll() {
    this.results = [];
    
    for (const test of this.tests) {
      try {
        await test.testFn();
        this.results.push({ name: test.name, passed: true });
      } catch (error) {
        this.results.push({ 
          name: test.name, 
          passed: false, 
          error: error.message 
        });
      }
    }
    
    return this.results;
  }

  // Core validation tests
  setupValidationTests() {
    this.addTest('Valid minimal document', async () => {
      const doc = {
        spec_version: 'nalt-protocol/1.2.0',
        document_id: '550e8400-e29b-41d4-a716-446655440000',
        date: '2025-01-15',
        meta: {
          language: 'en',
          timezone: 'UTC'
        },
        entries: [{
          entry_id: 'test-1',
          type: 'event',
          mode: 'morning',
          content_format: 'text/plain',
          content: 'Test content'
        }]
      };
      
      const validator = new NALTValidator();
      const result = validator.validate(doc);
      
      if (!result.valid) {
        throw new Error(`Validation failed: ${JSON.stringify(result.errors)}`);
      }
    });

    this.addTest('Invalid document - missing required field', async () => {
      const doc = {
        spec_version: 'nalt-protocol/1.2.0',
        // Missing document_id
        date: '2025-01-15',
        meta: {
          language: 'en',
          timezone: 'UTC'
        },
        entries: []
      };
      
      const validator = new NALTValidator();
      const result = validator.validate(doc);
      
      if (result.valid) {
        throw new Error('Should have failed validation');
      }
    });

    // v1.2.0: Mood testing moved to extension field validation
    this.addTest('Extension field validation', async () => {
      const entry = {
        entry_id: 'test-1',
        type: 'reflection',
        mode: 'evening',
        content_format: 'text/plain',
        content: 'Feeling good',
        x_moods: [
          { type: 'happy', intensity: 0.85 },
          { type: 'calm', intensity: 0.5 }
        ]
      };
      
      // v1.2.0: Extension fields should be preserved
      const validator = new NALTValidator();
      const doc = this.createTestDocument([entry]);
      const result = validator.validate(doc);
      
      if (!result.valid) {
        throw new Error('Document with extension fields rejected');
      }
    });
  }

  // Security tests
  setupSecurityTests() {
    this.addTest('Signature verification', async () => {
      const signer = new NALTSigner(testPrivateKey, testPublicKeyDID);
      const doc = this.createTestDocument();
      
      const signed = await signer.signDocument(doc);
      const verification = await signer.verifyDocument(signed);
      
      if (!verification.valid) {
        throw new Error('Valid signature failed verification');
      }
      
      // Tamper with document
      signed.entries[0].content = 'Tampered content';
      const tamperVerification = await signer.verifyDocument(signed);
      
      if (tamperVerification.valid) {
        throw new Error('Tampered document passed verification');
      }
    });

    this.addTest('Encryption roundtrip', async () => {
      const encryption = new NALTEncryption();
      const key = crypto.randomBytes(32);
      const doc = this.createTestDocument();
      
      const encrypted = encryption.encryptDocument(doc, key);
      const decrypted = encryption.decryptDocument(encrypted, key);
      
      // Verify structure preserved
      if (JSON.stringify(doc.entries) !== JSON.stringify(decrypted.entries)) {
        throw new Error('Encryption roundtrip failed');
      }
    });
  }

  // Performance tests
  setupPerformanceTests() {
    this.addTest('Large document validation performance', async () => {
      const entries = [];
      for (let i = 0; i < 1000; i++) {
        entries.push({
          entry_id: `entry-${i}`,
          type: 'event',
          mode: 'morning',
          content_format: 'text/plain',
          content: `Test content ${i}`.repeat(10)
        });
      }
      
      const doc = this.createTestDocument(entries);
      const validator = new NALTValidator();
      
      const start = Date.now();
      const result = validator.validate(doc);
      const duration = Date.now() - start;
      
      if (!result.valid) {
        throw new Error('Large document validation failed');
      }
      
      if (duration > 100) {
        throw new Error(`Validation too slow: ${duration}ms`);
      }
    });

    this.addTest('Indexing performance', async () => {
      const documents = [];
      for (let i = 0; i < 100; i++) {
        documents.push(this.createTestDocument(undefined, `2025-01-${String(i + 1).padStart(2, '0')}`));
      }
      
      const start = Date.now();
      const indexer = new NALTIndexer();
      
      documents.forEach(doc => indexer.indexDocument(doc));
      
      const duration = Date.now() - start;
      
      if (duration > 500) {
        throw new Error(`Indexing too slow: ${duration}ms for 100 documents`);
      }
      
      // Test search performance
      const searchStart = Date.now();
      const results = indexer.search({ text: 'test' });
      const searchDuration = Date.now() - searchStart;
      
      if (searchDuration > 10) {
        throw new Error(`Search too slow: ${searchDuration}ms`);
      }
    });
  }

  createTestDocument(entries, date = '2025-01-15') {
    return {
      spec_version: 'nalt-protocol/1.2.0',
      document_id: this.generateUUID(),
      date,
      meta: {
        language: 'en',
        timezone: 'UTC'
      },
      entries: entries || [{
        entry_id: 'test-entry-1',
        type: 'event',
        mode: 'morning',
        content_format: 'text/plain',
        content: 'Test content'
      }]
    };
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

// Run tests
const suite = new NALTTestSuite();
suite.setupValidationTests();
suite.setupSecurityTests();
suite.setupPerformanceTests();

suite.runAll().then(results => {
  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;
  
  console.log(`Tests: ${passed} passed, ${failed} failed`);
  
  results.filter(r => !r.passed).forEach(result => {
    console.error(`FAILED: ${result.name}`);
    console.error(`  Error: ${result.error}`);
  });
});
```

## 10. Error Handling and Edge Cases

### 10.1 Comprehensive Error Handler

```javascript
class NALTErrorHandler {
  constructor() {
    this.errorTypes = {
      VALIDATION_ERROR: 'ValidationError',
      PARSE_ERROR: 'ParseError',
      MIGRATION_ERROR: 'MigrationError',
      SECURITY_ERROR: 'SecurityError',
      STORAGE_ERROR: 'StorageError',
      PROCESSING_ERROR: 'ProcessingError'
    };
  }

  handle(error, context = {}) {
    const errorInfo = this.categorizeError(error);
    const recovery = this.suggestRecovery(errorInfo, context);
    
    return {
      type: errorInfo.type,
      message: errorInfo.message,
      details: errorInfo.details,
      recovery: recovery,
      context: context
    };
  }

  categorizeError(error) {
    if (error.message.includes('validation') || error.message.includes('schema')) {
      return {
        type: this.errorTypes.VALIDATION_ERROR,
        message: 'Document validation failed',
        details: this.extractValidationDetails(error)
      };
    }
    
    if (error.message.includes('JSON') || error instanceof SyntaxError) {
      return {
        type: this.errorTypes.PARSE_ERROR,
        message: 'Failed to parse JSON',
        details: {
          position: error.position,
          line: error.line,
          column: error.column
        }
      };
    }
    
    if (error.message.includes('signature') || error.message.includes('encryption')) {
      return {
        type: this.errorTypes.SECURITY_ERROR,
        message: 'Security operation failed',
        details: {
          operation: error.operation,
          reason: error.reason
        }
      };
    }
    
    return {
      type: this.errorTypes.PROCESSING_ERROR,
      message: error.message,
      details: {}
    };
  }

  extractValidationDetails(error) {
    if (error.errors && Array.isArray(error.errors)) {
      return {
        errors: error.errors.map(e => ({
          path: e.instancePath || e.path,
          message: e.message,
          params: e.params
        }))
      };
    }
    
    return { rawError: error.message };
  }

  suggestRecovery(errorInfo, context) {
    const suggestions = [];
    
    switch (errorInfo.type) {
      case this.errorTypes.VALIDATION_ERROR:
        suggestions.push(...this.getValidationRecoverySuggestions(errorInfo.details));
        break;
        
      case this.errorTypes.PARSE_ERROR:
        suggestions.push(
          'Check JSON syntax using a JSON validator',
          'Ensure proper escaping of special characters',
          'Verify file encoding is UTF-8'
        );
        break;
        
      case this.errorTypes.SECURITY_ERROR:
        suggestions.push(
          'Verify signature algorithm is supported',
          'Check key format and validity',
          'Ensure encryption keys match'
        );
        break;
    }
    
    return suggestions;
  }

  getValidationRecoverySuggestions(details) {
    const suggestions = [];
    
    if (details.errors) {
      details.errors.forEach(error => {
        if (error.message.includes('required')) {
          suggestions.push(`Add missing required field: ${error.path}`);
        }
        
        if (error.message.includes('enum')) {
          suggestions.push(`Use one of the allowed values for ${error.path}`);
        }
        
        if (error.message.includes('format')) {
          suggestions.push(`Check format of ${error.path} (e.g., date format, UUID)`);
        }
      });
    }
    
    return suggestions;
  }

  // Edge case handlers
  handleCorruptedDocument(document) {
    const repaired = { ...document };
    const issues = [];
    
    // Fix missing required fields
    if (!repaired.spec_version) {
      repaired.spec_version = 'nalt-protocol/1.1.0';
      issues.push('Added missing spec_version');
    }
    
    if (!repaired.document_id) {
      repaired.document_id = this.generateUUID();
      issues.push('Generated missing document_id');
    }
    
    if (!repaired.entries || !Array.isArray(repaired.entries)) {
      repaired.entries = [];
      issues.push('Fixed invalid entries array');
    }
    
    // Fix entry issues
    repaired.entries = repaired.entries.map((entry, index) => {
      const fixedEntry = { ...entry };
      
      if (!fixedEntry.entry_id) {
        fixedEntry.entry_id = `repaired-${index}-${Date.now()}`;
        issues.push(`Generated entry_id for entry ${index}`);
      }
      
      if (!fixedEntry.content_format || !this.isValidContentFormat(fixedEntry.content_format)) {
        fixedEntry.content_format = 'text/plain';
        issues.push(`Fixed content_format for entry ${fixedEntry.entry_id}`);
      }
      
      return fixedEntry;
    });
    
    return { repaired, issues };
  }

  isValidContentFormat(format) {
    const valid = ['text/plain', 'text/markdown', 'text/html', 'application/json', 'text/org'];
    return valid.includes(format);
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

// Usage example
const errorHandler = new NALTErrorHandler();

try {
  // Some operation that might fail
  const document = JSON.parse(invalidJSON);
  validator.validate(document);
} catch (error) {
  const handled = errorHandler.handle(error, {
    operation: 'document_validation',
    file: 'user_data.json'
  });
  
  console.error('Error:', handled.message);
  console.error('Type:', handled.type);
  console.error('Recovery suggestions:');
  handled.recovery.forEach(suggestion => {
    console.error(`  - ${suggestion}`);
  });
}
```

### 10.2 Edge Case Scenarios

```javascript
class NALTEdgeCaseHandler {
  // Handle extremely large entries
  handleLargeEntry(entry, maxSize = 10000) {
    if (entry.content.length <= maxSize) {
      return [entry];
    }
    
    const chunks = [];
    let remaining = entry.content;
    let chunkIndex = 0;
    
    while (remaining.length > 0) {
      const chunk = remaining.substring(0, maxSize);
      const lastSpace = chunk.lastIndexOf(' ');
      const cutPoint = lastSpace > maxSize * 0.8 ? lastSpace : maxSize;
      
      chunks.push({
        ...entry,
        entry_id: `${entry.entry_id}-chunk-${chunkIndex}`,
        content: remaining.substring(0, cutPoint).trim(),
        x_chunked: {
          original_id: entry.entry_id,
          chunk: chunkIndex,
          total_size: entry.content.length
        }
      });
      
      remaining = remaining.substring(cutPoint).trim();
      chunkIndex++;
    }
    
    return chunks;
  }

  // Handle circular references
  detectCircularReferences(entries) {
    const issues = [];
    
    entries.forEach(entry => {
      if (entry.x_relations) {
        const visited = new Set();
        const recursionStack = new Set();
        
        const hasCycle = this.dfsDetectCycle(
          entry.entry_id,
          entries,
          visited,
          recursionStack
        );
        
        if (hasCycle) {
          issues.push({
            entry_id: entry.entry_id,
            issue: 'Circular reference detected',
            severity: 'warning'
          });
        }
      }
    });
    
    return issues;
  }

  dfsDetectCycle(entryId, entries, visited, recursionStack) {
    visited.add(entryId);
    recursionStack.add(entryId);
    
    const entry = entries.find(e => e.entry_id === entryId);
    if (entry?.x_relations) {
      for (const relation of entry.x_relations) {
        if (!visited.has(relation.target_id)) {
          if (this.dfsDetectCycle(relation.target_id, entries, visited, recursionStack)) {
            return true;
          }
        } else if (recursionStack.has(relation.target_id)) {
          return true;
        }
      }
    }
    
    recursionStack.delete(entryId);
    return false;
  }

  // Handle date inconsistencies
  validateDateConsistency(document) {
    const issues = [];
    
    // Check if end_date is before date
    if (document.end_date && document.end_date < document.date) {
      issues.push({
        field: 'end_date',
        issue: 'end_date is before document date',
        severity: 'error'
      });
    }
    
    // Check entry dates against document date
    document.entries.forEach(entry => {
      if (entry.x_due_date && entry.x_due_date < document.date) {
        issues.push({
          entry_id: entry.entry_id,
          field: 'x_due_date',
          issue: 'Due date is in the past relative to document date',
          severity: 'warning'
        });
      }
    });
    
    return issues;
  }

  // Handle encoding issues
  sanitizeContent(content) {
    // Remove null bytes
    let sanitized = content.replace(/\0/g, '');
    
    // Fix common encoding issues
    const replacements = {
      '\u2018': "'", // Left single quote
      '\u2019': "'", // Right single quote
      '\u201C': '"', // Left double quote
      '\u201D': '"', // Right double quote
      '\u2013': '-', // En dash
      '\u2014': '--', // Em dash
      '\u2026': '...', // Ellipsis
    };
    
    Object.entries(replacements).forEach(([from, to]) => {
      sanitized = sanitized.replace(new RegExp(from, 'g'), to);
    });
    
    // Ensure valid UTF-8
    try {
      // Encode and decode to catch invalid sequences
      sanitized = new TextDecoder('utf-8', { fatal: true })
        .decode(new TextEncoder().encode(sanitized));
    } catch (e) {
      // Fallback to removing non-ASCII if encoding fails
      sanitized = sanitized.replace(/[^\x00-\x7F]/g, '');
    }
    
    return sanitized;
  }

  // Handle merge conflicts
  mergeDocuments(doc1, doc2, strategy = 'combine') {
    if (strategy === 'combine') {
      // Combine entries from both documents
      const allEntries = [...doc1.entries, ...doc2.entries];
      
      // Remove duplicates based on entry_id
      const uniqueEntries = Array.from(
        new Map(allEntries.map(e => [e.entry_id, e])).values()
      );
      
      return {
        spec_version: doc1.spec_version,
        document_id: this.generateUUID(),
        date: doc1.date < doc2.date ? doc1.date : doc2.date,
          meta: { ...doc1.meta, ...doc2.meta },
        entries: uniqueEntries.sort((a, b) => {
          // Sort by mode order, then by entry_id
          const modeOrder = ['morning', 'afternoon', 'evening', 'night', 'none'];
          const modeCompare = modeOrder.indexOf(a.mode) - modeOrder.indexOf(b.mode);
          return modeCompare !== 0 ? modeCompare : a.entry_id.localeCompare(b.entry_id);
        }),
        x_merged_from: [doc1.document_id, doc2.document_id]
      };
    }
    
    // Other strategies can be implemented
    throw new Error(`Unknown merge strategy: ${strategy}`);
  }

  generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}
```

## Appendix: Complete Implementation Checklist

When implementing NALT Protocol support, ensure:

### Required Features
- [ ] Full v1.1.1 schema validation
- [ ] UTF-8 encoding support
- [ ] UUID generation for document_id and entry_id
- [ ] Date/timestamp handling with timezone support
- [ ] All required fields properly validated
- [ ] Extension field support (x_ prefix)

### Recommended Features
- [ ] Digital signature support (EdDSA, ES256, RS256)
- [ ] Entry segmentation for large content
- [ ] UTC offset calculation and storage
- [ ] Mood tracking (x_moods with intensity precision)
- [ ] Multi-day entry support (end_date)
- [ ] Relationship tracking between entries

### Performance Optimizations
- [ ] Indexing for fast search
- [ ] Streaming parser for large files
- [ ] Caching mechanisms
- [ ] Batch processing capabilities
- [ ] UTC offset for timezone calculations

### Security Measures
- [ ] Input validation and sanitization
- [ ] Encryption at rest support
- [ ] Access control implementation
- [ ] Audit logging
- [ ] Signature verification

### Quality Assurance
- [ ] Comprehensive test coverage
- [ ] Performance benchmarks
- [ ] Error handling for all edge cases
- [ ] Migration tools from v1.0.0 and v1.1.0
- [ ] Documentation and examples

## 11. Migration Tools

Migration tools are provided to automatically convert data from older versions of the specification to newer versions.

### 11.1 v1.1.1 to v1.2.0 Migration

**Script Location**: `tools/migration/migrate_v1.1.1_to_v1.2.0.py`

#### Usage

```bash
python tools/migration/migrate_v1.1.1_to_v1.2.0.py <json_filename>
```

#### Example

```bash
python tools/migration/migrate_v1.1.1_to_v1.2.0.py old_data.json
# Output: migrated_old_data.json will be created
```

#### Migration Actions

The v1.1.1 to v1.2.0 migration script performs the following operations:

1. **Field Migration**: Moves all removed fields to extension fields with `x_` prefix:
   - `signature` → `x_signature`
   - `meta.x_utc_offset_minutes` → document-level `x_utc_offset_minutes`
   - Entry fields: `summary` → `x_summary`, `moods` → `x_moods`, `tags` → `x_tags`, `entities` → `x_entities`, `end_date` → `x_end_date`, `created_at` → `x_created_at`
   - `x_relations` and `x_due_date` remain as extension fields
2. **Version Update**: Updates `spec_version` to `nalt-protocol/1.2.0`
3. **Migration Metadata**: Adds `x_migrated_at` field with the migration timestamp

#### Implementation Details

```python
def migrate_document(old_doc):
    """
    Migrate a NALT Protocol document from v1.1.1 to v1.2.0.
    """
    new_doc = old_doc.copy()
    
    # Migrate top-level fields
    if 'signature' in new_doc:
        new_doc['x_signature'] = new_doc.pop('signature')
    
    # Migrate meta fields
    if 'x_utc_offset_minutes' in new_doc.get('meta', {}):
        new_doc['x_utc_offset_minutes'] = new_doc['meta'].pop('x_utc_offset_minutes')
    
    # Migrate each entry
    entries = new_doc.get('entries', [])
    new_doc['entries'] = [migrate_entry(entry) for entry in entries]

    # Update version and add migration metadata
    new_doc['spec_version'] = 'nalt-protocol/1.2.0'
    new_doc['x_migrated_at'] = datetime.utcnow().isoformat() + 'Z'

    return new_doc

def migrate_entry(entry):
    """Migrate entry fields to v1.2.0 extension format."""
    new_entry = entry.copy()
    
    # Migrate removed fields to x_ extensions
    field_mappings = {
        'summary': 'x_summary',
        'moods': 'x_moods',
        'tags': 'x_tags',
        'entities': 'x_entities',
        'end_date': 'x_end_date',
        'created_at': 'x_created_at'
    }
    
    for old_field, new_field in field_mappings.items():
        if old_field in new_entry:
            new_entry[new_field] = new_entry.pop(old_field)
    
    return new_entry
```

### 11.2 Batch Migration

For migrating multiple files, you can use shell scripting:

```bash
# Migrate all JSON files in current directory
for file in *.json; do
    python tools/migration/migrate_v1.1.1_to_v1.2.0.py "$file"
done
```

### 11.3 Validation After Migration

Always validate migrated files against the new schema:

```bash
# Using Python validator
python tools/validator/python/validator.py migrated_old_data.json --version v1.2.0

# Using Node.js validator
node tools/validator/nodejs/validator.js migrated_old_data.json --version v1.2.0
```

This completes the comprehensive AI documentation for NALT Protocol v1.2.0 (slim-core release). All technical details, implementation patterns, and best practices are included for AI systems to effectively work with the protocol.

## Key v1.2.0 Changes Summary

1. **Slim-Core Design**: Only essential fields remain in the core specification
2. **Removed Fields**: All non-essential fields moved to extension fields:
   - Top-level: `signature` → `x_signature`
   - Meta: `x_utc_offset_minutes` → document-level extension
   - Entry: `summary`, `moods`, `tags`, `entities`, `end_date`, `created_at` → `x_` prefixed extensions
3. **Extension Philosophy**: Applications can implement any removed functionality as extension fields
4. **Backward Compatibility**: Migration tools provided to convert v1.1.1 documents to v1.2.0 format

## Handling Legacy Fields in v1.2.0

When working with v1.2.0, applications should:

1. **Reading Documents**: Check for both legacy field names and new extension field names
2. **Writing Documents**: Always use the new `x_` prefixed extension fields
3. **Migration**: Use the provided migration tools to convert legacy documents

```javascript
// Example: Reading mood data that might be in old or new format
function getMoods(entry) {
  return entry.x_moods || entry.moods || [];
}

// Example: Writing mood data in v1.2.0 format
function setMoods(entry, moods) {
  entry.x_moods = moods;
  // Do not set entry.moods in v1.2.0
}

// Example: Handling all removed fields
function migrateEntry(entry) {
  const fieldMappings = {
    'summary': 'x_summary',
    'moods': 'x_moods',
    'tags': 'x_tags',
    'entities': 'x_entities',
    'end_date': 'x_end_date',
    'created_at': 'x_created_at'
  };
  
  Object.entries(fieldMappings).forEach(([old, new_]) => {
    if (entry[old] !== undefined && entry[new_] === undefined) {
      entry[new_] = entry[old];
      delete entry[old];
    }
  });
  
  return entry;
}
```