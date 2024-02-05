from fastapi import FastAPI
app = FastAPI()

from TM1py.Services import TM1Service
from typing import List, Tuple, Optional
import pandas as pd

from main import address, port, user, password
from main import list_dimensions, list_cubes_with_dimensions
from main import filter_dimension_element

from pydantic import BaseModel

class FilterRequest(BaseModel):
    dimension_name: str
    layer_filter: Optional[List[int]] = None
    conditions: Optional[List[Tuple[str, str, str]]] = None

@app.get('/book/{book_id}')
def get_book_by_id(book_id: int):
    return {
        'book_id': book_id
    }

@app.get('/all_dimensions')
def get_all_dimensions():
    with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
        result = list_dimensions(tm1)
    return result

@app.get('/cube_name_with_dimensions')
def get_cube_name_with_dimensions():
    with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
        result = list_cubes_with_dimensions(tm1)
    return result

@app.post('/filter_element_name')
async def get_filtered_element_name(request: FilterRequest):
    with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
        result = filter_dimension_element(
            tm1,
            dimension_name=request.dimension_name,
            layer_filter=request.layer_filter,
            conditions=request.conditions

        )
    return {'length': len(result), 'name': result}