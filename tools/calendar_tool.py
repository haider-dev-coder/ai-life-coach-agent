from langchain.tools import tool
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os
from config import GOOGLE_CREDENTIALS_FILE, CALENDAR_TOKEN_FILE

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_calendar_service():
    creds = None
    if os.path.exists(CALENDAR_TOKEN_FILE):
        with open(CALENDAR_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(CALENDAR_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

@tool
def add_to_calendar(event: str, date: str) -> str:
    """
    Adds an event to Google Calendar
    date format: 'YYYY-MM-DDTHH:MM:SS'
    """
    service = get_calendar_service()
    event_body = {
        "summary": event,
        "start": {"dateTime": date, "timeZone": "UTC"},
        "end": {"dateTime": date, "timeZone": "UTC"},
    }
    created_event = service.events().insert(calendarId='primary', body=event_body).execute()
    return f"Added '{event}' to calendar: {created_event.get('htmlLink')}"
