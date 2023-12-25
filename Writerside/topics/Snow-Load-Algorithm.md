# Snow Load Algorithm

This document outlines the algorithms used for calculating snow loads in the software. The algorithms consider various factors like roof type, slope, wind exposure, and more.

## get_slope_factor
**Implementation**: This function uses a match case structure to determine the slope factor (`cs`) based on the roof type (`RoofType`) and building's roof slope. It adjusts the snow load factor differently for unobstructed slippery roofs and other roof types.
- **Purpose**: Calculates the slope factor for snow load based on the roof type and slope.
- **Parameters**: `snow_load`, `selection` (roof type), `building`
- **Algorithm**:
    - Different calculations based on `RoofType`.
    - Adjusts `snow_load.factor.cs` based on roof slope.

## get_accumulation_factor
**Implementation**: A straightforward function that sets the accumulation factor (`ca`) for the snow load to a constant value, reflecting a standard accumulation condition.
- **Purpose**: Determines the accumulation factor for snow load.
- **Algorithm**:
    - Sets `snow_load.factor.ca` to a constant value.

## get_wind_exposure_factor
**Implementation**: It evaluates the wind exposure factor (`cw`) based on the importance of wind load (`WindImportanceFactor`) and the wind exposure factor selection. The function adjusts `cw` using predefined conditions and selections.

- **Purpose**: Calculates the wind exposure factor for snow load.
- **Parameters**: `snow_load`, `importance_selection`, `wind_exposure_factor_selection`
- **Algorithm**:
    - Adjusts `snow_load.factor.cw` based on wind importance factor and exposure.

## get_basic_roof_now_load_factor
**Implementation**: This function calculates the basic roof snow load factor (`cb`) using the roof dimensions and a mathematical formula. It incorporates an exponential function to determine `cb` based on the building's roof width and length, and the wind exposure factor.

- **Purpose**: Computes the basic roof snow load factor.
- **Parameters**: `snow_load`, `building`
- **Algorithm**:
    - Uses building dimensions to adjust `snow_load.factor.cb`.

## get_snow_load
**Implementation**: This is the primary function for calculating the total snow load (`s`). It combines local snow load (`ls`), snow density (`ss`), roof snow load (`sr`), and manual adjustments if provided. The total snow load is calculated by multiplying these factors with the previously calculated snow load factors.

- **Purpose**: Final calculation of snow load.
- **Parameters**: `snow_load`, `ls`, `ss`, `sr`, `manual`
- **Algorithm**:
    - Combines all factors to compute the total snow load.
