from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> Dict[Any, Any]:
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None) -> Dict[Any, Any]:
    return {"item_id": item_id, "q": q}
