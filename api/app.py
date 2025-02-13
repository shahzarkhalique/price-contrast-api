from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Initialize models
model = ChatOpenAI()
llm = Ollama(model="deepseek-r1")

# Define prompts
prompt_compare = ChatPromptTemplate.from_template("Provide a detailed comparison of {product1} and {product2} including features, prices, and user reviews.")
prompt_recommend = ChatPromptTemplate.from_template("Generate a personalized product recommendation for a user looking for {product_category} within a budget of {budget}.")
prompt_details = ChatPromptTemplate.from_template("Provide detailed information about {product}, including its features, price, and user reviews.")
prompt_price_history = ChatPromptTemplate.from_template("Provide the price history of {product} over the past {time_period}.")
prompt_reviews = ChatPromptTemplate.from_template("Summarize the user reviews for {product}, highlighting the main pros and cons.")
prompt_alternatives = ChatPromptTemplate.from_template("Suggest alternative products to {product} that are within a similar price range and have similar features.")

# Add routes
add_routes(
    app,
    prompt_compare | model,
    path="/compare"
)

add_routes(
    app,
    prompt_recommend | model,
    path="/recommend"
)

add_routes(
    app,
    prompt_details | model,
    path="/details"
)

add_routes(
    app,
    prompt_price_history | model,
    path="/price-history"
)

add_routes(
    app,
    prompt_reviews | model,
    path="/reviews"
)

add_routes(
    app,
    prompt_alternatives | model,
    path="/alternatives"
)

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)