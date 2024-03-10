import secrets
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from config import get_file_path

if __name__ == "__main__":
    api_env_path = Path(get_file_path('data/EnvironmentVariables/.env'))
    database_env_path = Path(get_file_path('database/.env'))

    api_env_valid = True
    database_env_valid = True

    # check that the files at the paths
    if not api_env_path.exists():
        # create the file
        api_env_path.touch()
        api_env_valid = False

    else:
        # get the keys of the .env file
        with open(api_env_path, 'r') as file:
            keys = {x.split('=')[0] for x in file.read().splitlines()}
            if keys != {'API_SECRET_KEY'}:
                api_env_valid = False

    if not database_env_path.exists():
        # create the file
        database_env_path.touch()
        database_env_valid = False

    else:
        # get the keys of the .env file
        with open(database_env_path, 'r') as file:
            keys = {x.split('=')[0] for x in file.read().splitlines()}
            if keys != {'ADMIN_PASSWORD', 'ADMIN_USERNAME', 'WRITE_USERNAME', 'READ_PASSWORD', 'WRITE_PASSWORD', 'HOST',
                        'READ_USERNAME', 'PORT'}:
                database_env_valid = False

    if api_env_valid is False:
        # populate the .env file
        with open(api_env_path, 'w') as file:
            file.write(f'API_SECRET_KEY={secrets.token_urlsafe(256)}\n')

    if database_env_valid is False:
        # populate the .env file
        with open(database_env_path, 'w') as file:
            print("Please enter the following information associated with the database.")
            file.write(f'ADMIN_USERNAME={input("Database Admin Username: ")}\n')
            file.write(f'ADMIN_PASSWORD={input("Database Admin Password: ")}\n')
            file.write(f'WRITE_USERNAME={input("Database Write Username: ")}\n')
            file.write(f'WRITE_PASSWORD={input("Database Write Password: ")}\n')
            file.write(f'READ_USERNAME={input("Database Read Username")}\n')
            file.write(f'READ_PASSWORD={input("Database Read Password")}\n')
            file.write(f'HOST={input("Database IP Address (HTTPS is Not Supported Here): ")}\n')
            file.write(f'PORT={input("Database Port: ")}')

    from backend.API.Endpoints.authentication import authentication_router
    from backend.API.Endpoints.building_endpoint import building_router
    from backend.API.Endpoints.cladding_endpoint import cladding_router
    from backend.API.Endpoints.dimensions_endpoint import dimensions_router
    from backend.API.Endpoints.height_zones_endpoint import height_zone_router
    from backend.API.Endpoints.importance_category_endpoint import importance_category_router
    from backend.API.Endpoints.location import location_router
    from backend.API.Endpoints.roof_endpoint import roof_router
    from backend.API.Endpoints.roof_load_combination_endpoint import roof_load_combination_router
    from backend.API.Endpoints.seismic_load_endpoint import seismic_load_router
    from backend.API.Endpoints.server_status_endpoint import server_status_endpoint
    from backend.API.Endpoints.snow_load_endpoint import snow_load_router
    from backend.API.Endpoints.user_data_endpoint import user_data_router
    from backend.API.Endpoints.wall_load_combination_endpoint import wall_load_combination_router
    from backend.API.Endpoints.wind_load_endpoint import wind_load_router
    from backend.API.Endpoints.visualization_endpoint import visualization_router
    from backend.API.Endpoints.output_endpoint import output_router

    app = FastAPI()
    app.include_router(authentication_router)
    app.include_router(location_router)
    app.include_router(dimensions_router)
    app.include_router(cladding_router)
    app.include_router(roof_router)
    app.include_router(building_router)
    app.include_router(importance_category_router)
    app.include_router(user_data_router)
    app.include_router(wind_load_router)
    app.include_router(height_zone_router)
    app.include_router(seismic_load_router)
    app.include_router(snow_load_router)
    app.include_router(wall_load_combination_router)
    app.include_router(roof_load_combination_router)
    app.include_router(server_status_endpoint)
    app.include_router(visualization_router)
    app.include_router(output_router)

    uvicorn.run(app, host="0.0.0.0", port=42613)
