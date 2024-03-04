from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.seismic_load_manager import process_seismic_load_data
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_importance_category, \
    get_user_location
from backend.API.Models.seismic_load_input import SeismicLoadInput

seismic_load_router = APIRouter()


@seismic_load_router.post("/set_seismic_load")
def set_seismic_load_endpoint(seismic_load_input: SeismicLoadInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username=username)
        importance_factor = get_user_importance_category(username=username)
        location = get_user_location(username=username)
        process_seismic_load_data(building=building, location=location, importance_category=importance_factor, ar=seismic_load_input.ar, rp=seismic_load_input.rp, cp=seismic_load_input.cp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
