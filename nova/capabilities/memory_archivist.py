"""Manages durable local memories and exports."""
NAME = "memory_archivist"
DESCRIPTION = "Manages durable local memories and exports."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
