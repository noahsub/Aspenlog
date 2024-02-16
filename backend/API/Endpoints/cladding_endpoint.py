from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.cladding_manager import process_cladding_data
from backend.API.Managers.user_data_manager import set_user_cladding, check_user_exists
from backend.API.Models.cladding_input import CladdingInput

cladding_router = APIRouter()


@cladding_router.post("/cladding")
def cladding_endpoint(cladding_input: CladdingInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        cladding = process_cladding_data(c_top=cladding_input.c_top, c_bot=cladding_input.c_bot)
        set_user_cladding(username=username, cladding=cladding)
        return cladding
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
