"""Generates notes and flashcards."""
NAME = "study_coach"
DESCRIPTION = "Generates notes and flashcards."
PERMISSIONS = ["local"]

def describe() -> dict[str, object]:
    return {"name": NAME, "description": DESCRIPTION, "permissions": PERMISSIONS}
