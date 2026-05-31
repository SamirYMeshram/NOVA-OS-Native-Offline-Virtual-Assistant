from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class PermissionProfile:
    name: str
    can_read_files: bool = True
    can_write_files: bool = False
    can_launch_apps: bool = False
    can_open_urls: bool = False
    can_run_scripts: bool = False
    protected_actions: set[str] = field(default_factory=lambda: {"delete", "overwrite", "terminate_process"})


DEFAULT_PROFILE = PermissionProfile(name="default")
POWER_USER_PROFILE = PermissionProfile(
    name="power-user",
    can_read_files=True,
    can_write_files=True,
    can_launch_apps=True,
    can_open_urls=False,
    can_run_scripts=False,
)
