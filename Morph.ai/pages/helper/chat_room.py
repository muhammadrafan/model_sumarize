import streamlit as st
import requests
import pages.helper.voice as voice
OLLAMA_IP = "http://localhost:11434"

# Function to handle AI responses
def response(user_input, model_name):
    payload = {
        "model": model_name,
        "prompt": user_input,
        "stream": False
    }
    try:
        res = requests.post(f"{OLLAMA_IP}/api/generate", json=payload)
        res.raise_for_status()
        return res.json().get('response', 'No response')
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {e}"            

def display_chat_room(title, model_name, session_state_key):
    st.title(title)

    # Initialize chat history and AI thinking state
    if session_state_key not in st.session_state:
        initial_response = response("hello", model_name)
        st.session_state[session_state_key] = [{"role": "assistant", "content": initial_response}]
    
    if f"{session_state_key}_thinking" not in st.session_state:
        st.session_state[f"{session_state_key}_thinking"] = False

    thinking = st.session_state[f"{session_state_key}_thinking"]

    # Display chat history
    for msg in st.session_state[session_state_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Always enable input fields, but block processing if thinking
    user_input = st.chat_input("Type your message...")

    # Voice input button
    if st.button("🎤 Speak"):
        if not thinking:
            with st.spinner("Listening..."):
                user_text = voice.spToText()
                if user_text:
                    st.session_state[session_state_key].append({"role": "user", "content": user_text})
                    with st.chat_message("user"):
                        st.markdown(user_text)

                    st.session_state[f"{session_state_key}_thinking"] = True
                    st.rerun()
        else:
            st.warning("Wait for the assistant to finish responding first.")

    # Handle typed input (only if not thinking)
    if user_input:
        if not thinking:
            st.session_state[session_state_key].append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            st.session_state[f"{session_state_key}_thinking"] = True
            st.rerun()
        else:
            st.warning("Please wait for the assistant to finish before sending another message.")

    # Handle assistant response
    if thinking:
        last_user_msg = next((msg["content"] for msg in reversed(st.session_state[session_state_key])
                             if msg["role"] == "user"), None)

        if last_user_msg:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    ai_response = response(last_user_msg, model_name)
                    st.markdown(ai_response)

            st.session_state[session_state_key].append({"role": "assistant", "content": ai_response})
            st.session_state[f"{session_state_key}_thinking"] = False
            voice.SpeakText(ai_response)
            st.rerun()