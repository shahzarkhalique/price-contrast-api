Price Contrast Chatbot

The Price Contrast Chatbot is a conversational AI tool that enables users to query clothing products from a PostgreSQL database for price comparisons across stores in Pakistan’s clothing sector. Powered by LangChain and the ChatGPT API, it processes natural language queries (e.g., "cheapest black shirt" or "Outfitters products under 5,000 PKR") and returns relevant product details. The frontend, built with Next.js, provides a user-friendly chat interface, and the backend API uses Python for scalability.

Features





Natural Language Queries: Ask for products by price, brand, or type (e.g., "shirts over 2,000 PKR") in conversational language.



Top 5 Results with "See More": Displays up to five product results initially, with a "See More" button for additional items.



Database Integration: Queries a PostgreSQL database with stores and products tables for real-time product data.



Scalable API: Backend API supports deployment on platforms like Render.



Session Memory (optional): Configurable to maintain conversation context.

Tech Stack





Backend: Python, FastAPI, LangChain, ChatGPT API



Frontend: Next.js, TypeScript, Tailwind CSS



Database: PostgreSQL



Deployment: Render (or similar platforms)

Prerequisites





Python (v3.9 or higher)



Node.js (v16 or higher)



PostgreSQL (v13 or higher)



OpenAI API key (for ChatGPT integration)



Render account (for deployment, optional)

Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/price-contrast-chatbot.git
cd price-contrast-chatbot

2. Backend Setup





Navigate to the app directory:

cd app



Create a virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt



Set up environment variables in app/.env:

DATABASE_URL=postgresql://user:password@localhost:5432/price_contrast
OPENAI_API_KEY=your-openai-api-key



Initialize the PostgreSQL database:





Create a database named price_contrast.



Run the SQL schema (e.g., init.sql) to create stores and products tables:

psql -U user -d price_contrast -f init.sql



Run the chatbot API:

python chat_api.py

The API will launch on http://localhost:8000.

3. Frontend Setup





Navigate to the frontend directory:

cd frontend



Install dependencies:

npm install



Set up environment variables in frontend/.env.local:

NEXT_PUBLIC_API_URL=http://localhost:8000/api/chat



Start the development server:

npm run dev

4. Access the Chatbot





Open http://localhost:3000 in your browser to access the chat interface.



Enter queries like "cheapest black shirt" or "Outfitters products under 5,000 PKR" to interact with the chatbot.

Database Schema

The chatbot queries the following tables:





stores: Contains store details.





store_id (integer, primary key)



store_name (varchar)



products: Contains product details.





product_id (integer, primary key)



store_id (integer, foreign key)



product_name (varchar)



price (numeric)



Additional fields as needed (e.g., description)

Usage





Query Examples:





"Find products between 1,000 and 3,000 PKR"



"Show me Outfitters products under 5,000 PKR"



"List shirts over 2,000 PKR"



Response Format: The chatbot returns up to five products with details like product name, store, and price. A "See More" button displays additional results.



Error Handling: If the API fails (e.g., 404 error), the chatbot displays "Sorry, something went wrong."

Deployment

Backend





Deploy the backend to a platform like Render:





Create a new web service on Render.



Set environment variables (DATABASE_URL, OPENAI_API_KEY).



Deploy the app directory, ensuring chat_api.py is the entry point.



Update the frontend’s .env.local with the deployed API URL:

NEXT_PUBLIC_API_URL=https://your-render-url.onrender.com/api/chat

Frontend





Deploy the frontend to Vercel or Netlify:





Push the frontend directory to a repository.



Configure the NEXT_PUBLIC_API_URL environment variable during deployment.



Ensure the frontend calls /api/chat to avoid 404 errors.

Development Notes





Limiting Results: The backend retrieves up to 50 products (configurable in chain.py), and the frontend (ChatBot.tsx) displays five initially with a "See More" button.



Session Memory: To enable session-based memory, implement a session store (e.g., Redis) and update chat_api.py to track conversation history (planned feature).



Troubleshooting 404 Errors: Ensure the frontend calls /api/chat. Check ChatBot.tsx and .env.local for the correct API URL.



Performance Optimization: Cache the vector store (in vectorstore.py) and use incremental updates to reduce database query times.

Testing

To test the chatbot’s accuracy:





Use the provided Python script (test_chatbot.py) to compare responses with SQL queries.



Example test cases:





Products between 1,000 and 3,000 PKR



Outfitters products under 5,000 PKR



Shirts over 2,000 PKR



Evaluate metrics: accuracy, precision, recall.

Contributing

Contributions are welcome! Please:





Fork the repository.



Create a branch (git checkout -b feature/your-feature).



Commit changes (git commit -m "Add your feature").



Push the branch (git push origin feature/your-feature).



Open a pull request.
