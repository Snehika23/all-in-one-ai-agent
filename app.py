import streamlit as st
import google.generativeai as genai
import pandas as pd

# Page config
st.set_page_config(page_title="All-in-One AI Agent", page_icon="🤖", layout="wide")
st.title("🤖 All-in-One AI Agent")
st.markdown("Powered by Google Gemini AI ✨")

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

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
    st.write("Upload a CSV file and ask anything about your data!")

    file = st.file_uploader("Upload your CSV file", type="csv")

    if file:
        df = pd.read_csv(file)
        st.success(f"✅ {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head(10))

        question = st.text_input("Ask anything about your data 👇",
                                  placeholder="e.g. What are the key insights?")

        if st.button("Analyze 🔍") and question:
            with st.spinner("Analyzing your data..."):
                prompt = f"""You are a Data Analyst. Analyze this dataset and answer: {question}

Columns: {list(df.columns)}
Sample data (first 50 rows):
{df.head(50).to_string()}

Basic Stats:
{df.describe().to_string()}

Give a clear structured answer with key insights."""

                st.write(ask_gemini(prompt))

# ── 2. RESEARCH AGENT ──
elif agent_type == "🔍 Research Agent":
    st.header("🔍 Research Agent")
    st.write("Ask anything and I'll give you a detailed summary!")

    query = st.text_input("What do you want to research? 👇",
                           placeholder="e.g. Latest trends in Data Analytics 2024")

    if st.button("Research 🔍") and query:
        with st.spinner("Researching..."):
            prompt = f"""Give a detailed, well structured answer about: {query}

Include:
- Key points
- Latest trends
- Important facts
- Summary

Format with clear bullet points and headings."""

            st.write(ask_gemini(prompt))

# ── 3. EMAIL AGENT ──
elif agent_type == "📧 Email Agent":
    st.header("📧 Email Agent")
    st.write("Describe what you want to say and I'll write the perfect email!")

    col1, col2 = st.columns(2)
    with col1:
        context = st.text_area("What is the email about? 👇",
                                placeholder="e.g. Following up on a Data Analyst job application",
                                height=150)
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual", "Formal", "Friendly"])
        email_type = st.selectbox("Type", [
            "Follow Up", "Introduction", "Job Application",
            "Thank You", "Request", "Complaint"
        ])

    if st.button("Write Email ✉️") and context:
        with st.spinner("Writing your email..."):
            prompt = f"""Write a {tone} {email_type} email about: {context}

Include:
- Subject line
- Professional greeting  
- Clear body
- Call to action
- Sign off

Keep it concise and impactful."""

            st.write(ask_gemini(prompt))

# ── 4. CUSTOMER SUPPORT AGENT ──
elif agent_type == "💬 Customer Support Agent":
    st.header("💬 Customer Support Agent")
    st.write("Ask any business or support related question!")

    question = st.text_area("What do you need help with? 👇",
                              placeholder="e.g. How do I handle a refund request?",
                              height=150)

    domain = st.selectbox("Domain", [
        "E-commerce", "Banking", "Healthcare",
        "Education", "Retail", "General"
    ])

    if st.button("Get Answer 💬") and question:
        with st.spinner("Finding the best answer..."):
            prompt = f"""You are an expert customer support agent for {domain} industry.

Question: {question}

Provide a clear, professional answer with step by step solution if needed."""

            st.write(ask_gemini(prompt))
