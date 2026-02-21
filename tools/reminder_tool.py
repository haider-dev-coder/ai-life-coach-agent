from langchain.tools import tool
import datetime

@tool
def set_reminder(reminder_text: str, time_str: str) -> str:
    """
    Sets a reminder with the given text at the specified time.
    Returns a confirmation string.
    """
    # You can add actual reminder logic here if needed
    return f"Reminder set: '{reminder_text}' at {time_str}"
