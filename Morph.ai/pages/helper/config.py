# config.py (in pages folder)
# Shared configuration file for all pages

# API Configuration
OLLAMA_IP = "http://localhost:11434"
MODEL_NAME = "granite3.3:2b"  # Default model for chat AI

# Database path (for storing summaries and context)
import os
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "data"
DATA_DIR.mkdir(exist_ok=True)
SUMMARY_DB = DATA_DIR / "summaries.json"

# Recommendation thresholds for psycholog and conflict resolution
STRESS_THRESHOLD = -0.3  # Threshold for recommending psychologist (sentiment score)
CONFLICT_THRESHOLD = -0.3  # Threshold for recommending conflict resolution (sentiment score)