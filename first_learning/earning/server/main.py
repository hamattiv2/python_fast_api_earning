from typing import Optional, List
from fastapi import FastAPI
from pydantic import BaseModel, Field





# @app.get('/countries/')
# async def country(country_name: Optional[str] = None, country_no: Optional[int] = None):
#     return {
#         "country_name": country_name,
#         "country_no": country_no
#     }

class ShopInfo(BaseModel):
    name: str
    location: str

class Item(BaseModel):
    name: str = Field(min_length=4, max_length=12)
    description: Optional[str] = None
    price: int
    tax:  Optional[float] = None
    
class Data(BaseModel):
    shop_info: ShopInfo
    items: List[Item]
    
app = FastAPI()

@app.post('/')
async def index(data: Data):
    return {"data": data}