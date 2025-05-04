from pages.helper.chat_room import display_chat_room
import streamlit as st

st.set_page_config(page_title="Sidekick", page_icon="📈")

display_chat_room(
    title="Sidekick",
    model_name="granite3.3:2b",
    session_state_key="sidekick_msg"
)