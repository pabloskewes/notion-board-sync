from datetime import datetime

from sqlalchemy.orm import Session

from notion_board_sync.ticket_parser import parse_tickets
from notion_board_sync.db import TicketDB
from notion_board_sync.types import TicketState, UpdateInfo


def sync_notion_and_db_tickets(
    notion_client,
    db_session: Session,
) -> list[UpdateInfo]:
    """
    Sync tickets from Notion and update the local database.

    Args:
        notion_client: The NotionClient instance for fetching tickets.
        db_session: The database session for updating tickets.

    Returns:
        List[UpdateInfo]: A list of created, updated, or deleted tickets
            to notify about.
    """
    raw_data = notion_client.query_database()
    current_tickets = parse_tickets(raw_data)

    updates_to_notify: list[UpdateInfo] = []
    current_ticket_ids = {ticket.id for ticket in current_tickets}

    # Handle existing tickets in the database
    for db_ticket in db_session.query(TicketDB).all():
        if db_ticket.id not in current_ticket_ids:
            # Ticket exists in the database but not in Notion -> Deleted
            before_state = TicketState(
                title=db_ticket.title,
                status=db_ticket.status,
                priority=db_ticket.priority,
            )
            updates_to_notify.append(
                UpdateInfo(ticket=None, before=before_state, current=None)
            )
            db_session.delete(db_ticket)

    # Handle tickets fetched from Notion
    for ticket in current_tickets:
        db_ticket = db_session.query(TicketDB).filter_by(id=ticket.id).first()

        before_state = None
        if db_ticket:
            before_state = TicketState(
                title=db_ticket.title,
                status=db_ticket.status,
                priority=db_ticket.priority,
            )

            current_state = TicketState(
                title=ticket.title,
                status=ticket.status,
                priority=ticket.priority,
            )

            # Skip if there are no changes
            if before_state == current_state:
                continue

            # Update the database record
            db_ticket.title = ticket.title
            db_ticket.status = ticket.status
            db_ticket.priority = ticket.priority
            db_ticket.last_edited_time = datetime.fromisoformat(
                ticket.last_edited_time,
            )

        else:
            # New ticket -> Create in database
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

            current_state = TicketState(
                title=ticket.title,
                status=ticket.status,
                priority=ticket.priority,
            )

        updates_to_notify.append(
            UpdateInfo(
                ticket=ticket,
                before=before_state,
                current=current_state,
            )
        )

    db_session.commit()

    return updates_to_notify
