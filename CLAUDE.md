# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project provides tools for converting PDF documents to Markdown format. The goal is to extract text, tables, and images from PDF files and convert them into well-structured Markdown output.

## Architecture

The project is organized as follows:

- `src/pdf2md_gui.py` - Tkinter GUI application with file selection and preview
- `src/pdf2md.py` - Simple CLI entry point
- `src/convert_simple.py` - CLI version with table support
- `requirements.txt` - Python dependencies

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI version
python src/pdf2md_gui.py

# Run CLI version (auto-names output)
python src/convert_simple.py input/document.pdf

# CLI with images embedded as base64
python src/convert_simple.py input/document.pdf --embed-images

# CLI with custom output path
python src/convert_simple.py input/document.pdf -o custom/output.md

# Build standalone EXE
pyinstaller --onefile --noconsole --name "pdf2md_converter" src/pdf2md_gui.py
```

## Building

The standalone executable is pre-built at `dist/pdf2md_converter.exe` (54MB). You can run it directly without Python installed.

## Dependencies

- `pymupdf` (fitz) - PDF text and image extraction
- `pdfplumber` - Table and structured data extraction  
- `pytesseract` - OCR for scanned PDFs (optional, requires Tesseract)
- `Pillow` - Image processing support

## Notes

- Output filename defaults to the same name as the input PDF (with .md extension)
- PyMuPDF (fitz) is the primary library for PDF processing
- PDF conversion quality depends on source document structure
- Scanned PDFs require Tesseract OCR to be installed on the system
- Tables are extracted using pdfplumber when available
- Images can be extracted to file or embedded as base64 in the markdown
- Check "Embed Images (Base64)" in the GUI to include images directly in the markdown file