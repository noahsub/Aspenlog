import pandas as pd

from backend.Constants.roof_load_combination_constants import ULSRoofLoadCombinationTypes, SLSRoofLoadCombinationTypes
from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad


########################################################################################################################
# HEIGHT ZONE CALCULATIONS
########################################################################################################################


def compute_height_zone_width(building: Building, zone_number: int):
    if zone_number == 1:
        return building.get_height_zone(zone_number).elevation
    else:
        prev_elevation = building.get_height_zone(zone_number - 1).elevation
        curr_elevation = building.get_height_zone(zone_number).elevation
        assert curr_elevation > prev_elevation
        return curr_elevation - prev_elevation


def compute_height_zone_variables(building: Building, zone_number: int):
    return {'xn': compute_height_zone_width(building, zone_number),
            'hx': building.get_height_zone(zone_number).elevation,
            'ce': building.get_height_zone(zone_number).wind_load.factor.ce,
            'ax': building.get_height_zone(zone_number).seismic_load.ax}


def compute_top_height_zone_variables(building: Building):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'xn': compute_height_zone_variables(building, top_height_zone.zone_num),
            'hx': top_height_zone.elevation,
            'ce': top_height_zone.wind_load.factor.ce,
            'ax': top_height_zone.seismic_load.ax}


def get_height_zone_variables_keys():
    return ['xn', 'hx', 'ce', 'ax']


########################################################################################################################
# ULS WALL COMBINATION CALCULATIONS
########################################################################################################################

def uls_wall_1_4D(building: Building, zone_num: int):
    return {'uls 1.4D': 1.4 * building.get_height_zone(zone_num).wp}


def get_uls_wall_1_4D_keys():
    return ['uls 1.4D']


def uls_wall_1_25D_1_4Wy(building: Building, snow_load: SnowLoad, zone_num: int):
    return {'uls 1.25D': building.get_height_zone(zone_num).wp * 1.25,
            'uls 1.4Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.pos_uls,
            'uls 1.4Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.pos_uls,
            'companion': snow_load.s_uls * 0.5}


def get_uls_wall_1_25D_1_4Wy_keys():
    return ['uls 1.25D', 'uls 1.4Wy (centre)', 'uls 1.4Wy (edge)', 'companion']


def uls_wall_0_9D_1_4Wx(building: Building, snow_load: SnowLoad, zone_num: int):
    return {'uls 0.9D': building.get_height_zone(zone_num).wp * 0.9,
            'uls 1.4Wx (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.neg_uls,
            'uls 1.4Wx (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.neg_uls,
            'companion': snow_load.s_uls * 0.5}


def get_uls_wall_0_9D_1_4Wx_keys():
    return ['uls 0.9D', 'uls 1.4Wx (centre)', 'uls 1.4Wx (edge)', 'companion']


def uls_wall_1_0D_1_0Ey(building: Building, snow_load: SnowLoad, zone_num: int):
    return {'uls 1.0D': building.get_height_zone(zone_num).wp,
            'uls 1.0Ey': building.get_height_zone(zone_num).seismic_load.vp,
            'companion': snow_load.s_uls * 0.25}


def get_uls_wall_1_0D_1_0Ey_keys():
    return ['uls 1.0D', 'uls 1.0Ey', 'companion']


def uls_wall_1_0D_1_0Ex(building: Building, snow_load: SnowLoad, zone_num: int):
    return {'uls 1.0D': building.get_height_zone(zone_num).wp,
            'uls 1.0Ex': building.get_height_zone(zone_num).seismic_load.vp,
            'companion': snow_load.s_uls * 0.25}


def get_uls_wall_1_0D_1_0Ex_keys():
    return ['uls 1.0D', 'uls 1.0Ex', 'companion']


########################################################################################################################
# SLS WALL COMBINATION CALCULATIONS
########################################################################################################################

def sls_wall_1_0D_1_0Wy(building: Building, zone_num: int):
    return {'sls 1.0D': building.get_height_zone(zone_num).wp,
            'sls 1.0Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.pos_sls,
            'sls 1.0Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.pos_sls}


def get_sls_wall_1_0D_1_0Wy_keys():
    return ['sls 1.0D', 'sls 1.0Wy (centre)', 'sls 1.0Wy (edge)']


def sls_wall_1_0D_1_0Wx(building: Building, zone_num: int):
    return {'sls 1.0D': building.get_height_zone(zone_num).wp,
            'sls 1.0Wy (centre)': building.get_height_zone(zone_num).wind_load.get_zone('wall_centre').pressure.neg_sls,
            'sls 1.0Wy (edge)': building.get_height_zone(zone_num).wind_load.get_zone('wall_corner').pressure.neg_sls}


def get_sls_wall_1_0D_1_0Wx_keys():
    return ['sls 1.0D', 'sls 1.0Wx (centre)', 'sls 1.0Wx (edge)']


########################################################################################################################
# ULS ROOF COMBINATION CALCULATIONS
########################################################################################################################

def uls_roof_1_4D(building: Building):
    return {'uls 1.4D': building.roof.wp * 1.4}


def get_uls_roof_1_4D_keys():
    return ['uls 1.4D']


def uls_roof_1_25D_1_4Wy(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.4Wy (corner)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls,
            'uls 1.4Wy (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls,
            'uls 1.4Wy (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls,
            'companion': max(snow_load.s_uls * 0.5, 1)}


def get_uls_roof_1_25D_1_4Wy_keys():
    return ['uls 1.25D', 'uls 1.4Wy (corner)', 'uls 1.4Wy (edge)', 'uls 1.4Wy (centre)', 'companion']


def uls_roof_0_9D_1_4Wx(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.4Wx (corner)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls,
            'uls 1.4Wx (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls,
            'uls 1.4Wx (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls,
            'companion': max(snow_load.s_uls * 0.5, 1)}


def get_uls_roof_0_9D_1_4Wx_keys():
    return ['uls 0.9D', 'uls 1.4Wx (corner)', 'uls 1.4Wx (edge)', 'uls 1.4Wx (centre)', 'companion']


def uls_roof_1_0D_1_0Ey(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.0D': building.roof.wp,
            'uls 1.0Ey': top_height_zone.seismic_load.vp,
            'companion': snow_load.s_uls * 0.25 + 1}


def get_uls_roof_1_0D_1_0Ey_keys():
    return ['uls 1.0D', 'uls 1.0Ey', 'companion']


def uls_roof_1_0D_1_0Ex(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.0D': building.roof.wp,
            'uls 1.0Ex': top_height_zone.seismic_load.vp,
            'companion': snow_load.s_uls * 0.25 + 1}


def get_uls_roof_1_0D_1_0Ex_keys():
    return ['uls 1.0D', 'uls 1.0Ex', 'companion']


def uls_roof_1_25D_1_5S(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.5S': snow_load.s_uls * 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls * 0.4, 1),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls * 0.4, 1)}


def get_uls_roof_1_25D_1_5S_keys():
    return ['uls 1.25D', 'uls 1.5S', 'companion (centre)', 'companion (edge)']


def uls_roof_0_9D_1_5S(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.5S': snow_load.s_uls * 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls * 0.4, 1),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls * 0.4, 1)}


def get_uls_roof_0_9D_1_5S_keys():
    return ['uls 0.9D', 'uls 1.5S', 'companion', 'companion (centre)', 'companion (edge)']


def uls_roof_1_25D_1_5L(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 1.25D': building.roof.wp * 1.25,
            'uls 1.5L': 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_uls * 0.4,
                                      snow_load.s_uls),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_uls * 0.4,
                                    snow_load.s_uls)}


def get_uls_roof_1_25D_1_5L_keys():
    return ['uls 1.25D', 'uls 1.5L', 'companion (centre)', 'companion (edge)']


def uls_roof_0_9D_1_5L(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'uls 0.9D': building.roof.wp * 0.9,
            'uls 1.5L': 1.5,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_uls * 0.4,
                                      snow_load.s_uls),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_uls * 0.4,
                                    snow_load.s_uls)}


def get_uls_roof_0_9D_1_5L_keys():
    return ['uls 0.9D', 'uls 1.5L', 'companion (centre)', 'companion (edge)']


########################################################################################################################
# SLS ROOF COMBINATION CALCULATIONS
########################################################################################################################


def sls_roof_1_0D_1_0Wy(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0Wy (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls,
            'sls 1.0Wy (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls * 0.3,
                                      snow_load.s_sls * 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls * 0.3,
                                    snow_load.s_sls * 0.35)}


def get_sls_roof_1_0D_1_0Wy_keys():
    return ['sls 1.0D', 'sls 1.0Wy (centre)', 'sls 1.0Wy (edge)', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0Wx(building: Building, snow_load: SnowLoad):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0Wx (centre)': top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls,
            'sls 1.0Wx (edge)': top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls * 0.3,
                                      snow_load.s_sls * 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls * 0.3,
                                    snow_load.s_sls * 0.35)}


def get_sls_roof_1_0D_1_0Wx_keys():
    return ['sls 1.0D', 'sls 1.0Wx (centre)', 'sls 1.0Wx (edge)', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0S(building: Building, snow_load: SnowLoad):
    # top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0S': snow_load.s_sls,
            'companion': max(snow_load.s_sls * 0.35, 0.35)}


def get_sls_roof_1_0D_1_0S_keys():
    return ['sls 1.0D', 'sls 1.0S', 'companion']


def sls_roof_1_0D_1_0L_Wx(building: Building):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0L': 1.0,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.neg_sls * 0.3, 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.neg_sls * 0.3, 0.35)}


def get_sls_roof_1_0D_1_0L_Wx_keys():
    return ['sls 1.0D', 'sls 1.0L', 'companion (centre)', 'companion (edge)']


def sls_roof_1_0D_1_0L_Wy(building: Building):
    top_height_zone = sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True)[0]
    return {'sls 1.0D': building.roof.wp,
            'sls 1.0L': 1.0,
            'companion (centre)': max(top_height_zone.wind_load.get_zone('roof_interior').pressure.pos_sls * 0.3, 0.35),
            'companion (edge)': max(top_height_zone.wind_load.get_zone('roof_corner').pressure.pos_sls * 0.3, 0.35)}


def get_sls_roof_1_0D_1_0L_Wy_keys():
    return ['sls 1.0D', 'sls 1.0L', 'companion (centre)', 'companion (edge)']


########################################################################################################################
# WALL COMBINATION CALCULATIONS
########################################################################################################################


def generate_wall_load_entries(columns, dataframe, variables, uls_wall, sls_wall):
    entry = {x: 0.0 for x in columns}
    for key, value in variables.items():
        entry[key] = value
    for key, value in uls_wall.items():
        entry[key] = value
    for key, value in sls_wall.items():
        entry[key] = value
    dataframe.loc[len(dataframe)] = [entry[column] for column in dataframe.columns]


def compute_wall_load_combinations(building: Building, snow_load: SnowLoad,
                                   uls_wall_load_combination_type: ULSWallLoadCombinationTypes,
                                   sls_wall_load_combination_type: SLSWallLoadCombinationTypes):
    selection = (uls_wall_load_combination_type, sls_wall_load_combination_type)
    match selection:
        case (ULSWallLoadCombinationTypes.ULS_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_4D_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_4D(building, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_4D_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_4D(building, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_25D_1_4Wy_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_25D_1_4Wy(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_25D_1_4Wy_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_25D_1_4Wy(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_0_9D_1_4WX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_wall_0_9D_1_4Wx_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_0_9D_1_4Wx(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_0_9D_1_4WX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_wall_0_9D_1_4Wx_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_0_9D_1_4Wx(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ey_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ey(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ey_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ey(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ex_keys() + get_sls_wall_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ex(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wy(building, height_zone.zone_num))
            return df
        case (ULSWallLoadCombinationTypes.ULS_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_wall_1_0D_1_0Ex_keys() + get_sls_wall_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num, reverse=True):
                generate_wall_load_entries(columns=columns,
                                           dataframe=df,
                                           variables=compute_height_zone_variables(building, height_zone.zone_num),
                                           uls_wall=uls_wall_1_0D_1_0Ex(building, snow_load, height_zone.zone_num),
                                           sls_wall=sls_wall_1_0D_1_0Wx(building, height_zone.zone_num))
            return df


########################################################################################################################
# ROOF COMBINATION CALCULATIONS
########################################################################################################################

def generate_roof_load_entries(columns, dataframe, variables, uls_roof, sls_roof):
    entry = {x: 0.0 for x in columns}
    for key, value in variables.items():
        entry[key] = value
    for key, value in uls_roof.items():
        entry[key] = value
    for key, value in sls_roof.items():
        entry[key] = value
    dataframe.loc[len(dataframe)] = [entry[column] for column in dataframe.columns]


def compute_roof_load_combinations(building: Building, snow_load: SnowLoad,
                                   uls_roof_load_combination_type: ULSRoofLoadCombinationTypes,
                                   sls_roof_load_combination_type: SLSRoofLoadCombinationTypes):
    selection = (uls_roof_load_combination_type, sls_roof_load_combination_type)
    match selection:
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_4_D, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_4D_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_4D(building),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_4WY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_4Wy_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_4Wy(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_4WX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_4Wx_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_4Wx(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EY, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ey_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ey(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_0D_1_0EX, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_0D_1_0Ex_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_0D_1_0Ex(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5S_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5S, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5S_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5S(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_1_25D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_1_25D_1_5L_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_1_25D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wy(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0Wx(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0S):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0S_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0S(building, snow_load))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WX):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0L_Wx_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wx(building))
            return df
        case (ULSRoofLoadCombinationTypes.ULS_0_9D_1_5L, SLSRoofLoadCombinationTypes.SLS_1_0D_1_0L_WY):
            columns = get_height_zone_variables_keys() + get_uls_roof_0_9D_1_5L_keys() + get_sls_roof_1_0D_1_0L_Wy_keys()
            df = pd.DataFrame(columns=columns)
            generate_roof_load_entries(columns=columns,
                                       dataframe=df,
                                       variables=compute_top_height_zone_variables(building),
                                       uls_roof=uls_roof_0_9D_1_5L(building, snow_load),
                                       sls_roof=sls_roof_1_0D_1_0L_Wy(building))
            return df
