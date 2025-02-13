import requests
import streamlit as st

# Function to get comparison of multiple products
def get_comparison_response(products):
    response = requests.post(
        "http://localhost:8000/compare/invoke",
        json={'input': {'products': products}}
    )
    print(response.status_code)
    print(response.json())
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Function to get personalized product recommendation
def get_recommendation_response(product_category, budget):
    response = requests.post(
        "http://localhost:8000/recommend/invoke",
        json={'input': {'product_category': product_category, 'budget': budget}}
    )
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Function to get detailed information about a product
def get_details_response(product):
    response = requests.post(
        "http://localhost:8000/details/invoke",
        json={'input': {'product': product}}
    )
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Function to get price history of a product
def get_price_history_response(product, time_period):
    response = requests.post(
        "http://localhost:8000/price-history/invoke",
        json={'input': {'product': product, 'time_period': time_period}}
    )
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Function to get user reviews summary
def get_reviews_response(product):
    response = requests.post(
        "http://localhost:8000/reviews/invoke",
        json={'input': {'product': product}}
    )
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Function to get alternative products
def get_alternatives_response(product):
    response = requests.post(
        "http://localhost:8000/alternatives/invoke",
        json={'input': {'product': product}}
    )
    return response.json().get('output', {}).get('content', 'Error: Unexpected response format')

# Streamlit UI
st.title("Price Contrast: Your Personal Shopping Assistant")

# Product Comparison
st.header("Compare Multiple Products")
products_input = st.text_area("Enter product names separated by commas", "Product A, Product B, Product C")
if st.button("Compare Products"):
    products = [product.strip() for product in products_input.split(',')]
    comparison_result = get_comparison_response(products)
    st.write(comparison_result)

# Personalized Recommendation
st.header("Get Personalized Product Recommendation")
product_category = st.text_input("Enter product category", "Electronics")
budget = st.number_input("Enter your budget", min_value=0)
if st.button("Get Recommendation"):
    recommendation_result = get_recommendation_response(product_category, budget)
    st.write(recommendation_result)

# Product Details
st.header("Get Product Details")
product = st.text_input("Enter product name for details", "Product A")
if st.button("Get Details"):
    details_result = get_details_response(product)
    st.write(details_result)

# Price History
st.header("Get Price History")
product = st.text_input("Enter product name for price history", "Product A")
time_period = st.text_input("Enter time period for price history", "1 year")
if st.button("Get Price History"):
    price_history_result = get_price_history_response(product, time_period)
    st.write(price_history_result)

# User Reviews Summary
st.header("Get User Reviews Summary")
product = st.text_input("Enter product name for reviews summary", "Product A")
if st.button("Get Reviews Summary"):
    reviews_result = get_reviews_response(product)
    st.write(reviews_result)

# Alternative Products
st.header("Get Alternative Products")
product = st.text_input("Enter product name for alternatives", "Product A")
if st.button("Get Alternatives"):
    alternatives_result = get_alternatives_response(product)
    st.write(alternatives_result)