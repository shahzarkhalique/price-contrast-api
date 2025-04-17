from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_all_products
from vectorstore import create_vector_store, update_vector_store
from chain import create_qa_chain
from config import OPENAI_API_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

products = get_all_products()
print(f"Loaded {len(products)} products")
vector_db = None
qa_chain = None
if products:
    try:
        vector_db = create_vector_store(products)
        qa_chain = create_qa_chain(vector_db)
    except Exception as e:
        print(f"Failed to initialize vector store or QA chain: {e}")

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Missing query")
        
        # Check for exact greeting queries
        greeting_keywords = ["hello", "hi", "hey", "how are you", "good morning", "thank you"]
        query_lower = request.query.lower().strip()
        is_greeting = query_lower in greeting_keywords
        print(f"Query: '{request.query}', Is Greeting: {is_greeting}")
        
        if is_greeting:
            return {
                "answer": "Hello! How can I assist you today?",
                "context": []
            }
        
        # Handle no products or QA chain
        if not products or not qa_chain:
            print("No products or QA chain available")
            return {
                "answer": "No products available. Please try again later.",
                "context": []
            }
        
        # Process product query
        response = qa_chain.invoke({'input': request.query})
        print(f"QA Chain Response: {response}")
        formatted_context = [
            {
                "product_id": doc.metadata["id"],
                "product_name": doc.metadata["name"],
                "image_url": doc.metadata["image"],
                "stores": {
                    "store_name": doc.metadata["store"]
                },
                "product_prices": [{"price": float(doc.metadata["price"])}] if doc.metadata["price"] is not None else []
            }
            for doc in response.get('context', [])
        ]
        return {
            'answer': response['answer'],
            'context': formatted_context
        }
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)