"""Reviews risk and protects paths."""
NAME = "security_sentinel"
DESCRIPTION = "Reviews risk and protects paths."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
