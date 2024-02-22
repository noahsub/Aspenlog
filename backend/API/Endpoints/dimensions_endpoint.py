from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.dimensions_manager import process_dimension_data
from backend.API.Managers.user_data_manager import check_user_exists, set_user_dimensions
from backend.API.Models.dimensions_input import DimensionsInput

dimensions_router = APIRouter()


@dimensions_router.post("/dimensions")
def dimensions_endpoint(dimensions_input: DimensionsInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        dimensions = process_dimension_data(width=dimensions_input.width, height=dimensions_input.height, eave_height=dimensions_input.eave_height, ridge_height=dimensions_input.ridge_height)
        set_user_dimensions(username=username, dimensions=dimensions)
        return dimensions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
