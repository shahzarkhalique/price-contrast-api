from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # Optional: LangSmith tracing
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # Optional: LangSmith tracing

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question:{question}"),
    ]
)

# OpenAI LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")  # Or gpt-4, or other model
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Streamlit App
st.set_page_config(page_title="Price Contrast Chatbot", page_icon=":robot:")  # Set title and icon
st.title("Price Contrast Chatbot")

# Chat History (using Streamlit's session state)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Container for chat messages (to control the order)
chat_container = st.container()

# Input field for user messages (at the bottom) with callback
def clear_text_input():
    st.session_state["user_input"] = ""

user_input = st.text_input("Ask me anything about products...", key="user_input")

# Handle user input
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
        

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):  # Add a spinner
            response = chain.invoke({"question": user_input})
            st.markdown(response)

    # Add messages to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "assistant", "content": response})

    # No need to clear user_input here, the callback does it
    st.rerun()  # Force Streamlit to rerun to update the chat display


# Display chat messages from history (in the container)
with chat_container:  # Place messages inside the container
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Optional: Add a clear chat history button (improves UX)
if st.button("Clear Chat History"):
    st.session_state["messages"] = []
    st.rerun()  # Use st.rerun() here as well