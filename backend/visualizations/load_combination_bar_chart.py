import pprint

import numpy as np

from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes, SLSWallLoadCombinationTypes
from backend.Entities.Building.building import Building
from backend.Entities.Snow.snow_load import SnowLoad
from backend.algorithms.load_combination_algorithms import compute_wall_load_combinations
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from config import get_file_path


def generate_bar_chart(id: str, building: Building, snow_load: SnowLoad):
    count = 0
    for height_zone in sorted(building.height_zones, key=lambda x: x.zone_num):
        x_labels = ['Full Wind Y', 'Seismic X', 'Seismic Y', 'Dead Load']
        y_labels = ['Wy', 'Ex', 'Ey', 'D']

        pairs = {(a, b): 0 for a in x_labels for b in y_labels}

        dead_load_data = compute_wall_load_combinations(building, snow_load, ULSWallLoadCombinationTypes.ULS_1_4_D, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY)
        pairs[('Dead Load', 'D')] = dead_load_data.loc[height_zone.zone_num - 1, 'uls 1.4D']

        full_wind_y_data = compute_wall_load_combinations(building, snow_load, ULSWallLoadCombinationTypes.ULS_1_25D_1_4WY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY)
        pairs[('Full Wind Y', 'D')] = full_wind_y_data.loc[height_zone.zone_num - 1, 'uls 1.25D']
        pairs[('Full Wind Y', 'Wy')] = full_wind_y_data.loc[height_zone.zone_num - 1, 'uls 1.4Wy (centre)']

        seismic_y_data = compute_wall_load_combinations(building, snow_load, ULSWallLoadCombinationTypes.ULS_1_0D_1_0EY, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY)
        pairs[('Seismic Y', 'D')] = seismic_y_data.loc[height_zone.zone_num - 1, 'uls 1.0D']
        pairs[('Seismic Y', 'Ey')] = seismic_y_data.loc[height_zone.zone_num - 1, 'uls 1.0Ey']

        seismic_x_data = compute_wall_load_combinations(building, snow_load, ULSWallLoadCombinationTypes.ULS_1_0D_1_0EX, SLSWallLoadCombinationTypes.SLS_1_0D_1_0WY)
        pairs[('Seismic X', 'D')] = seismic_x_data.loc[height_zone.zone_num - 1, 'uls 1.0D']
        pairs[('Seismic X', 'Ex')] = seismic_x_data.loc[height_zone.zone_num - 1, 'uls 1.0Ex']

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        _x = np.arange(len(x_labels))
        _y = np.arange(len(y_labels))

        for i in _x:
            for j in _y:
                value = pairs[(x_labels[i], y_labels[j])]
                ax.bar3d(i, j, 0, 0.5, 0.5, value, shade=True, color='#9bca6d')

        ax.set_xticks(_x)
        ax.set_yticks(_y)
        ax.set_xticklabels(x_labels)
        ax.set_yticklabels(y_labels)
        ax.set_xlabel('Load Combination Type')
        ax.set_ylabel('Load Type')
        ax.set_zlabel('Magnitude')

        # Adding title
        # plt.title(f'Load Combinations of Height Zone {height_zone.zone_num} (kPa)')
        plt.title(f'Height Zone {height_zone.zone_num} - Wall Centre Zone (kPa)')

        # Setting background color
        ax.set_facecolor('#f7f4ef')

        path = get_file_path(f'backend/output/bar_chart_hz_{height_zone.zone_num}_{id}.png')
        plt.savefig(path, dpi=300, transparent=True)
        count += 1
    return count





