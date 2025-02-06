import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"  # Optional: LangSmith tracing
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")  # Optional: LangSmith tracing

# Streamlit page configuration
st.set_page_config(
    page_title="Price Contrast Chatbot", 
    page_icon=":robot:", 
    layout="wide"
)

# Initialize session state for messages if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for additional controls
with st.sidebar:
    st.header("Chatbot Settings")
    model_choice = st.selectbox(
        "Select Model", 
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
    )
    st.button("Clear Chat History", on_click=lambda: st.session_state.messages.clear())

# Main chat interface
st.title("Price Contrast Chatbot")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("user", "Question:{question}"),
    ]
)

# Create LLM with selected model
llm = ChatOpenAI(model=model_choice)
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handling
if prompt := st.chat_input("Ask me anything about products..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({"question": prompt})
            st.markdown(response)
    
    # Add assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": response})