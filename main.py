from TM1py.Services import TM1Service
from typing import List

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
    
with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
    print(tm1.server.get_product_version())


    # question1
    all_dimensions = list_dimensions(tm1)
    print(all_dimensions)

    query1 = list_cubes_with_dimensions(tm1)
    print(query1)

