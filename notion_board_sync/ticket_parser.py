from typing import List
from notion_board_sync.types import Ticket


def parse_tickets(raw_data: dict) -> List[Ticket]:
    """
    Parses raw Notion database data into a list of Ticket objects.

    Args:
        raw_data (dict): The JSON response from the Notion API.

    Returns:
        List[Ticket]: A list of parsed Ticket objects.
    """
    tickets = []
    for page in raw_data.get("results", []):
        props = page["properties"]
        tickets.append(
            Ticket(
                id=page["id"],
                title=(
                    props["Name"]["title"][0]["text"]["content"]
                    if props["Name"]["title"]
                    else "Untitled"
                ),
                assignees=[person["id"] for person in props["Assigné à"]["people"]],
                status=(
                    props["État"]["select"]["name"] if props["État"]["select"] else None
                ),
                priority=(
                    props["Priorité"]["select"]["name"]
                    if props["Priorité"]["select"]
                    else None
                ),
                estimation=props["Estimation"]["number"],
                url=page["url"],
            )
        )
    return tickets
