from TM1py.Services import TM1Service
from typing import List

from TM1py import Element, ElementAttribute, Dimension
import pandas as pd

# Read settings from config
address = 'restapi195.skill.cubewise.asia'
port = '443'
user = 'admin'
password = ''


# These are query functions
def list_dimensions(tm1: TM1Service) -> List[str]:
    dimensions = tm1.dimensions.get_all_names(skip_control_dims=True)
    
    result = [dn for dn in dimensions]
    return result

def list_cubes_with_dimensions(tm1: TM1Service) -> List[str]:
    
    result = {}
    cubes = tm1.cubes.get_model_cubes()
    for cube in cubes:
        result[cube.name] = cube.dimensions
    return result
    
# def process_dimensions(dimension: ):

def get_df_of_the_view(tm1: TM1Service, cube_name: str, view_name: str, output_file_format: str) -> pd.DataFrame:
    
    # Issues: 
    # 1. 有時間的話做join把alias換掉變成預設值 (對應column name 去找dimension name)
    # 2. 有些(cube, view會失敗), column must not be empty, 檢查方法：全部組合都試一次
    # 3. 編碼問題

    # use native view 
    nv = tm1.views.get_native_view(cube_name=cube_name, view_name=view_name)
    print(nv.MDX)
    result = tm1.cubes.cells.execute_mdx_dataframe(nv.MDX)
    result.to_csv('result_csv.csv', encoding='utf-8')
    result.to_excel('result_excel.xlsx')
    result.to_feather('result.feather')


with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
    print(tm1.server.get_product_version())
    
    # question1
    # all_dimensions = list_dimensions(tm1)
    # print(all_dimensions)

    
    # print()
    # query1 = list_cubes_with_dimensions(tm1)
    # print(query1)

    cube_name = "plan_BudgetPlan"
    view_name = "Dy Slice To 2004 Exec Report"
    get_df_of_the_view(tm1, cube_name, view_name, output_file_format="")
    
    
    # question 2
    # Elements have differnet types: numeric, string, consolidated, etc
    # consolidates types have the hierarchical with edges and weights, indicated parent <-> component
    # d1 = tm1.dimensions.get(dimension_name='plan_time')
    # print(d1)   # The names contains all the element names
    
    
    

    #
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='Europe')
    # print(e1)
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='Europa')
    # print(e1)
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='유럽')
    # print(e1) 

    # attributes = tm1.elements.get_element_attributes(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit')
    # print(attributes)
    # for a in attributes:
    #     print(f"a: {a}")
    # print()
    # attributes_name = tm1.elements.get_element_attribute_names(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit')
    # for an in attributes_name:
    #     print(f"an: {an}")

    # alias = tm1.elements.get_alias_element_attributes(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit')
    # print(alias)

    # filter_attributes = tm1.elements.get_elements_filtered_by_attribute(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', attribute_name='BusinessUnit_Norwegian', attribute_value='USA')
    # print(filter_attributes)
