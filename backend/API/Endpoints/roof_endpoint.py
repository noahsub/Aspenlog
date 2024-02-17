from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.roof_manager import process_roof_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_roof
from backend.API.Models.roof_input import RoofInput

roof_router = APIRouter()


@roof_router.post("/roof")
def roof_endpoint(roof_input: RoofInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        roof = process_roof_data(w_roof=roof_input.w_roof, l_roof=roof_input.l_roof, slope=roof_input.slope, uniform_dead_load=roof_input.uniform_dead_load)
        set_user_roof(username=username, roof=roof)
        return roof
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
