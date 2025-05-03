import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(43)  # Different seed for week 2

# Create employee data (same as week 1)
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

# Read Week 1 data to create correlated Week 2 data
try:
    week1_df = pd.read_csv("Weekly_KPI_Data__IT_Support___Week_1_with_IDs.csv")
    have_week1 = True
except:
    have_week1 = False
    print("Week 1 data not found, generating unrelated week 2 data")

# Generate KPI data for Week 2
kpi_week2_data = []

for i, employee in enumerate(employees):
    # Create somewhat correlated data with Week 1 if available
    if have_week1:
        week1_record = week1_df[week1_df["Employee ID"] == employee["Employee ID"]]
        
        if not week1_record.empty:
            # Some employees improve, some decline
            improvement_factor = np.random.choice([-1, 1], p=[0.3, 0.7]) * np.random.uniform(0.05, 0.15)
            
            # Employees 3, 6, and a random one will have issues (for setting up need for psychologist/conflict resolution)
            if employee["Employee ID"] in ["EMP003", "EMP006"] or (random.random() < 0.2 and employee["Employee ID"] not in ["EMP003", "EMP006"]):
                improvement_factor = -abs(improvement_factor) * 1.5  # Ensure negative and stronger decline
            
            # Extract and adjust week 1 data
            tasks_completed = int(week1_record["Productivity: Number of tasks completed"].values[0])
            tasks_completed = max(5, int(tasks_completed * (1 + improvement_factor)))
            
            time_per_task = float(week1_record["Productivity: Time to complete tasks (hours/task)"].values[0])
            time_per_task = max(1.0, round(time_per_task * (1 - improvement_factor * 0.5), 2))
            
            error_rate = float(week1_record["Quality of Work: Error rate (%)"].values[0])
            error_rate = max(0.5, round(error_rate * (1 - improvement_factor), 2))
            
            customer_satisfaction = float(week1_record["Quality of Work: Customer satisfaction rate (%)"].values[0])
            customer_satisfaction = min(100.0, max(50.0, round(customer_satisfaction * (1 + improvement_factor * 0.5), 2)))
            
            attendance = float(week1_record["Presence and Punctuality: Attendance rate (%)"].values[0])
            attendance = min(100.0, max(50.0, round(attendance * (1 + improvement_factor * 0.3), 2)))
            
            punctuality = float(week1_record["Presence and Punctuality: Punctuality rate (%)"].values[0])
            punctuality = min(100.0, max(50.0, round(punctuality * (1 + improvement_factor * 0.3), 2)))
            
            individual_goal = float(week1_record["Goals and Objectives: Individual goal achievement (%)"].values[0])
            individual_goal = min(100.0, max(50.0, round(individual_goal * (1 + improvement_factor), 2)))
            
            team_goal = float(week1_record["Goals and Objectives: Team goal achievement (%)"].values[0])
            team_goal = min(100.0, max(50.0, round(team_goal * (1 + improvement_factor * 0.7), 2)))
            
            contribution = float(week1_record["Goals and Objectives: Contribution to company vision (1-5)"].values[0])
            contribution = min(5.0, max(1.0, round(contribution * (1 + improvement_factor * 0.5), 2)))
            
            communication = float(week1_record["Collaboration and Teamwork: Communication skills (1-5)"].values[0])
            communication = min(5.0, max(1.0, round(communication * (1 + improvement_factor * 0.5), 2)))
            
            teamwork = float(week1_record["Collaboration and Teamwork: Ability to work in a team (1-5)"].values[0])
            teamwork = min(5.0, max(1.0, round(teamwork * (1 + improvement_factor * 0.5), 2)))
            
            kpi_data = {
                "Productivity: Number of tasks completed": tasks_completed,
                "Productivity: Time to complete tasks (hours/task)": time_per_task,
                "Quality of Work: Error rate (%)": error_rate,
                "Quality of Work: Customer satisfaction rate (%)": customer_satisfaction,
                "Presence and Punctuality: Attendance rate (%)": attendance,
                "Presence and Punctuality: Punctuality rate (%)": punctuality,
                "Goals and Objectives: Individual goal achievement (%)": individual_goal,
                "Goals and Objectives: Team goal achievement (%)": team_goal,
                "Goals and Objectives: Contribution to company vision (1-5)": contribution,
                "Collaboration and Teamwork: Communication skills (1-5)": communication,
                "Collaboration and Teamwork: Ability to work in a team (1-5)": teamwork
            }
        else:
            # If employee not in week 1, generate random data
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
                # Generate random data for underperformers
                kpi_data = {
                    "Productivity: Number of tasks completed": np.random.randint(8, 15),
                    "Productivity: Time to complete tasks (hours/task)": round(np.random.uniform(2.8, 4.5), 2),
                    "Quality of Work: Error rate (%)": round(np.random.uniform(4.5, 9.0), 2),
                    "Quality of Work: Customer satisfaction rate (%)": round(np.random.uniform(65.0, 82.0), 2),
                    "Presence and Punctuality: Attendance rate (%)": round(np.random.uniform(75.0, 95.0), 2),
                    "Presence and Punctuality: Punctuality rate (%)": round(np.random.uniform(70.0, 95.0), 2),
                    "Goals and Objectives: Individual goal achievement (%)": round(np.random.uniform(65.0, 85.0), 2),
                    "Goals and Objectives: Team goal achievement (%)": round(np.random.uniform(60.0, 80.0), 2),
                    "Goals and Objectives: Contribution to company vision (1-5)": round(np.random.uniform(2.0, 4.0), 2),
                    "Collaboration and Teamwork: Communication skills (1-5)": round(np.random.uniform(2.0, 4.0), 2),
                    "Collaboration and Teamwork: Ability to work in a team (1-5)": round(np.random.uniform(2.0, 4.0), 2)
                }
    else:
        # If no week 1 data available, generate random data
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
            # Generate random data for underperformers
            kpi_data = {
                "Productivity: Number of tasks completed": np.random.randint(8, 15),
                "Productivity: Time to complete tasks (hours/task)": round(np.random.uniform(2.8, 4.5), 2),
                "Quality of Work: Error rate (%)": round(np.random.uniform(4.5, 9.0), 2),
                "Quality of Work: Customer satisfaction rate (%)": round(np.random.uniform(65.0, 82.0), 2),
                "Presence and Punctuality: Attendance rate (%)": round(np.random.uniform(75.0, 95.0), 2),
                "Presence and Punctuality: Punctuality rate (%)": round(np.random.uniform(70.0, 95.0), 2),
                "Goals and Objectives: Individual goal achievement (%)": round(np.random.uniform(65.0, 85.0), 2),
                "Goals and Objectives: Team goal achievement (%)": round(np.random.uniform(60.0, 80.0), 2),
                "Goals and Objectives: Contribution to company vision (1-5)": round(np.random.uniform(2.0, 4.0), 2),
                "Collaboration and Teamwork: Communication skills (1-5)": round(np.random.uniform(2.0, 4.0), 2),
                "Collaboration and Teamwork: Ability to work in a team (1-5)": round(np.random.uniform(2.0, 4.0), 2)
            }
    
    # Make specific employees need intervention to ensure we have cases requiring help
    if employee["Employee ID"] == "EMP003":  # Will need psychologist
        kpi_data.update({
            "Productivity: Number of tasks completed": max(5, int(kpi_data["Productivity: Number of tasks completed"] * 0.7)),
            "Productivity: Time to complete tasks (hours/task)": min(6.0, kpi_data["Productivity: Time to complete tasks (hours/task)"] * 1.3),
            "Quality of Work: Error rate (%)": min(12.0, kpi_data["Quality of Work: Error rate (%)"] * 1.5),
            "Presence and Punctuality: Attendance rate (%)": max(60.0, kpi_data["Presence and Punctuality: Attendance rate (%)"] * 0.7)
        })
    elif employee["Employee ID"] == "EMP006":  # Will need conflict resolution
        kpi_data.update({
            "Collaboration and Teamwork: Ability to work in a team (1-5)": max(1.5, kpi_data["Collaboration and Teamwork: Ability to work in a team (1-5)"] * 0.6),
            "Collaboration and Teamwork: Communication skills (1-5)": max(1.8, kpi_data["Collaboration and Teamwork: Communication skills (1-5)"] * 0.7),
            "Goals and Objectives: Team goal achievement (%)": max(50.0, kpi_data["Goals and Objectives: Team goal achievement (%)"] * 0.7)
        })
        
    # Add employee info
    kpi_data.update(employee)
    kpi_week2_data.append(kpi_data)

# Create DataFrame
kpi_week2_df = pd.DataFrame(kpi_week2_data)

# Display the data
print(kpi_week2_df)

# Export to CSV
kpi_week2_df.to_csv("Weekly_KPI_Data__IT_Support___Week_2_with_IDs.csv", index=False)