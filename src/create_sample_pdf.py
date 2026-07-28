#!/usr/bin/env python3
"""Create a sample PDF for testing the converter."""

import fitz

def create_sample_pdf(output_path="sample.pdf"):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size

    # Add some content
    content = """
    # Sample PDF Document

    This is a sample PDF created for testing the PDF to Markdown converter.

    ## Section 1: Introduction

    This PDF contains various elements to test conversion:

    - Bullet point 1
    - Bullet point 2
    - Bullet point 3

    ## Section 2: Text Content

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    nostrud exercitation ullamco laboris.

    ## Section 3: Numbered List

    1. First item in the list
    2. Second item in the list
    3. Third item in the list

    ## Section 4: Table-like Content

    Product | Price | Quantity
    ---|---|---
    Apple | $1.00 | 10
    Banana | $0.50 | 20
    Orange | $1.50 | 15

    Thank you for using the PDF to Markdown converter!
    """

    # Insert text
    text_rect = fitz.Rect(50, 50, 545, 792)
    page.insert_text(text_rect.tl, content, fontsize=12)

    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")

if __name__ == "__main__":
    create_sample_pdf("input/sample.pdf")