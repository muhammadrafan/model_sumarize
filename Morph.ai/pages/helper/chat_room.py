import streamlit as st
import requests
import os
import json
from pathlib import Path
import pages.helper.voice as voice
import re

# Import shared configuration
from pages.helper.config import OLLAMA_IP, MODEL_NAME
from pages.helper.summary_manager import (
    get_context_for_sidekick, 
    get_context_for_psycholog, 
    get_context_for_conflict_resolution,
    analyze_and_recommend_services,
    get_employee_summary_by_name
)

# Function to handle AI responses with context
def response(user_input, model_name, context=None, current_page=None):
    """
    Get response from Ollama API with optional context
    """
    # Add context to prompt if available
    prompt = user_input
    if context:
        prompt = f"{context}\n\nUser: {user_input}\n\nAssistant:"
    
    # Analyze input for potential recommendations (only for sidekick)
    recommendation = ""
    if current_page == "sidekick":
        # Extract employee name if mentioned
        employee_name = extract_employee_name(user_input)
        employee_data = None
        if employee_name:
            employee_data = get_employee_summary_by_name(employee_name)
        
        # Check if we need to recommend services
        need_psych, need_conflict, rec_text = analyze_and_recommend_services(user_input, employee_data)
        if need_psych or need_conflict:
            recommendation = rec_text
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        res = requests.post(f"{OLLAMA_IP}/api/generate", json=payload)
        res.raise_for_status()
        ai_response = res.json().get('response', 'No response')
        
        # Add recommendation if needed
        if recommendation:
            ai_response += f"\n\n{recommendation}"
            
        return ai_response
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {e}"

def extract_employee_name(text):
    """
    Try to extract an employee name from text
    Uses pattern matching for common phrases
    """
    patterns = [
        r"about\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
        r"employee\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})'s\s+performance",
        r"how\s+is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+doing",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return None

def display_chat_room(title, model_name, session_state_key):
    st.title(title)

    # Initialize chat history and AI thinking state
    if session_state_key not in st.session_state:
        # Get appropriate context based on page
        context = None
        if session_state_key == "sidekick_msg":
            context = get_context_for_sidekick()
        elif session_state_key == "psycholog_msg":
            context = get_context_for_psycholog()
        elif session_state_key == "conflict_msg":
            context = get_context_for_conflict_resolution()
        
        # Generate initial response
        initial_response = response("hello", model_name, context, current_page=get_page_type(session_state_key))
        st.session_state[session_state_key] = [{"role": "assistant", "content": initial_response}]
    
    if f"{session_state_key}_thinking" not in st.session_state:
        st.session_state[f"{session_state_key}_thinking"] = False
    
    # Store context in session state if not already present
    if f"{session_state_key}_context" not in st.session_state:
        if session_state_key == "sidekick_msg":
            st.session_state[f"{session_state_key}_context"] = get_context_for_sidekick()
        elif session_state_key == "psycholog_msg":
            st.session_state[f"{session_state_key}_context"] = get_context_for_psycholog()
        elif session_state_key == "conflict_msg":
            st.session_state[f"{session_state_key}_context"] = get_context_for_conflict_resolution()
        else:
            st.session_state[f"{session_state_key}_context"] = None

    thinking = st.session_state[f"{session_state_key}_thinking"]
    context = st.session_state[f"{session_state_key}_context"]

    # Display chat history
    for msg in st.session_state[session_state_key]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Option to change employee context
    if session_state_key in ["sidekick_msg", "psycholog_msg", "conflict_msg"]:
        with st.sidebar:
            st.subheader("Employee Context")
            employee_name = st.text_input("Enter employee name for context:")
            if st.button("Update Context"):
                if session_state_key == "sidekick_msg":
                    new_context = get_context_for_sidekick(employee_name)
                elif session_state_key == "psycholog_msg":
                    new_context = get_context_for_psycholog(employee_name)
                elif session_state_key == "conflict_msg":
                    new_context = get_context_for_conflict_resolution(employee_name)
                
                st.session_state[f"{session_state_key}_context"] = new_context
                st.success(f"Context updated for {employee_name if employee_name else 'all employees'}")

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
                    # Get context if available
                    context = st.session_state.get(f"{session_state_key}_context")
                    current_page = get_page_type(session_state_key)
                    
                    # Generate response with context
                    ai_response = response(last_user_msg, model_name, context, current_page)
                    st.markdown(ai_response)

            st.session_state[session_state_key].append({"role": "assistant", "content": ai_response})
            st.session_state[f"{session_state_key}_thinking"] = False
            voice.SpeakText(ai_response)
            st.rerun()

def get_page_type(session_state_key):
    """
    Get the page type from the session state key
    """
    if "sidekick" in session_state_key:
        return "sidekick"
    elif "psycholog" in session_state_key:
        return "psycholog"
    elif "conflict" in session_state_key:
        return "conflict"
    else:
        return None