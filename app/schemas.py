from pydantic import BaseModel

class TicketCreate(BaseModel):
    customer_name: str
    customer_email: str
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: str
    notes: str

class TicketResponse(BaseModel):
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    notes: str | None

    class Config:
        orm_mode = True