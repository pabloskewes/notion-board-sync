import logging
from typing import List

from notion_board_sync.types import UpdateInfo


LOGGER = logging.getLogger(__name__)


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
            # New ticket notification
            message = f"""
            *New Ticket:* {update.ticket.title}
            *Status:* {update.current.status or 'N/A'}
            *Priority:* {update.current.priority or 'N/A'}
            *URL:* {update.ticket.url}
            """
        elif update.is_deleted:
            # Deleted ticket notification
            message = f"""
            *Deleted Ticket:* {update.before.title}
            """
        elif update.is_updated:
            # Updated ticket notification
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

            message = f"""
            *Updated Ticket:* {update.ticket.title}
            {"\n".join(changes)}
            *URL:* {update.ticket.url}
            """
        else:
            # No actionable updates
            continue

        # Send the Slack message
        slack_client.send_message(channel=slack_channel, text=message)
        LOGGER.info(
            f"Notification sent for ticket: {update.ticket.title if update.ticket else update.before.title}"
        )
