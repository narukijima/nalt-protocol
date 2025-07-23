/**
 * DID/JWS Implementation Example for NALT Protocol v1.2.0
 * 
 * This example demonstrates how to:
 * 1. Generate a DID (Decentralized Identifier)
 * 2. Sign NALT Protocol documents with JWS (JSON Web Signature)
 * 3. Verify signatures
 */

const crypto = require('crypto');
const { base64url } = require('jose');

// Example implementation - in production, use proper DID/JWS libraries
// such as @digitalbazaar/ed25519-signature-2020 or jose

class NALTSigner {
  constructor() {
    // Generate Ed25519 key pair
    const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
    this.publicKey = publicKey;
    this.privateKey = privateKey;
    
    // Generate DID from public key
    this.did = this.generateDID(publicKey);
  }
  
  /**
   * Generate a DID:key from an Ed25519 public key
   */
  generateDID(publicKey) {
    // Export public key in raw format
    const publicKeyBytes = publicKey.export({ type: 'spki', format: 'der' });
    
    // Extract the raw Ed25519 public key (last 32 bytes)
    const ed25519PublicKey = publicKeyBytes.slice(-32);
    
    // Multicodec prefix for Ed25519 public key (0xed)
    const multicodec = Buffer.from([0xed, 0x01]);
    
    // Combine multicodec and public key
    const multikey = Buffer.concat([multicodec, ed25519PublicKey]);
    
    // Base58 encode (simplified - use proper base58 library in production)
    const base58 = this.base58Encode(multikey);
    
    return `did:key:z${base58}`;
  }
  
  /**
   * Sign a NALT Protocol document
   */
  async signDocument(naltDocument) {
    // Create JWS header
    const header = {
      alg: 'EdDSA',
      typ: 'JWT',
      kid: this.did
    };
    
    // Create payload with essential fields
    const payload = {
      document_id: naltDocument.document_id,
      date: naltDocument.date,
      // Create a hash of entries for integrity
      entries_hash: this.hashEntries(naltDocument.entries)
    };
    
    // Encode header and payload
    const encodedHeader = base64url.encode(JSON.stringify(header));
    const encodedPayload = base64url.encode(JSON.stringify(payload));
    
    // Create signature input
    const signatureInput = `${encodedHeader}.${encodedPayload}`;
    
    // Sign with Ed25519
    const signature = crypto.sign(null, Buffer.from(signatureInput), this.privateKey);
    const encodedSignature = base64url.encode(signature);
    
    // Create complete JWS
    const jws = `${signatureInput}.${encodedSignature}`;
    
    // Add signature to document
    return {
      ...naltDocument,
      signature: {
        alg: 'EdDSA',
        sig: jws,
        public_key: this.did
      }
    };
  }
  
  /**
   * Verify a signed NALT Protocol document
   */
  async verifyDocument(signedDocument) {
    if (!signedDocument.signature) {
      throw new Error('Document is not signed');
    }
    
    const { sig, public_key } = signedDocument.signature;
    
    // Parse JWS
    const [encodedHeader, encodedPayload, encodedSignature] = sig.split('.');
    
    // Decode header and payload
    const header = JSON.parse(base64url.decode(encodedHeader).toString());
    const payload = JSON.parse(base64url.decode(encodedPayload).toString());
    
    // Verify algorithm
    if (header.alg !== 'EdDSA') {
      throw new Error('Unsupported algorithm');
    }
    
    // Verify document integrity
    const currentHash = this.hashEntries(signedDocument.entries);
    if (payload.entries_hash !== currentHash) {
      throw new Error('Document has been modified');
    }
    
    // In production, resolve DID to get public key
    // For this example, we'll use the stored public key
    const signatureInput = `${encodedHeader}.${encodedPayload}`;
    const signature = base64url.decode(encodedSignature);
    
    // Verify signature
    const isValid = crypto.verify(
      null,
      Buffer.from(signatureInput),
      this.publicKey,
      signature
    );
    
    return {
      valid: isValid,
      signer: public_key,
      document_id: payload.document_id
    };
  }
  
  /**
   * Create a hash of entries for integrity checking
   */
  hashEntries(entries) {
    const hash = crypto.createHash('sha256');
    hash.update(JSON.stringify(entries));
    return hash.digest('hex');
  }
  
  /**
   * Simplified Base58 encoding (use proper library in production)
   */
  base58Encode(buffer) {
    // This is a placeholder - use a proper base58 library
    return buffer.toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }
}

// Example usage
async function example() {
  // Create a signer
  const signer = new NALTSigner();
  console.log('Generated DID:', signer.did);
  
  // Create a NALT Protocol document
  const naltDocument = {
    spec_version: "nalt-protocol/1.2.0",
    document_id: "550e8400-e29b-41d4-a716-446655440000",
    date: "2025-07-10",
    meta: {
      language: "en",
      timezone: "UTC"
    },
    entries: [
      {
        entry_id: "entry-001",
        type: "reflection",
        mode: "morning",
        content_format: "text/plain",
        content: "Today I learned about DIDs and JWS signatures.",
        moods: [
          { type: "excited", intensity: 0.90 }
        ]
      }
    ]
  };
  
  // Sign the document
  const signedDocument = await signer.signDocument(naltDocument);
  console.log('\nSigned document:');
  console.log(JSON.stringify(signedDocument, null, 2));
  
  // Verify the signature
  const verification = await signer.verifyDocument(signedDocument);
  console.log('\nVerification result:', verification);
  
  // Demonstrate tamper detection
  console.log('\nTesting tamper detection...');
  signedDocument.entries[0].content = "Modified content";
  
  try {
    await signer.verifyDocument(signedDocument);
  } catch (error) {
    console.log('Tamper detected:', error.message);
  }
}

// Production implementation tips:
console.log(`
Production Implementation Tips:
1. Use established libraries:
   - @digitalbazaar/ed25519-signature-2020
   - @digitalbazaar/did-method-key
   - jose for JWS operations

2. Implement proper key management:
   - Store private keys securely (HSM, secure enclave)
   - Rotate keys periodically
   - Implement key recovery mechanisms

3. Use DID resolution:
   - Implement DID Document resolution
   - Cache resolved DIDs for performance
   - Handle key rotation in DID Documents

4. Add additional security:
   - Timestamp signatures with trusted time service
   - Implement signature expiration
   - Add nonce for replay protection
`);

// Run example if called directly
if (require.main === module) {
  example().catch(console.error);
}

module.exports = { NALTSigner };