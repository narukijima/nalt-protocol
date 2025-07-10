const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

function validatePersonalProtocol(filePath) {
  const schemaPath = path.join(__dirname, '../../../schema/v1.0.0/schema.json');

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
    console.log(`✅ Validation successful: '${filePath}' conforms to Personal Protocol v1.0.0.`);
  } else {
    console.error(`❌ Validation failed: '${filePath}' does not conform to the schema.`);
    console.error("Error details:", validate.errors);
    process.exit(1);
  }
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.log("Usage: node validator.js <path_to_json_file>");
    process.exit(1);
  }
  const fileToValidate = args[0];
  validatePersonalProtocol(fileToValidate);
}