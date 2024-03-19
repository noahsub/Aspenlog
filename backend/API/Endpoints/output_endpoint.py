########################################################################################################################
# output_endpoint.py
# This file contains the endpoints used for creating an Excel output for a user. It includes the following endpoints:
#   - /excel_output: POST request to create an Excel output for a user
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################


########################################################################################################################
# IMPORTS
########################################################################################################################

import uuid

import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import FileResponse

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import (
    check_user_exists,
    get_user_location,
    get_user_dimensions,
    get_user_cladding,
    get_user_roof,
    get_user_importance_category,
    get_user_building,
    get_user_snow_load,
)
from backend.Constants.roof_load_combination_constants import (
    ULSRoofLoadCombinationTypes,
    SLSRoofLoadCombinationTypes,
)
from backend.Constants.wall_load_combination_constants import (
    ULSWallLoadCombinationTypes,
    SLSWallLoadCombinationTypes,
)
from backend.algorithms.load_combination_algorithms import (
    compute_wall_load_combinations,
    compute_roof_load_combinations,
)
from config import get_file_path

########################################################################################################################
# ROUTER
########################################################################################################################

output_router = APIRouter()


########################################################################################################################
# ENDPOINTS
########################################################################################################################


@output_router.post("/excel_output")
def excel_output_endpoint(username: str = Depends(decode_token)):
    """
    Creates an Excel output for a user using all the data stored in the user's memory slot
    :param username: The username of the user
    :return: A file response containing the Excel output
    """
    try:
        # If storage for the user does not exist in memory, create a slot for the user
        check_user_exists(username)
        # Create a unique identifier for the file
        id = str(uuid.uuid4())
        # Get the location data of the user
        location = get_user_location(username)
        location_headers = [
            "Address",
            "Latitude",
            "Longitude",
            "Site Designation",
            "Xv",
            "Xs",
            "Wind Velocity Pressure",
            "Snow Load",
            "Rain Load",
            "Design Spectral Acceleration 0.2s",
            "Design Spectral Acceleration 1.0s",
        ]
        location_data = [
            [
                location.address,
                location.latitude,
                location.longitude,
                location.site_designation,
                location.xv,
                location.xs,
                location.wind_velocity_pressure,
                location.snow_load,
                location.rain_load,
                location.design_spectral_acceleration_0_2,
                location.design_spectral_acceleration_1,
            ]
        ]
        location_df = pd.DataFrame(location_data, columns=location_headers)

        # Get the dimensions data of the user
        dimensions = get_user_dimensions(username)
        dimension_headers = ["Height", "Height Eave", "Height Ridge", "Width"]
        dimension_data = [
            [
                dimensions.height,
                dimensions.height_eave,
                dimensions.height_ridge,
                dimensions.width,
            ]
        ]
        dimension_df = pd.DataFrame(dimension_data, columns=dimension_headers)

        # Get the cladding data of the user
        cladding = get_user_cladding(username)
        cladding_headers = ["Top of Cladding", "Bottom of Cladding"]
        cladding_data = [[cladding.c_top, cladding.c_bot]]
        cladding_df = pd.DataFrame(cladding_data, columns=cladding_headers)

        # Get the roof data of the user
        roof = get_user_roof(username)
        roof_headers = [
            "Smaller Plan Dimension",
            "Larger Plan Dimension",
            "Slope",
            "Wall Slope",
            "Uniform Dead Load",
        ]
        roof_data = [[roof.w_roof, roof.l_roof, roof.slope, roof.wall_slope, roof.wp]]
        roof_df = pd.DataFrame(roof_data, columns=roof_headers)

        # Get the building data of the user
        building = get_user_building(username)
        building_headers = ["Number of Floors", "Mid Height"]
        building_data = [[building.num_floor, building.h_opening]]
        building_df = pd.DataFrame(building_data, columns=building_headers)

        # Get the importance category data of the user
        importance_category = get_user_importance_category(username)
        importance_category_headers = ["Importance Category"]
        importance_category_data = [[importance_category]]
        importance_category_df = pd.DataFrame(
            importance_category_data, columns=importance_category_headers
        )

        # Get the height zone data of the user
        building = get_user_building(username)
        height_zones = building.height_zones
        height_zone_elevation_headers = ["Height Zone", "Elevation"]
        height_zone_elevation_data = [
            [height_zone.zone_num, height_zone.elevation]
            for height_zone in sorted(height_zones, key=lambda x: x.zone_num)
        ]
        height_zone_elevation_df = pd.DataFrame(
            height_zone_elevation_data, columns=height_zone_elevation_headers
        )

        height_zone_material_headers = ["Height Zone", "Material Load"]
        height_zone_material_data = [
            [height_zone.zone_num, height_zone.wp]
            for height_zone in sorted(height_zones, key=lambda x: x.zone_num)
        ]
        height_zone_material_df = pd.DataFrame(
            height_zone_material_data, columns=height_zone_material_headers
        )

        # Get the wind factor and pressure data of the user
        height_zone_wind_factor_dataframes = []
        height_zone_wind_pressure_dataframes = []
        for height_zone in sorted(height_zones, key=lambda x: x.zone_num):
            wind_factor_headers = ["Height Zone", "ct", "ce", "cei", "cg"]
            wind_factor_data = [
                [
                    height_zone.zone_num,
                    height_zone.wind_load.factor.ct,
                    height_zone.wind_load.factor.ce,
                    height_zone.wind_load.factor.cei,
                    height_zone.wind_load.factor.cg,
                ]
            ]
            wind_factor_df = pd.DataFrame(wind_factor_data, columns=wind_factor_headers)
            height_zone_wind_factor_dataframes.append(wind_factor_df)

            wind_pressure_headers = [
                "Height Zone",
                "Zone",
                "Zone Name",
                "pi pos uls",
                "pi neg uls",
                "pe pos uls",
                "pe neg uls",
                "pos uls",
                "neg uls",
                "pi pos sls",
                "pi neg sls",
                "pe pos sls",
                "pe neg sls",
                "pos sls",
                "neg sls",
            ]
            wind_pressure_data = []
            for i in range(1, 6):
                wind_pressure_data_row = [
                    height_zone.zone_num,
                    i,
                    height_zone.wind_load.get_zone(i).name,
                    height_zone.wind_load.get_zone(i).pressure.pi_pos_uls,
                    height_zone.wind_load.get_zone(i).pressure.pi_neg_uls,
                    height_zone.wind_load.get_zone(i).pressure.pe_pos_uls,
                    height_zone.wind_load.get_zone(i).pressure.pe_neg_uls,
                    height_zone.wind_load.get_zone(i).pressure.pos_uls,
                    height_zone.wind_load.get_zone(i).pressure.neg_uls,
                    height_zone.wind_load.get_zone(i).pressure.pi_pos_sls,
                    height_zone.wind_load.get_zone(i).pressure.pi_neg_sls,
                    height_zone.wind_load.get_zone(i).pressure.pe_pos_sls,
                    height_zone.wind_load.get_zone(i).pressure.pe_neg_sls,
                    height_zone.wind_load.get_zone(i).pressure.pos_sls,
                    height_zone.wind_load.get_zone(i).pressure.neg_sls,
                ]
                wind_pressure_data.append(wind_pressure_data_row)
            wind_pressure_df = pd.DataFrame(
                wind_pressure_data, columns=wind_pressure_headers
            )
            height_zone_wind_pressure_dataframes.append(wind_pressure_df)

        # Get the seismic data of the user
        height_zone_seismic_dataframes = []
        for height_zone in sorted(height_zones, key=lambda x: x.zone_num):
            height_zone_seismic_headers = [
                "Height Zone",
                "ar",
                "rp",
                "cp",
                "ax",
                "sp",
                "vp",
                "vp_snow",
            ]
            height_zone_seismic_data = [
                [
                    height_zone.zone_num,
                    height_zone.seismic_load.factor.ar,
                    height_zone.seismic_load.factor.rp,
                    height_zone.seismic_load.factor.cp,
                    height_zone.seismic_load.ax,
                    height_zone.seismic_load.sp,
                    height_zone.seismic_load.vp,
                    height_zone.seismic_load.vp_snow,
                ]
            ]
            height_zone_seismic_df = pd.DataFrame(
                height_zone_seismic_data, columns=height_zone_seismic_headers
            )
            height_zone_seismic_dataframes.append(height_zone_seismic_df)

        # Get the snow load data of the user
        upwind_snow_load = get_user_snow_load(username)["upwind"]
        downwind_snow_load = get_user_snow_load(username)["downwind"]

        upwind_snow_load_headers = ["slope", "cs", "ca", "cw", "cb", "s_uls"]
        upwind_snow_load_data = [
            [
                "upwind",
                upwind_snow_load.factor.cs,
                upwind_snow_load.factor.ca,
                upwind_snow_load.factor.cw,
                upwind_snow_load.factor.cb,
                upwind_snow_load.s_uls,
            ]
        ]
        upwind_snow_load_df = pd.DataFrame(
            upwind_snow_load_data, columns=upwind_snow_load_headers
        )

        downwind_snow_load_headers = ["slope", "cs", "ca", "cw", "cb", "s_uls"]
        downwind_snow_load_data = [
            [
                "downwind",
                downwind_snow_load.factor.cs,
                downwind_snow_load.factor.ca,
                downwind_snow_load.factor.cw,
                downwind_snow_load.factor.cb,
                downwind_snow_load.s_uls,
            ]
        ]
        downwind_snow_load_df = pd.DataFrame(
            downwind_snow_load_data, columns=downwind_snow_load_headers
        )

        # Get the wall and roof load combination data of the user
        wall_load_combination_dataframes = {}
        for uls_wall in ULSWallLoadCombinationTypes:
            for sls_wall in SLSWallLoadCombinationTypes:
                wall_load_combination_dataframes[uls_wall, sls_wall] = (
                    compute_wall_load_combinations(
                        building=building,
                        snow_load=upwind_snow_load,
                        uls_wall_load_combination_type=uls_wall,
                        sls_wall_load_combination_type=sls_wall,
                    )
                )

        roof_load_combination_upwind_dataframes = {}
        roof_load_combination_downwind_dataframes = {}
        for uls_roof in ULSRoofLoadCombinationTypes:
            for sls_roof in SLSRoofLoadCombinationTypes:
                roof_load_combination_upwind_dataframes[uls_roof, sls_roof] = (
                    compute_roof_load_combinations(
                        building=building,
                        snow_load=upwind_snow_load,
                        uls_roof_load_combination_type=uls_roof,
                        sls_roof_load_combination_type=sls_roof,
                    )
                )
                roof_load_combination_downwind_dataframes[uls_roof, sls_roof] = (
                    compute_roof_load_combinations(
                        building=building,
                        snow_load=downwind_snow_load,
                        uls_roof_load_combination_type=uls_roof,
                        sls_roof_load_combination_type=sls_roof,
                    )
                )

        # Create an Excel file with all the data
        output_path = get_file_path(f"backend/output/aspenlog2022_report_{id}.xlsx")
        # Write each dataframe to a separate sheet in the Excel file
        with pd.ExcelWriter(output_path) as writer:
            location_df.to_excel(writer, sheet_name="Location")
            dimension_df.to_excel(writer, sheet_name="Dimensions")
            cladding_df.to_excel(writer, sheet_name="Cladding")
            roof_df.to_excel(writer, sheet_name="Roof")
            building_df.to_excel(writer, sheet_name="Building")
            importance_category_df.to_excel(writer, sheet_name="Importance Category")
            height_zone_elevation_df.to_excel(
                writer, sheet_name="Height Zone Elevation"
            )
            height_zone_material_df.to_excel(writer, sheet_name="Height Zone Material")
            for i, df in enumerate(height_zone_wind_factor_dataframes):
                df.to_excel(writer, sheet_name=f"Height Zone {i + 1} Wind Factor")
            for i, df in enumerate(height_zone_wind_pressure_dataframes):
                df.to_excel(writer, sheet_name=f"Height Zone {i + 1} Wind Pressure")
            for i, df in enumerate(height_zone_seismic_dataframes):
                df.to_excel(writer, sheet_name=f"Height Zone {i + 1} Seismic")
            upwind_snow_load_df.to_excel(writer, sheet_name="Upwind Snow Load")
            downwind_snow_load_df.to_excel(writer, sheet_name="Downwind Snow Load")

            # Write all wall combinations into a single sheet
            start_row = 0
            for (uls_wall, sls_wall), df in wall_load_combination_dataframes.items():
                title_df = pd.DataFrame({f"{uls_wall.value} {sls_wall.value}": []})
                title_df.to_excel(
                    writer, sheet_name="Wall Load Combinations", startrow=start_row
                )
                df.to_excel(
                    writer,
                    sheet_name="Wall Load Combinations",
                    startrow=start_row + 1,
                    index=False,
                )
                start_row += (
                    len(df.index) + 3
                )  # update start_row for the next dataframe

            # Write all roof combinations into a single sheet
            # reset start_row for the new sheet
            start_row = 0
            for (
                uls_roof,
                sls_roof,
            ), df in roof_load_combination_upwind_dataframes.items():
                title_df = pd.DataFrame(
                    {f"Upwind {uls_roof.value} {sls_roof.value}": []}
                )
                title_df.to_excel(
                    writer, sheet_name="Roof Load Combinations", startrow=start_row
                )
                df.to_excel(
                    writer,
                    sheet_name="Roof Load Combinations",
                    startrow=start_row + 1,
                    index=False,
                )
                # update start_row for the next dataframe
                start_row += len(df.index) + 3

            for (
                uls_roof,
                sls_roof,
            ), df in roof_load_combination_downwind_dataframes.items():
                title_df = pd.DataFrame(
                    {f"Downwind {uls_roof.value} {sls_roof.value}": []}
                )
                title_df.to_excel(
                    writer, sheet_name="Roof Load Combinations", startrow=start_row
                )
                df.to_excel(
                    writer,
                    sheet_name="Roof Load Combinations",
                    startrow=start_row + 1,
                    index=False,
                )
                # update start_row for the next dataframe
                start_row += len(df.index) + 3
        # return the file as a streaming response
        return FileResponse(
            output_path,
            filename=f"aspenlog2022_report_{id}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    # If something goes wrong, raise an error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
