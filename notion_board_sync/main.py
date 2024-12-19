from notion_board_sync.notion_client import NotionClient
from notion_board_sync.slack_client import SlackClient
from notion_board_sync.ticket_parser import parse_tickets
from notion_board_sync.config import settings


def main():
    notion_client = NotionClient(
        api_key=settings.NOTION_API_KEY,
        database_id=settings.NOTION_DATABASE_ID,
    )
    slack_client = SlackClient(bot_token=settings.SLACK_BOT_TOKEN)

    raw_data = notion_client.query_database()
    tickets = parse_tickets(raw_data)

    for ticket in tickets[:5]:
        message = f"""
        *Title:* {ticket.title}
        *Status:* {ticket.status or 'N/A'}
        *Assignees:* {', '.join(ticket.assignees) if ticket.assignees else 'None'}
        *Priority:* {ticket.priority or 'N/A'}
        *Estimation:* {ticket.estimation or 'N/A'}
        *URL:* {ticket.url}
        """
        slack_client.send_message(
            channel=settings.SLACK_CHANNEL_ID,
            text=message,
        )
        print(f"Message sent for ticket: {ticket.title}")


if __name__ == "__main__":
    main()
