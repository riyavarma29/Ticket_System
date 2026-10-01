from sqlalchemy import Column, String, DateTime
from datetime import datetime

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(String, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)

    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)

    category = Column(String, default="Other")
    priority = Column(String, default="Medium")
    status = Column(String, default="Open")

    assigned_to = Column(String, default="Unassigned")
    notes = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )