"""Compiles multi-step workflows."""
NAME = "workflow_director"
DESCRIPTION = "Compiles multi-step workflows."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
