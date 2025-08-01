# rag_main.py

from drive_processor import GoogleDriveProcessor
from text_processor import TextProcessor
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

        # 3️⃣ Initialize text processor
        text_processor = TextProcessor()

        # 4️⃣ For each new file → extract text
        for file_path_str in new_files:
            file_path = Path(file_path_str)
            extracted_text = text_processor.extract_text(file_path)

            if extracted_text.strip():
                print(f"✅ Extracted {len(extracted_text)} characters from: {file_path.name}")
                # 👉 Next: pass to chunker and embeddings here
            else:
                print(f"⚠️ No extractable text found in: {file_path.name}")

    print("RAG pipeline extraction step done.")


if __name__ == "__main__":
    main()
