import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
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
LOCAL_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL)


memory = ConversationMemory(system_prompt)
vector_store = None


def process_pdf(file):
    print("In process_pdf function")
    global vector_store, memory

    # 🔥 Reset everything
    vector_store = None
    memory = ConversationMemory(system_prompt)

    # Process new PDF
    text = read_pdf(file.name)
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)

    vector_store = VectorStore(len(embeddings[0]))
    vector_store.add(embeddings, chunks)

    print("PDF processed successfully.")

    return "PDF processed successfully. Memory and context reset."


def generate_local_reply(messages):
    print("Generating local reply...")
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.3,
        top_p=0.9,
        do_sample=True,
    )
    print("Model outputs:", outputs)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove prompt from output
    response = response[len(prompt):].strip()

    return response

def chat(message, history):
    print("In chat function")
    global vector_store

    lower_msg = message.lower()

    summary_keywords = ["summary", "talking about"]
    conversational_keywords = ["previous question", "repeat", "last answer"]

    summarize_chunks = any(kw in lower_msg for kw in summary_keywords)
    use_rag = not any(kw in lower_msg for kw in conversational_keywords)

    # 1️⃣ Build fresh document context
    context = ""
    if vector_store and use_rag:
        relevant_chunks = retrieve(vector_store, message)
        context = "\n".join(relevant_chunks)

    # 2️⃣ Get conversation memory FIRST (clean, no doc chunks inside)
    base_messages = memory.get_messages()

    # 3️⃣ Create a COPY for model input
    messages_for_model = base_messages.copy()

    # 4️⃣ Inject context ONLY into model copy
    if context:
        messages_for_model.append({
            "role": "user",
            "content": f"""
                Relevant document context:
                {context}

                User question:
                {message}
            """
        })
    else:
        messages_for_model.append({
            "role": "user",
            "content": message
        })

    # 5️⃣ Generate reply
    print("Messages for model:", messages_for_model)
    reply = generate_local_reply(messages_for_model)

    # 6️⃣ NOW store clean conversation into memory
    memory.add_user(message)        # store original question ONLY
    memory.add_assistant(reply)

    return reply


with gr.Blocks() as demo:
    gr.Markdown("# 📄 DocMind AI - Document Q&A Bot")

    pdf_input = gr.File(label="Upload PDF")
    upload_btn = gr.Button("Process PDF")
    upload_output = gr.Textbox()

    upload_btn.click(process_pdf, pdf_input, upload_output)

    chatbot = gr.ChatInterface(fn=chat)


if os.getenv("SPACE_ID"):  
    # Running on Hugging Face
    demo.launch()
else:
    # Running locally
    demo.launch(share=True, debug=True)