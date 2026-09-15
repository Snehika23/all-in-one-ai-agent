import streamlit as st
import anthropic
import pandas as pd

# Page config
st.set_page_config(page_title="All-in-One AI Agent", page_icon="🤖", layout="wide")
st.title("🤖 All-in-One AI Agent")
st.markdown("Powered by Claude AI")

# Direct Anthropic client - no LangChain!
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def ask_claude(prompt):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# Sidebar
agent_type = st.sidebar.selectbox("Choose Your Agent 👇", [
    "📊 Data Analyst Agent",
    "🔍 Research Agent",
    "📧 Email Agent",
    "💬 Customer Support Agent"
])
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Snehika Amudalapalli**")

# ── 1. DATA ANALYST AGENT ──
if agent_type == "📊 Data Analyst Agent":
    st.header("📊 Data Analyst Agent")
    file = st.file_uploader("Upload your CSV file", type="csv")
    if file:
        df = pd.read_csv(file)
        st.success(f"✅ {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head(10))
        question = st.text_input("Ask anything about your data 👇")
        if st.button("Analyze 🔍") and question:
            with st.spinner("Analyzing..."):
                prompt = f"""Analyze this dataset and answer: {question}

Columns: {list(df.columns)}
Sample data:
{df.head(50).to_string()}
Stats:
{df.describe().to_string()}"""
                st.write(ask_claude(prompt))

# ── 2. RESEARCH AGENT ──
elif agent_type == "🔍 Research Agent":
    st.header("🔍 Research Agent")
    query = st.text_input("What do you want to research? 👇")
    if st.button("Research 🔍") and query:
        with st.spinner("Researching..."):
            prompt = f"Give a detailed, well structured summary about: {query}. Include key points, latest trends and insights in bullet points."
            st.write(ask_claude(prompt))

# ── 3. EMAIL AGENT ──
elif agent_type == "📧 Email Agent":
    st.header("📧 Email Agent")
    col1, col2 = st.columns(2)
    with col1:
        context = st.text_area("What is the email about? 👇", height=150)
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual", "Formal", "Friendly"])
        email_type = st.selectbox("Type", ["Follow Up", "Introduction",
                                            "Job Application", "Thank You",
                                            "Request", "Complaint"])
    if st.button("Write Email ✉️") and context:
        with st.spinner("Writing..."):
            prompt = f"Write a {tone} {email_type} email about: {context}. Include subject line, greeting, body, and sign off."
            st.write(ask_claude(prompt))

# ── 4. CUSTOMER SUPPORT AGENT ──
elif agent_type == "💬 Customer Support Agent":
    st.header("💬 Customer Support Agent")
    question = st.text_area("What do you need help with? 👇", height=150)
    domain = st.selectbox("Domain", ["E-commerce", "Banking",
                                      "Healthcare", "Education",
                                      "Retail", "General"])
    if st.button("Get Answer 💬") and question:
        with st.spinner("Finding answer..."):
            prompt = f"You are an expert {domain} customer support agent. Answer this clearly with steps if needed: {question}"
            st.write(ask_claude(prompt))
