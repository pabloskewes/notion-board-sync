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
    ticket: Optional[Ticket]
    before: Optional[TicketState] = None
    current: Optional[TicketState] = None

    @property
    def is_created(self) -> bool:
        """Determine if the ticket was newly created."""
        return self.before is None and self.current is not None

    @property
    def is_deleted(self) -> bool:
        """Determine if the ticket was deleted."""
        return self.current is None

    @property
    def is_updated(self) -> bool:
        """Determine if the ticket was updated."""
        return (
            self.before is not None
            and self.current is not None
            and self.before != self.current
        )
