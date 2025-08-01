# rag_main.py

from drive_processor import GoogleDriveProcessor

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
        print(f"Processing {len(new_files)} files...")

        # TODO: For each new file:
        for file_path in new_files:
            print(f"Would process: {file_path}")
            # 👉 Add your chunking, embedding & upsert logic here

    print("RAG pipeline step done.")

if __name__ == "__main__":
    main()