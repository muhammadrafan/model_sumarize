from pages.helper.chat_room import display_chat_room
import streamlit as st
from pages.helper.config import MODEL_NAME
from pages.helper.summary_manager import get_employees_needing_psychologist

st.set_page_config(page_title="Psycholog", page_icon="🧠")

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
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Psycholog page description
st.markdown("""
### 🧠 Psychological Support Assistant
A confidential space to discuss work-related stress and mental well-being. I can:
- Help you manage work-related stress and anxiety
- Provide strategies for maintaining work-life balance
- Offer support for burnout prevention
- Guide you through difficult workplace situations

Everything shared here is confidential.
""")

# Add navigation buttons to other tools
st.markdown("""
<div class="navigation">
    <a class="nav-button" href="./Sidekick">Go to Sidekick</a>
    <a class="nav-button" href="./Conflic_Resolution">Go to Conflict Resolution</a>
    <a class="nav-button" href="./Summarizer">Go to Summarizer</a>
</div>
""", unsafe_allow_html=True)

# Display employees flagged for psychological support
with st.sidebar:
    st.subheader("Flagged Employees")
    st.write("Employees who may need psychological support:")
    
    flagged_employees = get_employees_needing_psychologist()
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
    title="Psycholog",
    model_name=MODEL_NAME,
    session_state_key="psycholog_msg"
)