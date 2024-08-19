from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import start, add_event, create_event_link_command, list_events, delete_event, help_command
from config import TELEGRAM_BOT_TOKEN

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addevent", add_event))
    app.add_handler(CommandHandler("createeventlink", create_event_link_command))
    app.add_handler(CommandHandler("listevents", list_events))
    app.add_handler(CommandHandler("deleteevent", delete_event))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()