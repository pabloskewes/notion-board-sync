import logging
import time

import schedule

from notion_board_sync.notion_client import NotionClient
from notion_board_sync.slack_client import SlackClient
from notion_board_sync.sync import sync_notion_and_db_tickets
from notion_board_sync.notifications import send_notifications
from notion_board_sync.db import Session
from notion_board_sync.config import settings

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOG_LEVEL)


def run_notion_board_sync():
    LOGGER.info("Starting Notion-Board-Sync...")
    init_time = time.perf_counter()

    notion_client = NotionClient(
        api_key=settings.NOTION_API_KEY,
        database_id=settings.NOTION_DATABASE_ID,
    )
    slack_client = SlackClient(bot_token=settings.SLACK_BOT_TOKEN)
    db_session = Session()

    try:
        # Sync tickets and gather updates
        LOGGER.info("Syncing tickets...")
        updates = sync_notion_and_db_tickets(notion_client, db_session)
        LOGGER.info(f"Sync completed. Found {len(updates)} updates.")

        # Send notifications
        if updates:
            LOGGER.info("Sending notifications...")
            send_notifications(
                slack_client,
                updates,
                settings.SLACK_CHANNEL_ID,
            )
            LOGGER.info("Notifications sent successfully.")
        else:
            LOGGER.info("No updates to notify.")

    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
    finally:
        db_session.close()

    LOGGER.info(f"Finished in {time.perf_counter() - init_time:.2f} seconds.")


def schedule_sync():
    schedule.every(settings.SYNC_INTERVAL_MINUTES).minutes.do(
        run_notion_board_sync,
    )
    while True:
        schedule.run_pending()
        time.sleep(1)


def manual_sync():
    while True:
        user_input = input("Sync Now? (y/n): ")
        if user_input.lower() == "y":
            run_notion_board_sync()
        else:
            break


if __name__ == "__main__":
    # schedule_sync()
    manual_sync()
