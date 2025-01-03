import streamlit as st
from openai import OpenAI
from menu import menu

# Redirect to homepage.py if not logged in
menu()

st.title("Squeaky")

st.write(f"It's nice to talk to you again, {st.session_state.username}!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

prompt= st.chat_input("What is on your mind?")
# React to user input
if prompt:
    with st.chat_message(name="user", avatar="visual_assets\Pessoa.png"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar":"visual_assets\Pessoa.png"})
    # Display assistant response in chat message container
    with st.chat_message(name="assistant", avatar="visual_assets\Ratinho.png"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar":"visual_assets\Ratinho.png"})
