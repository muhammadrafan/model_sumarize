import streamlit as st
import pandas as pd
import requests
import json
import io
import time
import plotly.express as px
import plotly.graph_objects as go
import base64

# App title
st.set_page_config(page_title="Employee Performance Analyzer with IBM Granite 8B", layout="wide")
st.title("Employee Performance Analyzer with IBM Granite 8B")

# Sidebar for configuration
st.sidebar.header("Configuration")

# Input API endpoint (ngrok URL)
api_endpoint = st.sidebar.text_input("API Endpoint (ngrok URL)", "https://your-ngrok-url")

# Function to check API status
def check_api_status():
    try:
        response = requests.get(f"{api_endpoint}/status")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

# Function to upload files
def upload_files(kpi_week1_file, kpi_week2_file, survey_file):
    files = {
        'kpi_week1': kpi_week1_file,
        'kpi_week2': kpi_week2_file,
        'survey': survey_file
    }
    
    try:
        response = requests.post(f"{api_endpoint}/upload", files=files)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

# Function to initialize model (no token needed anymore)
def init_model():
    try:
        response = requests.post(f"{api_endpoint}/init_model", json={})
        return response.json()
    except Exception as e:
        return {'error': str(e)}

# Function to process data
def process_data(employee_id=None):
    data = {}
    if employee_id:
        data['employee_id'] = employee_id
    
    try:
        response = requests.post(f"{api_endpoint}/process", json=data)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

# Function to export to JSON
def download_json(dict_obj, filename):
    json_str = json.dumps(dict_obj, indent=4, ensure_ascii=False)
    b64 = base64.b64encode(json_str.encode('utf-8')).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">Click to download {filename}</a>'
    return href

# Main UI
st.header("1. Upload Data")

# Upload file
kpi_week1_file = st.file_uploader("Upload KPI Week 1", type=["csv"])
kpi_week2_file = st.file_uploader("Upload KPI Week 2", type=["csv"])
survey_file = st.file_uploader("Upload Monthly Survey", type=["csv"])

# Display API status
api_status = check_api_status()
if api_status:
    st.sidebar.success("API connected")
    st.sidebar.json(api_status)
else:
    st.sidebar.error("API not connected. Make sure the endpoint is correct and the server is running.")

# Button to upload files
if st.button("Upload Files"):
    if kpi_week1_file is None or kpi_week2_file is None or survey_file is None:
        st.error("Please upload all required files.")
    else:
        with st.spinner("Uploading files..."):
            result = upload_files(kpi_week1_file, kpi_week2_file, survey_file)
            
            if 'error' in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Files uploaded successfully. {result['employee_count']} employees found.")
                st.session_state['files_uploaded'] = True

# Initialize model
st.header("2. Initialize IBM Granite 8B Model")

if st.button("Initialize IBM Granite Model"):
    with st.spinner("Initializing IBM Granite 8B model..."):
        result = init_model()
        
        if 'error' in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success("IBM Granite 8B model initialized successfully.")
            st.session_state['models_initialized'] = True

# Process data
st.header("3. Analyze Data with IBM Granite")

# Option to process all employees or specific employee
process_option = st.radio("Choose analysis method:", ["Analyze All Employees", "Analyze Specific Employee"])

if process_option == "Analyze Specific Employee":
    employee_id = st.text_input("Enter Employee ID")
else:
    employee_id = None

if st.button("Process Data"):
    if not st.session_state.get('files_uploaded', False):
        st.error("Please upload files first.")
    elif not st.session_state.get('models_initialized', False):
        st.error("Please initialize IBM Granite model first.")
    else:
        with st.spinner("Processing data with IBM Granite (this may take some time)..."):
            result = process_data(employee_id)
            
            if 'error' in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success("Data processed successfully with IBM Granite.")
                st.session_state['summaries'] = result['summaries']
                st.session_state['data_processed'] = True

# Display results
if st.session_state.get('data_processed', False):
    st.header("4. IBM Granite Analysis Results")
    
    summaries = st.session_state['summaries']
    
    # Visualize summaries
    st.subheader("Visualization")
    
    # Count psychologist and conflict resolution needs
    need_psychologist_count = sum(1 for s in summaries.values() if s['need_psychologist'])
    need_conflict_resolution_count = sum(1 for s in summaries.values() if s['need_conflict_resolution'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for psychologist need
        fig1 = go.Figure(data=[go.Pie(
            labels=['Needs Psychologist', 'No Psychologist Needed'],
            values=[need_psychologist_count, len(summaries) - need_psychologist_count],
            hole=.3,
            marker_colors=['#FF6B6B', '#4ECDC4']
        )])
        fig1.update_layout(title_text="Need for Psychologist")
        st.plotly_chart(fig1)
        
    with col2:
        # Pie chart for conflict resolution need
        fig2 = go.Figure(data=[go.Pie(
            labels=['Needs Conflict Resolution', 'No Conflict Resolution Needed'],
            values=[need_conflict_resolution_count, len(summaries) - need_conflict_resolution_count],
            hole=.3,
            marker_colors=['#FF8066', '#6CDED9']
        )])
        fig2.update_layout(title_text="Need for Conflict Resolution")
        st.plotly_chart(fig2)
    
    # Create pie chart for problematic metrics
    st.subheader("Metric Issues")
    
    # Collect all problematic metrics
    all_bad_metrics = []
    for emp_data in summaries.values():
        all_bad_metrics.extend(emp_data['bad_metrics'])
    
    # Count frequency of each metric
    metric_counts = {}
    for metric in all_bad_metrics:
        if metric in metric_counts:
            metric_counts[metric] += 1
        else:
            metric_counts[metric] = 1
    
    if metric_counts:
        # Create pie chart for problematic metrics
        fig3 = go.Figure(data=[go.Pie(
            labels=list(metric_counts.keys()),
            values=list(metric_counts.values()),
            hole=.3,
            marker_colors=['#FF9F1C', '#2EC4B6', '#E71D36', '#011627']
        )])
        fig3.update_layout(title_text="Problematic Metrics")
        st.plotly_chart(fig3)
    else:
        st.info("No problematic metrics detected")
    
    # Detail table
    st.subheader("Employee Details")
    
    # Convert summaries to dataframe
    summary_data = []
    for emp_id, data in summaries.items():
        summary_data.append({
            'Employee ID': emp_id,
            'Employee Name': data['employee_name'],
            'Needs Psychologist': 'Yes' if data['need_psychologist'] else 'No',
            'Needs Conflict Resolution': 'Yes' if data['need_conflict_resolution'] else 'No',
            'Problematic Metrics': ', '.join(data['bad_metrics']) if data['bad_metrics'] else 'None'
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Add highlight for problematic employees
    def highlight_need(val):
        color = 'background-color: #ffcccc' if val == 'Yes' else ''
        return color
    
    styled_df = summary_df.style.applymap(highlight_need, subset=['Needs Psychologist', 'Needs Conflict Resolution'])
    st.dataframe(styled_df)
    
    # Display details for selected employee
    st.subheader("Employee Summary Details (IBM Granite Analysis)")
    selected_employee = st.selectbox("Select Employee", summary_df['Employee ID'].tolist())
    
    if selected_employee:
        emp_name = summaries[selected_employee]['employee_name']
        st.write(f"**{emp_name} ({selected_employee})**")
        
        # Create container for styling summary
        with st.container():
            st.markdown("""
            <style>
            .summary-box {
                background-color: #2c2d2e;
                border-left: 5px solid #007bff;
                padding: 15px;
                border-radius: 5px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Solution to avoid backslash errors in f-string
            summary_text = summaries[selected_employee]['summary']
            summary_html = summary_text.replace('\n', '<br>')
            html_content = '<div class="summary-box">' + summary_html + '</div>'
            st.markdown(html_content, unsafe_allow_html=True)
        
        # Export summary
        if st.button("Export Summary to JSON"):
            tmp_download_link = download_json(summaries[selected_employee], f"{selected_employee}_summary.json")
            st.markdown(tmp_download_link, unsafe_allow_html=True)


# Export all summaries
if st.session_state.get('data_processed', False):
    st.header("5. Export Data")
    
    if st.button("Export All Summaries to JSON"):
        all_summaries = st.session_state['summaries']
        tmp_download_link = download_json(all_summaries, "all_employee_summaries.json")
        st.markdown(tmp_download_link, unsafe_allow_html=True)
    
    # Add export to CSV
    if st.button("Export Summaries to CSV"):
        # Create DataFrame for export
        export_data = []
        for emp_id, data in st.session_state['summaries'].items():
            export_data.append({
                'Employee ID': emp_id,
                'Employee Name': data['employee_name'],
                'Summary': data['summary'],
                'Needs Psychologist': 'Yes' if data['need_psychologist'] else 'No',
                'Needs Conflict Resolution': 'Yes' if data['need_conflict_resolution'] else 'No',
                'Problematic Metrics': ', '.join(data['bad_metrics']) if data['bad_metrics'] else 'None'
            })
        
        export_df = pd.DataFrame(export_data)
        csv = export_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="employee_summaries.csv">Click to download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

# Add information section and help
st.sidebar.markdown("---")
st.sidebar.header("Information")
st.sidebar.info("""
**About the Application**

This application uses the IBM Granite 8B model to analyze employee performance based on:
- Weekly KPI Data (Weeks 1 & 2)
- Monthly Survey Data

**Models Used**:
- IBM Granite 3.3 8B Instruct
- Sentiment analysis model from Hugging Face

**Note**: Hugging Face API token is already included in the backend.
""")

# Add information about Hugging Face and IBM Granite
st.sidebar.markdown("---")
st.sidebar.subheader("About IBM Granite")
st.sidebar.markdown("""
[IBM Granite](https://huggingface.co/ibm-granite) is IBM's latest family of language models available through the Hugging Face platform. These models are designed to provide advanced text understanding and generation capabilities.

This application uses the [ibm-granite/granite-3.3-8b-instruct](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct) model which has approximately 8 billion parameters, offering a good balance between performance and efficiency.
""")

# Add process information
st.sidebar.markdown("---")
st.sidebar.subheader("Analysis Process")
st.sidebar.markdown("""
1. **Upload Data**: Upload employee KPI and survey files
2. **Initialize Model**: Set up the IBM Granite 8B model
3. **Analysis**: Process data with the model to generate:
   - Employee performance summaries
   - Identification of areas needing improvement
   - Recommendations (psychologist/conflict resolution)
4. **Export Results**: Download analysis results in JSON/CSV format
""")

# Add system information
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

elapsed_time = time.time() - st.session_state['start_time']
st.sidebar.markdown("---")
st.sidebar.text(f"Execution time: {elapsed_time:.2f} seconds")
