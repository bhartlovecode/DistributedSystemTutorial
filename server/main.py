import fastapi
from fastapi import FastAPI, status
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    count: int

app = FastAPI()

# This will be a database eventually
items = {}

# Add item
@app.post("/items/", status_code=201)
async def create_item(item: Item):
    if item.name in items.keys():
       raise fastapi.HTTPException(status_code=409, detail=f'Item with name {item.name} already in inventory.')
    items[item.name] = item.count
    return item

# Update item
@app.put("/items/", status_code=201)
async def update_count(item: Item):
    if item.name in items.keys():
       items[item.name] = item.count 
       return {item.name: items[item.name]}
    raise fastapi.HTTPException(status_code=404, detail=f'Item with name {item.name} not found in inventory.')

# Delete Item
@app.delete("/items/{item_name}", status_code=204)
async def delete_item(item_name: str):
    if item_name in items.keys():
        items.pop(item_name)
        return item_name
    raise fastapi.HTTPException(status_code=404, detail=f'Item with name {item_name} not found in inventory.')

# Retrieve one item
@app.get("/items/{item_name}", status_code=200)
async def get_item(item_name: str):
    if item_name in items.keys():
        return {item_name: items[item_name]}
    raise fastapi.HTTPException(status_code=404, detail=f'Item with name {item_name} not found in inventory.')

# Retrieve all items
@app.get("/items/")
async def get_all_items():
    return items