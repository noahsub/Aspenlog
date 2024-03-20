########################################################################################################################
# console_walkthrough_v3.py
# This file contains the console walkthrough for the backend of the application.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import json
import os
from copy import deepcopy
from typing import List

import jsonpickle
import pandas as pd
import rich
import typer
from rich import print
from rich.prompt import Prompt

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Constants.roof_load_combination_constants import ULSRoofLoadCombinationTypes, SLSRoofLoadCombinationTypes
from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Constants.snow_constants import RoofType, WindDirection
from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Constants.wind_constants import WindExposureFactorSelections, InternalPressureSelections
from backend.Entities.Building.building import BuildingDefaultHeightDefaultMaterialBuilder, \
    BuildingCustomHeightDefaultMaterialBuilder
from backend.Entities.Building.cladding import CladdingBuilder, Cladding
from backend.Entities.Building.dimensions import BasicDimensionsBuilder, \
    EaveRidgeDimensionsBuilder, Dimensions
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Building.roof import RoofBuilder, Roof
from backend.Entities.Location.location import LocationXvBuilder, LocationXsBuilder
from backend.Entities.Seismic.seismic_factor import SeismicFactorBuilder
from backend.Entities.Seismic.seismic_load import SeismicLoadBuilder
from backend.Entities.Snow.snow_factor import SnowFactorBuilder
from backend.Entities.Snow.snow_load import SnowLoadBuilder
from backend.Entities.Wind.wind_factor import WindFactorBuilder
from backend.Entities.Wind.wind_load import WindLoadBuilder
from backend.Entities.Wind.wind_pressure import WindPressureBuilder
from backend.algorithms.load_combination_algorithms import compute_wall_load_combinations, \
    compute_roof_load_combinations
from backend.algorithms.seismic_load_algorithms import get_seismic_factor_values, get_floor_mapping, get_height_factor, \
    get_horizontal_force_factor, get_specified_lateral_earthquake_force
from backend.algorithms.snow_load_algorithms import get_slope_factor, get_accumulation_factor, \
    get_wind_exposure_factor_snow, get_basic_roof_snow_load_factor, get_snow_load
from backend.algorithms.wind_load_algorithms import get_wind_topographic_factor, get_wind_exposure_factor, \
    get_wind_gust_factor, get_internal_pressure, get_external_pressure

########################################################################################################################
# GLOBALS
########################################################################################################################

# The space available in the console
TERM_SIZE = 80


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


def check_save(name: str, func, *args):
    try:
        data = deserialize(name)
        if isinstance(data, list):
            rich.print(f"Found [bold red]{name}[/bold red] with the value [bold red]{[str(x) for x in data]}[/bold red]")
        else:
            rich.print(f"Found [bold red]{name}[/bold red] with the value [bold red]{str(data)}[/bold red]")
        confirm_save = confirm_choice(f"Would you like to keep it?")
        if confirm_save:
            return data
        else:
            obj = func(*args)
            serialize(name, obj)
            return obj
    except:
        obj = func(*args)
        serialize(name, obj)
        return obj

def check_save_simple(name: str):
    try:
        data = deserialize(name)
        if isinstance(data, list):
            rich.print(f"Found [bold red]{name}[/bold red] with the value [bold red]{[str(x) for x in data]}[/bold red]")
        else:
            rich.print(f"Found [bold red]{name}[/bold red] with the value [bold red]{str(data)}[/bold red]")
        return True
    except:
        return False

########################################################################################################################
# FUNCTIONS
########################################################################################################################

def location_data(address: str, site_designation: SiteDesignation, seismic_value: int | SiteClass):
    match site_designation:
        case SiteDesignation.XV:
            location_builder = LocationXvBuilder()
        case SiteDesignation.XS:
            location_builder = LocationXsBuilder()
    location_builder.set_address(address)
    location_builder.set_coordinates()
    location_builder.set_climatic_data()
    location_builder.set_seismic_data(seismic_value)
    return location_builder.get_location()


def building_dimensions(width: float, height: float = None, eave_height=None, ridge_height=None):
    if eave_height is None and ridge_height is None:
        dimensions_builder = BasicDimensionsBuilder()
        dimensions_builder.set_height(height)
        dimensions_builder.set_width(width)
    else:
        dimensions_builder = EaveRidgeDimensionsBuilder()
        dimensions_builder.set_width(width)
        dimensions_builder.set_height_eave(eave_height)
        dimensions_builder.set_height_ridge(ridge_height)
        dimensions_builder.compute_height()
    return dimensions_builder.get_dimensions()


def building_cladding(c_top: float, c_bot: float):
    cladding_builder = CladdingBuilder()
    cladding_builder.set_c_top(c_top)
    cladding_builder.set_c_bot(c_bot)
    return cladding_builder.get_cladding()


def building_roof(w_roof: float, l_roof: float, slope: float, uniform_dead_load: float):
    roof_builder = RoofBuilder()
    roof_builder.set_w_roof(w_roof)
    roof_builder.set_l_roof(l_roof)
    roof_builder.set_slope(slope)
    roof_builder.compute_wall_slope()
    roof_builder.set_wp(uniform_dead_load)
    return roof_builder.get_roof()


def building(dimensions: Dimensions, cladding: Cladding, roof: Roof, num_floor: int, h_opening: float, material_load: List[float] | float,
             height_zones: List[HeightZone] = None):

    print(height_zones)
    print(material_load)

    # Case default height zones and simple material load
    if height_zones is None and isinstance(material_load, (list, float)):
        building_builder = BuildingDefaultHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones()
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    # Case custom height zones and simple material load
    elif height_zones is not None and isinstance(material_load, (list, float)):
        building_builder = BuildingCustomHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones(height_zones)
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    else:
        raise NotImplementedError


########################################################################################################################
# MAIN
########################################################################################################################

if __name__ == '__main__':
    title = """
       d8888  .d8888b.  8888888b.  8888888888 888b    888 888      .d88888b.   .d8888b.  
      d88888 d88P  Y88b 888   Y88b 888        8888b   888 888     d88P" "Y88b d88P  Y88b 
     d88P888 Y88b.      888    888 888        88888b  888 888     888     888 888    888 
    d88P 888  "Y888b.   888   d88P 8888888    888Y88b 888 888     888     888 888        
   d88P  888     "Y88b. 8888888P"  888        888 Y88b888 888     888     888 888  88888 
  d88P   888       "888 888        888        888  Y88888 888     888     888 888    888 
 d8888888888 Y88b  d88P 888        888        888   Y8888 888     Y88b. .d88P Y88b  d88P 
d88P     888  "Y8888P"  888        8888888888 888    Y888 88888888 "Y88888P"   "Y8888P88                                                                                                                                                                                                                                                                                            
    """
    print_line()
    print(title)
    print("2020 CONSOLE EDITION V3")
    print_line()

    create_save_file()

    # address
    address = check_save('address', user_input, 'address')

    # site designation
    site_designation = check_save('site_designation', choice, 'site designation type', SiteDesignation)

    # seismic_value
    seismic_value = None
    if site_designation == SiteDesignation.XV:
        seismic_value = int(check_save('seismic_value_xv', user_input, 'xv value'))
    else:
        seismic_value = check_save('seismic_value_xs', choice, 'site class', SiteClass)

    print("Collecting information from database and external APIs...")

    location = location_data(address=address, site_designation=site_designation, seismic_value=seismic_value)



    print_line()
    print("LOCATION")
    print_line()
    print(location)
    print_line()

    # eave_height
    eave_height = None
    ridge_height = None
    height = None
    width = None

    confirm_eave_ridge_choice = check_save('confirm_eave_ridge_choice', confirm_choice, "Does the building have eave and ridge?")

    if confirm_eave_ridge_choice:
        eave_height = float(check_save('eave_height', user_input, "eave height"))
        ridge_height = float(check_save('ridge height', user_input, "ridge height"))
    else:
        height = float(check_save('height', user_input, "height"))
    width = float(check_save('width', user_input, "width"))

    confirm_height_zone = check_save('confirm_height_zone', confirm_choice, "Default is 20 m per height zone, meaning number of height zones = ⌈H/20⌉. Are you ok with this?")

    num_floor = int(check_save('num_floor', user_input, 'number of floors'))

    top_cladding = float(check_save('c_top', user_input, 'top of cladding'))

    dominant_opening = check_save('dominant_opening', confirm_choice, 'Does the building have Dominant Opening?')

    if dominant_opening:
        mid_height = float(check_save('mid_height', user_input, 'mid-height of the dominant opening'))
    else:
        mid_height = 0.0
        serialize('mid_height', mid_height)

    bottom_cladding = float(check_save('c_bot', user_input, 'bottom of cladding'))

    height_zones = None
    if not confirm_height_zone:
        custom_num_height_zones = int(check_save('custom_num_height_zones', user_input, 'number of height zones'))
        if check_save_simple('height_zones') and confirm_choice(f"Would you like to keep them?"):
            height_zones = deserialize('height_zones')
        else:
            height_zones = []
            for i in range(custom_num_height_zones):
                height_zones.append(HeightZone(zone_num=i + 1, elevation=float(user_input(f"Elevation of height zone {i + 1}"))))
        serialize('height_zones', height_zones)

    w_roof = float(check_save('w_roof', user_input, 'smaller plan dimension of the roof'))
    l_roof = float(check_save('l_roof', user_input, 'larger plan dimension of the roof'))
    slope = float(check_save('slope', user_input, 'slope of the roof'))

    confirm_material = check_save('confirm_material', confirm_choice, 'The material will be applied to all height zones?')
    material_list = None
    wp = None
    if confirm_material:
        wp = float(check_save('wp', user_input, 'material load'))
    else:
        # custom_num_material_zones = int(check_save('custom_num_material_zones', user_input, 'number of material zones (same as number of height zones)'))
        # if check_save_simple('material_zones') and confirm_choice(f"Would you like to keep them?"):
        #     material_zones = deserialize('material_zones')
        # else:
        #     material_zones = []
        #     for i in range(custom_num_material_zones):
        #         finished_materials = False
        #         materials_list = []
        #         k = 1
        #         while not finished_materials:
        #             materials_list.append(MaterialComposition(material=choice(f"material {k} for height zone {i + 1}", Materials), respected_percentage=float(user_input("respected percentage")), weight=float(user_input("weight"))))
        #             finished_materials = not confirm_choice("Would you like to add another material for the current height zone?")
        #             k += 1
        #         material_zones.append(MaterialZone(materials_list))
        # serialize('material_zones', material_zones)
        num_materials = int(check_save('num_materials', user_input, 'number of materials (same as number of height zones)'))
        if check_save_simple('material_list') and confirm_choice(f"Would you like to keep them?"):
            material_list = deserialize('material_list')
        else:
            material_list = []
            for i in range(num_materials):
                material_list.append(float(user_input(f"material load for height zone {i + 1}")))
            serialize('material_list', material_list)

    wp_roof = float(check_save('wp_roof', user_input, 'uniform dead load for roof'))

    dimensions = building_dimensions(width=width, height=height, eave_height=eave_height, ridge_height=ridge_height)
    cladding = building_cladding(c_top=top_cladding, c_bot=bottom_cladding)
    roof = building_roof(w_roof=w_roof, l_roof=l_roof, slope=slope, uniform_dead_load=wp_roof)

    material_load = material_list
    if material_list is None:
        material_load = wp

    building = building(dimensions=dimensions, cladding=cladding, roof=roof, num_floor=num_floor, h_opening=mid_height, material_load=material_load, height_zones=height_zones)

    print_line()
    print("BUILDING")
    print("~ LOAD CALCULATIONS HAVE NOT TAKEN PLACE YET ~")
    print_line()
    print(building)
    print_line()

    importance_category = check_save('importance_category', choice, 'importance category', ImportanceFactor)
    exposure_factor_selection = None

    for height_zone in building.height_zones:
        wind_factor_builder = WindFactorBuilder()

        confirm_topographic_factor = check_save(f'confirm_topographic_factor_{height_zone.zone_num}', confirm_choice, 'Would you like to use a custom topographic factor (default 1)?')
        topographic_factor = None
        if confirm_topographic_factor:
            topographic_factor = float(check_save(f'topographic_factor_{height_zone.zone_num}', user_input, 'topographic factor'))
            get_wind_topographic_factor(wind_factor_builder, topographic_factor)
        else:
            topographic_factor = 1
            get_wind_topographic_factor(wind_factor_builder)
            serialize(f'topographic_factor_{height_zone.zone_num}', topographic_factor)

        exposure_factor_selection = check_save(f'exposure_factor_selection_{height_zone.zone_num}', choice, 'exposure factor selection', WindExposureFactorSelections)
        if exposure_factor_selection == WindExposureFactorSelections.INTERMEDIATE:
            manual_ce_cei = float(check_save(f"exposure_factor_manual_value_{height_zone.zone_num}", user_input, "single value for both ce and cei"))
            get_wind_exposure_factor(wind_factor_builder, exposure_factor_selection, building, height_zone.zone_num, manual_ce_cei)
        else:
            get_wind_exposure_factor(wind_factor_builder, exposure_factor_selection, building, height_zone.zone_num)

        get_wind_gust_factor(wind_factor_builder)

        wind_factor = wind_factor_builder.get_wind_factor()
        wind_pressure_builder = WindPressureBuilder()
        internal_pressure_selection = check_save(f'internal_pressure_selection_{height_zone.zone_num}', choice, 'internal pressure selection',  InternalPressureSelections)

        get_internal_pressure(wind_factor, wind_pressure_builder, internal_pressure_selection, importance_category, location)

        wind_load_builder = WindLoadBuilder()
        get_external_pressure(wind_factor, wind_pressure_builder, wind_load_builder, importance_category, location)

        wind_load = wind_load_builder.get_wind_load()
        height_zone.wind_load = wind_load

        print_line()
        print(f"WIND LOAD FOR HEIGHT ZONE {height_zone.zone_num}")
        print(wind_load)
        print_line()

    roof_type = check_save('roof_type', choice, 'roof type', RoofType)
    snow_factor_builder_downwind = SnowFactorBuilder()
    snow_factor_builder_upwind = SnowFactorBuilder()

    # downwind snow_load
    get_slope_factor(snow_factor_builder_downwind, roof_type, building)
    get_accumulation_factor(snow_factor_builder_downwind, WindDirection.DOWNWIND, building)
    get_wind_exposure_factor_snow(snow_factor_builder_downwind, importance_category, exposure_factor_selection)
    get_basic_roof_snow_load_factor(snow_factor_builder_downwind, building)
    snow_load_builder_downwind = SnowLoadBuilder()
    get_snow_load(snow_factor_builder_downwind, snow_load_builder_downwind, importance_category, location)

    # upwind snow_load
    get_slope_factor(snow_factor_builder_upwind, roof_type, building)
    get_accumulation_factor(snow_factor_builder_upwind, WindDirection.UPWIND, building)
    get_wind_exposure_factor_snow(snow_factor_builder_upwind, importance_category, exposure_factor_selection)
    get_basic_roof_snow_load_factor(snow_factor_builder_upwind, building)
    snow_load_builder_upwind = SnowLoadBuilder()
    get_snow_load(snow_factor_builder_upwind, snow_load_builder_upwind, importance_category, location)

    snow_load_downwind = snow_load_builder_downwind.get_snow_load()
    snow_load_upwind = snow_load_builder_upwind.get_snow_load()
    print_line()
    print(f"SNOW LOAD DOWNWIND")
    print(snow_load_downwind)

    print(f"SNOW LOAD UPWIND")
    print(snow_load_upwind)
    print_line()

    seismic_factor_builder = SeismicFactorBuilder()
    ar = None
    confirm_ar = check_save('confirm_ar', confirm_choice, 'Would you like to use the default ar value of 1?')
    if confirm_ar:
        ar = 1
        serialize('ar', ar)
    else:
        ar = float(check_save('ar', user_input, 'ar'))

    rp = None
    confirm_rp = check_save('confirm_rp', confirm_choice, 'Would you like to use the default rp value of 2.5?')
    if confirm_rp:
        rp = 2.5
        serialize('rp', rp)
    else:
        rp = float(check_save('rp', user_input, 'rp'))

    cp = None
    confirm_cp = check_save('confirm_cp', confirm_choice, 'Would you like to use the default cp value of 1?')
    if confirm_cp:
        cp = 1
        serialize('cp', cp)
    else:
        cp = float(check_save('cp', user_input, 'cp'))

    get_seismic_factor_values(seismic_factor_builder, ar, rp, cp)

    floor_mapping = get_floor_mapping(building)
    
    print("FLOOR MAPPING")
    for x, y in floor_mapping.items():
        print(f"floor {x} : height zone {y}")

    for height_zone in building.height_zones:
        zone_seismic_factor_builder = deepcopy(seismic_factor_builder)
        seismic_load_builder = SeismicLoadBuilder()
        get_height_factor(seismic_load_builder, building, height_zone.zone_num)
        get_horizontal_force_factor(zone_seismic_factor_builder, seismic_load_builder)
        get_specified_lateral_earthquake_force(seismic_load_builder, building, height_zone.zone_num, location, importance_category)
        seismic_load = seismic_load_builder.get_seismic_load()
        height_zone.seismic_load = seismic_load

        print_line()
        print(f"SEISMIC LOAD FOR HEIGHT ZONE {height_zone.zone_num}")
        print(seismic_load)
        print_line()

    print("WALL LOAD COMBINATIONS")
    uls_for_wall = check_save('uls_for_wall', choice, 'ULS for wall', ULSWallLoadCombinationTypes)
    sls_for_wall = check_save('sls_for_wall', choice, 'SLS for wall', SLSWallLoadCombinationTypes)
    zone_num = user_input('Enter the zone number for which you want to compute the wall load combinations')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(compute_wall_load_combinations(building, snow_load_downwind, uls_for_wall, sls_for_wall))

    print("ROOF LOAD COMBINATIONS")
    uls_for_roof = check_save('uls_for_roof', choice, 'ULS for roof', ULSRoofLoadCombinationTypes)
    sls_for_roof = check_save('sls_for_roof', choice, 'SLS for roof', SLSRoofLoadCombinationTypes)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(compute_roof_load_combinations(building, snow_load_downwind, uls_for_roof, sls_for_roof))

    print("PROGRAM TERMINATING...")



