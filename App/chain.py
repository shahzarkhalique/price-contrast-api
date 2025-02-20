# chain.py (updated)
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.vectorstores.faiss import FAISS

def create_qa_chain(vector_db):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(
        "Using only the provided context, answer the question concisely and accurately. "
        "Prices are in Rupees (format as Rs. X). Context contains product names, prices, and stores. "
        "<context>{context}</context> "
        "Question: {input}"
    )
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_db.as_retriever()
    return create_retrieval_chain(retriever, document_chain)