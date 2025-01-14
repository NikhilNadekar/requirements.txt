import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import math

# Apply dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
    }
    .stNumberInput > div > div > input {
        background-color: #262730;
        color: #FAFAFA;
    }
    </style>
    """, unsafe_allow_html=True)

st.header('Dividend Calculator')

# Symbol input
ticker = st.text_input('Symbol Code', 'INFY')

# Initialize current_price as None
current_price = None

# Fetch stock price
url = f'https://www.google.com/finance/quote/{ticker}:NSE'

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    class1 = "YMlKec fxKbKc"

    # Find the price element and extract text
    price_element = soup.find(class_=class1)
    if price_element:
        current_price = float(price_element.text.strip()[1:].replace(",", ""))
        st.markdown(f"##### Current Price of {ticker}: ₹{current_price:,.2f}")
    else:
        st.error("Unable to fetch the price. Please check the symbol code.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Investment")
    # Investment input
    investment = st.number_input("Your Investment (₹)", min_value=0.0, value=0.0, step=1000.0)
    
    # Calculate quantity
    if current_price and investment > 0:
        quantity = math.floor(investment / current_price)
    else:
        quantity = 0

    st.subheader("Dividend")
    # Dividend input
    dividend_price = st.number_input("Dividend Price per Share (₹)", min_value=0.0, value=0.0, step=0.5)
    
    # Calculate profit from dividend
    if quantity > 0 and dividend_price > 0:
        dividend_profit = dividend_price * quantity

# Additional market information
if current_price:
    st.markdown("---")
    st.subheader("Investment Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.metric("Number of Shares", f"{quantity}")
    with summary_col2:
        if dividend_price > 0:
            st.metric("Expected Dividend Return", f"₹{dividend_profit:,.2f}")