import os
import json
from pathlib import Path

def check_setup():
    """
    Check if the required files and directories exist
    Creates missing directories if needed
    """
    # Define the expected directory structure
    expected_structure = {
        "pages": {
            "config.py": False,
            "1_Sidekick.py": False,
            "2_Psycholog.py": False,
            "3_Conflic Resolution.py": False,
            "4_Summarizer.py": False,
            "data": {},  # Directory
            "helper": {
                "chat_room.py": False,
                "summary_manager.py": False,
                "voice.py": False
            }
        },
        "Dashboard.py": False
    }
    
    # Get the current directory
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if we're in the right directory (parent of pages)
    if not (current_dir / "pages").exists():
        # Try going one level up
        current_dir = current_dir.parent
        if not (current_dir / "pages").exists():
            print(f"ERROR: Could not find 'pages' directory in {current_dir}")
            return False
    
    # Create data directory if it doesn't exist
    data_dir = current_dir / "pages" / "data"
    if not data_dir.exists():
        print(f"Creating missing directory: {data_dir}")
        data_dir.mkdir(exist_ok=True)
    
    # Check all expected files
    missing_files = []
    
    # Check root files
    for file in ["Dashboard.py"]:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    # Check pages files
    for file in ["config.py", "1_Sidekick.py", "2_Psycholog.py", "3_Conflic Resolution.py", "4_Summarizer.py"]:
        if not (current_dir / "pages" / file).exists():
            missing_files.append(f"pages/{file}")
    
    # Check helper files
    for file in ["chat_room.py", "summary_manager.py", "voice.py"]:
        if not (current_dir / "pages" / "helper" / file).exists():
            missing_files.append(f"pages/helper/{file}")
    
    # Report results
    if missing_files:
        print("Missing files detected:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print("Setup check completed successfully!")
        print(f"Data directory: {data_dir}")
        
        # Initialize empty summary database if it doesn't exist
        summary_db = data_dir / "summaries.json"
        if not summary_db.exists():
            print(f"Initializing empty summaries database at {summary_db}")
            with open(summary_db, 'w') as f:
                json.dump({}, f)
        
        return True

if __name__ == "__main__":
    check_setup()