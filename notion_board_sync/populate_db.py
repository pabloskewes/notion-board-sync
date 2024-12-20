from tqdm import tqdm
from sqlalchemy.orm import Session

from notion_board_sync.db import TicketDB, Session as DBSession
from notion_board_sync.notion_client import NotionClient
from notion_board_sync.sync import sync_notion_and_db_tickets
from notion_board_sync.config import settings


def main():
    notion_client = NotionClient(
        api_key=settings.NOTION_API_KEY,
        database_id=settings.NOTION_DATABASE_ID,
    )
    db_session: Session = DBSession()

    try:
        # Perform the sync and track progress with tqdm
        print("Syncing tickets from Notion...")
        updates = sync_notion_and_db_tickets(notion_client, db_session)
        for _ in tqdm(updates, desc="Processing tickets", unit="ticket"):
            pass

        # Fetch and display results from the database
        ticket_count = db_session.query(TicketDB).count()
        print(f"\nTotal tickets in the database: {ticket_count}")

        # Print an example ticket
        example_ticket = db_session.query(TicketDB).first()
        if example_ticket:
            print("\nExample ticket from the database:")
            print(f"ID: {example_ticket.id}")
            print(f"Title: {example_ticket.title}")
            print(f"Status: {example_ticket.status}")
            print(f"Priority: {example_ticket.priority}")
            print(f"URL: {example_ticket.url}")
        else:
            print("\nNo tickets found in the database.")

    finally:
        db_session.close()


if __name__ == "__main__":
    main()
