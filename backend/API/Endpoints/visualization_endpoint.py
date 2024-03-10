import uuid

import jsonpickle
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import FileResponse

from backend.API.Managers.authentication_manager import decode_token
from backend.API.Managers.user_data_manager import check_user_exists, get_user_building, get_user_snow_load
from backend.visualizations.load_combination_bar_chart import generate_bar_chart
from blender.scripts.blender_object import WindZone, SeismicZone
from blender.scripts.blender_request import run_blender_script
from config import get_file_path

visualization_router = APIRouter()


@visualization_router.post("/bar_chart")
def generate_bar_chart_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        id = str(uuid.uuid4())
        building = get_user_building(username)
        snow_load = get_user_snow_load(username)['upwind']
        num_generated = generate_bar_chart(id=id, building=building, snow_load=snow_load)
        return jsonpickle.encode({'id': id, 'num_bar_charts': num_generated})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.post("/load_model")
def generate_load_model_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        id = str(uuid.uuid4())
        building = get_user_building(username=username)
        height_zones = building.height_zones
        wind_cubes = []
        seismic_cubes = []
        prev_elevation = 0
        for height_zone in sorted(height_zones, key=lambda x: x.zone_num):
            wind_cubes.append(WindZone(h=height_zone.elevation - prev_elevation,
                                       wall_centre_pos=height_zone.wind_load.get_zone(4).pressure.pos_uls,
                                       wall_centre_neg=height_zone.wind_load.get_zone(4).pressure.neg_uls,
                                       wall_corner_pos=height_zone.wind_load.get_zone(5).pressure.pos_uls,
                                       wall_corner_neg=height_zone.wind_load.get_zone(5).pressure.neg_uls))
            seismic_cubes.append(SeismicZone(h=height_zone.elevation - prev_elevation,
                                             load=height_zone.seismic_load.vp))
            prev_elevation = height_zone.elevation

        json_wind = jsonpickle.encode(wind_cubes)
        path_wind = get_file_path('blender/scripts/wind_cube.py')
        run_blender_script(script_path=path_wind, id=id, json_str=json_wind)

        json_seismic = jsonpickle.encode(seismic_cubes)
        path_seismic = get_file_path('blender/scripts/seismic_cube.py')
        run_blender_script(script_path=path_seismic, id=id, json_str=json_seismic)
        return jsonpickle.encode(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.post('/simple_model')
def generate_simple_model_endpoint(username: str = Depends(decode_token)):
    try:
        check_user_exists(username)
        id = str(uuid.uuid4())
        building = get_user_building(username=username)
        total_elevation = building.dimensions.height
        roof_angle = building.roof.slope
        json_simple = jsonpickle.encode({'total_elevation': total_elevation, 'roof_angle': roof_angle})
        path_simple = get_file_path('blender/scripts/simple_cube.py')
        run_blender_script(script_path=path_simple, id=id, json_str=json_simple)
        return jsonpickle.encode(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_bar_chart")
def get_bar_chart_endpoint(id: str, zone_num: int):
    try:
        output_path = get_file_path(f'backend/output/bar_chart_hz_{zone_num}_{id}.png')
        return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_wind_load_model")
def get_wind_load_model_endpoint(id: str):
    try:
        output_path = get_file_path(f'backend/output/wind_{id}.png')
        return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_seismic_load_model")
def get_seismic_load_model_endpoint(id: str):
    try:
        output_path = get_file_path(f'backend/output/seismic_{id}.png')
        return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@visualization_router.get("/get_simple_model")
def get_simple_model_endpoint(id: str):
    try:
        output_path = get_file_path(f'backend/output/simple_{id}.png')
        return FileResponse(output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
