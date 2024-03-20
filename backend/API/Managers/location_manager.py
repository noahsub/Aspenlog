########################################################################################################################
# location_manager.py
# This file manages the location data for a user.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from backend.Constants.seismic_constants import SiteDesignation, SiteClass
from backend.Entities.Location.location import LocationXvBuilder, LocationXsBuilder


########################################################################################################################
# MANAGER
########################################################################################################################


def process_location_data(
    address: str, site_designation: str, seismic_value: int | str
):
    """
    Processes the location data and creates a location object
    :param address: The address of the location
    :param site_designation: The site designation of the location
    :param seismic_value: The seismic value of the location, int if xv, str if xs
    :return:
    """
    # Convert the site designation and seismic value to the correct enums
    site_designation = SiteDesignation.get_key_from_value(site_designation)
    # If the site designation is XS, convert the seismic value to the correct enum
    if site_designation == SiteDesignation.XS:
        seismic_value = SiteClass.get_key_from_value(seismic_value)
    # Create a location object based on the site designation type
    match site_designation:
        case SiteDesignation.XV:
            location_builder = LocationXvBuilder()
        case SiteDesignation.XS:
            location_builder = LocationXsBuilder()
    # Set the location data
    location_builder.set_address(address)
    location_builder.set_coordinates()
    # Set the climatic data
    location_builder.set_climatic_data()
    # Set the seismic data
    location_builder.set_seismic_data(seismic_value)
    # Return the location object
    return location_builder.get_location()
