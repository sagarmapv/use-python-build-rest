from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Items API", description="Educational REST API — all 5 HTTP verbs on one resource")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Topic 4 (Data Structures): plain dict as the in-memory store — no database needed
store: dict[str, dict] = {}


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# Topic 3 (Functions): each endpoint is a function — same concept, HTTP wrapper around it
@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
    item_id = str(uuid.uuid4())[:8]
    store[item_id] = {"id": item_id, **item.model_dump()}
    return store[item_id]


@app.get("/items")
def list_items():
    return list(store.values())


@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    return store[item_id]


@app.put("/items/{item_id}")
def replace_item(item_id: str, item: ItemCreate):
    if item_id not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    store[item_id] = {"id": item_id, **item.model_dump()}
    return store[item_id]


@app.patch("/items/{item_id}")
def update_item(item_id: str, item: ItemPatch):
    if item_id not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    existing = store[item_id]
    patch = {k: v for k, v in item.model_dump().items() if v is not None}
    store[item_id] = {**existing, **patch}
    return store[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    if item_id not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    del store[item_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8004, reload=True)
