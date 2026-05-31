# Plugin Development

A plugin exposes:

- `manifest`: name, version, description, permissions, commands
- `can_handle(command)`
- `handle(command)`

Plugins should be explicit about permissions and should not directly perform risky actions. They should return plans and use NOVA's safety guard.
