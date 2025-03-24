from embedding.generate_embeddings import get_embedding


def embed_chunks(chunks):
    """
    Embeds chunks of text using a pre-trained SentenceTransformer model.
    """

    # Generate embeddings for each chunk
    document_to_index = []
    for idx, doc in enumerate(chunks):
        try:
            embed = get_embedding(doc['chunk_content'])  # converting text to vector embedding
            document_to_index.append([
                idx + 1,
                doc['document_url'],
                doc['page_number'],
                doc['chunk_content'],
                embed
            ])
        except Exception as e:
            print(f"Error processing document {idx + 1}: {e}")
    return document_to_index
