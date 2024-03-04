from fastapi import APIRouter, HTTPException, status, Depends

from backend.API.Managers.authentication_manager import signup, login, decode_token
from backend.API.Managers.user_data_manager import set_user_profile
from backend.Entities.User.profile import Profile

authentication_router = APIRouter()


@authentication_router.post("/register")
def register_endpoint(username: str, first_name: str, last_name: str, password: str, email: str):
    if signup(username, first_name, last_name, password, email):
        return f"user '{username}' has been registered successfully"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


@authentication_router.post("/login")
def register_endpoint(username: str, password: str):
    api_key = login(username, password)
    if api_key is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        return api_key


@authentication_router.get("/protected")
def protected_endpoint(username: str = Depends(decode_token)):
    return {"message": f"Hello, {username}! You are authenticated."}
