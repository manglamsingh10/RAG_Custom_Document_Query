from parse.parse_pdf import parse_and_preprocess_from_directory
from chunking.chunk import chunk_contents
from embedding.embed_chunks import embed_chunks
from embedding.generate_embeddings import get_embedding_array
from dataoperation.hdbclinet import store_embeddings_to_db
from dataoperation.hdbclinet import run_vector_search
from dataoperation.hdbclinet import clear_indexes
from llm.llm_action import call_llm


def index_folder_and_store_embeddings(folder_path):
    print(f"Indexing folder: {folder_path}")

    content = parse_and_preprocess_from_directory(folder_path)
    print(f"Found {len(content)} pages to index")

    chunks = chunk_contents(content)
    print(f"Found {len(chunks)} chunks to index")

    chunks_to_index = embed_chunks(chunks)
    print(f"Generated embeddings for {len(chunks_to_index)} chunks")

    store_embeddings_to_db(chunks_to_index)
    print("Stored embeddings in database")


def get_relevant_chunk_text(query):
    query_embedding = get_embedding_array(query)
    result = run_vector_search(query_vector=query_embedding, metric="COSINE_SIMILARITY", k=4)

    context = []

    for match in result:
        context.append({
            "page_number": match[2],
            "document_url": match[3],
            "chunk_content": match[4]
        })
    return context


def get_response_for_query(query, context):
    print(f"Calling LLM with Query: {query} and Context: {context}")
    response = call_llm(query, context)
    print(f"LLM Response: {response}")
    return response


def answer_query(query):
    context = get_relevant_chunk_text(query)
    response = get_response_for_query(query, context)
    return response

def clear_index():
    print("Clearing indexes")
    clear_indexes()
    print("Indexes cleared")
