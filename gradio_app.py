import gradio as gr
import os
from dotenv import load_dotenv
from rag import answer_query


def handle_query(query, chat_history):
    response = answer_query(query)
    return response


load_dotenv()
gradio_app_port = int(os.getenv('GRADIO_APP_PORT'))

gradio_config = gr.ChatInterface(
    handle_query,
    chatbot=gr.Chatbot(height=350),
    textbox=gr.Textbox(placeholder="Enter your query here...", container=False, scale=7),
    title="RAG based Query System",
    description="Ask a query from your custom data",
    theme="huggingface",
    #examples=["What is Coronavirus ?", "Tell me about Zika Virus"],
    cache_examples=True,
).launch(server_name="0.0.0.0", server_port=gradio_app_port)
