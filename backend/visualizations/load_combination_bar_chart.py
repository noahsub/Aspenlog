from backend.Constants.wall_load_combination_constants import ULSWallLoadCombinationTypes


def get_axes():
    x = []
    y = []
    for combination in ULSWallLoadCombinationTypes:
        parts = combination.value.split('_')
        count = combination.value.count('_')
        if count == 1:
            x.append(parts[1])
            y.append('-')
        elif count == 2:
            x.append(parts[1])
            y.append(parts[2])
    return {'x': x, 'y': y}



if __name__ == '__main__':
    # cross x and y and fill with random data using numpy


