import re
from datetime import datetime, timedelta

def extract_time_from_task(task_text):
    """Extract time from task text like '7:00 AM' or '18:30'"""
    # Pattern for times like "7:00 AM", "7:30 PM", "07:00", "18:30"
    time_patterns = [
        r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)',  # 7:00 AM
        r'(\d{1,2}):(\d{2})',  # 18:30
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, task_text)
        if match:
            if len(match.groups()) == 3:  # 12-hour format
                hour = int(match.group(1))
                minute = int(match.group(2))
                period = match.group(3).upper()
                
                if period == 'PM' and hour != 12:
                    hour += 12
                elif period == 'AM' and hour == 12:
                    hour = 0
                    
                return f"{hour:02d}:{minute:02d}"
            else:  # 24-hour format
                hour = int(match.group(1))
                minute = int(match.group(2))
                return f"{hour:02d}:{minute:02d}"
    
    return None

def get_reminder_datetime(time_str):
    """Convert time string to tomorrow's datetime"""
    if not time_str:
        return None
    
    tomorrow = datetime.now() + timedelta(days=1)
    hour, minute = map(int, time_str.split(':'))
    
    return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)