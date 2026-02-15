import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from memory.conversation import ConversationMemory
from rag.pdf_reader import read_pdf
from rag.chunking import chunk_text
from rag.embedding import embed_texts
from rag.vector_store import VectorStore
from rag.retriever import retrieve


system_prompt = """
You are DocMind AI.
Professional. Structured. Analytical.
Always explain reasoning clearly.
"""

# 🧠 Load once when app starts
LOCAL_MODEL = "nomic/gpt4all-mini"
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL)


memory = ConversationMemory(system_prompt)
vector_store = None


def process_pdf(file):
    global vector_store
    text = read_pdf(file.name)
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    vector_store = VectorStore(len(embeddings[0]))
    vector_store.add(embeddings, chunks)

    return "PDF processed successfully."

def generate_local_reply(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # extract the model’s reply only
    return text

def chat(message, history):
    global vector_store

    memory.add_user(message)

    # Retrieve RAG context
    context = ""
    if vector_store:
        relevant_chunks = retrieve(vector_store, message)
        context = "\n".join(relevant_chunks)

    prompt = f"""
    You are DocMind AI.
    Here is context:
    {context}

    User:
    {message}
    """

    reply = generate_local_reply(prompt)
    memory.add_assistant(reply)

    return reply



with gr.Blocks() as demo:
    gr.Markdown("# 📄 DocMind AI - Document Q&A Bot")

    pdf_input = gr.File(label="Upload PDF")
    upload_btn = gr.Button("Process PDF")
    upload_output = gr.Textbox()

    upload_btn.click(process_pdf, pdf_input, upload_output)

    chatbot = gr.ChatInterface(fn=chat)

demo.launch(share=True)

