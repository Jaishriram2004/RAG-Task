# rag_main.py

from drive_processor import GoogleDriveProcessor
from text_processor import TextProcessor
from sentence_chunker import SentenceChunker  
from embeddings_manager import EmbeddingsManager  # ✅ NEW: Embeddings manager
from pathlib import Path


def main():
    # 1️⃣ Set your Google Drive folder ID here
    folder_id = "1KjS3WA7bSJWvYNcZvJOMJGw1ZGtKJlA1"

    # 2️⃣ Initialize Google Drive processor
    drive_processor = GoogleDriveProcessor(folder_id)

    # 3️⃣ Sync Drive → download new/updated files only
    new_files = drive_processor.sync_drive()

    if not new_files:
        print("No new or updated files found.")
    else:
        print(f"Processing {len(new_files)} new or updated files...")

        # 4️⃣ Initialize text processor
        text_processor = TextProcessor()

        # 5️⃣ Initialize sentence chunker
        chunker = SentenceChunker(target_chunk_size=500, overlap_sentences=2)

        # 6️⃣ Initialize embeddings manager
        embeddings_manager = EmbeddingsManager()

        # 7️⃣ For each new file → extract text → chunk → embed
        for file_path_str in new_files:
            file_path = Path(file_path_str)
            extracted_text = text_processor.extract_text(file_path)

            if extracted_text.strip():
                print(f"✅ Extracted {len(extracted_text)} characters from: {file_path.name}")

                # ➡️ Chunk by sentences
                chunks = chunker.chunk_text(extracted_text)
                print(f"🔹 Created {len(chunks)} sentence-based chunks for: {file_path.name}")

                # ➡️ Add chunks to embeddings index
                metadata = {"source_file": file_path.name}
                embeddings_manager.add_chunks(chunks, metadata)

            else:
                print(f"⚠️ No extractable text found in: {file_path.name}")

    print("RAG pipeline extraction + chunking + embedding step done.")


if __name__ == "__main__":
    main()
