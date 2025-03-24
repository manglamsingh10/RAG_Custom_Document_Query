from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_contents(contents):
    """
        content is list of sub-content of all pdfs in the folder with file_name, page_number, page_content.
        Return the chunks with document_url, page_number, chunk_content
    """
    # Parameters
    parameters = {
        "ingestion_chunk_size": 256,
        "ingestion_chunk_overlap": 128
    }

    # Text splitter initialization
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=parameters["ingestion_chunk_size"],
        chunk_overlap=parameters["ingestion_chunk_overlap"],
        disallowed_special=()
    )

    # Splitting documents
    chunks = []
    for idx, doc in enumerate(contents):
        try:
            split_doc = text_splitter.split_text(doc["page_content"])
            for split in split_doc:
                chunk = {
                    "document_url": doc["document_url"],
                    "page_number": doc["page_number"],
                    "chunk_content": split
                }
                chunks.append(chunk)
        except Exception as e:
            print(f"Error splitting document {idx + 1}: {e}")
    return chunks
