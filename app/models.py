from sqlalchemy import Column, String, DateTime
from datetime import datetime

from app.database import Base


class Ticket(Base):

    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, index=True)

    customer_name = Column(String)
    customer_email = Column(String)

    subject = Column(String)
    description = Column(String)

    status = Column(String, default="Open")
    notes = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)