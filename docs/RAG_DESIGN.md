# RAG Design

NOVA indexes local documents into chunks, creates local hash embeddings as a dependency-free fallback, stores chunks in SQLite, retrieves relevant chunks, and answers with source previews.

Optional libraries improve extraction:

- `pypdf` for PDF
- `python-docx` for DOCX
- `openpyxl` for XLSX
