import streamlit as st
from chatbot import get_answer

st.set_page_config(
    page_title="College FAQ Chatbot",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 College FAQ Chatbot")
st.write("Ask me anything about college!")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Get user question
user_question = st.chat_input("Type your question here...")

if user_question:
    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Generate chatbot response
    answer = get_answer(user_question)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()