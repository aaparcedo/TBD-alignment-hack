import os
from anthropic import Anthropic
import streamlit as st
from streamlit_feedback import streamlit_feedback


anthropic_api_key = os.getenv("ANTHROPIC_KEY")


# INITIALIZATIONS
if "responses" not in st.session_state:
    st.session_state["responses"] = {
        "Q1": None,
        "Q2": None
    }
if "selections" not in st.session_state:
    st.session_state["selections"] = {
        "Q1": None,
        "Q2": None
    }
if "feedback" not in st.session_state:
    st.session_state["feedback"] = {
        "Q1": None,
        "Q2": None
    }
    
    
# HANDLES
def handle_feedback(feedback, question_id):
    # Convert thumbs to binary (0 for down, 1 for up)
    score = 1 if feedback["score"] == "👍" else 0
    st.session_state["feedback"][question_id] = score
    return feedback

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
    
    
st.title("🤔 Are you sure about that?")

# Questions and their respective answers
questions = {
    "Q1": {"question": "What is 2+2?", "answer": "4"},
    "Q2": {"question": "What color is made from the combination of blue and red?", "answer": "Purple"}
}

# Create tabs
tab1, tab2, tab3 = st.tabs(["Q1", "Q2", "Summary"])

# Tab 1 content
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("Model 1")
        st.chat_message("user").write(questions["Q1"]["question"] + ' ' + questions["Q1"]["answer"])

    with col2:
        st.header("Model 2")
        st.chat_message("user").write(questions["Q1"]["question"] + ' ' + questions["Q1"]["answer"])

    # Radio buttons for Q1
    options = ["Model A", "Model B", "Both", "Neither"]
    st.session_state["selections"]["Q1"] = st.radio(
        "Select an option for Q1:",
        options,
        key="radio_Q1",
        index=options.index(st.session_state["selections"]["Q1"]) if st.session_state["selections"]["Q1"] else 0
    )

    # Evaluate button for Q1
    if st.button("Evaluate", key="evaluate_Q1"):
        with st.spinner("Generating response..."):
            st.session_state["responses"]["Q1"] = get_claude_response(questions["Q1"]["question"])
        st.rerun()
        
    if st.session_state["responses"]["Q1"]:
        st.write(f"Feedback for Q1:")
        st.chat_message("assistant").write(st.session_state["responses"]["Q1"])
        
        # Add feedback component
        feedback = streamlit_feedback(
            feedback_type="thumbs",
            key=f"feedback_Q1",
            on_submit=lambda f: handle_feedback(f, "Q1")
        )

# Tab 2 content
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.header("Model 1")
        st.chat_message("user").write(questions["Q2"]["question"] + ' ' + questions["Q2"]["answer"])

    with col2:
        st.header("Model 2")
        st.chat_message("user").write(questions["Q2"]["question"] + ' ' + questions["Q2"]["answer"])

    # Radio buttons for Q2
    options = ["Model A", "Model B", "Both", "Neither"]
    st.session_state["selections"]["Q2"] = st.radio(
        "Select an option for Q2:",
        options,
        key="radio_Q2",
        index=options.index(st.session_state["selections"]["Q2"]) if st.session_state["selections"]["Q2"] else 0
    )

    # Evaluate button for Q2
    if st.button("Evaluate", key="evaluate_Q2"):
        with st.spinner("Generating response..."):
            st.session_state["responses"]["Q2"] = get_claude_response(questions["Q2"]["question"])
        st.rerun()
        
    if st.session_state["responses"]["Q2"]:
        st.write(f"Feedback for Q2:")
        st.chat_message("assistant").write(st.session_state["responses"]["Q2"])
        
        # Add feedback component
        feedback = streamlit_feedback(
            feedback_type="thumbs",
            key=f"feedback_Q2",
            on_submit=lambda f: handle_feedback(f, "Q2")
        )

# Tab 3 (Summary) content
with tab3:
    st.header("Summary")
    
    for q_id in ["Q1", "Q2"]:
        st.subheader(f"Question {q_id}")
        
        # Display question and answer
        st.write(f"**Question:** {questions[q_id]['question']}")
        st.write(f"**Correct Answer:** {questions[q_id]['answer']}")
        
        # Display selection if made
        if st.session_state["selections"][q_id]:
            st.write(f"**Selected Option:** {st.session_state['selections'][q_id]}")
        else:
            st.write("**Selected Option:** No selection made")
            
        # Display Claude's response if available
        if st.session_state["responses"][q_id]:
            st.write("**Claude's Response:**")
            st.chat_message("assistant").write(st.session_state["responses"][q_id])
        else:
            st.write("**Claude's Response:** No response generated")
            
        # Display feedback if available
        if st.session_state["feedback"][q_id] is not None:
            feedback_text = "👍 Thumbs Up" if st.session_state["feedback"][q_id] == 1 else "👎 Thumbs Down"
            st.write(f"**Feedback:** {feedback_text}")
        else:
            st.write("**Feedback:** No feedback provided")
            
        st.divider()

# Clear All Responses button at the bottom
if st.button("Clear All Responses"):
    st.session_state["responses"] = {
        "Q1": None,
        "Q2": None
    }
    st.session_state["selections"] = {
        "Q1": None,
        "Q2": None
    }
    st.session_state["feedback"] = {
        "Q1": None,
        "Q2": None
    }
    st.rerun()