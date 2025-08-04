# rag_chat_ui.py

import gradio as gr
from rag_agent import RAGAgent

# Create one RAGAgent instance for the whole chat
agent = RAGAgent()

def rag_chat(query, history):
    """Handle incoming user query, return answer."""
    answer, retrieved = agent.ask(query)
    return answer

# Create the Gradio ChatInterface
chatbot = gr.ChatInterface(
    fn=rag_chat,
    title="Local RAG Chatbot",
    description="Ask questions about local company docs. Powered by FAISS + Ollama LLM.",
    examples=["What is the main policy?", "Who is the Samsung Prism winner?"],
)

if __name__ == "__main__":
    chatbot.launch()
