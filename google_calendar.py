from googleapiclient.discovery import build
from google.oauth2 import service_account
from urllib.parse import urlencode
import pytz

SERVICE_ACCOUNT_FILE = 'service_account_key.json'
SCOPES = ['<https://www.googleapis.com/auth/calendar>']

def get_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service

def create_event(event_name, start_time, end_time, description="", location=""):
    service = get_service()

    event = {
        'summary': event_name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Yerevan',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Yerevan',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')

def create_event_link(event_name, start_time, end_time, description="", location=""):
    if start_time.tzinfo is None:
        raise ValueError("Start time must be timezone-aware.")
    if end_time.tzinfo is None:
        raise ValueError("End time must be timezone-aware.")

    start_time_utc = start_time.astimezone(pytz.utc)
    end_time_utc = end_time.astimezone(pytz.utc)

    start_time_str = start_time_utc.strftime("%Y%m%dT%H%M%SZ")
    end_time_str = end_time_utc.strftime("%Y%m%dT%H%M%SZ")

    event_details = {
        'text': event_name,
        'dates': f"{start_time_str}/{end_time_str}",
        'details': description,
        'location': location,
        'sf': True,
        'output': 'xml',
    }

    link = f"<https://www.google.com/calendar/render?action=TEMPLATE&{urlencode(event_details)}>"
    return link
