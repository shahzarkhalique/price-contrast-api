import streamlit as st
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Text, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from a .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_wNTU4WiDqJQ5@ep-square-tooth-a1szbuny-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the table schema
class Product(Base):
    __tablename__ = 'shahzar_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    store = Column(Text, nullable=False)

# Create the table (if it doesn't exist)
Base.metadata.create_all(engine)

# Example function to query the database
def get_all_products():
    results = session.query(Product).all()
    return results

# Example function to get product info
def get_product_info(product_name):
    result = session.query(Product).filter(Product.name == product_name).first()
    return result

# Ingest data into vector database with chunking
def ingest_data():
    products = get_all_products()
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

    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db

# Initialize vector database
vector_db = ingest_data()

# Streamlit UI
st.title("Price Contrast: Your Personal Shopping Assistant")

# Product Search
st.header("Search for Products")
query = st.text_input("Enter product name or description", "Blue Shirt")
if st.button("Search"):
    results = vector_db.similarity_search(query)
    if results:
        for result in results:
            st.write(f"**Name:** {result.metadata['name']}")
            st.write(f"**Price:** {result.metadata['price']}")
            st.write(f"**Store:** {result.metadata['store']}")
            st.write(f"**URL:** [Link]({result.metadata['url']})")
            st.image(result.metadata['image'])
            st.write("---")
    else:
        st.write("No products found.")

# Product Details
st.header("Get Product Details")
product_name = st.text_input("Enter product name for details", "Product A")
if st.button("Get Details"):
    product_info = get_product_info(product_name)
    if product_info:
        st.write(f"**Name:** {product_info.name}")
        st.write(f"**Price:** {product_info.price}")
        st.write(f"**Store:** {product_info.store}")
        st.write(f"**URL:** [Link]({product_info.url})")
        st.image(product_info.image)
    else:
        st.write("Product not found.")
