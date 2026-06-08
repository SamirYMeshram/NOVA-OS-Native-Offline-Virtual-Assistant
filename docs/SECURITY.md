# Security Model

NOVA is not allowed to behave like malware, spyware, credential theft tooling, or stealth automation. The code is designed around transparent, local, permissioned behavior.

## Rules

- No paid API dependency.
- No cloud calls required for core features.
- No hidden persistence.
- No destructive action by default.
- No unrestricted shell tool.
- Protected OS paths are blocked.
- Logs redact secrets.
- Memory redacts obvious tokens/keys/passwords.
- File cleanup is a plan, not deletion.
- Side effects require `YES_NOVA_ACT`.

## Risk levels

- `safe`: read-only or local computation.
- `review`: file creation, moving, opening apps, writing generated project files.
- `dangerous`: delete, overwrite, kill process, system folder modification; blocked unless a specific safe wrapper exists.
- `blocked`: credential access, stealth, security bypass, hidden surveillance, destructive shell execution.

## Audit

Audit events are JSONL files under `~/.nova/logs/audit.jsonl` by default.
