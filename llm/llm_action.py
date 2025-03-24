from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Define the prompt template
prompt_template = """You are an AI assistant for answering query based on given context only. Answer the query based 
on given context only. If context doesn't have answer for the query asked, then simply say 'Information not found'

Query:
{query}

Context:
{context}

Answer:
"""

# Create a PromptTemplate object
template = PromptTemplate(input_variables=["context", "query"], template=prompt_template)

# Initialize the Ollama LLM
ollama_llm = OllamaLLM(model="llama3.2:3b", api_url="http://127.0.0.1:11434")

# Create an LLMChain with the prompt template and Ollama LLM
llm_chain = LLMChain(prompt=template, llm=ollama_llm)


def call_llm(query, context):
    """
    Calls Ollama with the given query and context using LangChain.

    Args:
        query (str): The query to be sent to Ollama.
        context (list): A list of context strings to be included in the prompt.

    Returns:
        str: The response from Ollama.
    """
    # Format the context as a single string

    # Call the LLMChain with the query and context
    response = llm_chain.run({"context": context, "query": query})
    return response


# # Example usage
# query = "When was the marriage ?"
# context = ['''Marital Status :   Married\nProfession :   Others\nDate of Birth :   02 Apr 1995\nDate of Marriage :   10/12/2024\nAge :   29 years\nPresent Address :   Ward No- 1, Village- Bishunpura, PO-\nBaraon, Rohtas (Sasaram), BIHAR, 802215\nDuration of Stay :   0 years, 1 months\nPermanent Address :   Ward No- 1, Village- Bishunpura, Post\noffice- Bara, Rohtas (Sasaram), BIHAR, 802215\nWife Details\nName :   Shrimati Madhurima  Singh\nRelation Name :  W/O Manglam  Kumar\nMarital Status :   Married\nProfession :   Others\nDate of Birth :   26 Nov 1991\nDate of Marriage :   10/12/2024\nAge :   33 years\nPresent Address :   Ward No- 1, Village- Bishunpura, PO-\nBaraon, Rohtas (Sasaram), BIHAR, 802215
# ''']
# response = call_llm(query, context)
# print(response)