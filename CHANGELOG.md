# Changelog

All notable changes to the NALT Protocol will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-23

### Changed
- **BREAKING**: Introduced slim-core specification by removing all non-essential fields
- Updated default schema version to v1.2.0 in validators

### Removed
- **BREAKING**: Removed `signature` field from top-level object
- **BREAKING**: Removed `x_utc_offset_minutes` from meta object
- **BREAKING**: Removed `summary`, `moods`, `tags`, `entities`, `end_date`, `created_at` fields from entries
- **BREAKING**: Removed `x_relations`, `x_due_date` extension fields from specification

### Added
- Migration tool for v1.1.1 to v1.2.0 conversion
- Migration documentation guide
- New v1.2.0 examples (minimal and full)

## [1.1.1] - 2025-07-21

### Changed
- Clarified that `mode` represents when the event occurred, not when recorded

### Removed
- Removed top-level `timestamp` field

### Added
- Optional `created_at` field for entries to track recording time

## [1.1.0] - 2025-07-10

### Added
- Required `document_id` field (was recommended in v1.0.0)
- `end_date` field for multi-day entries
- Digital signature support with `signature` object
- `x_utc_offset_minutes` field for timezone calculation optimization
- 20 predefined mood types with descriptions
- 0.01 precision requirement for mood intensity values

### Changed
- `content_format` now requires standard MIME types (e.g., `text/plain` instead of `plain_text`)
- Limited `content_format` to five supported types

## [1.0.0] - 2025-07-09

### Added
- Initial public release of NALT Protocol
- Core specification for personal diary data in AI-interpretable format
- Support for five entry types: event, reflection, task, idea, log
- Time-based entry modes: morning, afternoon, evening, night, none
- Extensible entity extraction system
- Relationship tracking between entries
- Multi-language and timezone support