import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(44)

# Create employee data (same as week 1 and 2)
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

# Positive survey responses
positive_self_performance = [
    "I've been performing well this month, meeting all my targets.",
    "I'm satisfied with my work performance, have been quite productive.",
    "I believe I've been doing a good job meeting my objectives.",
    "My performance has been strong, I've completed all assigned tasks efficiently.",
    "I feel I've been performing at a high level consistently."
]

positive_goals = [
    "I achieved all my goals this month and even exceeded some targets.",
    "I'm on track with all my objectives for this quarter.",
    "I've completed most of my planned goals ahead of schedule.",
    "My goal completion rate has been excellent this month.",
    "I've been successful in meeting all the goals set for me."
]

positive_challenges = [
    "No significant challenges, just the usual day-to-day issues.",
    "I've been able to overcome minor obstacles without much difficulty.",
    "Nothing particularly challenging this month, it's been smooth.",
    "Just the standard technical issues, nothing major.",
    "No serious challenges to report, everything has been manageable."
]

positive_stress = [
    "My stress levels have been quite manageable.",
    "I've been maintaining a good work-life balance.",
    "No significant stress or anxiety to report.",
    "I'm handling the workload well without feeling overwhelmed.",
    "Work has been busy but not stressful."
]

positive_colleagues = [
    "I have excellent relationships with all my colleagues.",
    "The team environment is very supportive and collaborative.",
    "I enjoy working with everyone on the team.",
    "My working relationships are strong and productive.",
    "I have great rapport with everyone in the department."
]

positive_communication = [
    "Communication flows smoothly in our department.",
    "I haven't experienced any communication issues this month.",
    "Information sharing in the team has been excellent.",
    "Our communication channels are working effectively.",
    "I find it easy to communicate with everyone on the team."
]

positive_conflicts = [
    "No conflicts to report, the team is working harmoniously.",
    "There have been no interpersonal issues this month.",
    "The team dynamic has been very positive with no conflicts.",
    "No disagreements or tensions to mention.",
    "Everyone has been getting along very well."
]

positive_collaboration = [
    "Collaboration within the team has been excellent.",
    "We've been working together effectively on all projects.",
    "Team coordination and support has been outstanding.",
    "Our collaborative efforts have been producing great results.",
    "I'm very satisfied with how we're working together as a team."
]

# Negative survey responses for psychological support needs
negative_stress = [
    "I've been feeling overwhelmed with the workload lately.",
    "I'm experiencing high levels of stress that are affecting my sleep.",
    "The pressure to meet deadlines is causing me significant anxiety.",
    "I'm struggling to cope with the current work demands and it's affecting my mental health.",
    "I've been feeling burnt out and having trouble focusing due to stress.",
    "The constant pressure is making it difficult for me to maintain my work-life balance.",
    "I'm finding it hard to manage my anxiety during team meetings and presentations.",
    "The stress from work has been affecting my personal relationships and overall wellbeing."
]

negative_self_performance = [
    "I'm concerned that I'm falling behind on my objectives.",
    "I don't feel I'm performing at my usual standard lately.",
    "I'm struggling to stay focused and productive during work hours.",
    "My performance has been inconsistent, and I'm worried about it.",
    "I feel like I'm not meeting expectations despite working longer hours."
]

negative_challenges = [
    "I'm having difficulty keeping up with the increasing workload.",
    "Technical challenges are taking longer for me to resolve than usual.",
    "I'm finding it hard to prioritize tasks effectively with so many competing demands.",
    "The complexity of recent projects has been particularly challenging for me.",
    "I'm struggling to adapt to the new systems while maintaining productivity."
]

# Negative survey responses for conflict resolution needs
negative_conflicts = [
    "There have been ongoing disagreements between team members that are affecting productivity.",
    "I'm experiencing difficulties working with specific colleagues due to conflicting work styles.",
    "Recent team conflicts have created a tense atmosphere that's hard to work in.",
    "There are unresolved issues between department members that are hindering collaboration.",
    "Communication breakdowns are leading to frequent misunderstandings and arguments.",
    "The competitive environment is creating unhealthy rivalries within the team.",
    "Certain team members are not respecting boundaries or responsibilities.",
    "Conflicting priorities between team members are causing friction and delays."
]

negative_collaboration = [
    "Collaboration has been challenging due to poor communication.",
    "Some team members aren't pulling their weight in group projects.",
    "I'm finding it difficult to get support from certain colleagues when needed.",
    "The team isn't functioning well as a unit on current projects.",
    "Information silos are preventing effective teamwork."
]

negative_communication = [
    "Important information isn't being shared properly within the team.",
    "There's confusion about project requirements due to inconsistent communication.",
    "I often feel left out of important discussions and decision-making processes.",
    "Feedback is not being delivered constructively, leading to defensiveness.",
    "Communication channels are ineffective, with messages frequently missed or ignored."
]

# Generate survey data
survey_data = []

for employee in employees:
    # Default to positive responses
    survey_response = {
        "Self-Performance": random.choice(positive_self_performance),
        "Goals Achieved": random.choice(positive_goals),
        "Personal Challenges": random.choice(positive_challenges),
        "Stress or Anxiety": random.choice(positive_stress),
        "Relationship with Colleagues": random.choice(positive_colleagues),
        "Communication Issues": random.choice(positive_communication),
        "Team Conflicts": random.choice(positive_conflicts),
        "Team Collaboration": random.choice(positive_collaboration)
    }
    
    # Make specific employees need intervention
    if employee["Employee ID"] == "EMP003":  # Will need psychologist
        survey_response.update({
            "Self-Performance": random.choice(negative_self_performance),
            "Personal Challenges": random.choice(negative_challenges),
            "Stress or Anxiety": random.choice(negative_stress)
        })
    elif employee["Employee ID"] == "EMP006":  # Will need conflict resolution
        survey_response.update({
            "Relationship with Colleagues": "I'm having difficulty working with some team members.",
            "Communication Issues": random.choice(negative_communication),
            "Team Conflicts": random.choice(negative_conflicts),
            "Team Collaboration": random.choice(negative_collaboration)
        })
    # Add a third person who also needs help (randomized issues)
    elif employee["Employee ID"] == "EMP008":  # Another one needing intervention
        if random.random() < 0.5:  # Psychological support
            survey_response.update({
                "Stress or Anxiety": random.choice(negative_stress),
                "Self-Performance": "I'm worried about my declining performance.",
                "Personal Challenges": "I'm finding it increasingly difficult to manage my workload."
            })
        else:  # Conflict resolution
            survey_response.update({
                "Team Conflicts": random.choice(negative_conflicts),
                "Team Collaboration": "Collaboration has become increasingly difficult in our team.",
                "Communication Issues": "There are serious communication breakdowns in our department."
            })
    
    # Add employee info
    survey_response.update(employee)
    survey_data.append(survey_response)

# Create DataFrame
survey_df = pd.DataFrame(survey_data)

# Display the data
print(survey_df)

# Export to CSV
survey_df.to_csv("Survei_Kinerja_Bulanan.csv", index=False)