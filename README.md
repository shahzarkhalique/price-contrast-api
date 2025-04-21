# Price Contrast Chatbot

The Price Contrast Chatbot is a conversational AI tool for querying clothing products from a PostgreSQL database, enabling price comparisons across stores in Pakistan’s clothing sector. Built with LangChain and the ChatGPT API, it handles natural language queries (e.g., "cheapest black shirt" or "Outfitters products under 5,000 PKR") and returns relevant product details. The frontend uses Next.js for a user-friendly chat interface, and the backend API is built with Python and FastAPI for scalability.

## Features

- **Natural Language Queries**: Search for products by price, brand, or type (e.g., "shirts over 2,000 PKR").
- **Top 5 Results with "See More"**: Displays up to five products initially, with a button to view more.
- **Database Integration**: Queries `stores` and `products` tables in PostgreSQL for real-time data.
- **Scalable API**: Deployable on platforms like Render for reliable performance.
- **Session Memory** (optional): Configurable to maintain conversation context.

## Tech Stack

- **Backend**: Python, FastAPI, LangChain, ChatGPT API
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Render (or similar platforms)

## Prerequisites

- Python (v3.9 or higher)
- Node.js (v16 or higher)
- PostgreSQL (v13 or higher)
- OpenAI API key (for ChatGPT integration)
- Render account (optional, for deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/price-contrast-chatbot.git
cd price-contrast-chatbot
