# vectorstore.py (updated)
import os
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import Product

def create_vector_store(products, cache_path="vector_store.faiss"):
    embeddings = OpenAIEmbeddings()
    if os.path.exists(cache_path):
        # Load existing vector store with deserialization allowed
        return FAISS.load_local(cache_path, embeddings, allow_dangerous_deserialization=True)
    else:
        # Create and save new vector store
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
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_documents(initial_documents)
        vector_db = FAISS.from_documents(documents, embeddings)
        vector_db.save_local(cache_path)
        return vector_db

def update_vector_store(vector_db, new_products):
    new_docs = [
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
        for product in new_products
    ]
    vector_db.add_documents(new_docs)
    vector_db.save_local("vector_store.faiss")