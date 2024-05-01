

from init import scheduler
from google_api import update_google_row


# Запускает плпнировцики
async def start_scheduler():
    scheduler.add_job(update_google_row, 'interval', seconds=3)
    scheduler.start()
