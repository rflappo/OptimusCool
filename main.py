from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.catalog.units import UNITS
from src.catalog.enum import CatalogReference


app = FastAPI()

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


@app.get("/catalog")
async def catalog(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})


@app.get("/api/catalog")
async def api_catalog(
    model: str = None,
    unit_type: str = None,
    min_capacity: int = None,
    max_capacity: int = None,
):
    """API endpoint to get filtered units"""
    filtered_units = UNITS.copy()

    # Filter by specific model if provided
    if model:
        filtered_units = [unit for unit in filtered_units if unit.get("Modelo") == model]
        return filtered_units  # Always return a list (empty if not found, single item if found)

    if unit_type:
        words = CatalogReference[unit_type].lower().split(";")
        filtered_units = [
            unit
            for unit in filtered_units
            if unit_type in unit.get("Modelo", "") or any((w in unit.get("Titulo") for w in words))
        ]

    if min_capacity is not None or max_capacity is not None:

        def get_capacity(unit):
            datos = unit.get("Datos", {})
            refrigeracion = datos.get("Capacidad de refrigeración", {})
            capacidad0a38 = refrigeracion.get("0a38", [])

            if capacidad0a38:
                watts = capacidad0a38[0]
                import re

                match = re.search(r"(\d+)W", watts)
                return int(match.group(1)) if match else 0
            return 0

        if min_capacity is not None:
            filtered_units = [unit for unit in filtered_units if get_capacity(unit) >= min_capacity]

        if max_capacity is not None:
            filtered_units = [unit for unit in filtered_units if get_capacity(unit) <= max_capacity]

    return filtered_units
