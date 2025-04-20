from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_all_products
from vectorstore import create_vector_store, update_vector_store
from chain import create_qa_chain
from config import OPENAI_API_KEY

app = FastAPI(
    title="Price Contrast API",
    description="API for price comparison chatbot with session memory",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-nextjs-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    history: list[dict[str, str]] = []  # List of {user: str, bot: str}

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

@app.get("/")
async def root():
    return {"message": "Welcome to the Price Contrast API. Use POST /api/chat to interact with the chatbot."}

@app.head("/")
async def head_root():
    return {}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Missing query")

        greeting_keywords = ["hello", "hi", "hey", "how are you", "good morning", "thank you"]
        query_lower = request.query.lower().strip()
        is_greeting = query_lower in greeting_keywords
        print(f"Query: '{request.query}', Is Greeting: {is_greeting}, History Length: {len(request.history)}")

        if is_greeting:
            answer = "Hello! How can I assist you today?"
            context = []
        else:
            if not products or not qa_chain:
                print("No products or QA chain available")
                answer = "No products available. Please try again later."
                context = []
            else:
                # Format history for QA chain
                history_str = "\n".join([f"User: {msg['user']}\nBot: {msg['bot']}" for msg in request.history if msg['user'] and msg['bot']])
                input_with_history = f"Previous conversation:\n{history_str}\nCurrent question: {request.query}" if history_str else request.query
                response_data = qa_chain.invoke({'input': input_with_history})
                print(f"QA Chain Response: {response_data}")
                answer = response_data['answer']
                context = [
                    {
                        "product_id": doc.metadata["id"],
                        "product_name": doc.metadata["name"],
                        "image_url": doc.metadata["image"],
                        "stores": {
                            "store_name": doc.metadata["store"]
                        },
                        "product_prices": [{"price": float(doc.metadata["price"])}] if doc.metadata["price"] is not None else []
                    }
                    for doc in response_data.get('context', [])
                ]

        return {
            "answer": answer,
            "context": context
        }
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)