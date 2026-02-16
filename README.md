# 📄 PDF Chatbot — DocMind AI

A local-AI powered **PDF Question-Answering and Chat Bot** built with **Gradio** and transformer models — designed to let users upload PDF documents and interact with them conversationally.

---

## ✨ Features

- 📤 Upload a PDF file  
- ✍️ Extract text from the PDF  
- 🔍 Generate responses from document content  
- 💬 Chat with the bot in natural language  
- 🧠 Retrieval-Augmented Generation (RAG)  
- 🔄 Conversation memory  
- 🖥️ Runs locally (no cloud API required)

---

## 🧠 How It Works

### 1️⃣ PDF Processing
- Reads uploaded PDF
- Splits into text chunks
- Converts chunks into embeddings

### 2️⃣ RAG Retrieval
- Retrieves relevant document chunks
- Injects them into the prompt

### 3️⃣ Local LLM Chat
- Uses `TinyLlama/TinyLlama-1.1B-Chat`
- Maintains chat history for context

### 4️⃣ Gradio Interface
- Web UI for upload + chat
- Runs locally on your machine

---

## 🛠️ Tech Stack

| Component | Purpose |
|-----------|----------|
| Python | Core language |
| Gradio | UI Interface |
| Transformers | Model loading & generation |
| TinyLlama-1.1B | Local LLM |
| Custom RAG | PDF parsing & retrieval |

---

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone https://github.com/Esabelle11/pdf_chatbot.git
cd pdf_chatbot

# 2. Install requirements
pip install -r requirements.txt

# 3. Run the app
python app.py
