from typing import List, Optional
from pydantic import BaseModel


class Ticket(BaseModel):
    id: str
    title: str
    assignees: List[str]
    status: Optional[str]
    priority: Optional[str]
    estimation: Optional[float]
    url: str
    last_edited_time: str


class TicketState(BaseModel):
    title: str
    status: Optional[str]
    priority: Optional[str]


class UpdateInfo(BaseModel):
    ticket: Ticket
    before: Optional[TicketState] = None
    current: TicketState

    @property
    def updated(self) -> bool:
        """Determine if the ticket has been updated."""
        return self.before != self.current
