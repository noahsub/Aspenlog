########################################################################################################################
# IMPORTS
########################################################################################################################

import json
import os
from typing import List, Dict

import jsonpickle
import typer
from rich import print
from rich.prompt import Prompt

from backend.Constants.materials import Materials
from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Entities.Building.building import BuildingBuilder, BuildingDefaultHeightDefaultMaterialBuilder, \
    BuildingDefaultHeightCustomMaterialBuilder, BuildingCustomHeightDefaultMaterialBuilder, \
    BuildingCustomHeightCustomMaterialBuilder
from backend.Entities.Building.cladding import CladdingBuilder, CladdingBuilderInterface, Cladding
from backend.Entities.Building.dimensions import DimensionsBuilderInterface, BasicDimensionsBuilder, \
    EaveRidgeDimensionsBuilder, Dimensions
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Building.material_zone import MaterialZone
from backend.Entities.Building.roof import RoofBuilder, RoofBuilderInterface, Roof
from backend.Entities.Location.location import LocationBuilderInterface, LocationXvBuilder, LocationXsBuilder

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

def building_dimensions(building_builder: BuildingBuilder, width: float, height: float=None, eave_height=None, ridge_height=None):
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

def building_cladding(building_builder: BuildingBuilder, c_top: float, c_bot: float):
    cladding_builder = CladdingBuilder()
    cladding_builder.set_c_top(c_top)
    cladding_builder.set_c_bot(c_bot)
    return cladding_builder.get_cladding()

def building_roof(building_builder: BuildingBuilder, w_roof: float, l_roof: float, slope: float, uniform_dead_load: float):
    roof_builder = RoofBuilder()
    roof_builder.set_w_roof(w_roof)
    roof_builder.set_l_roof(l_roof)
    roof_builder.set_slope(slope)
    roof_builder.compute_wall_slope()
    roof_builder.set_wp(uniform_dead_load)
    return roof_builder.get_roof()

def building(dimensions: Dimensions, cladding: Cladding, roof: Roof, material_load: List[MaterialZone] | float, height_zones: List[HeightZone] = None):
    # Case default height zones and simple material load
    if height_zones is None and isinstance(material_load, (float, int)):
        building_builder = BuildingDefaultHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.generate_height_zones()
        building_builder.set_wp(material_load)
    # Case default height zones and custom material load
    elif height_zones is None and not isinstance(material_load, (float, int)):
        building_builder = BuildingDefaultHeightCustomMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.generate_height_zones()
        building_builder.generate_material_zones(material_load)
    # Case custom height zones and simple material load
    elif height_zones is not None and isinstance(material_load, (float, int)):
        building_builder = BuildingCustomHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.generate_height_zones(height_zones)
        building_builder.set_wp(material_load)
    # Case custom height zones and custom material load
    elif height_zones is not None and not isinstance(material_load, (float, int)):
        building_builder = BuildingCustomHeightCustomMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.generate_height_zones(height_zones)
        building_builder.generate_material_zones(material_load)
    else:
        raise NotImplementedError














########################################################################################################################
# MAIN
########################################################################################################################

if __name__ == '__main__':
