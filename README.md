# RAG System - Retrieval-Augmented Generation Knowledge Base

## Overview
A comprehensive RAG (Retrieval-Augmented Generation) system that enables intelligent querying of documents stored in Google Drive using local LLM capabilities.

## Features
- Google Drive Integration: Automatically sync and process documents from specified folders
- Multi-format Support: Handles PDF, DOCX, and TXT files
- Intelligent Chunking: Sentence-based text segmentation for optimal embeddings
- Vector Search: High-performance similarity search using FAISS
- Local LLM: Uses Ollama for response generation
- Interactive UI: Gradio-based chat interface

## Architecture
The system follows a modular architecture with clear separation of concerns:

### Core Components
- **rag_main.py**: Data pipeline orchestrator
- **rag_agent.py**: Core RAG engine with retrieval and generation
- **embeddings_manager.py**: Vector embedding management
- **text_processor.py**: Document text extraction
- **sentence_chunker.py**: Text segmentation
- **drive_processor.py**: Google Drive integration
- **rag_chat_ui.py**: Gradio-based user interface

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Ollama: `ollama pull llama3`
4. Configure Google Drive API credentials

## Usage
1. Data Ingestion: `python rag_main.py`
2. Start Chat Interface: `python rag_chat_ui.py`
3. Query Documents via Gradio interface

## Architecture Diagram
See `architecture.html` for interactive visual documentation
