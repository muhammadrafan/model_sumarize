# summary_manager.py (in pages/helper folder)
# Manages summary data retrieval and analysis for other pages

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Import shared configuration
from pages.helper.config import SUMMARY_DB, STRESS_THRESHOLD, CONFLICT_THRESHOLD

def get_all_summaries():
    """
    Get all employee summaries from the database
    """
    if not os.path.exists(SUMMARY_DB):
        return {}
    
    try:
        with open(SUMMARY_DB, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading summaries: {e}")
        return {}

def get_employee_summary(employee_id):
    """
    Get summary for a specific employee
    """
    summaries = get_all_summaries()
    return summaries.get(str(employee_id), None)

def get_employee_summary_by_name(employee_name):
    """
    Get summary for a specific employee by name
    """
    summaries = get_all_summaries()
    for emp_id, data in summaries.items():
        if data['employee_name'].lower() == employee_name.lower():
            return data
    return None

def get_recent_summaries(days=7):
    """
    Get summaries generated within the last X days
    """
    summaries = get_all_summaries()
    recent_summaries = {}
    
    cut_off = (datetime.now() - timedelta(days=days)).isoformat()
    
    for emp_id, data in summaries.items():
        if 'timestamp' in data and data['timestamp'] >= cut_off:
            recent_summaries[emp_id] = data
    
    return recent_summaries

def get_employees_needing_psychologist():
    """
    Get list of employees that need psychological help
    """
    summaries = get_all_summaries()
    employees = []
    
    for emp_id, data in summaries.items():
        if data.get('need_psychologist', False):
            employees.append({
                'employee_id': emp_id,
                'employee_name': data['employee_name'],
                'summary': data['summary']
            })
    
    return employees

def get_employees_needing_conflict_resolution():
    """
    Get list of employees that need conflict resolution
    """
    summaries = get_all_summaries()
    employees = []
    
    for emp_id, data in summaries.items():
        if data.get('need_conflict_resolution', False):
            employees.append({
                'employee_id': emp_id,
                'employee_name': data['employee_name'],
                'summary': data['summary']
            })
    
    return employees

def get_context_for_sidekick(employee_name=None):
    """
    Get relevant context for sidekick assistant
    Returns a formatted context string
    """
    if employee_name:
        # Get specific employee summary
        employee_data = get_employee_summary_by_name(employee_name)
        if employee_data:
            context = f"""
            Employee Performance Context for {employee_data['employee_name']}:
            
            {employee_data['summary']}
            
            Performance Metrics:
            - Tasks Completed: {employee_data.get('performance_metrics', {}).get('tasks_completed', 'Unknown')}
            - Time per Task: {employee_data.get('performance_metrics', {}).get('time_per_task', 'Unknown')} hours
            - Error Rate: {employee_data.get('performance_metrics', {}).get('error_rate', 'Unknown')}%
            - Customer Satisfaction: {employee_data.get('performance_metrics', {}).get('customer_satisfaction', 'Unknown')}%
            """
            
            # Add recommendations if needed
            if employee_data.get('need_psychologist', False):
                context += "\nNOTE: This employee may benefit from psychological support."
            
            if employee_data.get('need_conflict_resolution', False):
                context += "\nNOTE: This employee may benefit from conflict resolution support."
                
            return context
    
    # If no specific employee or not found, return general context
    summaries = get_all_summaries()
    if not summaries:
        return "No employee performance data available."
    
    # Get counts for general status
    total = len(summaries)
    need_psych = len([1 for data in summaries.values() if data.get('need_psychologist', False)])
    need_conflict = len([1 for data in summaries.values() if data.get('need_conflict_resolution', False)])
    
    context = f"""
    Team Performance Context:
    - Total employees analyzed: {total}
    - Employees potentially needing psychological support: {need_psych}
    - Employees potentially needing conflict resolution: {need_conflict}
    """
    
    return context

def get_context_for_psycholog(employee_name=None):
    """
    Get relevant context for psycholog assistant
    Focuses on psychological aspects and stress indicators
    """
    if employee_name:
        # Get specific employee summary
        employee_data = get_employee_summary_by_name(employee_name)
        if employee_data:
            # Extract just the psychological aspects
            context = f"""
            Psychological Context for {employee_data['employee_name']}:
            
            {employee_data.get('structured_summary', {}).get('Performance Summary', 'No data')}
            
            Areas for improvement: 
            {employee_data.get('structured_summary', {}).get('Improvement Areas', 'No data')}
            
            Recommendation: 
            {employee_data.get('structured_summary', {}).get('Recommendation', 'No data')}
            """
            
            # Add specific flag if they need psychological support
            if employee_data.get('need_psychologist', False):
                context += f"\n\nNOTE: The employee has shown indicators of stress or anxiety that may require support."
                
            return context
    
    # Return list of employees needing psychological support
    employees = get_employees_needing_psychologist()
    if not employees:
        return "No employees currently flagged as needing psychological support."
    
    context = "Employees potentially needing psychological support:\n\n"
    for i, emp in enumerate(employees):
        context += f"{i+1}. {emp['employee_name']}\n"
    
    return context

def get_context_for_conflict_resolution(employee_name=None):
    """
    Get relevant context for conflict resolution assistant
    Focuses on team dynamics and conflict indicators
    """
    if employee_name:
        # Get specific employee summary
        employee_data = get_employee_summary_by_name(employee_name)
        if employee_data:
            # Extract just the conflict aspects
            context = f"""
            Conflict Resolution Context for {employee_data['employee_name']}:
            
            {employee_data.get('structured_summary', {}).get('Performance Summary', 'No data')}
            
            Team collaboration metrics:
            - Team goal achievement: {employee_data.get('performance_metrics', {}).get('team_goal_achievement', 'Unknown')}%
            
            Areas for improvement: 
            {employee_data.get('structured_summary', {}).get('Improvement Areas', 'No data')}
            
            Recommendation: 
            {employee_data.get('structured_summary', {}).get('Recommendation', 'No data')}
            """
            
            # Add specific flag if they need conflict resolution
            if employee_data.get('need_conflict_resolution', False):
                context += f"\n\nNOTE: The employee has shown indicators of team conflicts that may require mediation."
                
            return context
    
    # Return list of employees needing conflict resolution
    employees = get_employees_needing_conflict_resolution()
    if not employees:
        return "No employees currently flagged as needing conflict resolution."
    
    context = "Employees potentially needing conflict resolution:\n\n"
    for i, emp in enumerate(employees):
        context += f"{i+1}. {emp['employee_name']}\n"
    
    return context

def analyze_and_recommend_services(user_input, employee_context=None):
    """
    Analyze user input and context to recommend appropriate services
    Returns a tuple of (need_psychologist, need_conflict_resolution, recommendation_text)
    """
    # Look for keywords indicating psychological issues
    psych_keywords = ["stress", "anxiety", "worried", "depressed", "overwhelmed", 
                      "burnout", "tired", "exhausted", "mental health", "sad",
                      "unhappy", "feel bad", "can't sleep", "trouble sleeping"]
    
    # Look for keywords indicating conflict issues
    conflict_keywords = ["argument", "conflict", "disagreement", "team issues", 
                         "colleague", "fighting", "tension", "teammates", 
                         "communication problems", "misunderstanding", "clash"]
    
    # Check for keyword matches
    need_psychologist = any(keyword in user_input.lower() for keyword in psych_keywords)
    need_conflict_resolution = any(keyword in user_input.lower() for keyword in conflict_keywords)
    
    # If we have employee context, use that as well
    if employee_context:
        employee_data = employee_context
        need_psychologist = need_psychologist or employee_data.get('need_psychologist', False)
        need_conflict_resolution = need_conflict_resolution or employee_data.get('need_conflict_resolution', False)
    
    # Create recommendation text
    recommendation = ""
    if need_psychologist and need_conflict_resolution:
        recommendation = """Based on our conversation, you might benefit from both:
        1. Speaking with a psychologist about stress management
        2. Using our conflict resolution tools to address team dynamics
        
        Would you like me to connect you with either service?"""
    elif need_psychologist:
        recommendation = """Based on our conversation, you might benefit from speaking with our psychological support service about stress management and personal well-being.
        
        Would you like me to connect you to the Psycholog service?"""
    elif need_conflict_resolution:
        recommendation = """Based on our conversation, you might benefit from our conflict resolution tools to help address team dynamics and communication.
        
        Would you like me to connect you to the Conflict Resolution service?"""
    
    return (need_psychologist, need_conflict_resolution, recommendation)