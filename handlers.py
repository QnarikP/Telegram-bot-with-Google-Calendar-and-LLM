from telegram import Update
from telegram.ext import ContextTypes
import datetime
import pytz
from google_calendar import create_event, create_event_link, get_service

YEREVAN_TZ = pytz.timezone('Asia/Yerevan')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greeting = (
        "Hello! I'm your personal assistant bot for managing your Google Calendar.\\n\\n"
        "You can use the following commands:\\n"
        "/addevent \\"Event Name\\" YYYY-MM-DD HH:MM YYYY-MM-DD HH:MM - Add an event to your calendar\\n"
        "/createeventlink \\"Event Name\\" YYYY-MM-DD HH:MM YYYY-MM-DD HH:MM - Create a link to add an event to your calendar\\n"
        "/listevents YYYY-MM-DD - List all events for a specific day\\n"
        "/deleteevent \\"Event Name\\" - Delete an event by name\\n"
        "/help - Get help on how to use me"
    )
    await update.message.reply_text(greeting)

async def add_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = update.message.text.split(" ")
        event_name = args[1]
        start_time = datetime.datetime.strptime(args[2] + " " + args[3], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(args[4] + " " + args[5], "%Y-%m-%d %H:%M")

        start_time = YEREVAN_TZ.localize(start_time)
        end_time = YEREVAN_TZ.localize(end_time)

        calendar_link = create_event(event_name, start_time, end_time)
        await update.message.reply_text(f'Event "{event_name}" added to your Google Calendar.\\nView it here: {calendar_link}')

    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /addevent \\"Event Name\\" YYYY-MM-DD HH:MM YYYY-MM-DD HH:MM")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def create_event_link_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        args = update.message.text.split(" ")
        event_name = args[1]
        start_time = datetime.datetime.strptime(args[2] + " " + args[3], "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(args[4] + " " + args[5], "%Y-%m-%d %H:%M")

        start_time = YEREVAN_TZ.localize(start_time)
        end_time = YEREVAN_TZ.localize(end_time)

        calendar_link = create_event_link(event_name, start_time, end_time)
        await update.message.reply_text(f'Event link created: {calendar_link}')

    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /createeventlink \\"Event Name\\" YYYY-MM-DD HH:MM YYYY-MM-DD HH:MM")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        date_str = update.message.text.split(" ")[1]
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

        service = get_service()
        time_min = datetime.datetime.combine(date, datetime.time.min).isoformat() + 'Z'
        time_max = datetime.datetime.combine(date, datetime.time.max).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            await update.message.reply_text("No events found.")
        else:
            message = "Here are your events:\\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                message += f"- {event['summary']} at {start}\\n"
            await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def delete_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        event_name = " ".join(context.args)

        service = get_service()
        events_result = service.events().list(
            calendarId='primary',
            q=event_name,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            await update.message.reply_text(f'No event found with name "{event_name}".')
        else:
            for event in events:
                service.events().delete(calendarId='primary', eventId=event['id']).execute()
            await update.message.reply_text(f'Event "{event_name}" deleted.')
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "You can use the following commands:\\n"
        "/add_event \\"Event Name\\" start=\\"YYYY-MM-DDTHH:MM:SS\\" end=\\"YYYY-MM-DDTHH:MM:SS\\" "
        "[location=\\"Location\\"] [description=\\"Description\\"] [color=\\"Color\\"]\\n"
        "/list_events - List all events\\n"
        "/delete_event \\"Event Name\\" - Delete an event\\n"
        "/reload - Reload the configuration\\n"
    )
    await update.message.reply_text(help_text)
