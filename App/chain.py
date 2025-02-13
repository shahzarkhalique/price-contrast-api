from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.vectorstores.faiss import FAISS

def create_qa_chain(vector_db):
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_template("""
    Answer the following questions based on only the provided context. 
    Think step by step before providing a detailed answer. 
    I will tip you $1000 if the user finds your answer helpful.
    Also all the prices in the database are in Rupees. Therefore, the prices should be mentioned like Rs. 1000.
    <context>
    {context}
    </context>
    Question: {input}""")
    
    # Create document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create retriever
    retriever = vector_db.as_retriever()
    
    # Create and return retrieval chain
    return create_retrieval_chain(retriever, document_chain)
