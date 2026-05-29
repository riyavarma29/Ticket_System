from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    search: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):

    tickets = crud.get_all_tickets(db, search, status)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "tickets": tickets
        }
    )
@app.get("/create", response_class=HTMLResponse)
def create_page(request: Request):

    return templates.TemplateResponse(
        request,
        "create_ticket.html",
        {}
    )
@app.post("/create")
def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...)
):

    db = SessionLocal()

    class Data:
        pass

    data = Data()

    data.customer_name = customer_name
    data.customer_email = customer_email
    data.subject = subject
    data.description = description

    crud.create_ticket(db, data)

    return RedirectResponse("/", status_code=303)

@app.get("/ticket/{ticket_id}", response_class=HTMLResponse)
def ticket_detail(
    request: Request,
    ticket_id: str,
    db: Session = Depends(get_db)
):

    ticket = crud.get_ticket(db, ticket_id)

    return templates.TemplateResponse(
        request,
        "ticket_detail.html",
        {
            "ticket": ticket
        }
    )
@app.post("/ticket/{ticket_id}")
def update_ticket(
    ticket_id: str,
    status: str = Form(...),
    notes: str = Form(...),
    db: Session = Depends(get_db)
):

    crud.update_ticket(db, ticket_id, status, notes)

    return RedirectResponse(
        f"/ticket/{ticket_id}",
        status_code=303
    )