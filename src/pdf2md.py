#!/usr/bin/env python3
"""
PDF to Markdown Converter - Simple CLI Version
Converts PDF files to Markdown format.
"""

import sys
import os
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed."""
    missing = []
    try:
        import fitz
    except ImportError:
        missing.append("pymupdf")

    try:
        import pdfplumber
    except ImportError:
        missing.append("pdfplumber")

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    return True


def convert_pdf_simple(pdf_path, output_path=None):
    """Simple PDF to Markdown conversion using PyMuPDF."""
    if not check_dependencies():
        return None

    import fitz

    doc = fitz.open(pdf_path)
    markdown_parts = [f"# {Path(pdf_path).stem}\n\n"]

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Clean up text - remove excessive newlines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)

        # Detect headers (lines that look like titles)
        for line in lines[:5]:
            if len(line) < 100 and line.isupper():
                text = f"# {line}\n\n{text}"
                break

        markdown_parts.append(f"## Page {page_num + 1}\n\n{text}\n")

    result = "".join(markdown_parts)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Saved to: {output_path}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf2md.py <input.pdf> [-o output.md]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = None

    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]

    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    convert_pdf_simple(input_file, output_file)