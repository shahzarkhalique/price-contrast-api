import os
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_vector_store(products, cache_path="vector_store.faiss"):
    embeddings = OpenAIEmbeddings()
    if os.path.exists(cache_path):
        return FAISS.load_local(cache_path, embeddings, allow_dangerous_deserialization=True)
    else:
        initial_documents = [
            Document(
                metadata={
                    "id": product.id,
                    "name": product.name,
                    "price": product.price if product.price is not None else None,
                    "image": product.image,  # Ensure this is an array of URLs
                    "url": product.url,
                    "store": product.store
                },
                page_content=f"{product.name} at {product.store}" + (f" for Rs. {product.price}" if product.price is not None else "")
            )
            for product in products
        ]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        documents = text_splitter.split_documents(initial_documents)
        vector_db = FAISS.from_documents(documents, embeddings)
        vector_db.save_local(cache_path)
        return vector_db

def update_vector_store(vector_db, new_products, cache_path="vector_store.faiss"):
    new_docs = [
        Document(
            metadata={
                "id": product.id,
                "name": product.name,
                "price": product.price if product.price is not None else None,
                "image": product.image,  # Ensure this is an array of URLs
                "url": product.url,
                "store": product.store
            },
            page_content=f"{product.name} at {product.store}" + (f" for Rs. {product.price}" if product.price is not None else "")
        )
        for product in new_products
    ]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(new_docs)
    vector_db.add_documents(split_docs)
    vector_db.save_local(cache_path)