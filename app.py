from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import bank

bank.init_db()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Main Page (Landing Page)
@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Signup Page
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "message": None})

@app.post("/signup_form")
def signup_form(request: Request, name: str = Form(...), pin: int = Form(...), balance: float = Form(...)):
    success = bank.signup(name, pin, balance)
    msg = "Account created successfully!" if success else "Username already exists!"
    return templates.TemplateResponse("signup.html", {"request": request, "message": msg})

# Login Page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": None})

@app.post("/login_form")
def login_form(response: Response, name: str = Form(...), pin: int = Form(...)):
    user_id = bank.login(name, pin)
    if user_id:
        return RedirectResponse(url=f"/dashboard/{user_id}", status_code=303)
    return templates.TemplateResponse("login.html", {"request": {}, "message": "Invalid credentials"})

# Dashboard
@app.get("/dashboard/{user_id}", response_class=HTMLResponse)
def dashboard(request: Request, user_id: int, message: str = None, category: str = None):
    balance = bank.get_balance(user_id)
    transactions = bank.get_transactions(user_id)
    users = bank.get_all_users()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user_id": user_id,
            "balance": balance,
            "transactions": transactions,
            "users": users,
            "message": message,
            "category": category
        }
    )

# Transfer
@app.post("/transfer_form")
def transfer_form(sender_id: int = Form(...), receiver_id: int = Form(...), amount: float = Form(...)):
    success = bank.transfer(sender_id, receiver_id, amount)
    if success:
        return RedirectResponse(f"/dashboard/{sender_id}?message=Transfer+successful&category=success", status_code=303)
    else:
        return RedirectResponse(f"/dashboard/{sender_id}?message=Insufficient+balance&category=error", status_code=303)
