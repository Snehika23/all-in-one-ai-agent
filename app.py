import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.prompts import PromptTemplate
import pandas as pd
import os

# API Key from Streamlit secrets
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
llm = ChatAnthropic(model="claude-sonnet-4-6")

# 1. DATA ANALYST AGENT
if agent_type == "📊 Data Analyst Agent":
    st.header("📊 Data Analyst Agent")
    st.write("Upload a CSV file and ask anything about your data!")

    file = st.file_uploader("Upload your CSV file", type="csv")

    if file:
        df = pd.read_csv(file)
        st.success(f"✅ File uploaded! {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head())

        question = st.text_input("Ask anything about your data 👇",
                                  placeholder="e.g. What is the average sales? Which region has highest profit?")

        if st.button("Analyze 🔍") and question:
            with st.spinner("Analyzing your data..."):
                agent = create_pandas_dataframe_agent(
                    llm, df,
                    verbose=True,
                    allow_dangerous_code=True
                )
                result = agent.run(question)
                st.success("✅ Analysis Complete!")
                st.write(result)

# 2. RESEARCH AGENT
elif agent_type == "🔍 Research Agent":
    st.header("🔍 Research Agent")
    st.write("Ask anything and I'll search the web and summarize it for you!")

    query = st.text_input("What do you want to research? 👇",
                           placeholder="e.g. Latest trends in Data Analytics 2024")

    if st.button("Search & Summarize 🔍") and query:
        with st.spinner("Searching the web..."):
            search = DuckDuckGoSearchRun()
            agent = initialize_agent(
                tools=[search],
                llm=llm,
                agent="zero-shot-react-description",
                verbose=True
            )
            result = agent.run(query)
            st.success("✅ Research Complete!")
            st.write(result)

# 3. EMAIL AGENT
elif agent_type == "📧 Email Agent":
    st.header("📧 Email Agent")
    st.write("Describe what you want to say and I'll write the perfect email!")

    col1, col2 = st.columns(2)

    with col1:
        context = st.text_area("What is the email about? 👇",
                                placeholder="e.g. Following up on a job application for Data Analyst role at Google",
                                height=150)

    with col2:
        tone = st.selectbox("Select Tone", ["Professional", "Casual", "Formal", "Friendly"])
        email_type = st.selectbox("Email Type", ["Follow Up", "Introduction", "Job Application",
                                                   "Thank You", "Request", "Complaint"])

    if st.button("Write Email ✉️") and context:
        with st.spinner("Writing your email..."):
            prompt = PromptTemplate.from_template(
                """Write a {tone} {email_type} email about: {context}
                Include: Subject line, greeting, body, and sign off.
                Make it concise and impactful."""
            )
            chain = prompt | llm
            result = chain.invoke({
                "context": context,
                "tone": tone,
                "email_type": email_type
            })
            st.success("✅ Email Ready!")
            st.write(result.content)

# 4. CUSTOMER SUPPORT AGENT
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
            prompt = PromptTemplate.from_template(
                """You are an expert customer support agent for {domain} industry.
                Answer this question clearly and professionally: {question}
                Provide step by step solution if needed."""
            )
            chain = prompt | llm
            result = chain.invoke({
                "question": question,
                "domain": domain
            })
            st.success("✅ Answer Ready!")
            st.write(result.content)
