import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import base64
import json
import requests
import os
from pathlib import Path
from datetime import datetime

# Import shared configuration
from pages.helper.config import OLLAMA_IP, MODEL_NAME, SUMMARY_DB, STRESS_THRESHOLD, CONFLICT_THRESHOLD

# Set page configuration
st.set_page_config(page_title="Employee Performance Analyzer", layout="wide")
st.title("Employee Performance Analyzer")

# Function to analyze sentiment using Ollama API
def analyze_sentiment(text):
    """
    Analyzes sentiment from text using Ollama API
    """
    if not text or not isinstance(text, str) or len(text.strip()) < 5:
        return {'score': 0, 'label': 'neutral'}
    
    try:
        prompt = f"""
        Analyze the sentiment of the following text and respond with only one word: 'positive', 'negative', or 'neutral'.
        Then on a new line, give a score between -1 and 1, where -1 is very negative, 0 is neutral, and 1 is very positive.
        
        Text: "{text}"
        
        Response format:
        LABEL
        SCORE
        """
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        res = requests.post(f"{OLLAMA_IP}/api/generate", json=payload)
        res.raise_for_status()
        response_text = res.json().get('response', '')
        
        # Parse response
        lines = response_text.strip().split('\n')
        if len(lines) >= 2:
            label = lines[0].strip().lower()
            try:
                score = float(lines[1].strip())
            except ValueError:
                score = 0.0
        else:
            label = 'neutral'
            score = 0.0
        
        # Format result
        sentiment = {'label': label}
        if label == 'positive':
            sentiment['score'] = abs(score)
        elif label == 'negative':
            sentiment['score'] = -abs(score)
        else:
            sentiment['score'] = 0
            
        return sentiment
        
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        return {'score': 0, 'label': 'neutral'}

# Function to prepare performance data for prompt
def prepare_performance_data(employee_data, comparative_data=None):
    """
    Format the employee performance data for the prompt
    """
    # Format performance data 
    performance_text = f"""
    Employee Name: {employee_data['Employee Name']}
    Employee ID: {employee_data['Employee ID']}
    
    WEEKLY KPIs:
    - Productivity: {employee_data['Productivity: Number of tasks completed']} tasks completed, {employee_data['Productivity: Time to complete tasks (hours/task)']:.2f} hours/task
    - Work Quality: Error rate {employee_data['Quality of Work: Error rate (%)']:.2f}%, Customer satisfaction {employee_data['Quality of Work: Customer satisfaction rate (%)']:.2f}%
    - Attendance & Punctuality: Attendance {employee_data['Presence and Punctuality: Attendance rate (%)']:.2f}%, Punctuality {employee_data['Presence and Punctuality: Punctuality rate (%)']:.2f}%
    - Goals & Objectives: Individual achievement {employee_data['Goals and Objectives: Individual goal achievement (%)']:.2f}%, Team achievement {employee_data['Goals and Objectives: Team goal achievement (%)']:.2f}%, Contribution {employee_data['Goals and Objectives: Contribution to company vision (1-5)']:.2f}/5
    - Collaboration & Teamwork: Communication {employee_data['Collaboration and Teamwork: Communication skills (1-5)']:.2f}/5, Teamwork {employee_data['Collaboration and Teamwork: Ability to work in a team (1-5)']:.2f}/5
    """
    
    # Add comparative data if available
    if comparative_data is not None:
        performance_text += f"""
        COMPARISON WITH PREVIOUS WEEK:
        - Change in number of tasks: {employee_data['Productivity: Number of tasks completed'] - comparative_data['Productivity: Number of tasks completed']}
        - Change in time per task: {employee_data['Productivity: Time to complete tasks (hours/task)'] - comparative_data['Productivity: Time to complete tasks (hours/task)']:.2f} hours
        - Change in error rate: {employee_data['Quality of Work: Error rate (%)'] - comparative_data['Quality of Work: Error rate (%)']:.2f}%
        - Change in customer satisfaction: {employee_data['Quality of Work: Customer satisfaction rate (%)'] - comparative_data['Quality of Work: Customer satisfaction rate (%)']:.2f}%
        """
    
    # Add survey data if available
    if 'survey_data' in employee_data:
        survey = employee_data['survey_data']
        performance_text += f"""
        MONTHLY SURVEY:
        - Self-Performance: {survey.get('Self-Performance', 'No data')}
        - Goals Achieved: {survey.get('Goals Achieved', 'No data')}
        - Personal Challenges: {survey.get('Personal Challenges', 'No data')}
        - Stress/Anxiety: {survey.get('Stress or Anxiety', 'No data')}
        - Relationship with Colleagues: {survey.get('Relationship with Colleagues', 'No data')}
        - Communication Issues: {survey.get('Communication Issues', 'No data')}
        - Team Conflicts: {survey.get('Team Conflicts', 'No data')}
        - Team Collaboration: {survey.get('Team Collaboration', 'No data')}
        """
    
    return performance_text

# Function to create prompt for model
def create_summary_prompt(performance_text):
    """
    Create the prompt for the model using performance data
    """
    prompt = f"""
    You are an HR assistant expert in analyzing employee performance.
    
    Task:
    Analyze the following employee performance data and provide a summary that assesses:
    1. Whether performance is good or poor (compare with threshold: min. 15 tasks, max. 3 hours/task, max. 5% error, min. 80% satisfaction)
    2. How it compares to the previous week (up/down)
    3. Which areas need improvement
    4. Whether this employee needs a personal psychologist or conflict resolution (based on survey)
    
    EMPLOYEE DATA:
    {performance_text}
    
    Output format:
    Performance Summary: [good/poor and explanation]
    Comparison: [summary comparison with previous week]
    Improvement Areas: [1-3 main areas that need improvement]
    Recommendation: [psychologist/conflict resolution/not needed] and reason
    """
    return prompt

# Function to generate summary using Ollama API
def generate_summary(prompt):
    """
    Generate summary using Ollama API
    """
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        res = requests.post(f"{OLLAMA_IP}/api/generate", json=payload)
        res.raise_for_status()
        response = res.json().get('response', 'No response generated')
        
        return response
    
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return "Error generating summary"

# Function to extract summary from model response
def extract_summary(response):
    """
    Extract and format the summary from the model response
    """
    # Remove any prompt text that might have been included in the response
    if "You are an HR assistant" in response:
        response = response.split("You are an HR assistant", 1)[0]
    
    if "EMPLOYEE DATA:" in response:
        response = response.split("EMPLOYEE DATA:", 1)[0]
    
    if "Output format:" in response:
        response = response.split("Output format:", 1)[1]
    
    # Clean up and format the summary
    summary = response.strip()
    
    # Ensure the response includes the required sections
    sections = ["Performance Summary:", "Comparison:", "Improvement Areas:", "Recommendation:"]
    
    formatted_summary = {}
    for section in sections:
        if section in summary:
            section_index = summary.find(section)
            next_section_index = float('inf')
            
            for next_section in sections:
                if next_section != section and next_section in summary and summary.find(next_section) > section_index:
                    next_section_index = min(next_section_index, summary.find(next_section))
            
            if next_section_index == float('inf'):
                section_content = summary[section_index + len(section):].strip()
            else:
                section_content = summary[section_index + len(section):next_section_index].strip()
            
            formatted_summary[section.replace(":", "")] = section_content
        else:
            formatted_summary[section.replace(":", "")] = "No information available"
    
    return formatted_summary

# Function to create a rule-based summary when model fails
def create_rule_based_summary(employee_data, comparative_data=None):
    """
    Create a rule-based summary when the language model fails
    """
    # Analyze metrics based on thresholds
    performance_rating = "good" if len(employee_data.get('bad_metrics', [])) == 0 else "poor"
    
    # Compare with previous week if available
    comparison = "No comparison data available." 
    if comparative_data is not None:
        task_diff = employee_data['Productivity: Number of tasks completed'] - comparative_data['Productivity: Number of tasks completed']
        error_diff = employee_data['Quality of Work: Error rate (%)'] - comparative_data['Quality of Work: Error rate (%)']
        
        if task_diff > 0 and error_diff < 0:
            comparison = f"Performance improved (tasks +{task_diff}, error {error_diff:.2f}%)."
        elif task_diff < 0 or error_diff > 0:
            comparison = f"Performance declined (tasks {task_diff}, error {error_diff:.2f}%)."
        else:
            comparison = "Performance relatively stable compared to previous week."
    
    # Improvement areas
    areas = employee_data.get('bad_metrics', [])
    improvement = "No areas requiring urgent improvement." if not areas else f"Needs improvement in: {', '.join(areas)}."
    
    # Recommendation
    recommendation = "Not needed"
    if employee_data.get('need_psychologist', False):
        recommendation = "Psychologist - signs of stress/anxiety detected"
    elif employee_data.get('need_conflict_resolution', False):
        recommendation = "Conflict resolution - signs of team conflict detected"
    
    # Create manual summary in formatted structure
    rule_based_summary = {
        "Performance Summary": performance_rating,
        "Comparison": comparison,
        "Improvement Areas": improvement,
        "Recommendation": recommendation
    }
    
    return rule_based_summary

# Function to process employee data and generate summaries
def process_employee_data(kpi_week1_df, kpi_week2_df, survey_df, employee_id=None):
    """
    Process employee data and generate performance summaries
    """
    # Thresholds to determine if performance is good or poor
    thresholds = {
        'tasks_completed': 15,  # Minimum tasks to be completed
        'time_per_task': 3,     # Maximum time per task (hours)
        'error_rate': 5,        # Maximum error rate (%)
        'customer_satisfaction': 80,  # Minimum customer satisfaction (%)
    }
    
    all_summaries = {}
    recommendations = {
        "psychologist": [],
        "conflict_resolution": []
    }
    
    # If employee_id is provided, only process that employee
    if employee_id:
        employee_ids = [employee_id]
    else:
        employee_ids = kpi_week2_df['Employee ID'].unique()
    
    # Progress bar
    progress_bar = st.progress(0)
    
    # Verify Ollama connection
    try:
        test_payload = {
            "model": MODEL_NAME,
            "prompt": "hello",
            "stream": False
        }
        requests.post(f"{OLLAMA_IP}/api/generate", json=test_payload).raise_for_status()
        st.success(f"Successfully connected to Ollama API with model {MODEL_NAME}")
    except Exception as e:
        st.error(f"Error connecting to Ollama API: {e}")
        return {}
    
    # Iterate through each employee
    for i, emp_id in enumerate(employee_ids):
        try:
            # Update progress
            progress_bar.progress((i + 1) / len(employee_ids))
            
            # Get employee data from all sources
            if emp_id not in kpi_week2_df['Employee ID'].values:
                continue
                
            emp_week2 = kpi_week2_df[kpi_week2_df['Employee ID'] == emp_id].iloc[0].to_dict()
            emp_week1 = kpi_week1_df[kpi_week1_df['Employee ID'] == emp_id].iloc[0].to_dict() if emp_id in kpi_week1_df['Employee ID'].values else None
            emp_survey = survey_df[survey_df['Employee ID'] == emp_id].iloc[0].to_dict() if emp_id in survey_df['Employee ID'].values else None

            # Merge survey data to week 2 KPI data if available
            if emp_survey is not None:
                emp_week2['survey_data'] = emp_survey
            
            # Evaluate employee performance
            bad_metrics = []
            if emp_week2['Productivity: Number of tasks completed'] < thresholds['tasks_completed']:
                bad_metrics.append('number of tasks')
            if emp_week2['Productivity: Time to complete tasks (hours/task)'] > thresholds['time_per_task']:
                bad_metrics.append('time per task')
            if emp_week2['Quality of Work: Error rate (%)'] > thresholds['error_rate']:
                bad_metrics.append('error rate')
            if emp_week2['Quality of Work: Customer satisfaction rate (%)'] < thresholds['customer_satisfaction']:
                bad_metrics.append('customer satisfaction')
            
            # Detect issues from survey
            need_psychologist = False
            need_conflict_resolution = False
            
            if emp_survey is not None:
                # Sentiment analysis for personal and team issues
                stress_text = str(emp_survey.get('Stress or Anxiety', ''))
                conflict_text = str(emp_survey.get('Team Conflicts', ''))
                
                if len(stress_text) > 5:
                    stress_analysis = analyze_sentiment(stress_text)
                    need_psychologist = stress_analysis['label'] == 'negative' and stress_analysis['score'] < STRESS_THRESHOLD
                
                if len(conflict_text) > 5:
                    conflict_analysis = analyze_sentiment(conflict_text)
                    need_conflict_resolution = conflict_analysis['label'] == 'negative' and conflict_analysis['score'] < CONFLICT_THRESHOLD
            
            # Add evaluation results to employee data
            emp_week2['bad_metrics'] = bad_metrics
            emp_week2['need_psychologist'] = need_psychologist
            emp_week2['need_conflict_resolution'] = need_conflict_resolution
            
            # Generate summary
            try:
                # Create data for the prompt
                performance_text = prepare_performance_data(emp_week2, emp_week1)
                
                # Create the prompt
                prompt = create_summary_prompt(performance_text)
                
                # Generate summary
                response = generate_summary(prompt)
                
                # Extract and format the summary
                summary_data = extract_summary(response)
            except Exception as e:
                st.warning(f"Error generating summary for employee {emp_id}, using rule-based summary: {e}")
                # Use rule-based summary as fallback
                summary_data = create_rule_based_summary(emp_week2, emp_week1)
            
            # Create a combined summary string from the structured data
            combined_summary = "\n".join([f"{key}: {value}" for key, value in summary_data.items()])
            
            # Store summary (only required fields)
            all_summaries[emp_id] = {
                'employee_name': emp_week2['Employee Name'],
                'employee_id': emp_id,
                'summary': combined_summary,
                'structured_summary': summary_data,
                'timestamp': datetime.now().isoformat(),
                'need_psychologist': need_psychologist,
                'need_conflict_resolution': need_conflict_resolution,
                'performance_metrics': {
                    'tasks_completed': emp_week2['Productivity: Number of tasks completed'],
                    'time_per_task': emp_week2['Productivity: Time to complete tasks (hours/task)'],
                    'error_rate': emp_week2['Quality of Work: Error rate (%)'],
                    'customer_satisfaction': emp_week2['Quality of Work: Customer satisfaction rate (%)'],
                }
            }
            
            # Add to recommendations lists if needed
            if need_psychologist:
                recommendations["psychologist"].append(emp_week2['Employee Name'])
            if need_conflict_resolution:
                recommendations["conflict_resolution"].append(emp_week2['Employee Name'])
            
        except Exception as e:
            st.error(f"Error processing employee {emp_id}: {e}")
            continue
    
    # Clear progress bar
    progress_bar.empty()
    
    # Save summaries to JSON file for other pages to use
    try:
        # If file exists, read existing data and update it
        existing_data = {}
        if os.path.exists(SUMMARY_DB):
            with open(SUMMARY_DB, 'r') as file:
                existing_data = json.load(file)
        
        # Update with new data
        for emp_id, data in all_summaries.items():
            existing_data[emp_id] = data
        
        # Write back to file
        with open(SUMMARY_DB, 'w') as file:
            json.dump(existing_data, file, indent=2)
        
        st.success(f"Successfully saved {len(all_summaries)} employee summaries to database.")
    except Exception as e:
        st.error(f"Error saving summaries to database: {e}")
    
    return all_summaries, recommendations

# Function to export to CSV
def export_to_csv(summaries):
    """
    Export summaries to CSV
    """
    # Create DataFrame for export
    export_data = []
    for emp_id, data in summaries.items():
        export_data.append({
            'Employee ID': emp_id,
            'Employee Name': data['employee_name'],
            'Summary': data['summary']
        })
    
    export_df = pd.DataFrame(export_data)
    csv = export_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="employee_summaries.csv">Click to download CSV</a>'
    
    return href

# Main UI
st.header("1. Upload Data")

# Upload file
kpi_week1_file = st.file_uploader("Upload KPI Week 1", type=["csv"])
kpi_week2_file = st.file_uploader("Upload KPI Week 2", type=["csv"])
survey_file = st.file_uploader("Upload Monthly Survey", type=["csv"])

# Button to upload and process files
if st.button("Upload and Process Files"):
    if kpi_week1_file is None or kpi_week2_file is None or survey_file is None:
        st.error("Please upload all required files.")
    else:
        try:
            # Read CSV files
            kpi_week1_df = pd.read_csv(kpi_week1_file)
            kpi_week2_df = pd.read_csv(kpi_week2_file)
            survey_df = pd.read_csv(survey_file)
            
            st.success(f"Files uploaded successfully. {len(kpi_week2_df['Employee ID'].unique())} employees found.")
            
            # Verify Ollama is running
            with st.spinner("Checking Ollama connection..."):
                try:
                    test_payload = {
                        "model": MODEL_NAME,
                        "prompt": "hello",
                        "stream": False
                    }
                    requests.post(f"{OLLAMA_IP}/api/generate", json=test_payload).raise_for_status()
                    st.success("Ollama API is running and model is available")
                except Exception as e:
                    st.error(f"Error connecting to Ollama API: {e}")
                    st.stop()
                
            # Process data
            with st.spinner("Processing employee data..."):
                summaries, recommendations = process_employee_data(kpi_week1_df, kpi_week2_df, survey_df)
                
            if summaries:
                st.success(f"Successfully processed {len(summaries)} employees.")
                
                # Display summaries
                st.header("Employee Summaries")
                
                # Convert summaries to dataframe
                summary_data = []
                for emp_id, data in summaries.items():
                    summary_data.append({
                        'Employee ID': emp_id,
                        'Employee Name': data['employee_name'],
                        'Summary': data['summary']
                    })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df)
                
                # Display recommendations
                st.header("Recommendations")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Employees Needing Psychologist")
                    if recommendations["psychologist"]:
                        for emp in recommendations["psychologist"]:
                            st.write(f"- {emp}")
                    else:
                        st.write("None")
                
                with col2:
                    st.subheader("Employees Needing Conflict Resolution")
                    if recommendations["conflict_resolution"]:
                        for emp in recommendations["conflict_resolution"]:
                            st.write(f"- {emp}")
                    else:
                        st.write("None")
                
                # Export options
                st.header("Export Options")
                
                # Export to CSV
                download_link = export_to_csv(summaries)
                st.markdown(download_link, unsafe_allow_html=True)
                
                # Save to file
                if st.button("Save to CSV File"):
                    try:
                        # Create DataFrame for export
                        export_df = pd.DataFrame(summary_data)
                        export_df.to_csv("employee_summaries.csv", index=False)
                        st.success("File saved to employee_summaries.csv")
                    except Exception as e:
                        st.error(f"Error saving file: {e}")
            
        except Exception as e:
            st.error(f"Error processing files: {e}")

# Function to view existing summaries from database
def view_existing_summaries():
    """
    View previously generated summaries from database
    """
    if not os.path.exists(SUMMARY_DB):
        st.warning("No saved summaries found. Process employee data first.")
        return
    
    try:
        with open(SUMMARY_DB, 'r') as file:
            existing_data = json.load(file)
        
        if not existing_data:
            st.warning("No summaries found in database.")
            return
        
        # Display summaries
        st.subheader("Previously Generated Summaries")
        
        # Convert to dataframe
        summary_data = []
        for emp_id, data in existing_data.items():
            summary_data.append({
                'Employee ID': emp_id,
                'Employee Name': data['employee_name'],
                'Summary': data['summary'],
                'Timestamp': data.get('timestamp', 'Unknown')
            })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df)
        
        return existing_data
    except Exception as e:
        st.error(f"Error loading summaries from database: {e}")
        return None

# Add a section to view previously generated summaries
st.header("2. View Previous Summaries")
if st.button("Load Saved Summaries"):
    existing_data = view_existing_summaries()