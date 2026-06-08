"""Profiles CSV/JSON/XLSX data."""
NAME = "dataset_scientist"
DESCRIPTION = "Profiles CSV/JSON/XLSX data."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
