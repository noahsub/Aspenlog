import uvicorn
from fastapi import FastAPI

from backend.API.Endpoints.authentication import authentication_router
from backend.API.Endpoints.cladding_endpoint import cladding_router
from backend.API.Endpoints.dimensions_endpoint import dimensions_router
from backend.API.Endpoints.location import location_router

app = FastAPI()
app.include_router(authentication_router)
app.include_router(location_router)
app.include_router(dimensions_router)
app.include_router(cladding_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
