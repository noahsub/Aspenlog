import jsonpickle
from fastapi import HTTPException, Depends, APIRouter

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import get_user_building, check_user_exists

height_zone_router = APIRouter()


@height_zone_router.post("/get_height_zones")
def get_height_zones_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username=username)
        height_zones = {}
        for zone in building.height_zones:
            height_zones[zone.zone_num] = zone
        return jsonpickle.encode(height_zones)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
