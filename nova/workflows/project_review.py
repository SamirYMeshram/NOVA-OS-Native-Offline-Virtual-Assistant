from __future__ import annotations
from pathlib import Path
from nova.codegen.analyzer import CodebaseAnalyzer
from nova.codegen.reviewer import CodeReviewer

class ProjectReviewWorkflow:
    def run(self, root: str | Path) -> dict:
        return {'analysis': CodebaseAnalyzer().analyze(root), 'findings': CodeReviewer().review_tree(root)[:200]}
