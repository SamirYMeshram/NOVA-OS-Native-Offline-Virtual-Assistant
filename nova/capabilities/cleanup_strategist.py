"""Creates reversible cleanup plans."""
NAME = "cleanup_strategist"
DESCRIPTION = "Creates reversible cleanup plans."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
