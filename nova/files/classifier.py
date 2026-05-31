from __future__ import annotations

CATEGORY_BY_EXT = {
    "documents": {".pdf", ".docx", ".doc", ".txt", ".md", ".odt", ".rtf"},
    "spreadsheets": {".csv", ".xlsx", ".xls", ".ods"},
    "images": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".heic"},
    "videos": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".xz"},
    "code": {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".c", ".cpp", ".html", ".css", ".json", ".yaml", ".toml"},
    "installers": {".exe", ".msi", ".deb", ".rpm", ".appimage", ".flatpakref"},
}


def classify_file(name: str, suffix: str) -> str:
    suffix = suffix.lower()
    for category, exts in CATEGORY_BY_EXT.items():
        if suffix in exts:
            return category
    lowered = name.lower()
    if "screenshot" in lowered:
        return "screenshots"
    return "other"
