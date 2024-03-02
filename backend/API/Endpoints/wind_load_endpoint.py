from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_importance_category, \
    get_user_location
from backend.API.Managers.wind_load_manager import process_wind_load_data
from backend.API.Models.wind_load_input import WindLoadInput

wind_load_router = APIRouter()


@wind_load_router.post("/set_wind_load")
def set_wind_load_endpoint(wind_load_input: WindLoadInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username=username)
        importance_factor = get_user_importance_category(username=username)
        location = get_user_location(username=username)
        for height_zone in building.height_zones:
            i = height_zone.zone_num - 1
            process_wind_load_data(building=building, height_zone=height_zone, importance_category=importance_factor, location=location, ct=wind_load_input.ct[i], exposure_factor=wind_load_input.exposure_factor[i], internal_pressure_category=wind_load_input.internal_pressure_category[i], manual_ce_cei=wind_load_input.manual_ce_cei[i])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
