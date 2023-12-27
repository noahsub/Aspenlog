# from backend.Constants.seismic_constants import SiteDesignation, SiteClass
# from backend.Entities.location import Location
#

#
# if __name__ == '__main__':
#     print(LINE)
#     print("ASPENLOG 2020 CONSOLE WALKTHROUGH")
#     print(LINE)
#
#     # Step 0
#     print("Step #0")
#     print(LINE)
#     address = input("Address: ")
#     print("Select site designation type:")
#     for i, type in enumerate(['Vs30 (Xv)', 'Site Class (Xs)']):
#         print(f'\t{i}: {type}')
#     location = None
#     match int(input("Selection: ")):
#         case 0:
#             xv = int(input("Vs30 Value [140, 3000] m/s: "))
#             location = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
#         case 1:
#             print("Select site class: ")
#             site_class_mapping = {}
#             for i, type in enumerate(SiteClass):
#                 site_class_mapping[i] = type
#                 print(f'\t{i}: {type.value}')
#             location = Location(address=address, site_designation=SiteDesignation.XS, xs=site_class_mapping[int(input("Selection: "))])
#     print("Obtained Values: ")
#     print(location)
import json
import os
from enum import Enum

import jsonpickle
import typer
from rich import print

from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.materials import Materials
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from backend.Entities.building import Dimensions, HeightZone, Building, Cladding, Roof
from backend.Entities.location import Location
from rich.prompt import Prompt

TERM_SIZE = os.get_terminal_size()


def choice(prompt: str, options):
    print(f"[bold green]Select[bold /green] [bold white]{prompt}[/bold white]: ")
    mapping = {}
    for i, option in enumerate(options):
        mapping[i] = option
        print(f"  [bold red]{i}[/bold red]: [white]{option.value}[/white]")
    selection = int(input("Selection: "))
    print(f"  → [bold yellow]{mapping[selection]}[/bold yellow]")
    return mapping[selection]


def multi_choice(prompt: str, options):
    print(f"[bold green]Select[bold /green] [bold white]{prompt}[/bold white]: ")
    mapping = {}
    for i, option in enumerate(options):
        mapping[i] = option
        print(f"  [bold red]{i}[/bold red]: [white]{option.value}[/white]")
    selections = input("Selections (comma-separated): ").split(',')
    selected_options = [mapping[int(s)] for s in selections]
    print(f"  → [bold yellow]{selected_options}[/bold yellow]")
    return selected_options


def user_input(prompt: str):
    return Prompt.ask(f"[blue]Enter[/blue] {prompt}")


def confirm_choice(prompt: str):
    return typer.confirm(f"{prompt}")


def create_save_file():
    if not os.path.exists('save.json'):
        with open('save.json', 'w') as f:
            json.dump({}, f)


def serialize(name: str, obj):
    # save obj to save.json under name using jsonpickle
    with open('save.json', 'r') as f:
        data = json.load(f)
        data[name] = jsonpickle.encode(obj)
    with open('save.json', 'w') as f:
        json.dump(data, f, indent=4)


def deserialize(name: str):
    # get obj from save.json under name
    # it should not return the string representation, but the actual object
    with open('save.json', 'r') as f:
        data = json.load(f)
        return jsonpickle.decode(data[name])


def skip_step(step: int):
    print_line()
    confirm = confirm_choice(f"Would you like to skip Step {step}?")
    if confirm:
        match step:
            case 0:
                print_line()
                print_obtained_values(deserialize('location'))
            case 1:
                print_line()
                print_obtained_values(deserialize('building'))
    else:
        match step:
            case 0:
                step_0()
            case 1:
                step_1()


def print_obtained_values(obj):
    print("[bold red]Obtained Values: [/bold red]")
    lst = str(obj).split('\n')
    for i in range(len(lst)):
        print(f"  {lst[i]}")


def print_line():
    print('─' * (TERM_SIZE.columns - 1))


def print_step_heading(step: float):
    print_line()
    print(f"[bold red]STEP {step}[/bold red]")
    print_line()


LOCATION = None


def step_0():
    global LOCATION
    print_step_heading(0)
    address = user_input("Address")
    site_designation_type = choice(prompt="site designation type", options=SiteDesignation)
    match site_designation_type:
        case SiteDesignation.XV:
            xv = int(user_input("Vs30 value measured in situ between 140 - 3000 m/s"))
            LOCATION = Location(address=address, site_designation=SiteDesignation.XV, xv=xv)
        case SiteDesignation.XS:
            xs = choice(prompt="Site Class", options=SiteClass)
            LOCATION = Location(address=address, site_designation=SiteDesignation.XS, xs=xs)
    serialize('location', LOCATION)
    print_obtained_values(LOCATION)


DIMENSIONS = None
CLADDING = None
ROOF = None
BUILDING = None


def step_1():
    global DIMENSIONS
    print_step_heading(1.1)
    confirm_eave = confirm_choice("Does the building have eave?")
    width = int(user_input("Width of building in meters"))
    if confirm_eave:
        height_eave = int(user_input("Eave height in meters"))
        height_ridge = int(user_input("Ridge height in meters"))
        DIMENSIONS = Dimensions(width=width, height_eave=height_eave, height_ridge=height_ridge)
    else:
        height = int(user_input("Height of building in meters"))
        DIMENSIONS = Dimensions(width=width, height=height)

    global BUILDING

    confirm_height_zone = confirm_choice("Default is 20 m per height zone, meaning number of height zones = ⌈H/20⌉. Are you ok with this?")

    num_floors = user_input("Number of floors")

    global CLADDING
    c_top = user_input("Top of cladding in meters")
    c_bop = user_input("Bottom of cladding in meters")
    CLADDING = Cladding(c_top=c_top, c_bot=c_bop)

    confirm_h_opening = confirm_choice("Does the building have Dominant Opening?")
    if not confirm_h_opening:
        h_opening = 0
    else:
        h_opening = float(user_input("Mid-height of the dominant opening"))

    BUILDING = Building(dimensions=DIMENSIONS, cladding=CLADDING, roof=None, num_floor=num_floors, h_opening=h_opening)

    print_step_heading(1.2)
    if not confirm_height_zone:
        num_height_zones = user_input("Number of height zones")
        for i in range(num_height_zones):
            elevation = user_input(f"Elevation of height zone {i + 1}")
            BUILDING.height_zones.append(HeightZone(zone_num=i + 1, elevation=elevation))
        BUILDING.compute_height_zones(selection=DefaultSelections.CUSTOM, height_zones=BUILDING.height_zones)
    else:
        print("User selected 'yes', skipping step")
        BUILDING.compute_height_zones(selection=DefaultSelections.DEFAULT)

    print_step_heading(1.3)
    w_roof = float(user_input("Smaller Plan dimension of the roof in meters"))
    l_roof = float(user_input("Larger Plan dimension of the roof in meters"))
    slope = float(user_input("Slope of the roof in degrees"))

    global ROOF
    ROOF = Roof(w_roof=w_roof, l_roof=l_roof, slope=slope, wp=None)

    print_step_heading(1.4)
    confirm_material = confirm_choice(prompt="The material will be applied to all height zones?")

    if confirm_material:
        wp = float(user_input("Material Load"))
        BUILDING.compute_dead_load(selection=DefaultSelections.DEFAULT, wp=wp)
    else:
        print_step_heading(1.5)
        print_step_heading(1.6)
        for height_zone in BUILDING.height_zones:
            height_zone.wp_materials = {}
            materials = multi_choice(prompt=f"Material for height zone {height_zone.zone_num}", options=Materials)
            for material in materials:
                wp = float(user_input(f"Material Load for {material.value}"))
                height_zone.wp_materials[material] = wp
        BUILDING.compute_dead_load(selection=DefaultSelections.CUSTOM)

    print_step_heading(1.7)
    wp_roof = float(user_input("Uniform dead load for roof"))
    ROOF.wp = wp_roof
    BUILDING.roof = ROOF

    serialize('building', BUILDING)
    print_obtained_values(BUILDING)







if __name__ == '__main__':
    print_line()
    print("ASPENLOG 2020 CONSOLE WALKTHROUGH")

    create_save_file()
    skip_step(0)
    skip_step(1)
