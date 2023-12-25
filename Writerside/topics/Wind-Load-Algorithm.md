# Wind Load Algorithm

## Overview
This document describes the functions for calculating wind loads in a building structure. The calculations consider factors like wind exposure, internal pressure, and specific building characteristics.

## get_wind_topographic_factor
**Implementation**: Assigns the provided `ct` value to `wind_load.factor.ct`.

- **Purpose**: Sets the topographic factor for wind load.
- **Parameters**: `wind_load`, `ct` (default = 1)

## get_wind_exposure_factor
**Implementation**: Determines `ce` and `cei` based on building height, openings, and `WindExposureFactorSelections`.

- **Purpose**: Calculates the wind exposure factor.
- **Parameters**: `wind_load`, `selection`, `building`, `manual`

## get_internal_pressure
**Implementation**: Uses `lw`, `q`, and other factors to calculate positive and negative internal pressure based on `InternalPressureSelections`.

- **Purpose**: Computes the internal pressure of a building.
- **Parameters**: `wind_load`, `selection`, `lw`, `q`

## get_external_pressure
**Implementation**: Determines the external pressure on various building zones (roof, walls) using a match case structure and assigns them to respective zones in `wind_load`.

- **Purpose**: Calculates the external pressure on different zones of a building.
- **Parameters**: `wind_load`, `lw`, `q`

