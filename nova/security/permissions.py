from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class PermissionSet:
    file_read: bool = True
    file_write: bool = False
    app_launch: bool = False
    process_control: bool = False
    network: bool = False
    shell: bool = False
    memory_write: bool = True
    automation: bool = False
    extra: set[str] = field(default_factory=set)

    def allows(self, permission: str) -> bool:
        if hasattr(self, permission):
            return bool(getattr(self, permission))
        return permission in self.extra

DEFAULT_SAFE_PERMISSIONS = PermissionSet()
TRUSTED_LOCAL_PERMISSIONS = PermissionSet(file_write=True, app_launch=True, automation=True)
