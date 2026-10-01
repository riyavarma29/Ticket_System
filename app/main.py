from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app import models, crud


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Support Ticket CRM",
    description="Customer support ticket management system",
    version="2.0"
)

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


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
    priority: str = None,
    category: str = None,
    db: Session = Depends(get_db)
):

    tickets = crud.get_all_tickets(
        db,
        search,
        status,
        priority,
        category
    )

    stats = crud.get_dashboard_stats(db)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "tickets": tickets,
            "stats": stats,
            "search": search or "",
            "selected_status": status or "",
            "selected_priority": priority or "",
            "selected_category": category or ""
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
    description: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...),
    assigned_to: str = Form(...),
    db: Session = Depends(get_db)
):

    class Data:
        pass

    data = Data()

    data.customer_name = customer_name.strip()
    data.customer_email = customer_email.strip()
    data.subject = subject.strip()
    data.description = description.strip()
    data.category = category
    data.priority = priority
    data.assigned_to = assigned_to

    crud.create_ticket(db, data)

    return RedirectResponse(
        "/",
        status_code=303
    )


@app.get(
    "/ticket/{ticket_id}",
    response_class=HTMLResponse
)
def ticket_detail(
    request: Request,
    ticket_id: str,
    db: Session = Depends(get_db)
):

    ticket = crud.get_ticket(db, ticket_id)

    if not ticket:
        return HTMLResponse(
            "<h1>Ticket not found</h1>",
            status_code=404
        )

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
    priority: str = Form(...),
    assigned_to: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db)
):

    ticket = crud.update_ticket(
        db,
        ticket_id,
        status,
        priority,
        assigned_to,
        notes
    )

    if not ticket:
        return HTMLResponse(
            "<h1>Ticket not found</h1>",
            status_code=404
        )

    return RedirectResponse(
        f"/ticket/{ticket_id}",
        status_code=303
    )