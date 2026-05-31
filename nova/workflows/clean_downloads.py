from __future__ import annotations
from pathlib import Path
from nova.security.path_policy import PathPolicy
from nova.files.scanner import FileScanner
from nova.files.organizer import FileOrganizer

class CleanDownloadsWorkflow:
    def __init__(self, policy: PathPolicy):
        self.policy = policy

    def plan(self, folder: str | Path) -> str:
        report = FileScanner(self.policy).scan(folder)
        plan = FileOrganizer().plan_by_category(report)
        return FileOrganizer().render_plan(plan)
