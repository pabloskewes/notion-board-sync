from notion_board_sync.client import NotionClient
from notion_board_sync.parser import parse_tickets
from notion_board_sync.models import Ticket
from notion_board_sync.config import settings


def main():
    client = NotionClient(
        api_key=settings.NOTION_API_KEY,
        database_id=settings.NOTION_DATABASE_ID,
    )
    raw_data = client.query_database()

    tickets: list[Ticket] = parse_tickets(raw_data)

    for ticket in tickets:
        print(f"Ticket: {ticket.title}")
        print(f"  Status: {ticket.status}")
        print(
            f"  Assignees: {', '.join(ticket.assignees) if ticket.assignees else 'None'}"
        )
        print(f"  Priority: {ticket.priority}")
        print(f"  Estimation: {ticket.estimation}")
        print(f"  URL: {ticket.url}")
        print("-" * 50)


if __name__ == "__main__":
    main()
