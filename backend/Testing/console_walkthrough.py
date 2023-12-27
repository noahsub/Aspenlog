import json
import os

import jsonpickle
import typer
from rich import print
from rich.prompt import Prompt

from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.importance_factor_constants import WindImportanceFactor, SnowImportanceFactor
from backend.Constants.materials import Materials
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from backend.Constants.snow_constants import RoofType
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.building import Dimensions, HeightZone, Building, Cladding, Roof
from backend.Entities.location import Location
from backend.Entities.snow import SnowLoad, SnowFactor
from backend.Entities.wind import WindFactor, WindLoad, WindPressure
from backend.algorithms import snow_load_algorithms, wind_load_algorithms
from backend.algorithms.snow_load_algorithms import get_slope_factor, get_basic_roof_now_load_factor, get_snow_load
from backend.algorithms.wind_load_algorithms import get_wind_topographic_factor, get_internal_pressure, get_external_pressure

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
    global LOCATION
    global BUILDING
    global WIND_LOAD
    print_line()
    confirm = confirm_choice(f"Would you like to skip Step {step}?")
    if confirm:
        match step:
            case 0:
                print_line()
                LOCATION = deserialize('location')
                print_obtained_values(LOCATION)
            case 1:
                print_line()
                BUILDING = deserialize('building')
                print_obtained_values(BUILDING)
            case 2:
                pass
            case 3:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 4:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 5:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 6:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 7:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 8:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 9:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 10:
                print_line()
                WIND_LOAD = deserialize('wind_load')
                print_obtained_values(WIND_LOAD)
            case 11:
                print_line()
                SNOW_LOAD = deserialize('snow_load')
                print_obtained_values(SNOW_LOAD)
            case 12:
                print_line()
                SNOW_LOAD = deserialize('snow_load')
                print_obtained_values(SNOW_LOAD)
            case 13:
                print_line()
                SNOW_LOAD = deserialize('snow_load')
                print_obtained_values(SNOW_LOAD)
            case 14:
                print_line()
                SNOW_LOAD = deserialize('snow_load')
                print_obtained_values(SNOW_LOAD)
            case 15:
                print_line()
                SNOW_LOAD = deserialize('snow_load')
                print_obtained_values(SNOW_LOAD)
    else:
        match step:
            case 0:
                step_0()
            case 1:
                step_1()
            case 2:
                step_2()
            case 3:
                step_3()
            case 4:
                step_4()
            case 5:
                step_5()
            case 6:
                step_6()
            case 7:
                step_7()
            case 8:
                step_8()
            case 9:
                step_9()
            case 10:
                step_10()
            case 11:
                step_11()
            case 12:
                step_12()
            case 13:
                step_13()
            case 14:
                step_14()
            case 15:
                step_15()



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

    confirm_height_zone = confirm_choice(
        "Default is 20 m per height zone, meaning number of height zones = ⌈H/20⌉. Are you ok with this?")

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


def step_2():
    print_step_heading(2)
    print("Skipping step, importance factors saved as constants")


WIND_LOAD = None
WIND_FACTOR = None


def step_3():
    global WIND_LOAD
    global WIND_FACTOR
    print_step_heading(3)

    WIND_FACTOR = WindFactor(ct=None, ce=None, cei=None)
    WIND_LOAD = WindLoad(factor=WIND_FACTOR, pressure=None)

    confirm_ct = confirm_choice("Would you like to use default value for topographic factor?")
    if not confirm_ct:
        ct = float(user_input("Topographic factor"))
        get_wind_topographic_factor(WIND_LOAD, ct=ct)
    else:
        get_wind_topographic_factor(WIND_LOAD)

    serialize('wind_load', WIND_LOAD)
    print_obtained_values(WIND_LOAD)


def step_4():
    global WIND_LOAD
    global WIND_FACTOR
    global BUILDING
    print_step_heading(4)

    wind_exposure_selection = choice(prompt="Wind Exposure Factor", options=WindExposureFactorSelections)
    if wind_exposure_selection == WindExposureFactorSelections.INTERMEDIATE:
        value = float(user_input("Intermediate value for ce and cei"))
        wind_load_algorithms.get_wind_exposure_factor(wind_load=WIND_LOAD, selection=wind_exposure_selection, building=BUILDING,
                                 manual=value)
    else:
        wind_load_algorithms.get_wind_exposure_factor(wind_load=WIND_LOAD, selection=wind_exposure_selection, building=BUILDING)

    serialize('wind_load', WIND_LOAD)


def step_5():
    print_step_heading(5)
    print("Skipping step, gust factor saved as a constant")


def step_6():
    global WIND_LOAD
    global LOCATION
    print_step_heading(6)

    WIND_LOAD.pressure = WindPressure()

    internal_pressure_selection = choice(prompt="Internal Pressure Selection", options=InternalPressureSelections)
    wind_importance_factor = choice(prompt="Wind Importance Factor", options=WindImportanceFactor)
    get_internal_pressure(wind_load=WIND_LOAD, selection=internal_pressure_selection,
                          wind_importance_factor=wind_importance_factor, location=LOCATION)

    serialize('wind_load', WIND_LOAD)


def step_7():
    global WIND_LOAD
    global LOCATION
    print_step_heading(7)

    wind_importance_factor = choice(prompt="Wind Importance Factor", options=WindImportanceFactor)
    get_external_pressure(wind_load=WIND_LOAD, wind_importance_factor=wind_importance_factor, location=LOCATION)

    serialize('wind_load', WIND_LOAD)


def step_8():
    global WIND_LOAD
    print_step_heading(8)
    print_obtained_values(WIND_LOAD)


def step_9():
    print_step_heading(9)
    print("Skipping step, redundant")


def step_10():
    # TODO: Requires refactor, need input from the civil engineering team
    print_step_heading(10)
    print("Skipping step, TODO")


SNOW_FACTOR = None
SNOW_LOAD = None


def step_11():
    global SNOW_FACTOR
    global SNOW_LOAD
    global BUILDING
    print_step_heading(11)

    SNOW_FACTOR = SnowFactor(cs=None, cw=None, cb=None)
    SNOW_LOAD = SnowLoad(factor=SNOW_FACTOR, s=None)
    roof_type = choice("Roof Type", options=RoofType)
    get_slope_factor(snow_load=SNOW_LOAD, selection=roof_type, building=BUILDING)
    serialize('snow_load', SNOW_LOAD)


def step_12():
    print_step_heading(12)
    print("Skipping step, accumulation factor saved as a constant")


def step_13():
    global SNOW_LOAD
    print_step_heading(13)

    importance_selection = choice(prompt="Importance Selection", options=WindImportanceFactor)
    wind_exposure_factor_selection = choice(prompt="Wind Exposure Factor Selection",
                                            options=WindExposureFactorSelections)
    snow_load_algorithms.get_wind_exposure_factor(snow_load=SNOW_LOAD, importance_selection=importance_selection,
                             wind_exposure_factor_selection=wind_exposure_factor_selection)
    serialize('snow_load', SNOW_LOAD)

def step_14():
    global SNOW_LOAD
    global BUILDING
    print_step_heading(14)
    print("Computing basic snow load factor")
    get_basic_roof_now_load_factor(snow_load=SNOW_LOAD, building=BUILDING)
    serialize('snow_load', SNOW_LOAD)

def step_15():
    global SNOW_LOAD
    global LOCATION
    print_step_heading(15)

    snow_importance_factor = choice(prompt="Snow Importance Factor", options=SnowImportanceFactor)
    get_snow_load(snow_load=SNOW_LOAD, snow_importance_factor=snow_importance_factor, location=LOCATION)
    serialize('snow_load', SNOW_LOAD)
    print_obtained_values(SNOW_LOAD)


if __name__ == '__main__':
    print_line()
    print("ASPENLOG 2020 CONSOLE WALKTHROUGH")

    create_save_file()

    for i in range(16):
        skip_step(i)
