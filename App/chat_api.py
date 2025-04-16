from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_all_products
from vectorstore import create_vector_store
from chain import create_qa_chain
from config import OPENAI_API_KEY

app = FastAPI()

# Configure CORS to allow requests from Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

class ChatRequest(BaseModel):
    query: str

# Initialize vector store and QA chain
try:
    products = get_all_products()
    print(f"Loaded {len(products)} products")
    vector_db = create_vector_store(products)
    qa_chain = create_qa_chain(vector_db)
except Exception as e:
    print(f"Failed to initialize vector store or QA chain: {e}")
    raise

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.query:
            raise HTTPException(status_code=400, detail="Missing query")
        
        response = qa_chain.invoke({'input': request.query})
        # Transform context to match frontend Product type
        formatted_context = [
            {
                "product_id": doc.metadata["id"],
                "product_name": doc.metadata["name"],
                "image_url": doc.metadata["image"],
                "stores": {"store_name": doc.metadata["store"]},
                "product_prices": [{"price": float(doc.metadata["price"])}]
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