import uvicorn
from fastapi import FastAPI

from backend.API.Endpoints.authentication import authentication_router
from backend.API.Endpoints.building_endpoint import building_router
from backend.API.Endpoints.cladding_endpoint import cladding_router
from backend.API.Endpoints.dimensions_endpoint import dimensions_router
from backend.API.Endpoints.importance_category_endpoint import importance_category_router
from backend.API.Endpoints.location import location_router
from backend.API.Endpoints.roof_endpoint import roof_router
from backend.API.Endpoints.user_data_endpoint import user_data_router

app = FastAPI()
app.include_router(authentication_router)
app.include_router(location_router)
app.include_router(dimensions_router)
app.include_router(cladding_router)
app.include_router(roof_router)
app.include_router(building_router)
app.include_router(importance_category_router)
app.include_router(user_data_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=42613)
