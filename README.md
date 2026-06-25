#  Private Local Codebase RAG Engine

A high-performance, zero-data-leak Retrieval-Augmented Generation (RAG) engine designed to run completely offline on your local machine. This tool splits source code down by syntax trees, indexes it into a persistent vector database, and uses **Ollama** for context-injected reasoning without ever sending your data to external APIs.

---

##  System Architecture

* **Phase 1: Code-Aware Parser** – Leverages structural syntax-splitting to slice code documents into logical blocks based on function and class scopes instead of raw characters.
* **Phase 2: Local Vector Database** – Uses `ChromaDB` paired with the `all-MiniLM-L6-v2` embedding model to transform code strings into multidimensional vectors stored right on your disk.
* **Phase 3: Ollama Reasoning Framework** – Hooks into local language models to serve as an on-demand code architect.

---

##  Setup Instructions

### 1. Requirements
* Python 3.10+
* Ollama (`ollama pull qwen2.5-coder:1.5b`)

P### 2. Run Application
```bash
pip install -r requirements.txt
python main.py