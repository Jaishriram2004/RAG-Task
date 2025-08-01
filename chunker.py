# chunker.py

from langchain.text_splitter import RecursiveCharacterTextSplitter

class Chunker:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk_text(self, text):
        """
        Split raw text into overlapping chunks.
        Returns list of text chunks.
        """
        return self.splitter.split_text(text)
