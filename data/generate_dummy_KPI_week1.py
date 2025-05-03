import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Create employee data
employees = [
    {"Employee Name": "John Smith", "Employee ID": "EMP001"},
    {"Employee Name": "Jane Doe", "Employee ID": "EMP002"},
    {"Employee Name": "Michael Johnson", "Employee ID": "EMP003"},
    {"Employee Name": "Sarah Williams", "Employee ID": "EMP004"},
    {"Employee Name": "Robert Brown", "Employee ID": "EMP005"},
    {"Employee Name": "Emily Davis", "Employee ID": "EMP006"},
    {"Employee Name": "David Miller", "Employee ID": "EMP007"},
    {"Employee Name": "Lisa Wilson", "Employee ID": "EMP008"},
    {"Employee Name": "James Garcia", "Employee ID": "EMP009"},
    {"Employee Name": "Maria Martinez", "Employee ID": "EMP010"}
]

# Generate KPI data for Week 1
kpi_week1_data = []

for employee in employees:
    # Generate random data for good performers (generally above thresholds)
    if random.random() < 0.7:  # 70% will be good performers
        kpi_data = {
            "Productivity: Number of tasks completed": np.random.randint(15, 30),
            "Productivity: Time to complete tasks (hours/task)": round(np.random.uniform(1.5, 2.8), 2),
            "Quality of Work: Error rate (%)": round(np.random.uniform(1.0, 4.9), 2),
            "Quality of Work: Customer satisfaction rate (%)": round(np.random.uniform(80.0, 97.0), 2),
            "Presence and Punctuality: Attendance rate (%)": round(np.random.uniform(90.0, 100.0), 2),
            "Presence and Punctuality: Punctuality rate (%)": round(np.random.uniform(90.0, 100.0), 2),
            "Goals and Objectives: Individual goal achievement (%)": round(np.random.uniform(80.0, 95.0), 2),
            "Goals and Objectives: Team goal achievement (%)": round(np.random.uniform(75.0, 90.0), 2),
            "Goals and Objectives: Contribution to company vision (1-5)": round(np.random.uniform(3.5, 5.0), 2),
            "Collaboration and Teamwork: Communication skills (1-5)": round(np.random.uniform(3.5, 5.0), 2),
            "Collaboration and Teamwork: Ability to work in a team (1-5)": round(np.random.uniform(3.5, 5.0), 2)
        }
    else:
        # Generate random data for underperformers (below thresholds for some metrics)
        kpi_data = {
            "Productivity: Number of tasks completed": np.random.randint(8, 15),  # Below threshold of 15
            "Productivity: Time to complete tasks (hours/task)": round(np.random.uniform(2.8, 4.5), 2),  # Above threshold of 3
            "Quality of Work: Error rate (%)": round(np.random.uniform(4.5, 9.0), 2),  # Some above threshold of 5%
            "Quality of Work: Customer satisfaction rate (%)": round(np.random.uniform(65.0, 82.0), 2),  # Some below threshold of 80%
            "Presence and Punctuality: Attendance rate (%)": round(np.random.uniform(75.0, 95.0), 2),
            "Presence and Punctuality: Punctuality rate (%)": round(np.random.uniform(70.0, 95.0), 2),
            "Goals and Objectives: Individual goal achievement (%)": round(np.random.uniform(65.0, 85.0), 2),
            "Goals and Objectives: Team goal achievement (%)": round(np.random.uniform(60.0, 80.0), 2),
            "Goals and Objectives: Contribution to company vision (1-5)": round(np.random.uniform(2.0, 4.0), 2),
            "Collaboration and Teamwork: Communication skills (1-5)": round(np.random.uniform(2.0, 4.0), 2),
            "Collaboration and Teamwork: Ability to work in a team (1-5)": round(np.random.uniform(2.0, 4.0), 2)
        }
    
    # Add employee info
    kpi_data.update(employee)
    kpi_week1_data.append(kpi_data)

# Create DataFrame
kpi_week1_df = pd.DataFrame(kpi_week1_data)

# Display the data
print(kpi_week1_df)

# Export to CSV
kpi_week1_df.to_csv("Weekly_KPI_Data__IT_Support___Week_1_with_IDs.csv", index=False)
