import json

import jsonpickle
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.roof_load_combination_manager import process_roof_load_combination_data
from backend.API.Managers.user_data_manager import check_user_exists, get_user_snow_load, get_user_building
from backend.API.Models.roof_load_combination_input import RoofLoadCombinationInput

roof_load_combination_router = APIRouter()


@roof_load_combination_router.post("/get_roof_load_combinations")
def roof_load_combination_endpoint(roof_load_combination_input: RoofLoadCombinationInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username)
        snow_load_upwind = get_user_snow_load(username)['upwind']
        snow_load_downwind = get_user_snow_load(username)['downwind']
        dataframes = process_roof_load_combination_data(building=building, snow_load_upwind=snow_load_upwind, snow_load_downwind=snow_load_downwind, uls_roof_type=roof_load_combination_input.uls_roof_type, sls_roof_type=roof_load_combination_input.sls_roof_type)
        upwind_df = dataframes['upwind'].round(4)
        upwind_headers = [str(x) for x in upwind_df.columns]
        upwind_companion_indices = [i for i in range(len(upwind_headers)) if 'companion' in upwind_headers[i]]
        upwind_values = [float(x) for x in upwind_df.iloc[0].values]
        for index in sorted(upwind_companion_indices, reverse=True):
            upwind_headers.pop(index)
            upwind_values.pop(index)
        downwind_df = dataframes['downwind'].round(4)
        downwind_headers = [str(x) for x in downwind_df.columns]
        downwind_companion_indices = [i for i in range(len(downwind_headers)) if 'companion' in downwind_headers[i]]
        downwind_values = [float(x) for x in downwind_df.iloc[0].values]
        for index in sorted(downwind_companion_indices, reverse=True):
            downwind_headers.pop(index)
            downwind_values.pop(index)
        return json.dumps({'upwind': [upwind_headers, upwind_values], 'downwind': [downwind_headers, downwind_values]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
