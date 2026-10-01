from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models
from datetime import datetime
import random


def generate_ticket_id(db: Session):
    while True:
        ticket_id = f"TKT-{random.randint(1000, 9999)}"

        existing = (
            db.query(models.Ticket)
            .filter(models.Ticket.ticket_id == ticket_id)
            .first()
        )

        if not existing:
            return ticket_id


def create_ticket(db: Session, data):

    ticket = models.Ticket(
        ticket_id=generate_ticket_id(db),
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        subject=data.subject,
        description=data.description,
        category=data.category,
        priority=data.priority,
        assigned_to=data.assigned_to,
        status="Open",
        notes="",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_all_tickets(
    db: Session,
    search=None,
    status=None,
    priority=None,
    category=None
):

    query = db.query(models.Ticket)

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                models.Ticket.customer_name.ilike(search_term),
                models.Ticket.customer_email.ilike(search_term),
                models.Ticket.subject.ilike(search_term),
                models.Ticket.ticket_id.ilike(search_term)
            )
        )

    if status:
        query = query.filter(models.Ticket.status == status)

    if priority:
        query = query.filter(models.Ticket.priority == priority)

    if category:
        query = query.filter(models.Ticket.category == category)

    return query.order_by(
        models.Ticket.created_at.desc()
    ).all()


def get_ticket(db: Session, ticket_id: str):

    return (
        db.query(models.Ticket)
        .filter(models.Ticket.ticket_id == ticket_id)
        .first()
    )


def update_ticket(
    db: Session,
    ticket_id: str,
    status: str,
    priority: str,
    assigned_to: str,
    notes: str
):

    ticket = get_ticket(db, ticket_id)

    if not ticket:
        return None

    ticket.status = status
    ticket.priority = priority
    ticket.assigned_to = assigned_to
    ticket.notes = notes
    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket


def get_dashboard_stats(db: Session):

    total = db.query(models.Ticket).count()

    open_count = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "Open")
        .count()
    )

    progress_count = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "In Progress")
        .count()
    )

    closed_count = (
        db.query(models.Ticket)
        .filter(models.Ticket.status == "Closed")
        .count()
    )

    critical_count = (
        db.query(models.Ticket)
        .filter(models.Ticket.priority == "Critical")
        .count()
    )

    return {
        "total": total,
        "open": open_count,
        "in_progress": progress_count,
        "closed": closed_count,
        "critical": critical_count
    }