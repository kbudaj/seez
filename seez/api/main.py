from typing import Any

from fastapi import FastAPI, Query

from seez.domain.commands.get_cars_paged import GetCarsPaged
from seez.domain.commands.get_makes import GetAllMakes
from seez.domain.commands.get_models import GetAllModels
from seez.domain.commands.get_submodels import GetAllSubModels
from seez.main import configure_haps

app = FastAPI()


@app.get("/car/")
def list_cars(
    page_number: int = Query(1, title="Page number", ge=1),
    page_size: int = Query(20, title="Page number", ge=1),
    price_min: int = Query(None, title="Price min", ge=0),
    price_max: int = Query(None, title="Price min", ge=0),
    mileage_min: int = Query(None, title="Price min", ge=0),
    mileage_max: int = Query(None, title="Price min", ge=0),
) -> Any:
    # TODO: Validate for min > max
    return GetCarsPaged(
        page_number=page_number,
        page_size=page_size,
        price_min=price_min,
        price_max=price_max,
        mileage_min=mileage_min,
        mileage_max=mileage_max,
    ).handle()


@app.get("/make/")
def list_makes() -> Any:
    return GetAllMakes().handle()


@app.get("/model/")
def list_models() -> Any:
    return GetAllModels().handle()


@app.get("/submodel/")
def list_submodels() -> Any:
    return GetAllSubModels().handle()


configure_haps()
