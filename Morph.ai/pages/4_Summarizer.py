import pandas as pd
import numpy as np
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import streamlit as st
import plotly.graph_objects as go
import base64

# Set page configuration
st.set_page_config(page_title="Employee Performance Analyzer", layout="wide")
st.title("Employee Performance Analyzer")

# Global variables to store models and data
sentiment_tokenizer = None
sentiment_model = None
nlp_tokenizer = None
nlp_model = None
kpi_week1_df = None
kpi_week2_df = None
survey_df = None

# Function to analyze sentiment
def analyze_sentiment(text, sentiment_model_id="tabularisai/multilingual-sentiment-analysis"):
    """
    Analyzes sentiment from text using local sentiment model
    """
    global sentiment_tokenizer, sentiment_model
    
    if not text or not isinstance(text, str) or len(text.strip()) < 5:
        return {'score': 0, 'label': 'neutral'}
    
    try:
        # Initialize sentiment models if not already done
        if sentiment_tokenizer is None or sentiment_model is None:
            st.write("Loading sentiment analysis model...")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_id)
            sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_id).to(device)
            st.write(f"Sentiment model loaded on {device}")
        
        # Get the device where the model is loaded
        device = next(sentiment_model.parameters()).device
        
        # Tokenize and get prediction
        encoded_input = sentiment_tokenizer(text, return_tensors='pt', truncation=True, max_length=512).to(device)
        output = sentiment_model(**encoded_input)
        scores = softmax(output.logits, dim=1).detach().cpu().numpy()[0]
        
        # Get prediction
        predicted_class = torch.argmax(output.logits, dim=1).item()
        id2label = sentiment_model.config.id2label
        label = id2label[predicted_class].lower()
        score = float(scores[predicted_class])
        
        # Adjust score format
        sentiment = {'label': label}
        if label == 'positive':
            sentiment['score'] = score
        elif label == 'negative':
            sentiment['score'] = -score
        else:
            sentiment['score'] = 0
            
        return sentiment
        
    except Exception as e:
        st.error(f"Error analyzing sentiment: {e}")
        return {'score': 0, 'label': 'neutral'}

# Function to load language model
def load_language_model(model_id="ibm-granite/granite-3.3-2b-instruct"):
    """
    Initialize language model for summary generation
    """
    global nlp_tokenizer, nlp_model
    
    st.write(f"Loading language model: {model_id}")
    
    try:
        # Check if GPU is available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        st.write(f"Using device: {device}")
        
        # Initialize tokenizer and model
        nlp_tokenizer = AutoTokenizer.from_pretrained(model_id)
        nlp_model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
        
        st.write("Language model loaded successfully!")
        return True
    except Exception as e:
        st.error(f"Error loading language model: {e}")
        return False

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

# Function to generate summary using the language model
def generate_summary(prompt):
    """
    Generate summary using the language model
    """
    global nlp_tokenizer, nlp_model
    
    try:
        # Check if model is loaded
        if nlp_tokenizer is None or nlp_model is None:
            st.error("Language model is not loaded")
            return "Language model is not loaded"
        
        # Use the model for text generation
        device = next(nlp_model.parameters()).device
        inputs = nlp_tokenizer(prompt, return_tensors="pt").to(device)
        
        # Generate text
        with torch.no_grad():
            outputs = nlp_model.generate(
                inputs.input_ids,
                max_new_tokens=250,
                temperature=0.2,
                top_p=0.95,
                do_sample=True
            )
        
        # Decode the generated text
        response = nlp_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the generated part (remove the prompt)
        if prompt in response:
            response = response.replace(prompt, "").strip()
        
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
    
    # If employee_id is provided, only process that employee
    if employee_id:
        employee_ids = [employee_id]
    else:
        employee_ids = kpi_week2_df['Employee ID'].unique()
    
    # Progress bar
    progress_bar = st.progress(0)
    
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
                    need_psychologist = stress_analysis['label'] == 'negative' and stress_analysis['score'] < -0.3
                
                if len(conflict_text) > 5:
                    conflict_analysis = analyze_sentiment(conflict_text)
                    need_conflict_resolution = conflict_analysis['label'] == 'negative' and conflict_analysis['score'] < -0.3
            
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
                'summary': combined_summary
            }
            
        except Exception as e:
            st.error(f"Error processing employee {emp_id}: {e}")
            continue
    
    # Clear progress bar
    progress_bar.empty()
    
    return all_summaries

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
            
            # Initialize language model
            with st.spinner("Initializing language model..."):
                model_loaded = load_language_model()
                
            if model_loaded:
                st.success("Language model initialized successfully.")
                
                # Process data
                with st.spinner("Processing employee data..."):
                    summaries = process_employee_data(kpi_week1_df, kpi_week2_df, survey_df)
                    
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

# Simplified version for running without Streamlit UI
def run_without_ui(kpi_week1_path, kpi_week2_path, survey_path, output_path="employee_summaries.csv"):
    """
    Run the analysis without Streamlit UI
    """
    try:
        print("Reading files...")
        kpi_week1_df = pd.read_csv(kpi_week1_path)
        kpi_week2_df = pd.read_csv(kpi_week2_path)
        survey_df = pd.read_csv(survey_path)
        
        print(f"Files read successfully. {len(kpi_week2_df['Employee ID'].unique())} employees found.")
        
        # Initialize language model
        print("Initializing language model...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        global nlp_tokenizer, nlp_model
        model_id = "ibm-granite/granite-3.3-2b-instruct"
        nlp_tokenizer = AutoTokenizer.from_pretrained(model_id)
        nlp_model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
        
        print("Model initialized successfully.")
        
        # Process data
        print("Processing employee data...")
        summaries = process_employee_data(kpi_week1_df, kpi_week2_df, survey_df)
        
        # Export to CSV
        print(f"Exporting summaries to {output_path}...")
        summary_data = []
        for emp_id, data in summaries.items():
            summary_data.append({
                'Employee ID': emp_id,
                'Employee Name': data['employee_name'],
                'Summary': data['summary']
            })
        
        export_df = pd.DataFrame(summary_data)
        export_df.to_csv(output_path, index=False)
        
        print(f"Analysis complete. Results saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

# Entry point for CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # If command line arguments are provided, run without UI
        if len(sys.argv) >= 4:
            kpi_week1_path = sys.argv[1]
            kpi_week2_path = sys.argv[2]
            survey_path = sys.argv[3]
            output_path = sys.argv[4] if len(sys.argv) >= 5 else "employee_summaries.csv"
            
            run_without_ui(kpi_week1_path, kpi_week2_path, survey_path, output_path)
        else:
            print("Usage: python employee_analyzer.py <kpi_week1_path> <kpi_week2_path> <survey_path> [output_path]")
    # else the script is being run with Streamlit UI