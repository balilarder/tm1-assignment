from TM1py.Services import TM1Service
import typing

# Read settings from config
address = 'restapi195.skill.cubewise.asia'
port = '443'
user = 'admin'
password = ''


# These are query functions
def list_dimensions(tm1: TM1Service) -> list:
    dimensions = tm1.dimensions.get_all_names(skip_control_dims=True)
    for dn in dimensions:
        print(dn)

    result = [dn for dn in dimensions]
    return result

def list_cubes(cube_name: list) -> dict:
    if not cube_name:
        print("我全都要")
    else:
        print("onr by one")


with TM1Service(address=address, port=port, user=user, password=password, ssl=True) as tm1:
    # print(tm1.server.get_product_Version())
    print(tm1.server.get_product_version())


    # question1
    all_dimensions = list_dimensions(tm1)
    print(all_dimensions)

