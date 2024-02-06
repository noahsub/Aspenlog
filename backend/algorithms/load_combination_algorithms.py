import numpy as np
import pandas as pd

from backend.Constants.roof_load_combination_constants import ULSRoofLoadCombinationTypes, SLSRoofLoadCombinationTypes
from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad


def compute_xn(building: Building, height_zone_num):
    sorted_height_zones = sorted(building.zones.keys(), key=lambda x: x.zone_num)
    if height_zone_num == 1:
        return sorted_height_zones[0].elevation
    else:
        prev_elevation = sorted_height_zones[height_zone_num - 2].elevation
        curr_elevation = sorted_height_zones[height_zone_num - 1].elevation
        return curr_elevation - prev_elevation


def compute_wall_load_combinations(building: Building, uls_wall_load_combination_type: ULSWallLoadCombinationTypes=None, sls_wall_load_combination_type: SLSWallLoadCombinationTypes=None):
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
            return df
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
            return df
        case (ULSWallLoadCombinationTypes.ULS_FULL_WIND_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.25D', 'ULS 1.4Wy', 'ULS 1.4Wy C', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_25D = building.wp * 1.25
                uls_1_4Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_uls
                uls_1_4Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_uls
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.25D': uls_1_25D, 'ULS 1.4Wy': uls_1_4Wy, 'ULS 1.4Wy C': uls_1_4Wy_C, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]
            return df
        case (ULSWallLoadCombinationTypes.ULS_SEISMIC_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.0D', 'ULS 1.0Ey', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_0D = building.wp
                uls_1_0Ey = height_zone.seismic_load.vp
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.0D': uls_1_0D, 'ULS 1.0Ey': uls_1_0Ey, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]
            return df
        case (ULSWallLoadCombinationTypes.ULS_SEISMIC_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY):
            df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.0D', 'ULS 1.0Ex', 'SLS 1.0D', 'SLS 1.0Wy', 'SLS 1.0Wy C'])
            for height_zone in sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True):
                xn = compute_xn(building, height_zone.zone_num)
                hx = height_zone.elevation
                ce = height_zone.wind_load.factor.ce
                ax = height_zone.seismic_load.ax
                uls_1_0D = building.wp
                uls_1_0Ex = height_zone.seismic_load.vp
                sls_1_0D = building.wp
                sls_1_0Wy = height_zone.wind_load.get_zone('wall_centre').pressure.pos_sls
                sls_1_0Wy_C = height_zone.wind_load.get_zone('wall_corner').pressure.pos_sls
                entry = {'height_zone': height_zone.zone_num, 'top_of_zone': height_zone.elevation, 'xn': xn, 'hx': hx, 'ce': ce, 'ax': ax, 'ULS 1.0D': uls_1_0D, 'ULS 1.0Ex': uls_1_0Ex, 'SLS 1.0D': sls_1_0D, 'SLS 1.0Wy': sls_1_0Wy, 'SLS 1.0Wy C': sls_1_0Wy_C}
                df.loc[len(df)] = [entry[column] for column in df.columns]
            return df

    def compute_roof_load_combinations(building: Building, snow_load: SnowLoad, uls_roof_load_combination_type: ULSRoofLoadCombinationTypes=None, sls_roof_load_combination_type: SLSRoofLoadCombinationTypes=None):
        selection = (uls_roof_load_combination_type, sls_roof_load_combination_type)
        match selection:
            case(ULSRoofLoadCombinationTypes.ULS_DEAD_ONLY_1_4_D, SLSRoofLoadCombinationTypes.SLS_DEAD_AND_WIND_Y_NORMAL_TO_FACE_1_0D_1_0WY):
                df = pd.DataFrame(columns=['height_zone', 'top_of_zone', 'xn', 'hx', 'ce', 'ax', 'ULS 1.0Wy Center', 'ULS 1.0Wy Edge', 'ULS 1.0Wy Corner', 'SLS 1.0Wy Center', 'SLS 1.0Wy Edge', 'SLS 1.0Wy Corner'])
                top_height_zone = sorted(building.zones.keys(), key=lambda x: x.zone_num, reverse=True)[0]
                xn = compute_xn(building, top_height_zone.zone_num)
                hx = top_height_zone.elevation
                ce = top_height_zone.wind_load.factor.ce
                ax = top_height_zone.seismic_load.ax
                uls_1_0Wy_center = 1.4 * building.roof.wp

