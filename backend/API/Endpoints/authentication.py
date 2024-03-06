from fastapi import APIRouter, HTTPException, status, Depends

from backend.API.Managers.authentication_manager import signup, login, decode_token
from backend.API.Models.login_input import LoginInput
from backend.API.Models.register_input import RegisterInput

authentication_router = APIRouter()


@authentication_router.post("/register")
def register_endpoint(register_input: RegisterInput):
    if signup(register_input.username, register_input.first_name, register_input.last_name, register_input.password,
              register_input.email):
        return f"user '{register_input.username}' has been registered successfully"
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")


@authentication_router.post("/login")
def register_endpoint(login_input: LoginInput):
    api_key = login(login_input.username, login_input.password)
    if api_key is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        return api_key


@authentication_router.get("/protected")
def protected_endpoint(username: str = Depends(decode_token)):
    return {"message": f"Hello, {username}! You are authenticated."}
