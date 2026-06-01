# ADR 12

Decision: keep NOVA local-first and safe-by-default.

Context: the system handles personal files, memory, and automation. Unsafe shortcuts can harm the user.

Consequences: features should prefer planning, confirmation, auditability, and graceful fallback over uncontrolled execution.
