# streamlit_app.py
import streamlit as st
from database import get_all_products
from vectorstore import create_vector_store
from chain import create_qa_chain

def initialize_session_state():
    """Initialize session state variables."""
    if 'qa_chain' not in st.session_state:
        # Get products from database
        products = get_all_products()
        
        # Create vector store
        vector_db = create_vector_store(products)
        
        # Create QA chain
        st.session_state.qa_chain = create_qa_chain(vector_db)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def main():
    st.set_page_config(page_title="Product Database ChatBot", page_icon="🤖", layout="wide")
    
    st.title("🛍️ Product Database ChatBot")
    st.markdown("""
    Ask questions about the products in the database. For example:
    - What are the most expensive products?
    - Show me black shirts
    - What products are available from [store name]?
    """)
    
    # Initialize session state
    initialize_session_state()
    
    # Create a container for chat history
    chat_container = st.container()
    
    # Create the input container
    with st.container():
        with st.form(key='query_form', clear_on_submit=True):
            user_input = st.text_input("Your question:", placeholder="Ask about products...")
            submit_button = st.form_submit_button("Ask")
    
        if submit_button and user_input:
            # Get response from chain
            response = st.session_state.qa_chain.invoke({"input": user_input})
            
            # Add to chat history
            st.session_state.chat_history.append({"user": user_input, "bot": response['answer']})
    
    # Display chat history
    with chat_container:
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")
            st.markdown("---")

# Update main.py to use Streamlit
if __name__ == "__main__":
    main()