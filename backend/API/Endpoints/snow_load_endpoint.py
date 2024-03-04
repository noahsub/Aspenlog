import jsonpickle
from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.snow_load_manager import process_snow_load_data
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_importance_category, \
    get_user_location, set_user_snow_load
from backend.API.Models.snow_load_input import SnowLoadInput

snow_load_router = APIRouter()


@snow_load_router.post("/set_snow_load")
def set_snow_load_endpoint(snow_load_input: SnowLoadInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username=username)
        importance_factor = get_user_importance_category(username=username)
        location = get_user_location(username=username)
        snow_load = process_snow_load_data(building=building, location=location, importance_category=importance_factor, exposure_factor_selection=snow_load_input.exposure_factor_selection, roof_type=snow_load_input.roof_type)
        set_user_snow_load(username=username, snow_load=snow_load)
        return jsonpickle.encode(snow_load)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
