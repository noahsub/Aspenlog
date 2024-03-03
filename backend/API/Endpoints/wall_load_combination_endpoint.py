import json

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_snow_load
from backend.API.Managers.wall_load_combination_manager import process_wall_load_combination_data
from backend.API.Models.wall_load_combination_input import WallLoadCombinationInput

wall_load_combination_router = APIRouter()


@wall_load_combination_router.post("/get_wall_load_combinations")
def wall_load_combination_endpoint(wall_load_combination_input: WallLoadCombinationInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username)
        snow_load = get_user_snow_load(username)['upwind']
        df = process_wall_load_combination_data(building=building, snow_load=snow_load, uls_wall_type=wall_load_combination_input.uls_wall_type, sls_wall_type=wall_load_combination_input.sls_wall_type).to_json(orient='records')
        parsed = json.loads(df)
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
