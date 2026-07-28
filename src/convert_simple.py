#!/usr/bin/env python3
"""
Simple PDF to Markdown converter - command line interface
Usage: python convert_simple.py <input.pdf> [output.md]
"""

import sys
import os
from pathlib import Path

try:
    import fitz
    import pdfplumber
except ImportError:
    print("Missing dependencies. Install with: pip install -r requirements.txt")
    sys.exit(1)

def convert_pdf(pdf_path, output_path=None):
    """Convert PDF to Markdown."""
    if output_path is None:
        output_path = Path(pdf_path).with_suffix('.md')

    doc = fitz.open(pdf_path)
    markdown_parts = [f"# {Path(pdf_path).stem}\n\n"]

    # Extract with pdfplumber for tables
    try:
        with pdfplumber.open(pdf_path) as pdf_plum:
            for i, page in enumerate(pdf_plum.pages):
                text = page.extract_text()
                if text:
                    # Preserve paragraph breaks but clean up excessive whitespace
                    paragraphs = text.split('\n\n')
                    text = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
                    markdown_parts.append(f"## Page {i + 1}\n\n{text}\n")

                # Extract tables
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    if table:
                        md_table = table_to_markdown(table)
                        markdown_parts.append(f"\n### Table {table_idx + 1}\n\n{md_table}\n")
    except Exception:
        # Fallback to PyMuPDF only
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text = ' '.join(text.split())
            markdown_parts.append(f"## Page {page_num + 1}\n\n{text}\n")

    result = "".join(markdown_parts)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Converted: {pdf_path}")
    print(f"Output: {output_path}")
    return result


def table_to_markdown(table):
    """Convert table to Markdown."""
    if not table:
        return ""
    markdown = []
    for row_idx, row in enumerate(table):
        cells = [str(cell).strip() if cell else "" for cell in row]
        markdown.append("| " + " | ".join(cells) + " |")
        if row_idx == 0:
            markdown.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n".join(markdown)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/convert_simple.py <input.pdf> [output.md]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    convert_pdf(input_file, output_file)