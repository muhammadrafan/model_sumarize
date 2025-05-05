from pages.helper.chat_room import display_chat_room
import streamlit as st
from pages.helper.config import MODEL_NAME

st.set_page_config(page_title="Sidekick", page_icon="📈")

# Custom CSS for the navigation
st.markdown("""
<style>
    .navigation {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    .nav-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Sidekick page description
st.markdown("""
### 🤖 Sidekick Assistant
Your personal assistant for employee performance management. I can:
- Help you understand employee performance data
- Answer questions about specific employees
- Suggest which employees might need psychological support or conflict resolution
- Assist with performance improvement plans

Start a conversation by typing a message or using the voice input.
""")

# Add navigation buttons to other tools
st.markdown("""
<div class="navigation">
    <a class="nav-button" href="./Psycholog">Go to Psycholog</a>
    <a class="nav-button" href="./Conflic_Resolution">Go to Conflict Resolution</a>
    <a class="nav-button" href="./Summarizer">Go to Summarizer</a>
</div>
""", unsafe_allow_html=True)

display_chat_room(
    title="Sidekick",
    model_name=MODEL_NAME,
    session_state_key="sidekick_msg"
)