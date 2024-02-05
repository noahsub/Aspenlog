import numpy as np
import pandas as pd

from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad


def compute_xn(building: Building, height_zone_num):
    sorted_height_zones = sorted(building.zones.keys(), key=lambda x: x.zone_num)
    if height_zone_num == 1:
        return sorted_height_zones[0].elevation
    else:
        prev_elevation = sorted_height_zones[height_zone_num - 1].elevation
        curr_elevation = sorted_height_zones[height_zone_num - 1].elevation
        return curr_elevation - prev_elevation

def compute_load_combinations(building: Building, snow_load: SnowLoad, uls_wall_load_combination_type: ULSWallLoadCombinationTypes=None, sls_wall_load_combination_type: SLSWallLoadCombinationTypes=None):
    selection = (uls_wall_load_combination_type, sls_wall_load_combination_type)
    match selection:
        case (None, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax}
                df.loc[len(df)] = [entry[column] for column in df.columns]
        case (ULSWallLoadCombinationTypes.ULS_DEAD_ONLY_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.4D', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_4D = building.wp * 1.4
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.4D': uls_1_4D, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]
        case (ULSWallLoadCombinationTypes.ULS_FULL_WIND_1_25D_1_4WY_0_5S, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.25D', 'ULS 1.4Wy', 'ULS 1.4Wy C', 'ULS 0.5S', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_25D = building.wp * 1.25
                uls_1_4Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_uls * 1.4
                uls_1_4Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_uls * 1.4
                uls_0_5S = 0.5 * snow_load.s_uls
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.25D': uls_1_25D, 'ULS 1.4Wy': uls_1_4Wy, 'ULS 1.4Wy C': uls_1_4Wy_C, 'ULS 0.5S': uls_0_5S, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]
        case (ULSWallLoadCombinationTypes.ULS_FULL_SNOW_1_25D_1_5S_0_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.25D', 'ULS 1.5S', 'ULS 0.4Wy', 'ULS 0.4Wy C', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_25D = building.wp * 1.25
                uls_1_5S = 1.5 * snow_load.s_uls
                uls_0_4Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_uls * 0.4
                uls_0_4Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_uls * 0.4
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.25D': uls_1_25D, 'ULS 1.5S': uls_1_5S, 'ULS 0.4Wy': uls_0_4Wy, 'ULS 0.4Wy C': uls_0_4Wy_C, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]

