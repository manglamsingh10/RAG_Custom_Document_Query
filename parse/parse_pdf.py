import os
import fitz  # PyMuPDF


def extract_pdf_metadata_page(file_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        list: doc_list containing extracted text and metadata.
    """
    try:
        document = fitz.open(file_path)
        metadata = document.metadata

        metadata_fields = {
            "total_pages": document.page_count,
            "author": metadata.get('author', ""),
            "keywords": metadata.get('keywords', ""),
            "create_date": metadata.get('creationDate', ""),
            "modify_date": metadata.get('modDate', ""),
            "file_name": document.name
        }

        doc_list = []

        for page_num in range(document.page_count):
            page = document.load_page(page_num)

            doc = {
                "file_name": metadata_fields["file_name"],
                "total_pages": metadata_fields["total_pages"],
                "keywords": metadata_fields["keywords"],
                "create_date": metadata_fields["create_date"],
                "modify_date": metadata_fields["modify_date"],
                "page_content": page.get_text(),
                "page_number": page_num,
                "content_length": len(page.get_text())
            }
            doc_list.append(doc)
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return doc_list


def parse_pdfs_from_local_directory(directory):
    """
    Parses PDF files from a local directory using Tika.

    Args:
        directory (str): Path to the local directory containing PDFs.

    Returns:
        List of tuples with file path, content, and metadata.
    """
    all_pdf_data = []

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory, filename)
                try:
                    doc_lists = extract_pdf_metadata_page(file_path)
                    all_pdf_data.append(doc_lists)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return all_pdf_data


def preprocess_documents(documents):
    """
    Prepares documents by separating content and metadata.
    """
    content = []

    for doc in documents:
        for page in doc:
            content.append({
                "document_url": page.get("file_name", ""),
                "page_number": page.get("page_number", ""),  # TODO: Maybe add +1 to page number
                "page_content": page.get("page_content", "")
            })

    return content


def parse_and_preprocess_from_directory(directory):
    all_pdf_data = parse_pdfs_from_local_directory(directory)
    content = preprocess_documents(all_pdf_data)
    return content
