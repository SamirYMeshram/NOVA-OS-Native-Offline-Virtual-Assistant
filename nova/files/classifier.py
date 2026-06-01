from __future__ import annotations
from pathlib import Path

CATEGORIES = {
    'documents': {'.pdf', '.docx', '.doc', '.txt', '.md', '.odt', '.rtf'},
    'spreadsheets': {'.csv', '.xlsx', '.xls', '.ods'},
    'presentations': {'.pptx', '.ppt', '.odp'},
    'images': {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'},
    'audio': {'.mp3', '.wav', '.flac', '.m4a', '.ogg'},
    'video': {'.mp4', '.mkv', '.mov', '.webm'},
    'archives': {'.zip', '.tar', '.gz', '.7z', '.rar'},
    'code': {'.py', '.js', '.ts', '.java', '.go', '.rs', '.c', '.cpp', '.h', '.html', '.css', '.json', '.yaml', '.yml', '.toml'},
    'installers': {'.exe', '.msi', '.rpm', '.deb', '.appimage'},
}

def classify(path: str | Path) -> str:
    suffix = Path(path).suffix.lower()
    for category, suffixes in CATEGORIES.items():
        if suffix in suffixes:
            return category
    return 'other'
