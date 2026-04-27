import streamlit as st
from dotenv import load_dotenv
from api_client import send_chat_request

load_dotenv()

st.set_page_config(page_title="Azure AI Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    /* Styling for Streamlit elements to give a more modern, Azure-like aesthetic */
    .stApp {
        background-color: #f7f9fa;
    }
    .stAppHeader {
        background-color: #f7f9fa;
        color: #1f2937;
    }
    .stChatInputContainer {
        border-radius: 12px;
    }
    .stChatMessage {
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 5px;
    }
    /* Add a subtle shadow for elements */
    .stChatInput {
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)


st.title("🤖 Azure AI Chatbot")
st.markdown("Ask natural language questions to retrieve context-aware answers.")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is on your mind?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call backend function app
            response = send_chat_request(st.session_state.messages)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
