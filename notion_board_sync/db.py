from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class TicketDB(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)  # Ticket ID
    title = Column(String)
    status = Column(String)
    priority = Column(String)
    estimation = Column(Float)
    url = Column(String)
    last_edited_time = Column(DateTime)  # Last edited time in Notion


# Initialize SQLite
engine = create_engine("sqlite:///tickets.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
