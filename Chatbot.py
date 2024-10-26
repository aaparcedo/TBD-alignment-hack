import os
from anthropic import Anthropic
import streamlit as st

# Use environment variable for API key
anthropic_api_key = os.getenv("ANTHROPIC_KEY")

# Predefined questions
Q1 = "What are the three laws of robotics?"
Q2 = "Explain the concept of artificial consciousness in simple terms."

# Initialize session states
if "response1" not in st.session_state:
    st.session_state["response1"] = None
if "response2" not in st.session_state:
    st.session_state["response2"] = None

def get_claude_response(question):
    try:
        client = Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}]
        )
        return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create two columns
col1, col2 = st.columns(2)

# Display in columns with chat-like interface
with col1:
    st.title("Question 1")
    # User message with icon
    st.chat_message("user").write(Q1)
    if st.session_state["response1"]:
        # Assistant message with icon
        st.chat_message("assistant").write(st.session_state["response1"])

with col2:
    st.title("Question 2")
    # User message with icon
    st.chat_message("user").write(Q2)
    if st.session_state["response2"]:
        # Assistant message with icon
        st.chat_message("assistant").write(st.session_state["response2"])

# Centered buttons
col_buttons = st.columns([2, 1, 2])
with col_buttons[1]:
    if st.button("Generate Responses"):
        with st.spinner("Generating responses..."):
            st.session_state["response1"] = get_claude_response(Q1)
            st.session_state["response2"] = get_claude_response(Q2)
            st.rerun()

    if st.button("Clear Responses"):
        st.session_state["response1"] = None
        st.session_state["response2"] = None
        st.rerun()