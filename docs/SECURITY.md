# Security Model

NOVA must behave like trusted local software, never malware.

## Hard rules

- No stealth persistence.
- No credential theft.
- No hidden surveillance.
- No destructive file operations without explicit confirmation.
- No arbitrary shell execution by default.
- No paid API requirement.
- No external network calls for core operation.

## File safety

Protected paths are blocked by default. File organization creates move plans and undo logs. Deletion is intentionally blocked in the foundation implementation.

## Audit logs

Important commands and file actions are written to `~/.nova/logs/audit.jsonl`. Likely secrets are redacted before logging.

## Plugins

Plugins declare permissions. The current manager loads trusted built-ins only. Future external plugin loading should include manifests, signatures/checksums, and user approval.
