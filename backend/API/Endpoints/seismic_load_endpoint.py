from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists

seismic_load_router = APIRouter()


@seismic_load_router.post("/set_seismic_load")
def set_seismic_load_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
