from datetime import datetime

from sqlalchemy.orm import Session

from notion_board_sync.ticket_parser import parse_tickets
from notion_board_sync.db import TicketDB
from notion_board_sync.types import Ticket


def sync_tickets(
    notion_client,
    db_session: Session,
) -> list[Ticket]:
    """
    Sync tickets from Notion and update the local database.

    Args:
        notion_client: The NotionClient instance for fetching tickets.
        db_session: The database session for updating tickets.

    Returns:
        List[Ticket]: A list of new or updated tickets to send notifications for.
    """
    # Fetch tickets from Notion
    raw_data = notion_client.query_database()
    current_tickets = parse_tickets(raw_data)

    tickets_to_notify = []

    for ticket in current_tickets:
        # Check if the ticket exists in the database
        db_ticket = db_session.query(TicketDB).filter_by(id=ticket.id).first()

        if not db_ticket:
            # New ticket: Add to the database and mark for notification
            new_ticket = TicketDB(
                id=ticket.id,
                title=ticket.title,
                status=ticket.status,
                priority=ticket.priority,
                estimation=ticket.estimation,
                url=ticket.url,
                last_edited_time=datetime.fromisoformat(
                    ticket.last_edited_time,
                ),
            )
            db_session.add(new_ticket)
            tickets_to_notify.append(ticket)
            print(f"New ticket added: {ticket.title}")

        else:
            # Check for updates
            updated = False
            if db_ticket.status != ticket.status:
                updated = True
                db_ticket.status = ticket.status
            if db_ticket.priority != ticket.priority:
                updated = True
                db_ticket.priority = ticket.priority
            if db_ticket.last_edited_time != datetime.fromisoformat(
                ticket.last_edited_time
            ):
                updated = True
                db_ticket.last_edited_time = datetime.fromisoformat(
                    ticket.last_edited_time
                )

            if updated:
                tickets_to_notify.append(ticket)
                print(f"Updated ticket: {ticket.title}")

    db_session.commit()

    return tickets_to_notify
