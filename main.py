from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Inventory storage (In-memory dictionary)
inventory: Dict[int, dict] = {1: {"name":"pen",
                                  "quantity": 5,
                                  "price": 10},
                              2: {
                                  "name":"pencil",
                                  "quantity": 3,
                                  "price": 20
                              },
                              3: {
                                  "name":"book",
                                  "quantity": 2,
                                  "price": 50
                              },
                              4: {
                                  "name":"eraser",
                                  "quantity": 7,
                                  "price": 5
                              },
                              5: {
                                  "name":"ruler",
                                  "quantity": 4,
                                  "price": 12
                              }}
item_id_counter = 1  # Auto-incrementing ID

# Pydantic model for request validation
class Item(BaseModel):
    name: str
    quantity: int
    price: float

@app.post("/items/", response_model=dict)
def create_item(item: Item):
    global item_id_counter
    item_id = item_id_counter
    inventory[item_id] = item.dict()
    item_id_counter += 1
    return {"id": item_id, **inventory[item_id]}

@app.get("/items/{item_id}", response_model=dict)
def read_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **inventory[item_id]}

@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    inventory[item_id] = item.dict()
    return {"id": item_id, **inventory[item_id]}

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = inventory.pop(item_id)
    return {"message": "Item deleted", "deleted_item": deleted_item}

    
    