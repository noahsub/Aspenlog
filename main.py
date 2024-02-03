import uvicorn
from fastapi import FastAPI

from backend.Endpoints.authentication import authentication_router

app = FastAPI()
app.include_router(authentication_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
