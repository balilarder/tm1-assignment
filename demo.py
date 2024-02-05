from fastapi import FastAPI
app = FastAPI()

from TM1py.Services import TM1Service
from typing import List, Tuple
import pandas as pd

from main import address, port, user, password
from main import list_dimensions, list_cubes_with_dimensions

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
