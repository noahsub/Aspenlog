from fastapi import APIRouter, Depends, HTTPException

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.location_manager import process_location_data
from backend.API.Managers.user_data_manager import set_user_location, check_user_exists
from backend.API.Models.location_input import LocationInput

location_router = APIRouter()


@location_router.post("/location")
def location_endpoint(location_input: LocationInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        location = process_location_data(address=location_input.address, site_designation=location_input.site_designation, seismic_value=location_input.seismic_value)
        set_user_location(username=username, location=location)
        return location
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
