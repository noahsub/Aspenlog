import io
import json

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import StreamingResponse

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_data, get_all_user_save_data, \
    get_user_save_file, set_user_save_data, set_user_current_save_file, get_user_current_save_file, get_user_profile, \
    delete_user_save_file, get_user_save_file_json
from backend.API.Models.save_data_input import SaveDataInput

user_data_router = APIRouter()


@user_data_router.post("/user_data")
def user_data_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return get_user_data(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_profile")
def get_user_profile_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return jsonpickle.encode(get_user_profile(username))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_all_user_save_data")
def get_all_user_save_data_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return get_all_user_save_data(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_save_file")
def get_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return get_user_save_file(username, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/set_user_save_data")
def set_user_save_data_endpoint(data: SaveDataInput, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return set_user_save_data(username, data.json_data, data.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/set_user_current_save_file")
def set_user_current_save_file_endpoint(current_save_file: int, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return set_user_current_save_file(username, current_save_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/get_user_current_save_file")
def get_user_current_save_file_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return get_user_current_save_file(username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/delete_user_current_save_file")
def delete_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        return delete_user_save_file(username, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_data_router.post("/download_user_save_file")
def download_user_save_file_endpoint(id: int, username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        data = get_user_save_file_json(username, id)

        # Create a string of JSON data
        json_str = json.dumps(data)

        # Create an in-memory file
        file_like_object = io.StringIO(json_str)

        # Return a response to download the file
        return StreamingResponse(
            file_like_object,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={username}_{id}_save_file.json"
            },
        )
    except Exception as e:
        return {"error": str(e)}
