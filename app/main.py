# File: app/main.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from agent import CostOptimizerAgent

st.set_page_config(page_title="Multi-Cloud Cost Optimization Agent", layout="wide")
st.title("🤖 Multi-Cloud Cost Optimization AI Agent")

# --- Session state setup ---
if "optimizer_agent" not in st.session_state:
    st.session_state.optimizer_agent = CostOptimizerAgent()

if "last_result" not in st.session_state:
    st.session_state.last_result = None

cloud_provider = st.selectbox("Select Cloud Provider", ["GCP", "AWS", "Azure"])
project_id = st.text_input("Enter Project/Account ID")
mode = st.selectbox("Choose Mode", ["Recommendations Only", "Execute Actions"])
freq = st.selectbox("Run Frequency", ["1 hour", "2 hours", "6 hours", "12 hours", "24 hours", "Weekly"])

run_button = st.button("Run Cost Optimizer")

if run_button and project_id:
    with st.spinner("Running cost optimization agent..."):
        response = st.session_state.optimizer_agent.run(cloud_provider, project_id, mode)
        st.session_state.last_result = response
        st.success("✅ Agent completed.")

if st.session_state.last_result:
    st.subheader("💡 Output")
    st.code(st.session_state.last_result)
