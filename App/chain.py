from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def create_qa_chain(vector_db):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant for a price comparison website. "
        "If the question is a greeting like 'hello', 'hi', or 'how are you', ignore the context and respond with 'Hello! How can I assist you today?' "
        "For other questions, use only the provided context to answer concisely and accurately. "
        "Prices are in Rupees (format as Rs. X). If no price is available, say 'Price not listed'. "
        "Context contains product names, stores, and prices (if available). "
        "Only include products if the question is about products, stores, or prices. "
        "<context>{context}</context> "
        "Question: {input}"
    )
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    return create_retrieval_chain(retriever, document_chain)