import jsonpickle
from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.building_manager import process_building_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_building, get_user_building
from backend.API.Models.building_input import BuildingInput

building_router = APIRouter()


@building_router.post("/building")
def building_endpoint(building_input: BuildingInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = process_building_data(num_floor=building_input.num_floor, h_opening=building_input.h_opening,
                                         zones=building_input.zones, materials=building_input.materials,
                                         username=username)
        set_user_building(username=username, building=building)
        print(get_user_building(username))
        return jsonpickle.encode(building)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
