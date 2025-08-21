# filename: main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Example in-memory database
fake_db = []

# Templates setup (HTML files in 'templates' folder)
templates = Jinja2Templates(directory="templates")

# Item model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

# Root → GUI Home
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": fake_db})

# Handle form submission → POST item
@app.post("/add-item")
def add_item(name: str = Form(...), description: str = Form(""), price: float = Form(...)):
    item_id = len(fake_db) + 1
    item = {"id": item_id, "name": name, "description": description, "price": price}
    fake_db.append(item)
    return RedirectResponse(url="/", status_code=303)

# API endpoint (if you want JSON access)
@app.get("/items/")
def get_items():
    return {"items": fake_db}
