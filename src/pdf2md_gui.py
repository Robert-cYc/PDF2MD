#!/usr/bin/env python3
"""
PDF to Markdown Converter - GUI Application
Converts PDF files to Markdown format using PyMuPDF and pdfplumber.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import fitz  # PyMuPDF
import pdfplumber
import os
import re
import base64
from pathlib import Path


class PDFToMarkdownConverter:
    def __init__(self):
        self.setup_gui()

    def setup_gui(self):
        """Initialize the GUI window."""
        self.root = tk.Tk()
        self.root.title("PDF to Markdown Converter")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Input file selection
        ttk.Label(main_frame, text="PDF File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_path, width=60)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_pdf).grid(row=0, column=2, padx=5)

        # Output file selection
        ttk.Label(main_frame, text="Output MD:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=60)
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_output).grid(row=1, column=2, padx=5)

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        self.extract_images = tk.BooleanVar(value=True)
        self.extract_tables = tk.BooleanVar(value=True)
        self.preserve_format = tk.BooleanVar(value=True)
        self.embed_images_base64 = tk.BooleanVar(value=False)

        ttk.Checkbutton(options_frame, text="Extract Images", variable=self.extract_images).grid(row=0, column=0, padx=10)
        ttk.Checkbutton(options_frame, text="Embed Images (Base64)", variable=self.embed_images_base64).grid(row=0, column=1, padx=10)
        ttk.Checkbutton(options_frame, text="Extract Tables", variable=self.extract_tables).grid(row=0, column=2, padx=10)
        ttk.Checkbutton(options_frame, text="Preserve Formatting", variable=self.preserve_format).grid(row=0, column=3, padx=10)

        # Convert button
        ttk.Button(main_frame, text="Convert to Markdown", command=self.convert).grid(row=3, column=0, columnspan=3, pady=10)

        # Preview area
        ttk.Label(main_frame, text="Markdown Preview:").grid(row=4, column=0, sticky=tk.W)
        self.preview = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20)
        self.preview.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Status bar
        self.status = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

    def browse_pdf(self):
        """Open file dialog to select PDF."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if file_path:
            self.input_path.set(file_path)
            # Always auto-update output path to match PDF name
            md_path = Path(file_path).with_suffix('.md')
            self.output_path.set(str(md_path))

    def browse_output(self):
        """Open file dialog to select output MD file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Markdown As",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)

    def convert(self):
        """Convert PDF to Markdown."""
        pdf_path = self.input_path.get()
        md_path = self.output_path.get()

        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        # Auto-generate output path if not specified
        if not md_path:
            md_path = str(Path(pdf_path).with_suffix('.md'))
            self.output_path.set(md_path)

        try:
            self.status.config(text="Converting...")
            self.root.update()

            markdown_content = self.pdf_to_markdown(pdf_path)

            # Save to file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Show preview
            self.preview.delete(1.0, tk.END)
            self.preview.insert(1.0, markdown_content[:10000])  # Limit preview size

            self.status.config(text=f"Converted successfully! Saved to: {md_path}")
            messagebox.showinfo("Success", f"PDF converted to Markdown!\nSaved to: {md_path}")

        except Exception as e:
            self.status.config(text="Error occurred")
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

    def pdf_to_markdown(self, pdf_path):
        """Convert PDF file to Markdown string."""
        markdown_parts = []

        # Extract with pdfplumber for tables
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_num = i + 1

                # Extract text
                text = page.extract_text()
                if text:
                    # Clean up text
                    text = self.clean_text(text)
                    markdown_parts.append(f"\n## Page {page_num}\n\n{text}\n")

                # Extract tables if enabled
                if self.extract_tables.get():
                    tables = page.extract_tables()
                    for table_idx, table in enumerate(tables):
                        if table:
                            markdown_table = self.table_to_markdown(table)
                            markdown_parts.append(f"\n### Table {table_idx + 1} (Page {page_num})\n\n{markdown_table}\n")

        # Extract images with PyMuPDF if enabled
        if self.extract_images.get():
            doc = fitz.open(pdf_path)
            if self.embed_images_base64.get():
                # Embed images as base64 directly in markdown
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images()
                    for img_idx, img in enumerate(image_list):
                        if img:
                            try:
                                xref = img[0]
                                pix = fitz.Pixmap(doc, xref)
                                if pix.n > 4:
                                    pix = fitz.Pixmap(fitz.csRGB, pix)
                                # Convert to base64
                                img_bytes = pix.tobytes("png")
                                b64_str = base64.b64encode(img_bytes).decode('utf-8')
                                markdown_parts.append(f'\n![Page {page_num + 1} Image {img_idx + 1}](data:image/png;base64,{b64_str})\n')
                            except Exception:
                                pass
            else:
                # Save images to files
                image_dir = Path(self.output_path.get()).parent / "images"
                if self.output_path.get():
                    image_dir.mkdir(exist_ok=True)
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images()
                    for img_idx, img in enumerate(image_list):
                        if img:
                            try:
                                xref = img[0]
                                pix = fitz.Pixmap(doc, xref)
                                if pix.n > 4:
                                    pix = fitz.Pixmap(fitz.csRGB, pix)
                                img_path = image_dir / f"page{page_num + 1}_img{img_idx + 1}.png"
                                pix.save(str(img_path))
                                markdown_parts.append(f"\n![Page {page_num + 1} Image {img_idx + 1}](images/{img_path.name})\n")
                            except Exception:
                                pass

        return "".join(markdown_parts)

    def clean_text(self, text):
        """Clean and format extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def table_to_markdown(self, table):
        """Convert table data to Markdown format."""
        if not table:
            return ""

        markdown = []
        for row_idx, row in enumerate(table):
            # Clean cells
            cells = [self.clean_text(str(cell)) if cell else "" for cell in row]
            markdown.append("| " + " | ".join(cells) + " |")

            # Add separator after header row
            if row_idx == 0:
                separator = "| " + " | ".join(["---"] * len(cells)) + " |"
                markdown.append(separator)

        return "\n".join(markdown)

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


if __name__ == "__main__":
    app = PDFToMarkdownConverter()
    app.run()