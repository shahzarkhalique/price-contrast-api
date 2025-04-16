from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def create_qa_chain(vector_db):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant for a price comparison website. "
        "If the question is a greeting (e.g., 'hello', 'hi', 'how are you'), respond conversationally with a simple reply like 'Hello! How can I assist you today?' and do not include any product information. "
        "For other questions, use only the provided context to answer concisely and accurately. "
        "Prices are in Rupees (format as Rs. X). Context contains product names, prices, and stores. "
        "Only include products if the question explicitly asks about products, stores, or prices. "
        "Prioritize products from smaller retailers when relevant, highlighting their unique offerings. "
        "<context>{context}</context> "
        "Question: {input}"
    )
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})  # Limit to 3 results