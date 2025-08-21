# filename: main.py

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# setup templates folder
templates = Jinja2Templates(directory="templates")

# in-memory DB
fake_db = []


# Root route - show the todo list
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "items": fake_db}
    )


# Handle form submission
@app.post("/add-item")
def add_item(
    name: str = Form(...),
    status: str | None = Form(None),   # checkbox → might be None or "on"
):
    item_id = len(fake_db) + 1
    item = {"id": item_id, "name": name, "status": bool(status)}
    fake_db.append(item)

    # redirect back to homepage to show updated list
    return RedirectResponse(url="/", status_code=303)


# Extra route just for debugging (raw JSON)
@app.get("/items")
def get_items():
    return {"items": fake_db}
