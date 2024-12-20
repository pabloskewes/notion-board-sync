from typing import Dict, Any, List
import requests


class NotionClient:
    BASE_URL = "https://api.notion.com/v1"

    def __init__(self, api_key: str, database_id: str):
        self.api_key = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def query_database(self) -> List[Dict[str, Any]]:
        """
        Queries the Notion database and handles pagination.

        Returns:
            List[dict]: A list of all items in the database.
        """
        url = f"{self.BASE_URL}/databases/{self.database_id}/query"
        all_results = []
        next_cursor = None

        while True:
            payload = {"start_cursor": next_cursor} if next_cursor else {}
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=60,
            )

            if not response.ok:
                raise Exception(
                    f"Failed to query Notion database: {response.status_code} - {response.text}"
                )

            data = response.json()
            all_results.extend(data.get("results", []))
            next_cursor = data.get("next_cursor")

            if not next_cursor:
                break

        return all_results
