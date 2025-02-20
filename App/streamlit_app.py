# streamlit_app.py (updated)
import streamlit as st
from database import get_all_products, get_product_count_and_max_id, get_new_products
from vectorstore import create_vector_store, update_vector_store
from chain import create_qa_chain

# ...existing code...
def initialize_session_state():
    if 'vector_db' not in st.session_state or 'qa_chain' not in st.session_state:
        products = get_all_products()
        st.session_state.vector_db = create_vector_store(products)
        st.session_state.qa_chain = create_qa_chain(st.session_state.vector_db)
        st.session_state.last_count, st.session_state.last_max_id = get_product_count_and_max_id()
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def check_and_update_database():
    current_count, current_max_id = get_product_count_and_max_id()
    if current_count != st.session_state.last_count or current_max_id != st.session_state.last_max_id:
        new_products = get_new_products(st.session_state.last_max_id)
        if new_products:
            update_vector_store(st.session_state.vector_db, new_products)
            st.session_state.qa_chain = create_qa_chain(st.session_state.vector_db)
        st.session_state.last_count, st.session_state.last_max_id = current_count, current_max_id
        return True
    return False

def main():
    st.set_page_config(page_title="Product Database ChatBot", page_icon="🤖", layout="wide")
    st.title("🛍️ Product Database ChatBot")
    st.markdown("""
    Ask questions about the products in the database. For example:
    - What are the most expensive products?
    - Show me black shirts
    - What products are available from [store name]?
    """)

    initialize_session_state()

    if st.button("Refresh Database"):
        products = get_all_products()
        st.session_state.vector_db = create_vector_store(products)
        st.session_state.qa_chain = create_qa_chain(st.session_state.vector_db)
        st.session_state.last_count, st.session_state.last_max_id = get_product_count_and_max_id()
        st.success("Database fully refreshed!")

    if check_and_update_database():
        st.success("Database updated with new products!")

    chat_container = st.container()
    with st.container():
        with st.form(key='query_form', clear_on_submit=True):
            user_input = st.text_input("Your question:", placeholder="Ask about products...")
            submit_button = st.form_submit_button("Ask")
        if submit_button and user_input:
            response = st.session_state.qa_chain.invoke({"input": user_input})
            st.session_state.chat_history.append({"user": user_input, "bot": response['answer']})

    with chat_container:
        for chat in st.session_state.chat_history:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**Bot:** {chat['bot']}")
            st.markdown("---")

if __name__ == "__main__":
    main()