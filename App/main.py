# main.py
import sys
from database import get_all_products
from vectorstore import create_vector_store
from chain import create_qa_chain

def main():
    # Get products from database
    products = get_all_products()
    
    # Create vector store
    vector_db = create_vector_store(products)
    
    # Create QA chain
    qa_chain = create_qa_chain(vector_db)
    
    # Example query
    while True:
        query = input("Enter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        response = qa_chain.invoke({"input": query})
        print("\nAnswer:", response['answer'])
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()