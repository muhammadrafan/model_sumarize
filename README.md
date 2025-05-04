# model_sumarize
The functionality of this model is to make a decision if employee need conflict resolution with another employee or need personal psycholog.

## Please Attention
1. In the Backend file please input your huggingface token and ngrok token
2. Backend use ngrok because i used kaggle for the computing power :)
3. Generate Data dummy, use python file in the Data folder.

# model new
# Employee Performance Analyzer

An AI-powered tool for analyzing employee performance data and generating comprehensive assessments.

## Overview

The Employee Performance Analyzer is a Streamlit application that analyzes employee performance metrics and survey data. It uses natural language processing and sentiment analysis to generate performance summaries, identify areas for improvement, and make recommendations for employee support.

## Features

- **Data Analysis**: Processes weekly KPI data and monthly survey responses
- **AI-Powered Summaries**: Generates comprehensive performance summaries using a language model
- **Sentiment Analysis**: Detects potential psychological or conflict resolution needs
- **Comparative Analysis**: Compares performance between weeks to identify trends
- **Export Options**: Export summaries to CSV files

## Requirements

- Python 3.7+
- pandas
- numpy
- torch
- transformers
- streamlit
- plotly
- Internet connection (for model downloads if not cached)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install pandas numpy torch transformers streamlit plotly
   ```

## Usage

### Streamlit UI

Run the Streamlit application:
```
streamlit run employee_analyzer.py
```

1. Upload the required CSV files:
   - KPI Week 1 (performance data from previous week)
   - KPI Week 2 (current performance data)
   - Monthly Survey (employee survey responses)

2. Click "Upload and Process Files" to analyze the data
3. View employee summaries in the application
4. Export summaries via download link or save to file

### Command Line Interface

The application can also be run from the command line without the Streamlit UI:
```
python employee_analyzer.py <kpi_week1_path> <kpi_week2_path> <survey_path> [output_path]
```

## Data Format

### KPI Data Format
KPI CSV files should include the following columns:
- Employee ID
- Employee Name
- Productivity: Number of tasks completed
- Productivity: Time to complete tasks (hours/task)
- Quality of Work: Error rate (%)
- Quality of Work: Customer satisfaction rate (%)
- Presence and Punctuality: Attendance rate (%)
- Presence and Punctuality: Punctuality rate (%)
- Goals and Objectives: Individual goal achievement (%)
- Goals and Objectives: Team goal achievement (%)
- Goals and Objectives: Contribution to company vision (1-5)
- Collaboration and Teamwork: Communication skills (1-5)
- Collaboration and Teamwork: Ability to work in a team (1-5)

### Survey Data Format
Survey CSV files should include:
- Employee ID
- Employee Name
- Self-Performance
- Goals Achieved
- Personal Challenges
- Stress or Anxiety
- Relationship with Colleagues
- Communication Issues
- Team Conflicts
- Team Collaboration

## How It Works

1. **Data Processing**: The application loads and processes KPI and survey data
2. **Language Model**: A causal language model is used to generate performance summaries
3. **Sentiment Analysis**: Survey responses are analyzed for sentiment to detect potential issues
4. **Performance Evaluation**: Metrics are compared against thresholds to identify areas of concern
5. **Summary Generation**: The model creates structured summaries with:
   - Performance Summary (good/poor with explanation)
   - Comparison to previous week
   - Improvement Areas
   - Recommendations (psychologist/conflict resolution if needed)

## Performance Thresholds

The application uses the following thresholds to evaluate performance:
- Minimum 15 tasks completed per week
- Maximum 3 hours per task
- Maximum 5% error rate
- Minimum 80% customer satisfaction

## Models Used

- **Language Model**: IBM Granite 3.3 2B Instruct (`ibm-granite/granite-3.3-2b-instruct`)
- **Sentiment Analysis**: Multilingual Sentiment Analysis (`tabularisai/multilingual-sentiment-analysis`)

## Fallback Mechanism

If the language model fails to generate a summary, the application falls back to a rule-based summary approach to ensure all employees get an assessment.

## Error Handling

The application includes comprehensive error handling to ensure stability, including:
- Model loading failures
- File processing errors
- Data format inconsistencies
- Model generation failures

## License

[Your license information here]

## Contact

[Your contact information here]
