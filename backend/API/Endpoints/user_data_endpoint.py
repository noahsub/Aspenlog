from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_data

user_data_router = APIRouter()


@user_data_router.post("/user_data")
def user_data_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return get_user_data(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
