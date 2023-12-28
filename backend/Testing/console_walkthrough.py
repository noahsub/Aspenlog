########################################################################################################################
# console_walkthrough.py
# This file contains a walkthrough of the ASPENLOG 2020 application in console format. It is meant to be used for
# testing purposes only.
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import json
import os
import jsonpickle
import typer
from rich import print
from rich.prompt import Prompt
from backend.Constants.decision_constants import DefaultSelections
from backend.Constants.importance_factor_constants import WindImportanceFactor, SnowImportanceFactor, \
    SeismicImportanceFactor
from backend.Constants.materials import Materials
from backend.Constants.seismic_constants import SiteClass, SiteDesignation
from backend.Constants.snow_constants import RoofType
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.building import Dimensions, HeightZone, Building, Cladding, Roof
from backend.Entities.location import Location
from backend.Entities.seismic import SeismicFactor, SeismicLoad
from backend.Entities.snow import SnowLoad, SnowFactor
from backend.Entities.wind import WindFactor, WindLoad, WindPressure
from backend.algorithms import snow_load_algorithms, wind_load_algorithms
from backend.algorithms.seismic_load_algorithms import get_seismic_factor_values, get_floor_mapping, get_height_factor, \
    get_horizontal_force_factor, get_specified_lateral_earthquake_force
from backend.algorithms.snow_load_algorithms import get_slope_factor, get_basic_roof_now_load_factor, get_snow_load
from backend.algorithms.wind_load_algorithms import get_wind_topographic_factor, get_internal_pressure, \
    get_external_pressure

########################################################################################################################
# GLOBALS
########################################################################################################################

# The space available in the console
TERM_SIZE = 80
# The location of the building
LOCATION = None
# The dimensions of the building
DIMENSIONS = None
# The cladding of the building
CLADDING = None
# The roof of the building
ROOF = None
# The building
BUILDING = None
# The wind load
WIND_LOAD = None
# The wind load factor
WIND_FACTOR = None
# The snow load factor
SNOW_FACTOR = None
# The snow load
SNOW_LOAD = None
# The seismic load factor
SEISMIC_FACTOR = None
# The seismic load
SEISMIC_LOAD = None


########################################################################################################################
# USER INPUT FUNCTIONS
########################################################################################################################

def choice(prompt: str, options):
    """
    Prompts the user to select an option from a list of options
    :param prompt: The prompt to display to the user
    :param options: The list of options
    :return: The selected option
    """
    # Print the prompt
    print(f"[bold green]Select[bold /green] [bold white]{prompt}[/bold white]: ")
    # Create a mapping from the index to the option
    mapping = {}
    for i, option in enumerate(options):
        mapping[i] = option
        print(f"  [bold red]{i}[/bold red]: [white]{option.value}[/white]")
    # Get the user's selection
    selection = int(input("Selection: "))
    # Print the user's selection
    print(f"  → [bold yellow]{mapping[selection]}[/bold yellow]")
    # Return the selected option
    return mapping[selection]


def multi_choice(prompt: str, options):
    """
    Prompts the user to select multiple options from a list of options
    :param prompt: The prompt to display to the user
    :param options: The list of options
    :return: The selected options
    """
    # Print the prompt
    print(f"[bold green]Select[bold /green] [bold white]{prompt}[/bold white]: ")
    # Create a mapping from the index to the option
    mapping = {}
    for i, option in enumerate(options):
        mapping[i] = option
        print(f"  [bold red]{i}[/bold red]: [white]{option.value}[/white]")
    # Get the user's selection
    selections = input("Selections (comma-separated): ").split(',')
    selected_options = [mapping[int(s)] for s in selections]
    # Print the user's selection
    print(f"  → [bold yellow]{selected_options}[/bold yellow]")
    # Return the selected options
    return selected_options


def user_input(prompt: str):
    """
    Prompts the user to enter a value
    :param prompt: The prompt to display to the user
    :return: The user's input
    """
    return Prompt.ask(f"[blue]Enter[/blue] {prompt}")


def confirm_choice(prompt: str):
    """
    Prompts the user to confirm a choice
    :param prompt: The prompt to display to the user
    :return: The user's choice
    """
    return typer.confirm(f"{prompt}")


########################################################################################################################
# PRINTING FUNCTIONS
########################################################################################################################

def print_obtained_values(obj):
    print("[bold red]Obtained Values: [/bold red]")
    lst = str(obj).split('\n')
    for i in range(len(lst)):
        print(f"  {lst[i]}")


def print_line():
    print('─' * (TERM_SIZE - 1))


def print_step_heading(step: float):
    print_line()
    print(f"[bold red]STEP {step}[/bold red]")
    print_line()


########################################################################################################################
# JSON FUNCTIONS
########################################################################################################################

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


########################################################################################################################
# STEPS
########################################################################################################################

def skip_step(step: int):
    """
    Skips a step
    :param step: The step to skip
    :return: None
    """
    # Global variables
    global LOCATION
    global BUILDING
    global WIND_LOAD
    global SNOW_LOAD
    global SEISMIC_LOAD
    print_line()
    confirm = confirm_choice(f"Would you like to skip Step {step}?")
    # TODO: match statements need to be refactored, they are too long and contain duplicate code
    # If the user chooses to skip the step, then we load the step data from the save file
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
            case 16:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
            case 17:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
            case 18:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
            case 19:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
            case 20:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
            case 21:
                print_line()
                SEISMIC_LOAD = deserialize('seismic_load')
                print_obtained_values(SEISMIC_LOAD)
    # If the user chooses not to skip the step, then we run the step
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
            case 16:
                step_16()
            case 17:
                step_17()
            case 18:
                step_18()
            case 19:
                step_19()
            case 20:
                step_20()
            case 21:
                step_21()


def step_0():
    """
    Step 0: Obtain reference 1-in-50 yr wind velocity pressure, snow load, rain load, seismic parameters
    :return: None
    """
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


def step_1():
    """
    Step 1: Building dimension & height zone, material selection -> compute dead load
    :return: None
    """
    global DIMENSIONS
    print_step_heading(1.1)
    confirm_eave = confirm_choice("Does the building have eave?")
    width = int(user_input("Width of building in meters"))
    if confirm_eave:
        height_eave = float(user_input("Eave height in meters"))
        height_ridge = float(user_input("Ridge height in meters"))
        DIMENSIONS = Dimensions(width=width, height_eave=height_eave, height_ridge=height_ridge)
    else:
        height = float(user_input("Height of building in meters"))
        DIMENSIONS = Dimensions(width=width, height=height)

    global BUILDING

    confirm_height_zone = confirm_choice(
        "Default is 20 m per height zone, meaning number of height zones = ⌈H/20⌉. Are you ok with this?")

    num_floors = int(user_input("Number of floors"))

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
    """
    Step 2: Input Importance Category
    :return: None
    """
    print_step_heading(2)
    print("Skipping step, importance factors saved as constants")


def step_3():
    """
    Step 3: Input Topographic Factor
    :return: None
    """
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
    """
    Step 4: Input Wind Exposure Factor
    :return: None
    """
    global WIND_LOAD
    global WIND_FACTOR
    global BUILDING
    print_step_heading(4)

    wind_exposure_selection = choice(prompt="Wind Exposure Factor", options=WindExposureFactorSelections)
    if wind_exposure_selection == WindExposureFactorSelections.INTERMEDIATE:
        value = float(user_input("Intermediate value for ce and cei"))
        wind_load_algorithms.get_wind_exposure_factor(wind_load=WIND_LOAD, selection=wind_exposure_selection,
                                                      building=BUILDING,
                                                      manual=value)
    else:
        wind_load_algorithms.get_wind_exposure_factor(wind_load=WIND_LOAD, selection=wind_exposure_selection,
                                                      building=BUILDING)

    serialize('wind_load', WIND_LOAD)


def step_5():
    """
    Step 5: Input Gust Factor
    :return: None
    """
    print_step_heading(5)
    print("Skipping step, gust factor saved as a constant")


def step_6():
    """
    Step 6: Input Internal Pressure
    :return:
    """
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
    """
    Step 7: Input External Pressure
    :return: None
    """
    global WIND_LOAD
    global LOCATION
    print_step_heading(7)

    wind_importance_factor = choice(prompt="Wind Importance Factor", options=WindImportanceFactor)
    get_external_pressure(wind_load=WIND_LOAD, wind_importance_factor=wind_importance_factor, location=LOCATION)

    serialize('wind_load', WIND_LOAD)


def step_8():
    """
    Step 8: Check # of variables stored
    :return: None
    """
    global WIND_LOAD
    print_step_heading(8)
    print_obtained_values(WIND_LOAD)


def step_9():
    """
    Step 9: Display Output in User Interface
    :return: None
    """
    print_step_heading(9)
    print("Skipping step, redundant")


def step_10():
    """
    Step 10: Repeat Step1) to 10) for different values of H based on the # of height zones in step 1)
    :return:
    """
    # TODO: Requires refactor, need input from the civil engineering team
    print_step_heading(10)
    print("Skipping step, TODO")


def step_11():
    """
    Step 11: Obtain Slope Factor Cs
    :return: None
    """
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
    """
    Step 12: Display Accumulation Factor Ca
    :return: None
    """
    print_step_heading(12)
    print("Skipping step, accumulation factor saved as a constant")


def step_13():
    """
    Step 13: Obtain Wind Exposure Factor Cw
    :return: None
    """
    global SNOW_LOAD
    print_step_heading(13)

    importance_selection = choice(prompt="Importance Selection", options=WindImportanceFactor)
    wind_exposure_factor_selection = choice(prompt="Wind Exposure Factor Selection",
                                            options=WindExposureFactorSelections)
    snow_load_algorithms.get_wind_exposure_factor(snow_load=SNOW_LOAD, importance_selection=importance_selection,
                                                  wind_exposure_factor_selection=wind_exposure_factor_selection)
    serialize('snow_load', SNOW_LOAD)


def step_14():
    """
    Step 14: Obtain Basic Snow Load Factor Cb
    :return: None
    """
    global SNOW_LOAD
    global BUILDING
    print_step_heading(14)
    print("Computing basic snow load factor")
    get_basic_roof_now_load_factor(snow_load=SNOW_LOAD, building=BUILDING)
    serialize('snow_load', SNOW_LOAD)


def step_15():
    """
    Step 15: Obtain Snow Load S
    :return:
    """
    global SNOW_LOAD
    global LOCATION
    print_step_heading(15)

    snow_importance_factor = choice(prompt="Snow Importance Factor", options=SnowImportanceFactor)
    get_snow_load(snow_load=SNOW_LOAD, snow_importance_factor=snow_importance_factor, location=LOCATION)
    serialize('snow_load', SNOW_LOAD)
    print_obtained_values(SNOW_LOAD)


def step_16():
    """
    Step 16: Check Wp
    :return:
    """
    global BUILDING
    print_step_heading(16)

    print(BUILDING.wp)


def step_17():
    """
    Step 17: User Select values for Ar and Rp: choose either 1 or 2.5. For Cp: display as 1
    :return: None
    """
    global SEISMIC_FACTOR
    global SEISMIC_LOAD
    print_step_heading(17)

    SEISMIC_FACTOR = SeismicFactor()
    SEISMIC_LOAD = SeismicLoad(factor=SEISMIC_FACTOR, ax=None, sp=None, vp=None, vp_snow=None)

    confirm_ar = confirm_choice("Would you like to use default value of 1 for Ar?")
    if not confirm_ar:
        ar = float(user_input("Ar"))
        get_seismic_factor_values(seismic_load=SEISMIC_LOAD, ar=ar)
    confirm_rp = confirm_choice("Would you like to use default value of 2.5 for Rp?")
    if not confirm_rp:
        rp = float(user_input("Rp"))
        get_seismic_factor_values(seismic_load=SEISMIC_LOAD, rp=rp)
    confirm_cp = confirm_choice("Would you like to use default value of 1 for Cp?")
    if not confirm_cp:
        cp = float(user_input("Cp"))
        get_seismic_factor_values(seismic_load=SEISMIC_LOAD, cp=cp)

    serialize('seismic_load', SEISMIC_LOAD)


def step_18():
    """
    Step 18: Create a df for each floor elevation based on Step 1) N_floor and H  2)hz_num
    :return: None
    """
    global BUILDING

    print(f"BUILDING {BUILDING.dimensions.height}")
    print(f"BUILDING {BUILDING.num_floor}")

    floor_mapping = get_floor_mapping(building=BUILDING)
    print(floor_mapping)


def step_19():
    """
    Step 19: Calculate Ax, do not display this to user
    :return: None
    """
    global SEISMIC_LOAD
    global BUILDING
    print_step_heading(19)

    floor = int(user_input("Floor number"))
    get_height_factor(seismic_load=SEISMIC_LOAD, building=BUILDING, floor=floor)
    serialize('seismic_load', SEISMIC_LOAD)


def step_20():
    """
    Step 20: Calculate Sp
    :return: None
    """
    global SEISMIC_LOAD
    print_step_heading(20)

    get_horizontal_force_factor(seismic_load=SEISMIC_LOAD)
    serialize('seismic_load', SEISMIC_LOAD)


def step_21():
    """
    Step 21: Calculate Vp
    :return: None
    """
    global SEISMIC_LOAD
    global SNOW_LOAD
    global BUILDING
    global LOCATION
    print_step_heading(21)

    seismic_importance_factor = choice(prompt="Seismic Importance Factor", options=SeismicImportanceFactor)
    get_specified_lateral_earthquake_force(seismic_load=SEISMIC_LOAD, snow_load=SNOW_LOAD, building=BUILDING,
                                           location=LOCATION, seismic_importance_factor=seismic_importance_factor)
    serialize('seismic_load', SEISMIC_LOAD)
    print_obtained_values(SEISMIC_LOAD)


########################################################################################################################
# MAIN
########################################################################################################################

if __name__ == '__main__':
    print_line()
    print("ASPENLOG 2020 CONSOLE WALKTHROUGH")

    create_save_file()

    for i in range(22):
        skip_step(i)
