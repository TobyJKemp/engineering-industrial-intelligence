# Encryption at Rest

## At a Glance
| | |
|---|---|
| **Category** | Security Practice / Data Protection |
| **Complexity** | Intermediate |
| **Time to Learn** | 1-2 days for concepts, 1 week for implementation |
| **Prerequisites** | Cryptography basics, storage systems, compliance requirements |

## One-Sentence Summary
Encryption at rest is the practice of encrypting data stored on disk (databases, files, backups, cloud storage) so that it remains protected from unauthorized access even if the underlying storage is compromised.

## Why This Matters to You
If your AI agents, databases, or cloud services store sensitive data (customer records, model weights, logs), encryption at rest ensures that even if a disk is stolen, a backup is leaked, or a cloud admin is compromised, the data remains unreadable without the decryption key. Many regulations (GDPR, HIPAA, PCI-DSS) require encryption at rest for compliance. In 2026, with AI systems handling valuable and regulated data, encryption at rest is a baseline security control—protecting against both external attackers and insider threats.

## The Core Idea
### What It Is
Encryption at rest means applying cryptographic algorithms to data before it is written to persistent storage. The data is only decrypted when accessed by authorized applications or users with the correct keys. This protects against physical theft, unauthorized snapshots, or improper disposal of storage media.

Modern implementations use strong symmetric encryption (e.g., AES-256) and integrate with key management systems (KMS) to automate key rotation and access control. Encryption can be applied at the disk, file, database, or application level, depending on requirements.

### What It Isn’t
Encryption at rest is not a substitute for encryption in transit (protecting data as it moves across networks) or for access controls (who can read/write data). It does not prevent authorized users or applications from accessing data—if an attacker compromises the application, they may still access decrypted data. It is not a one-time setup; keys must be rotated and managed securely.

## How It Works
1. **Key Generation:** Generate a strong symmetric encryption key (e.g., AES-256).
2. **Encryption:** Data is encrypted before being written to disk (by storage system, database, or application).
3. **Key Management:** Keys are stored in a secure key management system (KMS), not on the same disk as the data.
4. **Decryption:** Authorized applications retrieve the key and decrypt data as needed.
5. **Key Rotation:** Keys are rotated periodically to limit exposure if compromised.

## Think of It Like This
Encryption at rest is like storing valuables in a safe: even if someone steals the safe (disk, backup), they can’t access the contents without the combination (encryption key).

## The "So What?" Factor
**If you use this:**
- Data remains protected even if storage is lost, stolen, or improperly disposed.
- You meet compliance requirements for data protection.
- You reduce risk from insider threats and cloud provider staff.

**If you don't:**
- Physical theft or cloud breaches can expose all stored data.
- You may fail audits and face regulatory penalties.
- Attackers can access sensitive information from backups or snapshots.

## Practical Checklist
Before implementing, ask yourself:
- [ ] Is all sensitive data encrypted before being written to disk or cloud storage?
- [ ] Are encryption keys managed and rotated securely (not stored with the data)?
- [ ] Is encryption enabled for all backups and snapshots?

## Watch Out For
⚠️ Storing encryption keys on the same system as the data (defeats the purpose).
⚠️ Relying solely on disk-level encryption for highly sensitive data (consider application-level encryption too).

## Connections
**Builds On:** Cryptography, Key Management, Compliance
**Works With:** Encryption in Transit, Key Vault, Key Rotation
**Leads To:** Data Loss Prevention, Zero Trust, Security Scanning

## Quick Decision Guide
**Use this when you need to:** Protect stored data from physical theft, insider threats, or regulatory risk.
**Skip this when:** Data is non-sensitive, ephemeral, or already protected by other means (rare in production).

## Further Exploration
- 📖 [Azure Encryption at Rest Documentation](https://learn.microsoft.com/en-us/azure/security/fundamentals/encryption-atrest)
- 🎯 [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
- 💡 [NIST SP 800-111: Guide to Storage Encryption Technologies](https://csrc.nist.gov/publications/detail/sp/800-111/final)

---
*Added: 2026-06-07 | Updated: 2026-06-07 | Confidence: High*
