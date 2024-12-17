import streamlit as st
from dotenv import load_dotenv
import os
import openai
from openai import OpenAI

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=openai.api_key ,
    base_url="https://api.x.ai/v1",
)

# Page Configuration
st.set_page_config(page_title="Shivi", page_icon="💬", layout="wide")

# Title
st.title("💬 Shivi ")

# Initialize the conversation history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display the conversation
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Append user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using OpenAI API
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
            {"role": "user", "content":user_input },
        ],
    )
    print("response:::::::::::::::",response)
    # Append assistant response to session state
    st.session_state["messages"].append({"role": "assistant", "content": response.choices[0].message.content})

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response.choices[0].message.content)