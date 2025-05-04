import pandas as pd
import random

# Define possible responses for each column
performance_responses = ['Very Bad', 'Bad', 'Fair', 'Good', 'Very Good']
goal_achieved_responses = ['No goals achieved', 'Some goals achieved', 'All goals achieved']
challenge_responses = ['No challenges', 'Minor challenges', 'Significant challenges']
stress_responses = ['Not at all', 'Occasionally', 'Frequently', 'Almost always']
improvement_responses = ['Focus on self-development', 'Improve time management', 'Enhance communication skills']
relationship_responses = ['Very Bad', 'Bad', 'Fair', 'Good', 'Very Good']
communication_issues_responses = ['No issues', 'Minor issues', 'Major issues']
team_conflict_responses = ['Not at all', 'Slightly', 'Moderately', 'Significantly']
collaboration_responses = ['Very Bad', 'Bad', 'Fair', 'Good', 'Very Good']
interpersonal_issues_responses = ['No issues', 'Minor issues', 'Major issues']
support_responses = ['Not at all', 'Sometimes', 'Often', 'Always']
steps_for_improvement_responses = ['Collaborative approach', 'Focus on self-awareness', 'Improve stress management']
areas_for_improvement_responses = ['Improve communication skills', 'Increase productivity', 'Better stress management']
plans_for_next_month_responses = ['Improve team collaboration', 'Focus on personal growth', 'Increase work efficiency']
comments_responses = ['No comments', 'Need more feedback', 'Improving steadily']

# Generate dummy data
dummy_data = []
for i in range(1, 11):
    dummy_data.append({
        "Self-Performance": random.choice(performance_responses),
        "Goals Achieved": random.choice(goal_achieved_responses),
        "Personal Challenges": random.choice(challenge_responses),
        "Stress or Anxiety": random.choice(stress_responses),
        "Improvement in Personal Performance": random.choice(improvement_responses),
        "Relationship with Colleagues": random.choice(relationship_responses),
        "Communication Issues": random.choice(communication_issues_responses),
        "Team Conflicts": random.choice(team_conflict_responses),
        "Team Collaboration": random.choice(collaboration_responses),
        "Interpersonal Issues": random.choice(interpersonal_issues_responses),
        "Support from Colleagues or Supervisors": random.choice(support_responses),
        "Steps for Improvement": random.choice(steps_for_improvement_responses),
        "Areas for Improvement": random.choice(areas_for_improvement_responses),
        "Plans for Next Month": random.choice(plans_for_next_month_responses),
        "Other Comments": random.choice(comments_responses),
        "Employee Name": f"Employee_{i}",
        "Employee ID": f"EMP{i:04}"
    })

# Create DataFrame and save to CSV
dummy_df = pd.DataFrame(dummy_data)
dummy_df.to_csv('dummy_survey_data.csv', index=False)

# Output the first few rows of the data
print(dummy_df.head())
