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
async def api_catalog(request: Request):
    """API endpoint to get filtered units with composable filtering"""
    filtered_units = UNITS.copy()

    # Get query parameters
    query_params = request.query_params

    # Handle legacy single filters for backward compatibility
    model = query_params.get("model")
    # Filter by specific model if provided
    if model:
        filtered_units = [unit for unit in filtered_units if unit.get("Modelo") == model]
        return filtered_units

    # Handle composable filters
    composable_filters = {}
    for key, value in query_params.items():
        if key.startswith("filters["):
            # Parse filter parameters like filters[0][type], filters[0][value], etc.
            import re

            match = re.match(r"filters\[(\d+)\]\[(\w+)\]", key)
            if match:
                filter_index = int(match.group(1))
                filter_param = match.group(2)

                if filter_index not in composable_filters:
                    composable_filters[filter_index] = {}

                composable_filters[filter_index][filter_param] = value

    # Apply composable filters
    filters_by_type = {}
    for filter_data in composable_filters.values():
        filter_type = filter_data.get("type")
        if not filter_type:
            continue

        if filter_type not in filters_by_type:
            filters_by_type[filter_type] = []
        filters_by_type[filter_type].append(filter_data)

    # Apply filters by type
    for filter_type, filter_list in filters_by_type.items():
        # Use AND logic for all filter types - show units that match ALL selected criteria
        for filter_data in filter_list:
            filtered_units = apply_composable_filter(filtered_units, filter_type, filter_data)

    return filtered_units


def apply_composable_filter(units, filter_type, filter_data):
    """Apply a single composable filter to the units list"""

    if filter_type == "unit_type":
        unit_type = filter_data.get("value")
        if unit_type:
            words = CatalogReference[unit_type].lower().split(";")
            return [
                unit
                for unit in units
                if unit_type in unit.get("Modelo", "") or any((w in unit.get("Titulo", "").lower() for w in words))
            ]

    return units
