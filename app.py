import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
import pandas as pd
import os

# API Key
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

# Page config
st.set_page_config(page_title="All-in-One AI Agent", page_icon="🤖", layout="wide")
st.title("🤖 All-in-One AI Agent")
st.markdown("Powered by Claude AI")

# Sidebar
agent_type = st.sidebar.selectbox("Choose Your Agent 👇", [
    "📊 Data Analyst Agent",
    "🔍 Research Agent",
    "📧 Email Agent",
    "💬 Customer Support Agent"
])
st.sidebar.markdown("---")
st.sidebar.markdown("Built by **Snehika Amudalapalli**")

# LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", max_tokens=1024)

# ── 1. DATA ANALYST AGENT ──
if agent_type == "📊 Data Analyst Agent":
    st.header("📊 Data Analyst Agent")
    st.write("Upload a CSV file and ask anything about your data!")

    file = st.file_uploader("Upload your CSV file", type="csv")

    if file:
        df = pd.read_csv(file)
        st.success(f"✅ File uploaded! {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head(10))

        # Take sample and convert to string
        df_sample = df.head(100)
        df_info = f"""
Columns: {list(df.columns)}
Shape: {df.shape}
Sample data (first 5 rows):
{df_sample.head().to_string()}

Basic stats:
{df_sample.describe().to_string()}
        """

        question = st.text_input("Ask anything about your data 👇",
                                  placeholder="e.g. What are the key insights? Summarize this data.")

        if st.button("Analyze 🔍") and question:
            with st.spinner("Analyzing your data..."):
                prompt = f"""You are a Data Analyst. Analyze this dataset and answer the question.

Dataset Info:
{df_info}

Question: {question}

Give a clear, structured answer with insights."""

                result = llm.invoke(prompt)
                st.success("✅ Analysis Complete!")
                st.write(result.content)

# ── 2. RESEARCH AGENT ──
elif agent_type == "🔍 Research Agent":
    st.header("🔍 Research Agent")
    st.write("Ask anything and I'll search the web and summarize it!")

    query = st.text_input("What do you want to research? 👇",
                           placeholder="e.g. Latest trends in Data Analytics 2024")

    if st.button("Search & Summarize 🔍") and query:
        with st.spinner("Searching the web..."):
            try:
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
                result_text = "\n".join([r['body'][:300] for r in results])
                prompt = f"Summarize these search results in 5 clear bullet points about '{query}':\n\n{result_text}"
                summary = llm.invoke(prompt)
                st.success("✅ Research Complete!")
                st.write(summary.content)
            except Exception as e:
                # Fallback to Claude's own knowledge
                prompt = f"Give me a detailed summary about: {query}. Include latest trends and key points in bullet points."
                summary = llm.invoke(prompt)
                st.success("✅ Research Complete!")
                st.write(summary.content)

# ── 3. EMAIL AGENT ──
elif agent_type == "📧 Email Agent":
    st.header("📧 Email Agent")
    st.write("Describe what you want to say and I'll write the perfect email!")

    col1, col2 = st.columns(2)
    with col1:
        context = st.text_area("What is the email about? 👇",
                                placeholder="e.g. Following up on a job application for Data Analyst role",
                                height=150)
    with col2:
        tone = st.selectbox("Select Tone", ["Professional", "Casual", "Formal", "Friendly"])
        email_type = st.selectbox("Email Type", [
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

            result = llm.invoke(prompt)
            st.success("✅ Email Ready!")
            st.write(result.content)

# ── 4. CUSTOMER SUPPORT AGENT ──
elif agent_type == "💬 Customer Support Agent":
    st.header("💬 Customer Support Agent")
    st.write("Ask any business or support related question!")

    question = st.text_area("What do you need help with? 👇",
                              placeholder="e.g. How do I handle a refund request from a customer?",
                              height=150)

    domain = st.selectbox("Select Domain", [
        "E-commerce", "Banking", "Healthcare",
        "Education", "Retail", "General"
    ])

    if st.button("Get Answer 💬") and question:
        with st.spinner("Finding the best answer..."):
            prompt = f"""You are an expert customer support agent for {domain} industry.
            
Question: {question}

Provide a clear, professional answer with step by step solution if needed."""

            result = llm.invoke(prompt)
            st.success("✅ Answer Ready!")
            st.write(result.content)
