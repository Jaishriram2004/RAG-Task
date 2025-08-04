# embeddings_manager.py

from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore.document import Document

import os


class EmbeddingsManager:
    def __init__(self, persist_dir="faiss_index", model_name="all-MiniLM-L6-v2"):
        self.persist_dir = persist_dir
        self.model_name = model_name

        # Create embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name
        )

        # ✅ If FAISS index exists, load it safely with trusted deserialization
        if os.path.exists(self.persist_dir):
            print(f"✅ Loading existing FAISS index from: {self.persist_dir}")
            self.vectorstore = FAISS.load_local(
                self.persist_dir,
                self.embeddings,
                allow_dangerous_deserialization=True  # ✅ This fixes your error
            )
        else:
            self.vectorstore = None

    def add_chunks(self, chunks, metadata):
        """
        Adds a list of text chunks with metadata to the vector store.
        Each chunk gets same metadata dict, updated with chunk index.
        """
        docs = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    **metadata,
                    "chunk_index": i
                }
            )
            docs.append(doc)

        if self.vectorstore is None:
            # Create new index
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        else:
            # Add to existing index
            self.vectorstore.add_documents(docs)

        # Save updated index
        self.vectorstore.save_local(self.persist_dir)
        print(f"✅ Stored {len(docs)} chunks → FAISS index: {self.persist_dir}")
