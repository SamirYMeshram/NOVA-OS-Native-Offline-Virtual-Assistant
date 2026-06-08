from __future__ import annotations

from dataclasses import dataclass

@dataclass(slots=True)
class WorkflowRecipe:
    name: str
    description: str
    goals: list[str]

RECIPES = {
    "study_pack": WorkflowRecipe("study_pack", "Index documents, create notes, flashcards, and tasks", [
        "index target documents", "ask document for key points", "generate study notes", "create revision tasks"
    ]),
    "project_review": WorkflowRecipe("project_review", "Analyze a codebase and produce improvements", [
        "scan project files", "analyze codebase", "run security review", "recommend fixes"
    ]),
    "downloads_cleanup": WorkflowRecipe("downloads_cleanup", "Safe Downloads cleanup plan", [
        "scan Downloads", "detect duplicates", "create cleanup plan", "write undo manifest"
    ]),
    "dataset_report": WorkflowRecipe("dataset_report", "Profile dataset and generate report", [
        "load dataset", "profile columns", "find missing values", "export markdown report"
    ]),
}

def list_recipes() -> list[dict[str, object]]:
    return [{"name": r.name, "description": r.description, "goals": r.goals} for r in RECIPES.values()]


def recipe_prompt(name: str, target: str | None = None) -> str:
    r = RECIPES[name]
    suffix = f" for {target}" if target else ""
    return "; then ".join(r.goals) + suffix
