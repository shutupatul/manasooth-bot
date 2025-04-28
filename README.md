# Mental Health Support Chatbot 🤖💙

A compassionate AI assistant that provides empathetic listening and mental health support using retrieval-augmented generation (RAG) with Llama 3.

## Features

- **Empathetic Conversations**: Trained to provide warm, non-judgmental support
- **Context-Aware Responses**: Uses vector embeddings for relevant suggestions
- **Privacy-Focused**: Local processing of sensitive data
- **Customizable**: Easily adapt prompts and responses

## Project Structure
mental-health-tool/
├── .env # Environment variables (API keys)
├── .gitignore # Ignore files/folders
├── chatbot.py # Main chat interface
├── vector_store.py # ChromaDB vector operations
├── build_vectorstore.py # Script to create vector database
├── dataset/ # Mental health Q&A datasets
├── vectorstore/ # ChromaDB vector storage
├── pycache/ # Python cache
└── test_vectorstore.py # Vector store tests


## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Together AI account ([sign up](https://together.ai))
- ChromaDB (`pip install chromadb`)

### 2. Installation
```bash
git clone https://github.com/shutupatul/manasooth-bot
cd mental-health-tool
```

### 3. Configuration
- 1. Create .env file:
  
  TOGETHER_API_KEY=your_api_key_here

- 2. Build vector store:
   ```bash
   python build_vectorstore.py

### 4. Running the Chatbot

``` bash
 python chatbot.py