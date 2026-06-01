# Security Model

NOVA is designed to be helpful without becoming dangerous.

Default safety rules:

- No paid cloud APIs required.
- No telemetry by default.
- Data remains local by default.
- Shell commands are evaluated before execution.
- Destructive patterns are blocked.
- System folders are protected.
- File cleanup creates plans first.
- Risky operations require confirmation.
- Audit logs redact secrets.
- Plugins declare permissions.

NOVA must not be used for malware, spyware, credential theft, stealth persistence, unauthorized surveillance, bypassing security controls, or destructive automation.
