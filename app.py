import streamlit as st
from orchestrator import run_system

st.title("Autonomous AI Research Team")

query = st.text_input("Ask a research question")

if query:
    result = run_system(query)
    st.write(result)