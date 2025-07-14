# Security Best Practices for NALT Protocol

This guide provides security recommendations for implementing and using NALT Protocol v1.1.0.

## 1. Data Classification and Sensitivity Levels

### Classify Your Data
Before storing personal data, classify it by sensitivity:

- **Public**: Data that can be freely shared (e.g., published thoughts, public events)
- **Private**: Personal reflections and experiences
- **Sensitive**: Health data, financial information, intimate thoughts
- **Critical**: Authentication credentials, encryption keys

### Recommendation
```json
{
  "entries": [
    {
      "x_sensitivity_level": "private",
      "x_access_control": ["self", "trusted_family"],
      // ... other fields
    }
  ]
}
```

## 2. Digital Signatures (v1.1.0 Feature)

### Why Sign Your Data?
- **Integrity**: Ensures data hasn't been tampered with
- **Authenticity**: Proves the data came from you
- **Non-repudiation**: Creates an audit trail

### Implementation with DID and JWS

```javascript
// Example using Ed25519 signatures
const { Ed25519VerificationKey2020 } = require('@digitalbazaar/ed25519-verification-key-2020');
const { sign } = require('@digitalbazaar/ed25519-signature-2020');

async function signNALTDocument(document, privateKey) {
  // Create canonical representation
  const payload = {
    document_id: document.document_id,
    date: document.date,
    timestamp: document.timestamp,
    entries_hash: await hashEntries(document.entries)
  };
  
  // Sign with EdDSA
  const signature = await sign({
    data: payload,
    privateKey: privateKey
  });
  
  return {
    ...document,
    signature: {
      alg: "EdDSA",
      sig: signature,
      public_key: privateKey.publicKeyDid
    }
  };
}
```

## 3. Encryption at Rest

### Encrypt Sensitive Entries
```javascript
// Example: Encrypting individual entries
const crypto = require('crypto');

function encryptEntry(entry, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  const encrypted = Buffer.concat([
    cipher.update(JSON.stringify(entry), 'utf8'),
    cipher.final()
  ]);
  
  return {
    entry_id: entry.entry_id,
    type: "encrypted",
    encrypted_data: encrypted.toString('base64'),
    iv: iv.toString('base64'),
    auth_tag: cipher.getAuthTag().toString('base64')
  };
}
```

## 4. Access Control

### Implement Fine-Grained Permissions
```json
{
  "x_access_policy": {
    "default": "deny",
    "rules": [
      {
        "subject": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
        "actions": ["read"],
        "conditions": {
          "date_range": {
            "from": "2025-01-01",
            "to": "2025-12-31"
          }
        }
      }
    ]
  }
}
```

## 5. Secure Storage

### Storage Recommendations

1. **Local Storage**
   - Use encrypted filesystems (FileVault, BitLocker, LUKS)
   - Set appropriate file permissions (600 for private data)
   - Regular encrypted backups

2. **Cloud Storage**
   - Client-side encryption before upload
   - Use zero-knowledge storage providers
   - Enable MFA on cloud accounts

3. **Database Storage**
   - Enable encryption at rest
   - Use row-level security
   - Audit all access

## 6. Data Minimization

### Only Store What's Necessary
- Avoid storing PII in entries when possible
- Use references instead of duplicating sensitive data
- Regularly review and purge old data

```json
{
  "entries": [
    {
      // Bad: Storing full credit card
      "content": "Bought coffee with card 1234-5678-9012-3456",
      
      // Good: Using references
      "content": "Bought coffee with personal card",
      "x_payment_ref": "card_001"
    }
  ]
}
```

## 7. Secure Transmission

### API Security
When building APIs for NALT Protocol data:

```javascript
// Example: Secure API endpoint
app.post('/api/pdp/documents', 
  authenticateJWT,
  validateSignature,
  rateLimiter,
  async (req, res) => {
    // Verify document ownership
    if (req.body.signature.public_key !== req.user.did) {
      return res.status(403).json({ error: 'Unauthorized' });
    }
    
    // Validate against schema
    const isValid = await validateNALT(req.body);
    if (!isValid) {
      return res.status(400).json({ error: 'Invalid NALT Protocol format' });
    }
    
    // Store securely
    await secureStore(req.body);
    res.status(201).json({ success: true });
  }
);
```

## 8. Privacy-Preserving Analytics

### Analyze Without Exposing Raw Data
```javascript
// Example: Privacy-preserving mood analytics
function analyzeMoods(entries) {
  // Aggregate without exposing individual entries
  const moodCounts = {};
  const moodIntensities = {};
  
  entries.forEach(entry => {
    if (entry.moods) {
      entry.moods.forEach(mood => {
        // Count frequencies
        moodCounts[mood.type] = (moodCounts[mood.type] || 0) + 1;
        
        // Average intensities (not individual values)
        if (!moodIntensities[mood.type]) {
          moodIntensities[mood.type] = [];
        }
        moodIntensities[mood.type].push(mood.intensity);
      });
    }
  });
  
  // Return only aggregated data
  return {
    mood_frequencies: moodCounts,
    average_intensities: Object.fromEntries(
      Object.entries(moodIntensities).map(([type, values]) => [
        type, 
        (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2)
      ])
    )
  };
}
```

## 9. Audit Logging

### Track All Access
```json
{
  "x_audit_log": [
    {
      "timestamp": "2025-07-10T10:30:00Z",
      "action": "read",
      "subject": "did:key:z6Mk...",
      "ip": "192.168.1.100",
      "user_agent": "NALT-Client/1.0"
    }
  ]
}
```

## 10. Regular Security Reviews

### Security Checklist
- [ ] All sensitive data is encrypted at rest
- [ ] Signatures are verified on data import
- [ ] Access logs are reviewed monthly
- [ ] Encryption keys are rotated annually
- [ ] Backups are tested for recovery
- [ ] Dependencies are updated regularly
- [ ] Security patches are applied promptly

## 11. Incident Response

### Data Breach Protocol
1. **Detect**: Monitor for unauthorized access
2. **Contain**: Revoke compromised credentials
3. **Assess**: Determine scope of breach
4. **Notify**: Inform affected users within 72 hours
5. **Review**: Update security measures

## 12. Compliance Considerations

### GDPR and Privacy Laws
- Implement right to deletion (forget)
- Provide data portability
- Obtain explicit consent
- Maintain processing records

```javascript
// Example: GDPR-compliant deletion
async function deleteUserData(userId) {
  // Delete all NALT Protocol documents
  await deleteNALTDocuments(userId);
  
  // Delete from backups (mark for deletion)
  await markBackupsForDeletion(userId);
  
  // Log the deletion
  await auditLog({
    action: 'gdpr_deletion',
    user_id: userId,
    timestamp: new Date().toISOString()
  });
  
  return { deleted: true, timestamp: new Date().toISOString() };
}
```

## Additional Resources

- [W3C DID Specification](https://www.w3.org/TR/did-core/)
- [JSON Web Signature (JWS) RFC 7515](https://tools.ietf.org/html/rfc7515)
- [OWASP Application Security Guide](https://owasp.org/www-project-application-security-verification-standard/)

Remember: Security is not a one-time implementation but an ongoing process. Regular reviews and updates are essential for maintaining the security of personal data.