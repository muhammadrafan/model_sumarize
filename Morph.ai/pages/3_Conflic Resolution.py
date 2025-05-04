from pages.helper.chat_room import display_chat_room
import streamlit as st

st.set_page_config(page_title="Conflic Resolution", page_icon="📈")

display_chat_room(
    title="Conflic Resolution",
    model_name="granite3.3:2b",
    session_state_key="conflict_msg"
)