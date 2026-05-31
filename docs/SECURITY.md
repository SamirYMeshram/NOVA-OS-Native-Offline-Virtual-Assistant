# Security Model

NOVA is designed for legitimate local personal automation only.

## What NOVA refuses by default

- Silent deletion.
- Silent overwrite.
- Writes to protected system paths.
- Stealth persistence.
- Credential extraction.
- Security bypass.
- Hidden monitoring.

## Confirmation gates

Any write operation can require explicit confirmation. File organization creates a plan first and execution must be called with `confirmed=True` from code.

## Privacy

Memory and indexes are local SQLite databases. NOVA does not transmit them to cloud APIs.

## Redaction

Likely secrets such as `api_key=...`, `password=...`, and private key blocks are redacted before memory/log storage.
