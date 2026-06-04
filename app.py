import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Page Configuration
st.set_page_config(page_title="AI Test Engineering Assistant", page_icon="🤖", layout="wide")

# 2. Header & Introduction
st.title("🤖 Test Engineering Assistant")
st.caption("A complete, free, high-performance solution for QA professionals using Llama 3 via Groq.")

# 3. Sidebar Configuration
with st.sidebar:
    st.header("Settings & Tools")
    qa_task = st.selectbox(
        "Choose QA Task:",
        [
            "Test Plan & Strategy",
            "Test Scenarios & Cases",
            "Automation Code Snippets",
            "Test Reports & Root Cause Analysis (RCA)"
        ]
    )
    st.info("The agent is powered by Llama 3. Provide detailed logs or requirements for best results.")

# 4. Core AI Logic (Safely Passing the Key Directly)
try:
    # Safely fetch the key from Streamlit's secrets manager
    api_key = st.secrets["GROQ_API_KEY"]
    
    # Initialize the Groq LLM with the explicit key and stable model name
    llm = ChatGroq(
        temperature=0.2, 
        groq_api_key=api_key,
        model_name="llama-3.1-70b-versatile"  # Updated stable model name
    )
    output_parser = StrOutputParser()

    base_instructions = (
        "You are an expert, world-class Lead QA Engineer and Automation Architect. "
        "Your task is to provide exceptionally detailed, comprehensive, and production-ready "
        "QA artifacts based on the user's input. Avoid generic answers. Include edge cases, "
        "structural frameworks, and best practices.\n\n"
    )

    # --- MODE 1: TEST PLAN & STRATEGY ---
    if qa_task == "Test Plan & Strategy":
        st.subheader("📋 Generate Test Plan & Strategy")
        user_input = st.text_area("Paste your Project Requirements or Product Description here:", height=200)
        
        if st.button("Generate Strategy"):
            if user_input:
                with st.spinner("Analyzing requirements and drafting strategy..."):
                    template = base_instructions + (
                        "Create a comprehensive Test Plan and Strategy for the following requirements:\n"
                        "{input}\n\n"
                        "Ensure you include: Scope (In/Out), Test Strategy (Functional, Security, Performance), "
                        "Environment Requirements, Risks & Mitigations, and Entry/Exit Criteria."
                    )
                    prompt = PromptTemplate(input_variables=["input"], template=template)
                    chain = prompt | llm | output_parser
                    response = chain.invoke({"input": user_input})
                    st.markdown(response)
            else:
                st.error("Please provide requirements first.")

    # --- MODE 2: TEST SCENARIOS & CASES ---
    elif qa_task == "Test Scenarios & Cases":
        st.subheader("🔍 Generate Test Scenarios & Detailed Cases")
        user_input = st.text_area("Enter Feature Details / User Stories:", height=200)
        
        if st.button("Generate Test Cases"):
            if user_input:
                with st.spinner("Mapping scenarios and drafting test cases..."):
                    template = base_instructions + (
                        "Generate detailed Test Scenarios and explicit Test Cases for the following feature:\n"
                        "{input}\n\n"
                        "For each test case, strictly provide: Test Case ID, Description, Pre-conditions, "
                        "Step-by-step Execution, Expected Result, and include Positive, Negative, and Boundary Edge Cases."
                    )
                    prompt = PromptTemplate(input_variables=["input"], template=template)
                    chain = prompt | llm | output_parser
                    response = chain.invoke({"input": user_input})
                    st.markdown(response)
            else:
                st.error("Please provide feature details.")

    # --- MODE 3: AUTOMATION CODE SNIPPETS ---
    elif qa_task == "Automation Code Snippets":
        st.subheader("💻 Automation Code Generator")
        framework = st.selectbox("Select Framework:", ["Playwright (Python)", "Selenium (Python)", "Playwright (JavaScript/TypeScript)"])
        user_input = st.text_area("Describe the workflow or paste the HTML elements/steps to automate:", height=150)
        
        if st.button("Generate Code"):
            if user_input:
                with st.spinner(f"Writing optimized {framework} code..."):
                    template = base_instructions + (
                        f"Write clean, highly maintainable automation code using {framework} based on this request:\n"
                        "{{input}}\n\n"
                        "Follow Page Object Model (POM) principles where applicable, include explicit waits, "
                        "proper assertions, and add comments explaining the code logic."
                    )
                    prompt = PromptTemplate(input_variables=["input"], template=template)
                    chain = prompt | llm | output_parser
                    response = chain.invoke({"input": user_input})
                    st.code(response, language='python' if 'Python' in framework else 'javascript')
            else:
                st.error("Please describe the workflow to automate.")

    # --- MODE 4: TEST REPORTS & RCA ---
    elif qa_task == "Test Reports & Root Cause Analysis (RCA)":
        st.subheader("📊 Test Execution Report & Root Cause Analysis")
        user_input = st.text_area("Paste Failure Logs, Execution Summary, or Bug details here:", height=200)
        
        if st.button("Analyze Failures"):
            if user_input:
                with st.spinner("Analyzing data and generating RCA..."):
                    template = base_instructions + (
                        "Analyze the following test execution results or failure logs:\n"
                        "{input}\n\n"
                        "Provide: A clean Executive Summary of the test run, a deep Root Cause Analysis (RCA) "
                        "of the failures, identified patterns, and concrete preventive/corrective actions."
                    )
                    prompt = PromptTemplate(input_variables=["input"], template=template)
                    chain = prompt | llm | output_parser
                    response = chain.invoke({"input": user_input})
                    st.markdown(response)
            else:
                st.error("Please paste failure logs or execution data.")

except KeyError:
    st.error("Setup Error: 'GROQ_API_KEY' was not found inside your Streamlit Cloud Secrets dashboard. Please check your spelling.")
except Exception as e:
    st.error(f"Execution Error: {str(e)}")