# text_processor.py

import os
from pathlib import Path

import fitz  # PyMuPDF
import docx


class TextProcessor:
    def __init__(self, input_dir="downloads"):
        self.input_dir = Path(input_dir)

    def extract_text(self, file_path):
        ext = file_path.suffix.lower()

        if ext == ".pdf":
            return self._extract_pdf(file_path)
        elif ext == ".docx":
            return self._extract_docx(file_path)
        elif ext == ".txt":
            return self._extract_txt(file_path)
        else:
            print(f"Unsupported file type: {file_path.name}")
            return ""

    def _extract_pdf(self, file_path):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text

    def _extract_docx(self, file_path):
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

    def _extract_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def extract_all(self):
        """
        Extract text from all files in the input folder.
        Returns:
            List of (file_path, extracted_text)
        """
        results = []
        for file in self.input_dir.iterdir():
            if file.is_file():
                text = self.extract_text(file)
                if text.strip():
                    results.append((file, text))
        return results


if __name__ == "__main__":
    # For testing
    processor = TextProcessor()
    docs = processor.extract_all()
    for f, t in docs:
        print(f"--- {f.name} ---")
        print(t[:200], "...")  # Show first 200 chars
