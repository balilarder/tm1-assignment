from TM1py.Services import TM1Service
from typing import List, Tuple

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
    
def filter_dimension_element(tm1: TM1Service, dimension_name: str, layer_filter: List[int]=None, conditions: List[Tuple[str, str, str]]=None) -> List[str]:
    # this is for the multiple languages result mappnig
    df = tm1.elements.get_elements_dataframe(dimension_name=dimension_name, hierarchy_name=dimension_name, skip_consolidations=False)
    
    
    # mdx filter layer
    if not layer_filter:
        mdx = f'''
            [{dimension_name}].[{dimension_name}].Members
        '''
    else:
        mdx = f'''
        TM1FILTERBYLEVEL({{
            [{dimension_name}].[{dimension_name}].Members
        }}, {",".join([str(n) for n in layer_filter])})
        '''
    
    # add filter
    
    if not conditions:
        conditions = []
    def add_condition(key, value, wildcard_location,mdx) -> str:
        # if key == '', means filter by the element name itself
        if wildcard_location == 'contains':
            return f"TM1FILTERBYPATTERN( {mdx}, '*{value}*', '{key}' )"
        elif wildcard_location == 'startswith':
            return f"TM1FILTERBYPATTERN( {mdx}, '{value}*', '{key}' )"
        elif wildcard_location == 'endwith':
            return f"TM1FILTERBYPATTERN( {mdx}, '*{value}', '{key}' )"
        elif wildcard_location == 'exactly':
            return f"TM1FILTERBYPATTERN( {mdx}, '{value}', '{key}' )"
    for key, value, wildcard_location in conditions:
        mdx = add_condition(key, value, wildcard_location, mdx)
    
    mdx = '{' + mdx + '}'
    mdx_result = tm1.elements.execute_set_mdx(mdx=mdx)
    print("mdx_result")
    print(mdx_result)
    element_names = [element[0]['Name'] for element in mdx_result]
    return element_names



def get_df_of_the_view(tm1: TM1Service, cube_name: str, view_name: str, output_file_format: str) -> pd.DataFrame:
    
    # Issues: 
    # 1. 有時間的話做join把alias換掉變成預設值 (對應column name 去找dimension name)
    # 2. 有些(cube, view會失敗), column must not be empty, 檢查方法：全部組合都試一次
    # 3. 編碼問題

    # use native view 
    nv = tm1.views.get_native_view(cube_name=cube_name, view_name=view_name)
    print(nv.MDX)
    result = tm1.cubes.cells.execute_mdx_dataframe(nv.MDX)
    if output_file_format == 'csv':
        result.to_csv(f"{cube_name}-{view_name}.csv", encoding='utf-8')
    elif output_file_format == 'xlsx':
        result.to_excel(f"{cube_name}-{view_name}.xlsx")
    elif output_file_format == 'feather':
        result.to_feather(f"{cube_name}-{view_name}.feather")

    return result


with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
    print(tm1.server.get_product_version())
    
    # question1
    # all_dimensions = list_dimensions(tm1)
    # print(all_dimensions)

    
    # print()
    # query1 = list_cubes_with_dimensions(tm1)
    # print(query1)

    # cube_name = "plan_BudgetPlan"
    # view_name = "Dy Slice To 2004 Exec Report"
    # get_df_of_the_view(tm1, cube_name, view_name, output_file_format="")
    
    
    # question 2
    # Elements have differnet types: numeric, string, consolidated, etc
    # consolidates types have the hierarchical with edges and weights, indicated parent <-> component
    # d1 = tm1.dimensions.get(dimension_name='plan_lines')
    # print(d1)   # The names contains all the element names
    
    
    conditions = [
        ['Time_Spanish','er','contains']
    ]
    element_names = filter_dimension_element(tm1, dimension_name='plan_time', layer_filter=[], conditions=conditions)
    print(element_names)
    print(len(element_names))
    
    

    #
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='Europe')
    # print(e1)
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='Europa')
    # print(e1)
    # e1 = tm1.elements.get(dimension_name='plan_business_unit', hierarchy_name='plan_business_unit', element_name='유럽')
    # print(e1) 

    # attributes = tm1.elements.get_element_attributes(dimension_name='plan_lines', hierarchy_name='plan_lines')
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
