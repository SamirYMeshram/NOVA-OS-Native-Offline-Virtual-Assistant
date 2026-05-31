from __future__ import annotations

CATEGORY_BY_EXTENSION = {
    '.pdf': 'documents', '.docx': 'documents', '.txt': 'documents', '.md': 'documents', '.pptx': 'presentations',
    '.xlsx': 'spreadsheets', '.csv': 'spreadsheets', '.json': 'data', '.zip': 'archives', '.7z': 'archives', '.rar': 'archives',
    '.png': 'images', '.jpg': 'images', '.jpeg': 'images', '.webp': 'images', '.gif': 'images',
    '.mp4': 'videos', '.mkv': 'videos', '.mp3': 'audio', '.wav': 'audio', '.py': 'code', '.js': 'code', '.java': 'code',
    '.exe': 'executables', '.msi': 'executables', '.sh': 'scripts', '.bat': 'scripts', '.AppImage': 'executables',
}

def classify_extension(extension: str) -> str:
    return CATEGORY_BY_EXTENSION.get(extension.lower(), 'other')
