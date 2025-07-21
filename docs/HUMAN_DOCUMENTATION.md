# NALT Protocol - Human Documentation

## What is NALT Protocol?

NALT Protocol is an open standard for preserving your personal digital diary in a format that future AI systems can understand and work with. Think of it as a time capsule for your thoughts, experiences, and personality that remains meaningful and accessible as technology evolves.

## Quick Start

### Creating Your First NALT Document

Here's the simplest possible NALT document:

```json
{
  "spec_version": "nalt-protocol/1.1.1",
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "date": "2025-01-15",
  "meta": {
    "language": "en",
    "timezone": "America/New_York"
  },
  "entries": [
    {
      "entry_id": "morning-reflection",
      "type": "reflection",
      "mode": "morning",
      "content_format": "text/plain",
      "content": "Today I'm feeling grateful for the sunny weather and looking forward to my meeting with the team."
    }
  ]
}
```

### Understanding the Structure

Every NALT document has:
- **One day** of diary entries (the `date` field)
- **Metadata** about language and timezone
- **Multiple entries** throughout the day

Each entry captures:
- **What type** it is (event, reflection, task, idea, or log)
- **When** it happened (morning, afternoon, evening, night)
- **The content** in plain text or other formats

## Entry Types Explained

### Event
Something that actually happened:
```json
{
  "type": "event",
  "content": "Had lunch with Sarah at the new Italian restaurant"
}
```

### Reflection
Your thoughts and feelings:
```json
{
  "type": "reflection",
  "content": "Feeling overwhelmed by the project deadline but confident we can deliver"
}
```

### Task
Things you need to do:
```json
{
  "type": "task",
  "content": "Finish the quarterly report",
  "x_due_date": "2025-01-20"
}
```

### Idea
Creative thoughts and inspirations:
```json
{
  "type": "idea",
  "content": "What if we created an app that helps people practice gratitude daily?"
}
```

### Log
Routine records:
```json
{
  "type": "log",
  "content": "Slept 7 hours, woke up refreshed"
}
```

## Optional Enhancements

### Adding Moods
Track your emotional state:
```json
{
  "moods": [
    { "type": "happy", "intensity": 0.8 },
    { "type": "energetic", "intensity": 0.6 }
  ]
}
```

### Using Tags
Organize entries by topic:
```json
{
  "tags": ["work", "project_alpha", "milestone"]
}
```

### Connecting Entries
Show how thoughts and events relate:
```json
{
  "x_relations": [
    {
      "type": "caused_by",
      "target_id": "previous-entry-id"
    }
  ]
}
```

## Best Practices

### 1. One File Per Day
Create a separate JSON file for each day's entries. Name them by date:
- `2025-01-15.json`
- `2025-01-16.json`

### 2. Regular Entries
The more you write, the richer your digital diary becomes. Aim for:
- Morning reflection
- Afternoon events
- Evening summary

### 3. Be Authentic
Write naturally. The goal is to capture your genuine thoughts and experiences.

### 4. Privacy First
- Store files securely
- Consider encryption for sensitive content
- Only share with trusted systems

## Validation Tools

### Check Your Files

**Python:**
```bash
python tools/validator/python/validator.py yourfile.json
```

**Node.js:**
```bash
node tools/validator/nodejs/validator.js yourfile.json
```

## Common Questions

### Q: How detailed should my entries be?
A: Write as much or as little as feels natural. A few sentences per entry is often enough.

### Q: Can I edit past entries?
A: Yes, but consider adding new reflection entries instead to preserve your thought evolution.

### Q: What about privacy?
A: NALT files are just text - you control where they're stored and who has access.

### Q: How do I handle multi-day events?
A: Use the `end_date` field:
```json
{
  "content": "Family vacation in Hawaii",
  "end_date": "2025-01-22"
}
```

## Getting Help

- **Examples**: Check the `examples/` folder for more complete examples
- **Issues**: Report problems at the GitHub repository
- **Community**: Join discussions about personal data preservation

## Why NALT Protocol?

In an age where AI is becoming increasingly integrated into our lives, NALT Protocol ensures that your personal history, thoughts, and experiences are preserved in a way that future AI assistants can understand and use to better serve you. It's about maintaining the continuity of your digital self across time and technological change.

Start today. Your future self will thank you.