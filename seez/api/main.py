from typing import Any, Dict

from fastapi import FastAPI

from seez.domain.commands.get_car import GetCarCommand
from seez.main import configure_haps

app = FastAPI()


@app.get("/")
def read_root() -> Dict[Any, Any]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None) -> Dict[Any, Any]:
    return {"item_id": item_id, "q": q}


@app.get("/make")
def read_make() -> Dict[Any, Any]:
    make = GetCarCommand().handle()
    return {"make", make.name}
