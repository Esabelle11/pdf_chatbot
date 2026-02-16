📄 PDF Chatbot — DocMind AI

A local-AI powered PDF Question-Answering and Chat Bot built with Gradio and transformer models — designed to let users upload PDF documents and interact with them conversationally.

This project lets you:

✨ Upload a PDF file
✍️ Extract text from the PDF
🔍 Generate responses from the document content
💬 Chat with the bot in natural language

It uses a lightweight transformer model locally — no cloud API required.

🧠 How It Works

PDF Processing

Reads your uploaded PDF, splits it into text chunks.

Converts chunks into embeddings for search and retrieval.

RAG-Style Retrieval (Optional)

On user questions, it retrieves relevant chunks from past PDF text.

Combines relevant document context with conversation memory.

Local LLM Chat

Uses a local language model (TinyLlama/TinyLlama-1.1B-Chat) to generate replies.

Memory is stored between exchanges for context-aware conversation.

Gradio Interface

Simple web UI where you upload PDFs and then chat with the bot.

Works entirely locally (model runs on your machine).

🚀 Features

✅ Upload and analyze PDF files
✅ Conversational Q&A based on PDF content
✅ Retrieval-Augmented Generation (RAG) for better context
✅ Memory keeps track of the chatbot history
✅ Local model — no reliance on external LLM APIs

🛠️ Tech Stack
Component	Used For
Python	Core language
Gradio	UI / Frontend interface
Transformers	LLM model loading & generation
TinyLlama-1.1B	Local chat model
Custom RAG modules	PDF reading, embeddings & vector store
🚀 Quick Start
# 1. Clone repo
git clone https://github.com/Esabelle11/pdf_chatbot.git
cd pdf_chatbot

# 2. Install requirements
pip install -r requirements.txt

# 3. Run the app
python app.py


Then open your Gradio interface in the browser, upload a PDF, and start chatting!

🧩 Use Cases

✔️ Academic paper exploration
✔ Document knowledge base Q&A
✔ Fast summarization and topic extraction
✔ Local AI assistant for PDFs