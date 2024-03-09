from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_snow_load
from backend.visualizations.load_combination_bar_chart import generate_bar_chart

visualization_router = APIRouter()


@visualization_router.post("/bar_chart")
def generate_bar_chart_endpoint(height_zone: int, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        building = get_user_building(username)
        snow_load = get_user_snow_load(username)['upwind']
        generate_bar_chart(building, 1, snow_load)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
