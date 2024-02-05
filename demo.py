from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
app = FastAPI()

from TM1py.Services import TM1Service
from typing import List, Tuple, Optional
import pandas as pd

from main import address, port, user, password
from main import list_dimensions, list_cubes_with_dimensions
from main import filter_dimension_element
from main import get_df_of_the_view

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

@app.get('/download_file/', response_class=StreamingResponse)
async def get_download_file(cube_name: str, view_name: str, output_file_format: str):
    with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
        # cube_name = "plan_BudgetPlan"
        # view_name = "Dy Slice To 2004 Exec Report"
        df = get_df_of_the_view(tm1, cube_name=cube_name, view_name=view_name, output_file_format=output_file_format)

        stream = io.StringIO()
        if output_file_format == 'csv':
            df.to_csv(stream)
            response = StreamingResponse(
                iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=export.csv"
            return response
        
        elif output_file_format == 'xlsx':
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, sheet_name='Sheet1')
            excel_buffer.seek(0)
            headers = {
                "Content-Disposition": "attachment; filename=export.xlsx",
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
            response = StreamingResponse(
                iter([excel_buffer.getvalue()]), headers=headers
            )
            return response

