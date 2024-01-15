import json
import os
import jsonpickle
import typer
from rich import print
from rich.prompt import Prompt

from backend.Constants.materials import Materials
from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Entities.Building.building import BuildingBuilder
from backend.Entities.Building.cladding import CladdingBuilder
from backend.Entities.Building.dimensions import EaveRidgeDimensionsBuilder, BasicDimensionsBuilder
from backend.Entities.Building.height_zone import HeightZoneBuilder
from backend.Entities.Building.roof import RoofBuilder
from backend.Entities.Location.location import LocationXsBuilder, LocationXvBuilder


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


if __name__ == '__main__':
    # STEP 0
    address = user_input("Address")
    site_designation_type = choice(prompt="site designation type", options=SiteDesignation)
    location_builder = None
    match site_designation_type:
        case SiteDesignation.XV:
            location_builder = LocationXvBuilder()
            location_builder.set_address(address)
            location_builder.set_coordinates()
            location_builder.set_climatic_data()
            xv = int(user_input("Vs30 value measured in situ between 140 - 3000 m/s"))
            location_builder.set_seismic_data(xv)
        case SiteDesignation.XS:
            location_builder = LocationXsBuilder()
            location_builder.set_address(address)
            location_builder.set_coordinates()
            location_builder.set_climatic_data()
            xs = choice(prompt="Site Class", options=SiteClass)
            location_builder.set_seismic_data(xs)
    location = location_builder.get_location()
    print(location)

    # STEP 1
    building_builder = BuildingBuilder()
    # STEP 1.1
    confirm_eave = confirm_choice("Does the building have eave?")
    dimensions_builder = None
    if confirm_eave:
        dimensions_builder = EaveRidgeDimensionsBuilder()
        height_eave = float(user_input("Eave height in meters"))
        height_ridge = float(user_input("Ridge height in meters"))
        dimensions_builder.set_height_eave(height_eave)
        dimensions_builder.set_height_ridge(height_ridge)
        dimensions_builder.compute_height()
    else:
        dimensions_builder = BasicDimensionsBuilder()
        height = float(user_input("Building height above grade in meters"))
        dimensions_builder.set_height(height)
    width = int(user_input("Width of building in meters"))

    dimensions = dimensions_builder.get_dimensions()
    building_builder.set_dimensions(dimensions)

    confirm_height_zone = confirm_choice("Default is 20 m per height zone, meaning number of height zones = ⌈H/20⌉. Are you ok with this?")

    num_floors = int(user_input("Number of floors"))
    building_builder.set_num_floor(num_floors)

    cladding_builder = CladdingBuilder()
    c_top = float(user_input("Top of cladding in meters"))
    cladding_builder.set_c_top(c_top)

    confirm_h_opening = confirm_choice("Does the building have Dominant Opening?")
    if not confirm_h_opening:
        building_builder.set_h_opening(0)
    else:
        h_opening = float(user_input("Mid-height of the dominant opening"))
        building_builder.set_h_opening(h_opening)

    c_bot = float(user_input("Bottom of cladding in meters"))
    cladding_builder.set_c_bot(c_bot)

    cladding = cladding_builder.get_cladding()
    building_builder.set_cladding(cladding)

    # STEP 1.2
    if not confirm_height_zone:
        num_height_zones = user_input("Number of height zones")
        height_zone_builders = []
        for i in range(num_height_zones):
            height_zone_builder = HeightZoneBuilder()
            height_zone_builder.set_zone_num(i + 1)
            elevation = user_input(f"Elevation of height zone {i + 1}")
            height_zone_builder.set_elevation(elevation)
            height_zone_builders.append(height_zone_builder)
    else:
        height_zone_builders = building_builder.compute_default_height_zones()

    # STEP 1.3
    w_roof = float(user_input("Smaller Plan dimension of the roof in meters"))
    l_roof = float(user_input("Larger Plan dimension of the roof in meters"))
    slope = float(user_input("Slope of the roof in degrees"))

    roof_builder = RoofBuilder()
    roof_builder.set_w_roof(w_roof)
    roof_builder.set_l_roof(l_roof)
    roof_builder.set_slope(slope)
    roof_builder.compute_wall_slope()

    # STEP 1.4
    confirm_material = confirm_choice(prompt="The material will be applied to all height zones?")

    if confirm_material:
        # There are no custom materials, hence we use an empty dictionary
        for height_zone_builder in height_zone_builders:
            height_zone_builder.set_wp_materials(dict())
        wp = float(user_input("Material Load"))
        building_builder.set_wp(wp)
    else:
        for height_zone_builder in height_zone_builders:
            wp_materials = dict()
            materials = multi_choice(prompt=f"Material for height zone {height_zone_builder.get_zone_num()}", options=Materials)
            for material in materials:
                wp = float(user_input(f"Material Load for {material.value}"))
                wp_materials[material] = wp
            height_zone_builder.set_wp_materials(wp_materials)

    building_builder.set_height_zones([x.get_height_zone() for x in height_zone_builders])

    if not confirm_material:
        building_builder.compute_advanced_dead_load()


    # STEP 1.7
    wp_roof = float(user_input("Uniform dead load for roof"))
    roof_builder.set_wp(wp_roof)

    roof = roof_builder.get_roof()
    building_builder.set_roof(roof)

    building = building_builder.get_building()
    print(building)







