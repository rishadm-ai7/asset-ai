import os
import numpy as np
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from decouple import config

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(api_key=config("OPENAI_API_KEY"))


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = splitter.split_text(text)
    return chunks


def process_pdfs(pdf_paths, index_path):
    all_documents = []
    for pdf_path in pdf_paths:
        text = read_pdf(pdf_path)
        chunks = chunk_text(text)
        metadata = [{"source": os.path.basename(pdf_path)} for _ in chunks]
        documents = [
            Document(page_content=chunk, metadata=meta)
            for chunk, meta in zip(chunks, metadata)
        ]
        all_documents.extend(documents)

    # Create FAISS index
    faiss_index = FAISS.from_documents(all_documents, embedding_model)

    # Save FAISS index
    faiss_index.save_local(index_path)


# Example usage
pdf_paths = ["/home/asus/mitz/asset-ai/backend/demo_data/ataccama.pdf"]
faiss_index_path = os.path.join(os.path.dirname(__file__), config("FAISS_INDEX_PATH"))
process_pdfs(pdf_paths, faiss_index_path)
