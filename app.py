import streamlit as st
from agents.orchestrator import orchestrator

st.title("Autonomous AI Research Team")

query = st.text_input("Ask a research question")

if query:
    result = orchestrator(query)
    st.write(result)