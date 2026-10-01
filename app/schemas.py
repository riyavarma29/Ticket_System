from pydantic import BaseModel, EmailStr


class TicketCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str
    category: str = "Other"
    priority: str = "Medium"
    assigned_to: str = "Unassigned"


class TicketUpdate(BaseModel):
    status: str
    priority: str
    assigned_to: str
    notes: str


class TicketResponse(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    category: str
    priority: str
    status: str
    assigned_to: str
    notes: str | None
    created_at: object
    updated_at: object

    class Config:
        orm_mode = True