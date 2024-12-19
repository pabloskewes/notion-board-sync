from typing import Optional

import requests
from notion_board_sync.config import settings


class NotionDatabaseClient:
    """
    A client to interact with a specific Notion database.
    """

    def __init__(
        self, database_id: Optional[str] = None, notion_api_key: Optional[str] = None
    ):
        """
        Initializes the NotionDatabaseClient with a database ID and API key.

        Args:
            database_id (str, optional): The ID of the Notion database to
                interact with.
            notion_api_key (str, optional): The Notion API key to use for
                authentication.
        """
        self.database_id = database_id or settings.notion_database_id
        self.notion_api_key = notion_api_key or settings.notion_api_key

        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_api_key}",
            "Notion-Version": "2022-06-28",
        }

    def _send_request(self, method: str, endpoint: str, data=None) -> dict:
        """
        Sends an HTTP request to the Notion API.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            endpoint (str): The API endpoint (relative to the base URL).
            data (dict, optional): The JSON payload to include in the request.
                Defaults to None.

        Returns:
            dict: The parsed JSON response from the Notion API.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method, url, headers=self.headers, json=data, timeout=10
        )

        if not response.ok:
            raise Exception(
                f"Error {method} {endpoint}: {response.status_code} - {response.text}"
            )

        return response.json()

    def fetch_database(self):
        """
        Fetches the contents of the configured Notion database.

        Returns:
            dict: The JSON representation of the database contents.
        """
        return self._send_request("POST", f"/databases/{self.database_id}/query")

    def get_page_details(self, page_id: str):
        """
        Fetches details of a specific page in the configured Notion database.

        Args:
            page_id (str): The ID of the Notion page to fetch.

        Returns:
            dict: The JSON representation of the page details.
        """
        return self._send_request("GET", f"/pages/{page_id}")


if __name__ == "__main__":
    # Example usage of the NotionDatabaseClient
    notion_client = NotionDatabaseClient()
    try:
        database = notion_client.fetch_database()
        print("Database fetched successfully!")
        print(database)
    except Exception as e:
        print(f"Error: {e}")
