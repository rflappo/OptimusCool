from json import load
from fastapi import FastAPI, Request, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

UNITS = []
# This should be a database in the future
with open("static/data/models.json", encoding="utf-8") as data_file:
    UNITS = load(data_file)

# Serve /static/*
app.mount("/static", StaticFiles(directory="./static"), name="static")

# Jinja2
templates = Jinja2Templates(directory="./templates")

# Commonly used vars
templates.env.globals["company_name"] = "Optimus Cool"
templates.env.globals["phone"] = "+5493425496386"
templates.env.globals["email"] = "contact@optimuscool.com"
templates.env.globals["year"] = 2025  # for footer, etc.


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})
