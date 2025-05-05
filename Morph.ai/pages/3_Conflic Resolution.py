from pages.helper.chat_room import display_chat_room
import streamlit as st
from pages.helper.summary_manager import get_employees_needing_conflict_resolution
from pages.helper.config import MODEL_NAME

st.set_page_config(page_title="Conflict Resolution", page_icon="🤝")

# Custom CSS for the navigation and flagged employees
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
    .flagged-employee {
        background-color: #E2F0FD;
        border-left: 5px solid #0D6EFD;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Conflict Resolution page description
st.markdown("""
### 🤝 Conflict Resolution Assistant
A mediator to help navigate workplace conflicts and improve team dynamics. I can:
- Help analyze and understand team conflicts
- Provide strategies for effective communication
- Guide mediation processes between team members
- Suggest approaches to resolve disagreements constructively

Use this space to discuss team challenges in a safe environment.
""")

# Add navigation buttons to other tools
st.markdown("""
<div class="navigation">
    <a class="nav-button" href="./Sidekick">Go to Sidekick</a>
    <a class="nav-button" href="./Psycholog">Go to Psycholog</a>
    <a class="nav-button" href="./Summarizer">Go to Summarizer</a>
</div>
""", unsafe_allow_html=True)

# Display employees flagged for conflict resolution
with st.sidebar:
    st.subheader("Flagged Employees")
    st.write("Employees who may need conflict resolution:")
    
    flagged_employees = get_employees_needing_conflict_resolution()
    if flagged_employees:
        for employee in flagged_employees:
            st.markdown(f"""
            <div class="flagged-employee">
                <strong>{employee['employee_name']}</strong><br>
                Employee ID: {employee['employee_id']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No employees currently flagged.")

display_chat_room(
    title="Conflict Resolution",
    model_name=MODEL_NAME,
    session_state_key="conflict_msg"
)