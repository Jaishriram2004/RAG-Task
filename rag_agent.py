# rag_agent.py

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
import requests

class RAGAgent:
    def __init__(
        self,
        persist_dir="faiss_index",
        model_name="all-MiniLM-L6-v2",
        top_k=3,
        ollama_url="http://localhost:11434/api/generate",
        ollama_model="llama3"
    ):
        self.persist_dir = persist_dir
        self.model_name = model_name
        self.top_k = top_k

        self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
        self.vectorstore = FAISS.load_local(
            self.persist_dir,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        # Ollama endpoint
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model

    def retrieve(self, query):
        """Embed query → search FAISS → return top chunks"""
        docs = self.vectorstore.similarity_search(query, k=self.top_k)
        return docs

    def build_prompt(self, query, retrieved_docs):
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = (
            f"Use the following context to answer the question accurately and concisely. "
            f"If the answer is unknown, say 'I don't know.' "
            f"Always end your answer with 'END OF ANSWER.'\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer:"
        )
        return prompt


    def ask(self, query):
        retrieved_docs = self.retrieve(query)
        prompt = self.build_prompt(query, retrieved_docs)

        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "options": {
                "num_predict": 250
            },
            "stream": False,
            "stop": ["END OF ANSWER"]
        }

        response = requests.post(self.ollama_url, json=payload)
        response.raise_for_status()
        answer = response.json()["response"]
        answer = answer.replace("END OF ANSWER", "").strip()

        return answer, retrieved_docs


