from __future__ import annotations
from nova.documents.study import StudyToolkit
from nova.documents.vector_store import VectorStore

class ExamPrepWorkflow:
    def __init__(self, store: VectorStore):
        self.study = StudyToolkit(store)

    def plan(self, subject: str, days: int = 7) -> list[str]:
        return self.study.study_plan(subject, days)
