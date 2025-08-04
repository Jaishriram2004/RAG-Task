# sentence_chunker.py

import nltk

# Download sentence tokenizer data once
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize


class SentenceChunker:
    def __init__(self, target_chunk_size=500, overlap_sentences=2):
        """
        target_chunk_size: approx. max words per chunk
        overlap_sentences: how many sentences to overlap between chunks
        """
        self.target_chunk_size = target_chunk_size
        self.overlap_sentences = overlap_sentences

    def chunk_text(self, text):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_length = 0

        for sent in sentences:
            words = sent.split()
            sent_length = len(words)

            if current_length + sent_length > self.target_chunk_size:
                chunks.append(" ".join(current_chunk))

                # Overlap: reuse last few sentences
                overlap = current_chunk[-self.overlap_sentences:] if self.overlap_sentences < len(current_chunk) else current_chunk
                current_chunk = overlap.copy()
                current_length = sum(len(s.split()) for s in current_chunk)

            current_chunk.append(sent)
            current_length += sent_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
