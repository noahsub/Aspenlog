########################################################################################################################
# load_combination_algorithms.py
# This file contains the algorithms for computing the load combinations of a building. The load combinations are
# computed for both the roof and the walls and for both the ULS and SLS.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import pandas as pd

from backend.Constants.roof_load_combination_constants import ULSRoofLoadCombinationTypes, SLSRoofLoadCombinationTypes
from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad


########################################################################################################################
# HEIGHT ZONE CALCULATIONS
########################################################################################################################


def compute_height_zone_width(building: Building, zone_number: int):
    """
    Compute the height of a height zone (not elevation)
    :param building: The building associated with the height zone
    :param zone_number: The number identifier of the height zone
    :return: The height of the height zone
    """
    # The height of the first height zone is simply its elevation
    if zone_number == 1:
        return building.get_height_zone(zone_number).elevation
    # The height of the height zone is the difference between its elevation and the elevation of the previous
    # height zone
    else:
        prev_elevation = building.get_height_zone(zone_number - 1).elevation
        curr_elevation = building.get_height_zone(zone_number).elevation
        assert curr_elevation > prev_elevation
        return curr_elevation - prev_elevation


def compute_height_zone_variables(building: Building, zone_number: int):
    """
    Get the xn, hx, ce, ax for a height zone
    :param building: The building associated with the height zone
    :param zone_number: The number identifier of the height zone
    :return: A dictionary containing the xn, hx, ce, ax for the height zone
    """
    return {'xn': compute_height_zone_width(building, zone_number),
            'hx': building.get_height_zone(zone_number).elevation,
            'ce': building.get_height_zone(zone_number).wind_load.factor.ce,
            'ax': building.get_height_zone(zone_number).seismic_load.ax}


def compute_top_height_zone_variables(building: Building):
    """
    Get the xn, hx, ce, ax for the top height zone
    :param building: The building associated with the height zone
    :return: A dictionary containing the xn, hx, ce, ax for the top height zone
    """
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'xn': compute_height_zone_variables(building, top_height_zone.zone_num)['xn'],
            'hx': top_height_zone.elevation,
            'ce': top_height_zone.wind_load.factor.ce,
            'ax': top_height_zone.seismic_load.ax}


def get_height_zone_variables_keys():
    """
    Get the keys for the height zone variables
    :return: A list containing the keys for the height zone variables
    """
    return ['xn', 'hx', 'ce', 'ax']


########################################################################################################################
# ULS WALL COMBINATION CALCULATIONS
########################################################################################################################

def uls_wall_1_4D(building: Building, zone_num: int):
    """
    ULS Wall 1.4D combination calculation
    :param building: The building associated with the height zone
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed ULS 1.4D combination value
    """
    return {'uls 1.4D': 1.4 * building.get_height_zone(zone_num).wp}


def get_uls_wall_1_4D_keys():
    """
    Get the keys for the ULS wall 1.4D combination calculation
    :return: A list containing the keys for the ULS wall 1.4D combination calculation
    """
    return ['uls 1.4D']


def uls_wall_1_25D_1_4Wy(building: Building, snow_load: SnowLoad, zone_num: int):
    """
    ULS wall 1.25D 1.4Wy combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed ULS wall 1.25D 1.4Wy combination values
    """
    return {'uls 1.25D': building.get_height_zone(zone_num).wp * 1.25,
            'uls 1.4Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.pos_uls,
            'uls 1.4Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.pos_uls,
            'companion': snow_load.s_uls * 0.5}


def get_uls_wall_1_25D_1_4Wy_keys():
    """
    Get the keys for the ULS wall 1.25D 1.4Wy combination calculation
    :return: A list containing the keys for the ULS wall 1.25D 1.4Wy combination calculation
    """
    return ['uls 1.25D', 'uls 1.4Wy (centre)', 'uls 1.4Wy (edge)', 'companion']


def uls_wall_0_9D_1_4Wx(building: Building, snow_load: SnowLoad, zone_num: int):
    """
    ULS wall 0.9D 1.4Wx combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed ULS wall 0.9D 1.4Wx combination values
    """
    return {'uls 0.9D': building.get_height_zone(zone_num).wp * 0.9,
            'uls 1.4Wx (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.neg_uls,
            'uls 1.4Wx (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.neg_uls,
            'companion': snow_load.s_uls * 0.5}


def get_uls_wall_0_9D_1_4Wx_keys():
    """
    Get the keys for the ULS wall 0.9D 1.4Wx combination calculation
    :return: A list containing the keys for the ULS wall 0.9D 1.4Wx combination calculation
    """
    return ['uls 0.9D', 'uls 1.4Wx (centre)', 'uls 1.4Wx (edge)', 'companion']


def uls_wall_1_0D_1_0Ey(building: Building, snow_load: SnowLoad, zone_num: int):
    """
    ULS wall 1.0D 1.0Ey combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed ULS wall 1.0D 1.0Ey combination values
    """
    return {'uls 1.0D': building.get_height_zone(zone_num).wp,
            'uls 1.0Ey': building.get_height_zone(zone_num).seismic_load.vp,
            'companion': snow_load.s_uls * 0.25}


def get_uls_wall_1_0D_1_0Ey_keys():
    """
    Get the keys for the ULS wall 1.0D 1.0Ey combination calculation
    :return: A list containing the keys for the ULS wall 1.0D 1.0Ey combination calculation
    """
    return ['uls 1.0D', 'uls 1.0Ey', 'companion']


def uls_wall_1_0D_1_0Ex(building: Building, snow_load: SnowLoad, zone_num: int):
    """
    ULS wall 1.0D 1.0Ex combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed ULS wall 1.0D 1.0Ex combination values
    """
    return {'uls 1.0D': building.get_height_zone(zone_num).wp,
            'uls 1.0Ex': building.get_height_zone(zone_num).seismic_load.vp,
            'companion': snow_load.s_uls * 0.25}


def get_uls_wall_1_0D_1_0Ex_keys():
    """
    Get the keys for the ULS wall 1.0D 1.0Ex combination calculation
    :return: A list containing the keys for the ULS wall 1.0D 1.0Ex combination calculation
    """
    return ['uls 1.0D', 'uls 1.0Ex', 'companion']


########################################################################################################################
# SLS WALL COMBINATION CALCULATIONS
########################################################################################################################

def sls_wall_1_0D_1_0Wy(building: Building, zone_num: int):
    """
    SLS wall 1.0D 1.0Wy combination calculation
    :param building: The building associated with the height zone
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed SLS wall 1.0D 1.0Wy combination values
    """
    return {'sls 1.0D': building.get_height_zone(zone_num).wp,
            'sls 1.0Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.pos_sls,
            'sls 1.0Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.pos_sls}


def get_sls_wall_1_0D_1_0Wy_keys():
    """
    Get the keys for the SLS wall 1.0D 1.0Wy combination calculation
    :return: A list containing the keys for the SLS wall 1.0D 1.0Wy combination calculation
    """
    return ['sls 1.0D', 'sls 1.0Wy (centre)', 'sls 1.0Wy (edge)']


def sls_wall_1_0D_1_0Wx(building: Building, zone_num: int):
    """
    SLS wall 1.0D 1.0Wx combination calculation
    :param building: The building associated with the height zone
    :param zone_num: The number identifier of the height zone
    :return: A dictionary containing the computed SLS wall 1.0D 1.0Wx combination values
    """
    return {'sls 1.0D': building.get_height_zone(zone_num).wp,
            'sls 1.0Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.neg_sls,
            'sls 1.0Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.neg_sls}


def get_sls_wall_1_0D_1_0Wx_keys():
    """
    Get the keys for the SLS wall 1.0D 1.0Wx combination calculation
    :return: A list containing the keys for the SLS wall 1.0D 1.0Wx combination calculation
    """
    return ['sls 1.0D', 'sls 1.0Wx (centre)', 'sls 1.0Wx (edge)']


########################################################################################################################
# ULS ROOF COMBINATION CALCULATIONS
########################################################################################################################

def uls_roof_1_4D(building: Building):
    """
    ULS roof 1.4D combination calculation
    :param building: The building associated with the height zone
    :return: A dictionary containing the computed ULS roof 1.4D combination value
    """
    return {'uls 1.4D': building.roof.wp * 1.4}


def get_uls_roof_1_4D_keys():
    """
    Get the keys for the ULS roof 1.4D combination calculation
    :return: A list containing the keys for the ULS roof 1.4D combination calculation
    """
    return ['uls 1.4D']


def uls_roof_1_25D_1_4Wy(building: Building, snow_load: SnowLoad):
    """
    ULS roof 1.25D 1.4Wy combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 1.25D 1.4Wy combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.4Wy (corner)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls,
            'uls 1.4Wy (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls,
            'uls 1.4Wy (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls,
            'companion': max(snow_load.s_uls * 0.5, 1)}


def get_uls_roof_1_25D_1_4Wy_keys():
    """
    Get the keys for the ULS roof 1.25D 1.4Wy combination calculation
    :return: A list containing the keys for the ULS roof 1.25D 1.4Wy combination calculation
    """
    return ['uls 1.25D', 'uls 1.4Wy (corner)', 'uls 1.4Wy (edge)', 'uls 1.4Wy (centre)', 'companion']


def uls_roof_0_9D_1_4Wx(building: Building, snow_load: SnowLoad):
    """
    ULS roof 0.9D 1.4Wx combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 0.9D 1.4Wx combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.4Wx (corner)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls,
            'uls 1.4Wx (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls,
            'uls 1.4Wx (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls,
            'companion': max(snow_load.s_uls * 0.5, 1)}


def get_uls_roof_0_9D_1_4Wx_keys():
    """
    Get the keys for the ULS roof 0.9D 1.4Wx combination calculation
    :return: A list containing the keys for the ULS roof 0.9D 1.4Wx combination calculation
    """
    return ['uls 0.9D', 'uls 1.4Wx (corner)', 'uls 1.4Wx (edge)', 'uls 1.4Wx (centre)', 'companion']


def uls_roof_1_0D_1_0Ey(building: Building, snow_load: SnowLoad):
    """
    ULS roof 1.0D 1.0Ey combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 1.0D 1.0Ey combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.0D': building.roof.wp,
            'uls 1.0Ey': top_height_zone.seismic_load.vp,
            'companion': snow_load.s_uls * 0.25 + 1}


def get_uls_roof_1_0D_1_0Ey_keys():
    """
    Get the keys for the ULS roof 1.0D 1.0Ey combination calculation
    :return: A list containing the keys for the ULS roof 1.0D 1.0Ey combination calculation
    """
    return ['uls 1.0D', 'uls 1.0Ey', 'companion']


def uls_roof_1_0D_1_0Ex(building: Building, snow_load: SnowLoad):
    """
    ULS roof 1.0D 1.0Ex combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 1.0D 1.0Ex combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.0D': building.roof.wp,
            'uls 1.0Ex': top_height_zone.seismic_load.vp,
            'companion': snow_load.s_uls * 0.25 + 1}


def get_uls_roof_1_0D_1_0Ex_keys():
    """
    Get the keys for the ULS roof 1.0D 1.0Ex combination calculation
    :return: A list containing the keys for the ULS roof 1.0D 1.0Ex combination calculation
    """
    return ['uls 1.0D', 'uls 1.0Ex', 'companion']


def uls_roof_1_25D_1_5S(building: Building, snow_load: SnowLoad):
    """
    ULS roof 1.25D 1.5S combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 1.25D 1.5S combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.5S': snow_load.s_uls * 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls * 0.4, 1),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls * 0.4, 1)}


def get_uls_roof_1_25D_1_5S_keys():
    """
    Get the keys for the ULS roof 1.25D 1.5S combination calculation
    :return: A list containing the keys for the ULS roof 1.25D 1.5S combination calculation
    """
    return ['uls 1.25D', 'uls 1.5S', 'companion (centre)', 'companion (edge)']


def uls_roof_0_9D_1_5S(building: Building, snow_load: SnowLoad):
    """
    ULS roof 0.9D 1.5S combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 0.9D 1.5S combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.5S': snow_load.s_uls * 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls * 0.4, 1),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls * 0.4, 1)}


def get_uls_roof_0_9D_1_5S_keys():
    """
    Get the keys for the ULS roof 0.9D 1.5S combination calculation
    :return: A list containing the keys for the ULS roof 0.9D 1.5S combination calculation
    """
    return ['uls 0.9D', 'uls 1.5S', 'companion', 'companion (centre)', 'companion (edge)']


def uls_roof_1_25D_1_5L(building: Building, snow_load: SnowLoad):
    """
    ULS roof 1.25D 1.5L combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 1.25D 1.5L combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.5L': 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls * 0.4,
                                      snow_load.s_uls),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls * 0.4,
                                    snow_load.s_uls)}


def get_uls_roof_1_25D_1_5L_keys():
    """
    Get the keys for the ULS roof 1.25D 1.5L combination calculation
    :return: A list containing the keys for the ULS roof 1.25D 1.5L combination calculation
    """
    return ['uls 1.25D', 'uls 1.5L', 'companion (centre)', 'companion (edge)']


def uls_roof_0_9D_1_5L(building: Building, snow_load: SnowLoad):
    """
    ULS roof 0.9D 1.5L combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed ULS roof 0.9D 1.5L combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.5L': 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls * 0.4,
                                      snow_load.s_uls),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls * 0.4,
                                    snow_load.s_uls)}


def get_uls_roof_0_9D_1_5L_keys():
    """
    Get the keys for the ULS roof 0.9D 1.5L combination calculation
    :return: A list containing the keys for the ULS roof 0.9D 1.5L combination calculation
    """
    return ['uls 0.9D', 'uls 1.5L', 'companion (centre)', 'companion (edge)']


########################################################################################################################
# SLS ROOF COMBINATION CALCULATIONS
########################################################################################################################


def sls_roof_1_0D_1_0Wy(building: Building, snow_load: SnowLoad):
    """
    SLS roof 1.0D 1.0Wy combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed SLS roof 1.0D 1.0Wy combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0Wy (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls,
            'sls 1.0Wy (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls * 0.3,
                                      snow_load.s_sls * 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls * 0.3,
                                    snow_load.s_sls * 0.35)}


def get_sls_roof_1_0D_1_0Wy_keys():
    """
    Get the keys for the SLS roof 1.0D 1.0Wy combination calculation
    :return: A list containing the keys for the SLS roof 1.0D 1.0Wy combination calculation
    """
    return ['sls 1.0D', 'sls 1.0Wy (centre)', 'sls 1.0Wy (edge)', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0Wx(building: Building, snow_load: SnowLoad):
    """
    SLS roof 1.0D 1.0Wx combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed SLS roof 1.0D 1.0Wx combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0Wx (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls,
            'sls 1.0Wx (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls * 0.3,
                                      snow_load.s_sls * 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls * 0.3,
                                    snow_load.s_sls * 0.35)}


def get_sls_roof_1_0D_1_0Wx_keys():
    """
    Get the keys for the SLS roof 1.0D 1.0Wx combination calculation
    :return: A list containing the keys for the SLS roof 1.0D 1.0Wx combination calculation
    """
    return ['sls 1.0D', 'sls 1.0Wx (centre)', 'sls 1.0Wx (edge)', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0S(building: Building, snow_load: SnowLoad):
    """
    SLS roof 1.0D 1.0S combination calculation
    :param building: The building associated with the height zone
    :param snow_load: The snow load associated with the building
    :return: A dictionary containing the computed SLS roof 1.0D 1.0S combination values
    """
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0S': snow_load.s_sls,
            'companion': max(snow_load.s_sls * 0.35, 0.35)}


def get_sls_roof_1_0D_1_0S_keys():
    """
    Get the keys for the SLS roof 1.0D 1.0S combination calculation
    :return: A list containing the keys for the SLS roof 1.0D 1.0S combination calculation
    """
    return ['sls 1.0D', 'sls 1.0S', 'companion']


def sls_roof_1_0D_1_0L_Wx(building: Building):
    """
    SLS roof 1.0D 1.0L Wx combination calculation
    :param building: The building associated with the height zone
    :return: A dictionary containing the computed SLS roof 1.0D 1.0L Wx combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0L': 1.0,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls * 0.3, 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls * 0.3, 0.35)}


def get_sls_roof_1_0D_1_0L_Wx_keys():
    """
    Get the keys for the SLS roof 1.0D 1.0L Wx combination calculation
    :return: A list containing the keys for the SLS roof 1.0D 1.0L Wx combination calculation
    """
    return ['sls 1.0D', 'sls 1.0L', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0L_Wy(building: Building):
    """
    SLS roof 1.0D 1.0L Wy combination calculation
    :param building: The building associated with the height zone
    :return: A dictionary containing the computed SLS roof 1.0D 1.0L Wy combination values
    """
    # The top height zone is the height zone with the highest zone number
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0L': 1.0,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls * 0.3, 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls * 0.3, 0.35)}


def get_sls_roof_1_0D_1_0L_Wy_keys():
    """
    Get the keys for the SLS roof 1.0D 1.0L Wy combination calculation
    :return: A list containing the keys for the SLS roof 1.0D 1.0L Wy combination calculation
    """
    return ['sls 1.0D', 'sls 1.0L', 'companion (centre)', 'companion (edge)']


########################################################################################################################
# WALL COMBINATION CALCULATIONS
########################################################################################################################


def generate_wall_load_entries(columns, dataframe, variables, uls_wall, sls_wall):
    """
    Generate wall load entries
    :param columns: The columns of the dataframe
    :param dataframe: The dataframe to add the entries to
    :param variables: The variables associated with the height zone
    :param uls_wall: The ULS wall load combination values
    :param sls_wall: The SLS wall load combination values
    :return: A dataframe containing the wall load entries
    """
    # Create a new entry
    entry = {x: 0.0 for x in columns}
    # Add the variables to the entry
    for key, value in variables.items():
        entry[key] = value
    # Add the ULS wall load combination values to the entry
    for key, value in uls_wall.items():
        entry[key] = value
    # Add the SLS wall load combination values to the entry
    for key, value in sls_wall.items():
        entry[key] = value
    # Add the entry to the dataframe
    dataframe.loc[len(dataframe)] = [entry[column] for column in dataframe.columns]


def compute_wall_load_combinations(building: Building, snow_load: SnowLoad,
                                   uls_wall_load_combination_type: ULSWallLoadCombinationTypes,
                                   sls_wall_load_combination_type: SLSWallLoadCombinationTypes):
    """
    Compute the wall load combinations
    :param building: The building to compute the wall load combinations for
    :param snow_load: THe snow load associated with the building
    :param uls_wall_load_combination_type: The ULS wall load combination type
    :param sls_wall_load_combination_type: The SLS wall load combination type
    :return: A dataframe containing the wall load combinations
    """
    # Determine the wall load combination type
    selection = (uls_wall_load_combination_type, sls_wall_load_combination_type)
    # Compute the appropriate combination based on the selection
    match selection:
        # ULS 1.4D and SLS 1.0D 1.0Wy
        case (ULSWallLoadCombinationTypes.ULS_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_4D_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_4D(building, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wx
        case (ULSWallLoadCombinationTypes.ULS_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_4D_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_4D(building, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0Wy
        case (ULSWallLoadCombinationTypes.ULS_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_wall_1_25D_1_4Wy_keys() +
                       get_sls_wall_1_0D_1_0Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_25D_1_4Wy(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0Wx
        case (ULSWallLoadCombinationTypes.ULS_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_wall_1_25D_1_4Wy_keys() +
                       get_sls_wall_1_0D_1_0Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_25D_1_4Wy(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0Wx
        case (ULSWallLoadCombinationTypes.ULS_0_9D_1_4WX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_0_9D_1_4Wx_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_0_9D_1_4Wx(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0Wx
        case (ULSWallLoadCombinationTypes.ULS_0_9D_1_4WX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_0_9D_1_4Wx_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_0_9D_1_4Wx(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0Wy
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ey_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ey(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.0D 1.0Ex and SLS 1.0D 1.0Wx
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ey_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ey(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0S
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ex_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ex(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0S
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ex_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Iterate through the height zones
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                # Generate the wall load entries
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ex(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            # Return the dataframe containing the wall load combinations
            return df


########################################################################################################################
# ROOF COMBINATION CALCULATIONS
########################################################################################################################

def generate_roof_load_entries(columns, dataframe, variables, uls_roof, sls_roof):
    """
    Generate roof load entries
    :param columns: The columns of the dataframe
    :param dataframe: The dataframe to add the entries to
    :param variables: The variables associated with the height zone
    :param uls_roof: The ULS roof load combination values
    :param sls_roof: The SLS roof load combination values
    :return:
    """
    # Create a new entry
    entry = {x: 0.0 for x in columns}
    # Add the variables to the entry
    for key, value in variables.items():
        entry[key] = value
    # Add the ULS roof load combination values to the entry
    for key, value in uls_roof.items():
        entry[key] = value
    # Add the SLS roof load combination values to the entry
    for key, value in sls_roof.items():
        entry[key] = value
    # Add the entry to the dataframe
    dataframe.loc[len(dataframe)] = [entry[column] for column in dataframe.columns]


def compute_roof_load_combinations(building: Building, snow_load: SnowLoad,
                                   uls_roof_load_combination_type: ULSRoofLoadCombinationTypes,
                                   sls_roof_load_combination_type: SLSRoofLoadCombinationTypes):
    """
    Compute the roof load combinations
    :param building: The building to compute the roof load combinations for
    :param snow_load: The snow load associated with the building
    :param uls_roof_load_combination_type: The ULS roof load combination type
    :param sls_roof_load_combination_type: The SLS roof load combination type
    :return: A dataframe containing the roof load combinations
    """
    # Determine the roof load combination type
    selection = (uls_roof_load_combination_type, sls_roof_load_combination_type)
    # Compute the appropriate combination based on the selection
    match selection:
        # ULS 1.4D and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_4Wy_keys() +
                       get_sls_roof_1_0D_1_0Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_4Wy_keys() +
                       get_sls_roof_1_0D_1_0Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_4Wy_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.4Wy and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_4Wy_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0S
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_4Wx_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.4Wx and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_4Wx_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0S
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_0D_1_0Ey_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0Ey and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_0D_1_0Ey_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0EX and SLS 1.0D 1.0WX
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0EX and SLS 1.0D 1.0WY
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0EX and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_0D_1_0Ex_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.0D 1.0EX and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_0D_1_0Ex_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0WY
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_5S_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5S and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_5S_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0WY
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0S
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_5S_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.4D and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_5S_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5L and SLS 1.0D 1.0WY
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5L and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5L and SLS 1.0D 1.0Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5L and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_5L_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 1.25D 1.5L and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_1_25D_1_5L_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.5L and SLS 1.0D 1.0WY
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.5L and SLS 1.0D 1.0Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.5L and SLS 1.0D 1.0S
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            # Get the columns for the dataframe
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0S_keys()
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.5L and SLS 1.0D 1.0L Wx
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_5L_keys() +
                       get_sls_roof_1_0D_1_0L_Wx_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            # Return the dataframe containing the roof load combinations
            return df
        # ULS 0.9D 1.5L and SLS 1.0D 1.0L Wy
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            # Get the columns for the dataframe
            columns = (get_height_zone_variables_keys() +
                       get_uls_roof_0_9D_1_5L_keys() +
                       get_sls_roof_1_0D_1_0L_Wy_keys())
            # Create a new dataframe
            df = pd.DataFrame(columns=columns)
            # Generate the roof load entries
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            # Return the dataframe containing the roof load combinations
            return df
