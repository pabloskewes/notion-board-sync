import logging
from typing import List

from notion_board_sync.types import UpdateInfo

LOGGER = logging.getLogger(__name__)

NEW_TICKET_MESSAGE = """
*New Ticket:* {ticket_url}
*Status:* {status}
*Priority:* {priority}
"""

DELETED_TICKET_MESSAGE = """
*Deleted Ticket:* {title}
"""

UPDATED_TICKET_MESSAGE = """
*Updated Ticket:* {ticket_url}
{changes}
"""


def format_slack_url(url: str, text: str) -> str:
    """
    Format a URL for Slack message formatting.

    Args:
        url: The URL to format.
        text: The text to display for the URL.

    Returns:
        str: The formatted URL for Slack.
    """
    return f"<{url}|{text}>"


def send_notifications(
    slack_client,
    updates: List[UpdateInfo],
    slack_channel: str,
):
    """
    Send Slack notifications for a list of ticket updates.

    Args:
        slack_client: The SlackClient instance for sending messages.
        updates: The list of updates to notify about.
        slack_channel: The Slack channel ID to send notifications to.
    """
    for update in updates:
        if update.is_created:
            message = NEW_TICKET_MESSAGE.format(
                ticket_url=format_slack_url(
                    update.ticket.url,
                    update.ticket.title,
                ),
                status=update.current.status or "N/A",
                priority=update.current.priority or "N/A",
            )

        elif update.is_deleted:
            message = DELETED_TICKET_MESSAGE.format(
                title=update.before.title,
            )

        elif update.is_updated:
            changes = []
            if update.before.title != update.current.title:
                changes.append(
                    f"*Title:* {update.before.title} → {update.current.title}"
                )
            if update.before.status != update.current.status:
                changes.append(
                    f"*Status:* {update.before.status} → {update.current.status}"
                )
            if update.before.priority != update.current.priority:
                changes.append(
                    f"*Priority:* {update.before.priority} → {update.current.priority}"
                )

            message = UPDATED_TICKET_MESSAGE.format(
                ticket_url=format_slack_url(update.ticket.url, update.ticket.title),
                changes="\n".join(changes),
            )

        else:
            LOGGER.warning("Invalid update type. Skipping...")
            continue

        slack_client.send_message(channel=slack_channel, text=message.strip())
        LOGGER.info(
            f"Notification sent for ticket: {update.ticket.title if update.ticket else update.before.title}"
        )
