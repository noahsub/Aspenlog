import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import jwt, JWTError

app = FastAPI()

# OAuth2PasswordBearer for handling token in the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key to sign and verify JWT tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def login(username: str, password: str):
    return True

# Function to validate and decode JWT tokens
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

# Login route
@app.post("/authenticate")
async def get_token(username: str, password: str):
    if login(username, password):
        # Create JWT token
        token_data = {"sub": username}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"token_type": "bearer", "access_token": token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Updated Protected route (GET request)
@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! You are authenticated."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
