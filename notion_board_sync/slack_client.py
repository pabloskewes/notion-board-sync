from typing import Any, Dict

import requests

from notion_board_sync.config import settings


class SlackClient:
    """
    A simple client to interact with Slack's API.
    """

    BASE_URL = "https://slack.com/api"

    def __init__(self, bot_token: str = settings.SLACK_BOT_TOKEN):
        """
        Initialize the SlackClient with the bot token.

        Args:
            bot_token (str): The Slack bot token for authentication.
        """
        self.bot_token = bot_token
        self.headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json",
        }

    def send_message(self, channel: str, text: str) -> Dict[str, Any]:
        """
        Sends a message to a Slack channel.

        Args:
            channel (str): The Slack channel ID where the message will be sent.
            text (str): The message content.

        Returns:
            dict: The JSON response from the Slack API.
        """
        url = f"{self.BASE_URL}/chat.postMessage"
        payload = {"channel": channel, "text": text}

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=10,
        )

        if not response.ok:
            raise Exception(
                f"Failed to send message to Slack: {response.status_code} - {response.text}"
            )

        return response.json()
