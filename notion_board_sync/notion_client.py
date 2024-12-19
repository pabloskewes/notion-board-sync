from typing import Dict, Any

import requests


class NotionClient:
    """
    A simple client to interact with the Notion API.
    """

    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, api_key: str, database_id: str):
        """
        Initialize the NotionClient with API key and database ID.

        Args:
            api_key (str): The Notion API key.
            database_id (str): The ID of the Notion database to query.
        """
        self.api_key = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def query_database(self) -> Dict[str, Any]:
        """
        Queries the Notion database and returns the raw JSON response.

        Returns:
            dict: The JSON response from the Notion API.
        """
        url = f"{self.BASE_URL}/databases/{self.database_id}/query"
        response = requests.post(url, headers=self.headers, timeout=10)

        if not response.ok:
            raise Exception(
                f"Failed to query Notion database: {response.status_code} - {response.text}"
            )

        return response.json()
