import json

import jsonpickle
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
        df = process_roof_load_combination_data(building=building, snow_load_upwind=snow_load_upwind, snow_load_downwind=snow_load_downwind, uls_roof_type=roof_load_combination_input.uls_roof_type, sls_roof_type=roof_load_combination_input.sls_roof_type).to_json(orient='records')
        parsed = json.loads(df)
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
