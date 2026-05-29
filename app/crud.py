from sqlalchemy.orm import Session
from app import models
from datetime import datetime
import random


def generate_ticket_id():
    return f"TKT-{random.randint(1000,9999)}"


def create_ticket(db: Session, data):

    ticket = models.Ticket(
        ticket_id=generate_ticket_id(),
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        subject=data.subject,
        description=data.description,

        # ADD THESE
        status="Open",
        notes="",
        created_at=datetime.now()
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket

def get_all_tickets(db: Session, search=None, status=None):
    query = db.query(models.Ticket)

    if search:
        query = query.filter(
            models.Ticket.customer_name.contains(search) |
            models.Ticket.customer_email.contains(search) |
            models.Ticket.subject.contains(search) |
            models.Ticket.description.contains(search)
        )

    if status:
        query = query.filter(models.Ticket.status == status)

    return query.all()

def get_ticket(db: Session, ticket_id: str):
    return db.query(models.Ticket).filter(
        models.Ticket.ticket_id == ticket_id
    ).first()

def update_ticket(db: Session, ticket_id: str, status: str, notes: str):
    ticket = get_ticket(db, ticket_id)

    ticket.status = status
    ticket.notes = notes
    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket

