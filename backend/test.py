import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Cookie, Response, Body
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# OAuth2PasswordBearer for handling token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def login(username: str, password: str):
    return True

# Login route
@app.post("/authenticate")
async def get_token(username: str, password: str, response: Response):
    if login(username, password):
        response.set_cookie(key="user_token", value=username, max_age=1800)  # Max age is in seconds (e.g., 1800 seconds = 30 minutes)
        return {"token_type": "bearer", "access_token": username}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Updated Protected route (GET request)
@app.get("/protected")
async def protected_route(username: str = Depends(oauth2_scheme), user_token: str = Cookie(None)):
    if user_token and username:
        return {"message": f"Hello, {username}! You are authenticated using the token from the cookie."}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
