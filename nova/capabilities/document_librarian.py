"""Indexes and searches local documents."""
NAME = "document_librarian"
DESCRIPTION = "Indexes and searches local documents."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
