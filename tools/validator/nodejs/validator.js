const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

function validateNALTProtocol(filePath, version = 'v1.2.0', checkWarnings = true) {
  const schemaPath = path.join(__dirname, `../../../schema/${version}/schema.json`);

  let schema, instance;

  try {
    schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'));
  } catch (err) {
    console.error(`❌ Error: Could not read or parse schema file at ${schemaPath}`);
    process.exit(1);
  }

  try {
    instance = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    console.error(`❌ Error: Could not read or parse data file at ${filePath}`);
    process.exit(1);
  }

  const ajv = new Ajv();
  addFormats(ajv);

  const validate = ajv.compile(schema);
  const valid = validate(instance);

  if (valid) {
    console.log(`✅ Validation successful: '${filePath}' conforms to NALT Protocol ${version}.`);
    
    // Check for strongly recommended fields (only for older versions)
    if (checkWarnings && ['v1.1.0', 'v1.1.1'].includes(version)) {
      const warnings = checkStronglyRecommendedFields(instance);
      warnings.forEach(warning => {
        console.log(`⚠️  Warning: ${warning}`);
      });
    }
  } else {
    console.error(`❌ Validation failed: '${filePath}' does not conform to the schema.`);
    console.error("Error details:", validate.errors);
    process.exit(1);
  }
}

function checkStronglyRecommendedFields(data) {
  const warnings = [];
  
  // Check mood intensity precision
  if (data.entries) {
    data.entries.forEach((entry, index) => {
      if (entry.moods) {
        entry.moods.forEach(mood => {
          if (mood.intensity && mood.intensity !== Math.round(mood.intensity * 100) / 100) {
            warnings.push(`Mood intensity should use 0.01 precision (entry ${index})`);
          }
        });
      }
    });
  }
  
  // Check for valid mood types (v1.1.0 enforces 20 predefined types)
  const validMoods = new Set([
    // Positive moods
    'happy', 'excited', 'peaceful', 'content', 'grateful', 
    'calm', 'hopeful', 'proud', 'motivated',
    // Negative moods
    'sad', 'angry', 'anxious', 'frustrated', 'tired', 
    'confused', 'lonely',
    // Neutral moods
    'neutral', 'curious', 'nostalgic', 'surprised'
  ]);
  if (data.entries) {
    let invalidMoodFound = false;
    data.entries.forEach(entry => {
      if (entry.moods && !invalidMoodFound) {
        entry.moods.forEach(mood => {
          if (mood.type && !validMoods.has(mood.type)) {
            warnings.push(`Mood type '${mood.type}' is not in the list of 20 predefined mood types`);
            invalidMoodFound = true;
          }
        });
      }
    });
  }
  
  // Check date consistency
  if (data.end_date && data.date) {
    const startDate = new Date(data.date);
    const endDate = new Date(data.end_date);
    if (endDate < startDate) {
      warnings.push('end_date must be greater than or equal to date');
    }
  }
  
  return warnings;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  
  // Parse command line arguments
  let filePath, version = 'v1.2.0', checkWarnings = true;
  
  if (args.length === 0 || args.includes('--help')) {
    console.log('Usage: node validator.js <path_to_json_file> [options]');
    console.log('Options:');
    console.log('  --version <version>  Schema version (default: v1.2.0)');
    console.log('  --no-warnings        Disable strongly recommended field warnings');
    process.exit(args.length === 0 ? 1 : 0);
  }
  
  filePath = args[0];
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--version' && i + 1 < args.length) {
      version = args[++i];
    } else if (args[i] === '--no-warnings') {
      checkWarnings = false;
    }
  }
  
  validateNALTProtocol(filePath, version, checkWarnings);
}