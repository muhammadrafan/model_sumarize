# Morph.AI Employee Management Suite - Quick Start Guide

This guide will walk you through setting up and testing the Morph.AI Employee Management Suite.

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- The granite3.3:2b model downloaded in Ollama

## Step 1: Installation

1. Clone or download the repository to your local machine
2. Open a terminal in the project directory
3. Run the automated installation script:

```bash
python install.py
```

This script will:
- Install required Python packages
- Check for Ollama installation and the required model
- Set up the directory structure
- Create configuration files

## Step 2: Start the Application

Start the Streamlit application:

```bash
streamlit run Dashboard.py
```

The dashboard will open in your web browser. If this is your first time running the application, you'll see a message that no employee data is available yet.

## Step 3: Process Employee Data with Summarizer

1. Click on "Launch Summarizer" or navigate to the Summarizer page using the navigation menu
2. You'll need three CSV files:
   - KPI Week 1 (previous performance data)
   - KPI Week 2 (current performance data)
   - Monthly Survey (employee survey responses)

3. **Sample Data Format:**

### KPI Data (CSV format)
```
Employee ID,Employee Name,Productivity: Number of tasks completed,Productivity: Time to complete tasks (hours/task),Quality of Work: Error rate (%),Quality of Work: Customer satisfaction rate (%),Presence and Punctuality: Attendance rate (%),Presence and Punctuality: Punctuality rate (%),Goals and Objectives: Individual goal achievement (%),Goals and Objectives: Team goal achievement (%),Goals and Objectives: Contribution to company vision (1-5),Collaboration and Teamwork: Communication skills (1-5),Collaboration and Teamwork: Ability to work in a team (1-5)
1001,John Smith,22,2.5,3.2,92,98,95,90,85,4,4,5
1002,Sarah Johnson,18,3.1,4.5,88,92,97,85,85,3,5,4
1003,David Lee,14,3.8,6.2,78,95,90,75,85,3,3,4
```

### Survey Data (CSV format)
```
Employee ID,Employee Name,Self-Performance,Goals Achieved,Personal Challenges,Stress or Anxiety,Relationship with Colleagues,Communication Issues,Team Conflicts,Team Collaboration
1001,John Smith,Satisfied with my work this month,Met most of my targets,Finding time for all tasks,Sometimes feel overwhelmed with deadlines,Good relationships overall,None major to report,No significant conflicts,Working well with my team
1002,Sarah Johnson,Did well but can improve,Achieved key priorities,Work-life balance is difficult,Feeling stressed most days,Generally positive,Some miscommunication with product team,Minor disagreements about approach,Collaboration is good overall
1003,David Lee,Below my usual standard,Missed some important goals,Too many competing priorities,Very anxious about performance review,Strained with some team members,Regular miscommunication issues,Ongoing conflict with marketing team,Finding teamwork challenging lately
```

4. After uploading the files, click "Upload and Process Files"
5. The Summarizer will analyze the data and generate performance summaries
6. These summaries will be stored in the database for other tools to use

## Step 4: Test Sidekick Assistant

1. Navigate to the Sidekick page
2. Sidekick will automatically load the employee performance context
3. Try asking some of these questions:
   - "What's the overall team performance like?"
   - "Tell me about John Smith's performance"
   - "Which employees need psychological support?"
   - "I'm noticing that Sarah seems stressed lately. What should I do?"

The Sidekick assistant should respond with context-aware answers and recommend Psycholog or Conflict Resolution services when appropriate.

## Step 5: Test Psycholog Service

1. Navigate to the Psycholog page
2. Notice that the sidebar shows employees flagged for psychological support
3. Try having conversations related to employee well-being:
   - "How can I help David manage his anxiety?"
   - "What are some stress management techniques I could suggest?"
   - "I need to have a difficult conversation with an employee about their mental health"

## Step 6: Test Conflict Resolution Service

1. Navigate to the Conflict Resolution page
2. The sidebar shows employees flagged for conflict resolution
3. Try having conversations about team conflicts:
   - "How should I approach the conflict between David and the marketing team?"
   - "What are some effective mediation techniques?"
   - "I need to improve communication between teams"

## Step 7: Explore the Dashboard

Return to the main Dashboard to see visualizations of:
- Overall employee performance metrics
- Employees needing intervention
- Performance distribution across the team

## Troubleshooting

### Ollama Connection Issues
If you encounter errors connecting to Ollama:
1. Ensure Ollama is running (`ollama serve`)
2. Verify the granite3.3:2b model is downloaded (`ollama list`)
3. Check that the API endpoint in pages/config.py is correct

### Missing Employee Data
If assistants aren't showing employee context:
1. Ensure you've processed data through the Summarizer first
2. Check that the data/summaries.json file exists and contains data
3. Try clearing your browser cache or restarting the application

### Voice Features Not Working
Voice features require:
1. A working microphone
2. The SpeechRecognition and pyttsx3 packages
3. On Linux, additional packages may be required: `sudo apt-get install python3-pyaudio portaudio19-dev`

## Next Steps

- Create custom surveys to gather more employee data
- Adjust thresholds in config.py to tune recommendations
- Add more visualization options to the Dashboard
- Develop your own AI tools building on this framework