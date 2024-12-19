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
