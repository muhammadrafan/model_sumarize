# Employee Performance Management System

A comprehensive Streamlit application for employee performance analysis, psychological support, and conflict resolution, powered by Ollama API.

## Overview

This application consists of several integrated components:

1. **Summarizer**: Analyzes employee KPI data and surveys, generating performance summaries and recommendations.
2. **Sidekick**: A general assistant that helps with employee performance management and can suggest appropriate services.
3. **Psycholog**: A specialized assistant for psychological support and stress management.
4. **Conflict Resolution**: A specialized assistant for mediating workplace conflicts and improving team dynamics.

## System Architecture

The system is designed with the following architecture:

- **Central Configuration** (`config.py`): Stores shared settings like API endpoints and model names.
- **Summary Manager** (`summary_manager.py`): Handles data flow between components, especially retrieving summary data.
- **Chat Room** (`chat_room.py`): Core chat interface used by all assistant pages.
- **Voice Module** (`voice.py`): Provides speech-to-text and text-to-speech functionality.
- **Persistence Layer**: Summaries and recommendations are stored in a JSON database for cross-application usage.

## Key Features

### 1. Shared Context Across Applications

The Summarizer generates detailed employee performance analyses that are stored and made available to other components:

- **Sidekick** can access complete performance summaries for context-aware assistance
- **Psycholog** can access psychological indicators and stress factors
- **Conflict Resolution** can access team dynamics and conflict indicators

### 2. Intelligent Service Recommendations

Sidekick analyzes conversations and can recommend more specialized services:

- Detects psychological needs (stress, anxiety, burnout) and recommends Psycholog
- Detects conflict situations (team issues, communication problems) and recommends Conflict Resolution
- Uses both conversation analysis and stored employee data to make recommendations

### 3. Employee Context Awareness

All assistants can access specific employee contexts:

- Type an employee name in the sidebar to get specific context for that employee
- Each page shows employees flagged for specific interventions
- Summary database maintains employee-specific recommendations and metrics

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install streamlit requests speechrecognition pyttsx3 pandas plotly
   ```

2. **Install Ollama**:
   Follow the instructions at [Ollama's website](https://ollama.ai/download) to install Ollama locally.

3. **Download Required Model**:
   ```bash
   ollama pull granite3.3:2b
   ```

4. **Directory Structure**:
   Ensure your directory structure looks like:
   ```
   ├── Dashboard.py
   ├── pages/
   │   ├── config.py
   │   ├── 1_Sidekick.py
   │   ├── 2_Psycholog.py
   │   ├── 3_Conflic Resolution.py
   │   ├── 4_Summarizer.py
   │   ├── data/
   │   │   └── summaries.json  (created automatically)
   │   └── helper/
   │       ├── chat_room.py
   │       ├── summary_manager.py
   │       └── voice.py
   ```

5. **Run the Application**:
   ```bash
   streamlit run Dashboard.py
   ```

## Usage Workflow

1. **Generate Summaries**: 
   - Start with the Summarizer page to upload and analyze employee data
   - Process the data to generate and store summaries

2. **General Assistance**:
   - Use Sidekick for general performance management queries
   - Sidekick will recommend other services if needed

3. **Specialized Support**:
   - Use Psycholog for employees needing mental health support
   - Use Conflict Resolution for team dynamics issues

4. **Contextual Awareness**:
   - Use the sidebar to focus on specific employees
   - All tools share the same underlying database

## Technical Details

### Context Flow

1. **Data Analysis**:
   - Summarizer processes KPIs and survey data
   - Sentiment analysis detects psychological needs and conflict indicators
   - Results are stored in the database

2. **Data Retrieval**:
   - `summary_manager.py` provides functions to retrieve context
   - Different functions format context appropriately for each assistant

3. **Conversation Enhancement**:
   - Context is injected into the prompt sent to Ollama
   - Response is enhanced with recommendations if needed

### Configuration

- API endpoint and model settings are centralized in `config.py`
- Threshold settings for recommendations can be adjusted

## Customization

- **Model Selection**: Change the model in `config.py` to use a different Ollama model
- **Thresholds**: Adjust the thresholds for psychological support and conflict resolution
- **Interface**: Modify the CSS in each page to customize the appearance

## Contributing

Feel free to contribute to this project by submitting pull requests or issues on GitHub.