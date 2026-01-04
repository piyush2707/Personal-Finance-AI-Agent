import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from processor import process_statement, get_ai_prompt

# .env file se API Key load karna
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="AI Finance Agent", layout="wide")

st.title("💰 AI Personal Finance Agent")
st.write("Upload your bank statement and get professional financial advice instantly.")

# Sidebar for API Key (Optionally)
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("Upload your Bank Statement (CSV)", type=["csv"])


if uploaded_file is not None:
    # Processing the data
    df, summary = process_statement(uploaded_file)
    
    # Dashboard Layout
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${summary['total_income']}")
    col2.metric("Total Spent", f"${summary['total_spent']}")
    col3.metric("Current Balance", f"${summary['balance']}")

    st.subheader("Transaction Overview")
    st.dataframe(df)

    # AI Analysis Section
    if st.button("Generate AI Financial Advice"):
        with st.spinner("Analyzing your habits..."):
            model = genai.GenerativeModel('gemini-pro')
            prompt = get_ai_prompt(summary)
            response = model.generate_content(prompt)
            
            st.markdown("---")
            st.subheader("🤖 AI Financial Advisor Says:")
            st.write(response.text)

else:
    st.info("Please upload a CSV file to begin. Make sure it has 'Date', 'Description', and 'Amount' columns.")
  
