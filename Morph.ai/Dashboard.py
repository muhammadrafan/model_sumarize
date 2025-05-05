import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from pathlib import Path
from datetime import datetime

# Import shared configuration
from pages.helper.config import SUMMARY_DB

# Set page configuration
st.set_page_config(page_title="Morph.AI Dashboard", layout="wide")

# --- STYLE & BACKGROUND ---
st.markdown(
    """
    <style>
    .morph-header {
        width: 100vw;
        min-height: 120px;
        padding-top: 32px;
        padding-bottom: 24px;
        margin-left: -3vw;
        margin-top: -3.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        border-radius: 0 0 40px 40px;
        box-shadow: 0 4px 24px 0 rgba(60,60,100,0.09);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .morph-title {
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        font-weight: 900;
        font-size: 2.7rem;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 0.2rem;
        text-shadow: 0 2px 12px rgba(80,80,120,0.10);
    }
    .morph-subtitle {
        font-family: 'Segoe UI', 'Montserrat', 'Arial', sans-serif;
        font-weight: 400;
        font-size: 1.18rem;
        color: #e0e7ef;
        margin-bottom: 0.2rem;
        text-shadow: 0 1px 6px rgba(80,80,120,0.08);
    }
    .badge-karyawan {
        display: inline-block;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 60%, #EC4899 100%);
        color: white;
        font-weight: 600;
        padding: 7px 18px;
        border-radius: 999px;
        margin: 4px 8px 4px 0;
        font-size: 1.06rem;
        box-shadow: 0 2px 8px 0 rgba(139,92,246,0.09);
        letter-spacing: 0.5px;
    }
    .dashboard-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    .nav-pills {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }
    .nav-pill {
        background-color: #f8f9fa;
        color: #495057;
        border: none;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.2s;
    }
    .nav-pill:hover {
        background-color: #e9ecef;
        color: #212529;
    }
    .nav-pill-active {
        background-color: #6c5ce7;
        color: white;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3B82F6;
    }
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER (GRADIENT, TITLE) ---
st.markdown(
    """
    <div class="morph-header">
        <div class="morph-title">Morph.AI</div>
        <div class="morph-subtitle">Employee Performance Management Suite</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- NAVIGATION ---
st.markdown(
    """
    <div class="nav-pills">
        <a class="nav-pill nav-pill-active" href="./">Dashboard</a>
        <a class="nav-pill" href="./Sidekick">Sidekick</a>
        <a class="nav-pill" href="./Psycholog">Psycholog</a>
        <a class="nav-pill" href="./Conflic_Resolution">Conflict Resolution</a>
        <a class="nav-pill" href="./Summarizer">Summarizer</a>
    </div>
    """,
    unsafe_allow_html=True
)

# --- LOAD SUMMARY DATA ---
def load_summaries():
    if not os.path.exists(SUMMARY_DB):
        return {}
    
    try:
        with open(SUMMARY_DB, 'r') as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading summaries: {e}")
        return {}

summaries = load_summaries()

# --- DASHBOARD OVERVIEW ---
st.header("📊 Employee Performance Overview")

if not summaries:
    st.info("No employee data available. Please use the Summarizer tool to analyze employee performance first.")
else:
    # Extract key metrics
    total_employees = len(summaries)
    need_psychologist = len([1 for data in summaries.values() if data.get('need_psychologist', False)])
    need_conflict = len([1 for data in summaries.values() if data.get('need_conflict_resolution', False)])
    
    # Calculate average metrics
    avg_tasks = sum(data.get('performance_metrics', {}).get('tasks_completed', 0) for data in summaries.values()) / total_employees if total_employees > 0 else 0
    avg_error = sum(data.get('performance_metrics', {}).get('error_rate', 0) for data in summaries.values()) / total_employees if total_employees > 0 else 0
    avg_satisfaction = sum(data.get('performance_metrics', {}).get('customer_satisfaction', 0) for data in summaries.values()) / total_employees if total_employees > 0 else 0
    
    # Display metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="metric-label">Total Employees</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(total_employees),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="metric-label">Avg Tasks Completed</div>
                <div class="metric-value">{:.1f}</div>
            </div>
            """.format(avg_tasks),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="metric-label">Need Psychological Support</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(need_psychologist),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div class="dashboard-card">
                <div class="metric-label">Need Conflict Resolution</div>
                <div class="metric-value">{}</div>
            </div>
            """.format(need_conflict),
            unsafe_allow_html=True
        )
    
    # Prepare data for charts
    chart_data = []
    for emp_id, data in summaries.items():
        chart_data.append({
            'Employee Name': data['employee_name'],
            'Tasks Completed': data.get('performance_metrics', {}).get('tasks_completed', 0),
            'Error Rate (%)': data.get('performance_metrics', {}).get('error_rate', 0),
            'Customer Satisfaction (%)': data.get('performance_metrics', {}).get('customer_satisfaction', 0),
            'Need Psychologist': 'Yes' if data.get('need_psychologist', False) else 'No',
            'Need Conflict Resolution': 'Yes' if data.get('need_conflict_resolution', False) else 'No'
        })
    
    chart_df = pd.DataFrame(chart_data)
    
    # Tasks per employee chart
    st.subheader("Tasks Completed per Employee")
    fig1 = px.bar(
        chart_df,
        x='Employee Name',
        y='Tasks Completed',
        color='Tasks Completed',
        color_continuous_scale=['#3B82F6', '#8B5CF6', '#EC4899'],
        labels={'Tasks Completed': 'Tasks', 'Employee Name': 'Employee'}
    )
    fig1.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Error vs Satisfaction scatter plot
    st.subheader("Error Rate vs Customer Satisfaction")
    fig2 = px.scatter(
        chart_df,
        x='Error Rate (%)',
        y='Customer Satisfaction (%)',
        color='Need Psychologist',
        size='Tasks Completed',
        hover_name='Employee Name',
        color_discrete_map={'Yes': '#EC4899', 'No': '#3B82F6'},
        labels={'Error Rate (%)': 'Error Rate (%)', 'Customer Satisfaction (%)': 'Customer Satisfaction (%)'}
    )
    fig2.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    fig2.add_shape(
        type="rect",
        x0=0, x1=5,
        y0=80, y1=100,
        line=dict(color="green", width=2, dash="dash"),
        fillcolor="rgba(0,255,0,0.1)",
    )
    fig2.add_annotation(
        x=2.5, y=90,
        text="Ideal Zone",
        showarrow=False,
        font=dict(color="green")
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Employee intervention chart
    intervention_data = {
        'Intervention Type': ['Psychological Support', 'Conflict Resolution', 'No Intervention'],
        'Count': [
            need_psychologist,
            need_conflict,
            total_employees - (need_psychologist + need_conflict)
        ]
    }
    
    intervention_df = pd.DataFrame(intervention_data)
    
    st.subheader("Recommended Interventions")
    fig3 = px.pie(
        intervention_df,
        values='Count',
        names='Intervention Type',
        color='Intervention Type',
        color_discrete_map={
            'Psychological Support': '#EC4899',
            'Conflict Resolution': '#8B5CF6',
            'No Intervention': '#3B82F6'
        },
    )
    fig3.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    fig3.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig3, use_container_width=True)

# --- TOOLS SUMMARY ---
st.header("🛠️ Available Tools")

# Create summary cards for each tool
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="dashboard-card">
            <h3 style="color:#3B82F6;">Summarizer</h3>
            <p>Analyze employee performance data and generate insights. Upload KPI and survey data to create comprehensive summaries and identify employees who need support.</p>
            <a href="./Summarizer" style="color:#3B82F6; text-decoration:none; font-weight:bold;">Launch Summarizer →</a>
        </div>
        
        <div class="dashboard-card">
            <h3 style="color:#8B5CF6;">Psycholog</h3>
            <p>Specialized assistant for psychological support and stress management. Get personalized guidance for maintaining mental well-being in the workplace.</p>
            <a href="./Psycholog" style="color:#8B5CF6; text-decoration:none; font-weight:bold;">Launch Psycholog →</a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="dashboard-card">
            <h3 style="color:#EC4899;">Sidekick</h3>
            <p>Your personal assistant for employee performance management. Get guidance on performance improvement and recommendations for specialized tools.</p>
            <a href="./Sidekick" style="color:#EC4899; text-decoration:none; font-weight:bold;">Launch Sidekick →</a>
        </div>
        
        <div class="dashboard-card">
            <h3 style="color:#F97316;">Conflict Resolution</h3>
            <p>Mediator to help navigate workplace conflicts and improve team dynamics. Get strategies for effective communication and conflict resolution.</p>
            <a href="./Conflic_Resolution" style="color:#F97316; text-decoration:none; font-weight:bold;">Launch Conflict Resolution →</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- FOOTER ---
st.markdown(
    """
    <div style="text-align:center; margin-top:50px; padding:20px; color:#6c757d; font-size:0.9rem;">
        <p>Employee Performance Management Suite © 2025</p>
    </div>
    """,
    unsafe_allow_html=True
)