import argparse
import secrets
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from config import get_file_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--install', action='store_true', help='Installation Mode Only')
    parser.add_argument('-ip', '--host', type=str, help='Database ip Address (HTTPS is Not Supported Here)')
    parser.add_argument('-p', '--port', type=int, help='Port Number')
    parser.add_argument('-du', '--admin_username', type=str, help='Admin Username')
    parser.add_argument('-dp', '--admin_password', type=str, help='Admin Password')
    args = parser.parse_args()

    api_env_path = Path(get_file_path('data/EnvironmentVariables/.env'))
    database_env_path = Path(get_file_path('database/.env'))

    api_env_valid = True
    database_env_valid = True

    # check that the files at the paths
    if not api_env_path.exists():
        # create the directory
        api_env_path.parent.mkdir(parents=True, exist_ok=True)
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
        # create the directory
        database_env_path.parent.mkdir(parents=True, exist_ok=True)
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
            if args.host:
                file.write(f'HOST={args.host}\n')
            else:
                file.write(f'HOST={input("Database IP Address (HTTPS is Not Supported Here): ")}\n')
            if args.port:
                file.write(f'PORT={args.port}\n')
            else:
                file.write(f'PORT={input("Database Port: ")}\n')
            if args.admin_username:
                file.write(f'ADMIN_USERNAME={args.admin_username}\n')
            else:
                file.write(f'ADMIN_USERNAME={input("Database Admin Username: ")}\n')
            if args.admin_password:
                file.write(f'ADMIN_PASSWORD={args.admin_password}\n')
            else:
                file.write(f'ADMIN_PASSWORD={input("Database Admin Password: ")}\n')
            file.write(f'WRITE_USERNAME=NONE\n')
            file.write(f'WRITE_PASSWORD=NONE\n')
            file.write(f'READ_USERNAME=NONE\n')
            file.write(f'READ_PASSWORD=NONE\n')

    # Installation mode
    if args.install:
        exit(0)

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
