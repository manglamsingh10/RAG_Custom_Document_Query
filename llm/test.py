from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.2:3b", api_url="http://127.0.0.1:11434")

chain = prompt | model

result = chain.invoke({"question": "What is LangChain?"})

print(result)