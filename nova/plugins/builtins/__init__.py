from .notes import NotesPlugin
from .tasks import TasksPlugin
from .reminders import RemindersPlugin
from .file_cleaner import FileCleanerPlugin
from .study_planner import StudyPlannerPlugin
from .code_generator import CodeGeneratorPlugin
from .document_summarizer import DocumentSummarizerPlugin
from .csv_analyst import CsvAnalystPlugin
from .system_monitor import SystemMonitorPlugin
from .local_search import LocalSearchPlugin
from .voice_assistant import VoiceAssistantPlugin
from .automation_manager import AutomationManagerPlugin
from .knowledge_base import KnowledgeBasePlugin
from .report_generator import ReportGeneratorPlugin
from .project_reviewer import ProjectReviewerPlugin
from .workflow_builder import WorkflowBuilderPlugin

BUILTIN_PLUGINS = [
    NotesPlugin(), TasksPlugin(), RemindersPlugin(), FileCleanerPlugin(), StudyPlannerPlugin(),
    CodeGeneratorPlugin(), DocumentSummarizerPlugin(), CsvAnalystPlugin(), SystemMonitorPlugin(),
    LocalSearchPlugin(), VoiceAssistantPlugin(), AutomationManagerPlugin(), KnowledgeBasePlugin(),
    ReportGeneratorPlugin(), ProjectReviewerPlugin(), WorkflowBuilderPlugin(),
]
