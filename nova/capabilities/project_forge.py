"""Builds project blueprints and files."""
NAME = "project_forge"
DESCRIPTION = "Builds project blueprints and files."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
