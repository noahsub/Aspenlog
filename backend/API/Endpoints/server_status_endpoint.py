from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from config import get_file_path

server_status_endpoint = APIRouter()


@server_status_endpoint.get("/server_status")
def user_data_endpoint():
    try:
        path = get_file_path('backend/API/Pages/StatusPage/statusPage.html')
        return FileResponse(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
