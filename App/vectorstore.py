from typing import List
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import Product

def create_vector_store(products):
    # Create initial Document objects
    initial_documents = [
        Document(
            metadata={
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "image": product.image,
                "url": product.url,
                "store": product.store
            },
            page_content=f"{product.name} {product.price} {product.store}"
        )
        for product in products
    ]

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(initial_documents)

    # Create embeddings and vector database
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents(documents, embeddings)