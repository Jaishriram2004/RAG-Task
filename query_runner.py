# query_runner.py

from rag_agent import RAGAgent

def main():
    print("🔎 Local RAG Agent is ready! Type a question or 'exit' to quit.")
    # Initialize your agent
    agent = RAGAgent()
    while True:
        query = input("\nYour question: ")
        if query.strip().lower() in ["exit", "quit"]:
            print("👋 Exiting RAG Agent. Bye!")
            break
        # Get answer + retrieved docs
        answer, retrieved_docs = agent.ask(query)
        print("\n✅ === Answer ===")
        print(answer)
        print("\n📄 === Retrieved Chunks ===")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"\n--- Chunk {i} ---")
            print(f"Source: {doc.metadata}")
            print(f"Content:\n{doc.page_content}")
if __name__ == "__main__":
    main()
