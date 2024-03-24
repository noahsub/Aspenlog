# API Implementation

## Overview
This document describes the basic setup and functionalities of a FastAPI application for the SEEDA-UOFT Backend.

## FastAPI Setup
- Utilizes the FastAPI framework.
- Configured to run with Uvicorn.

## Endpoints
- `/GET_HEIGHT_ZONES`: POST request to get the height zones for a user's building​​.

- `/LOCATION`: POST request to set the location for a user​​.

- `/DIMENSIONS`: POST request to create a dimensions object for a user​​.

- `/ROOF`: POST request to create a roof object for a user​​.

- `/CLADDING`: POST request to create a cladding object for a user​​.

- `/IMPORTANCE_CATEGORY`: POST request to set the importance category for a user​​.

- `/BUILDING`: POST request to create a building object for a user​​.

- `/REGISTER`: POST request to register a new user​​.

- `/LOGIN`: POST request to login an existing user​​.

- `/EXCEL_OUTPUT`: POST request to create an Excel output for a user​​

- `/GET_HEIGHT_ZONES`: POST request to get the height zones for a user's building.

- `/LOCATION`: POST request to set the location for a user.

- `/DIMENSIONS`: POST request to create a dimensions object for a user.

- `/ROOF`: POST request to create a roof object for a user.

- `/CLADDING`: POST request to create a cladding object for a user.

- `/IMPORTANCE_CATEGORY`: POST request to set the importance category for a user.

- `/BUILDING`: POST request to create a building object for a user.

- `/REGISTER`: POST request to register a new user.

- `/LOGIN`: POST request to login an existing user.

- `/EXCEL_OUTPUT`: POST request to create an Excel output for a user.

- `/SERVER_STATUS`: GET request to view the server status page.

- `/SET_SEISMIC_LOAD`: POST request to create a seismic load object for a user.

- `/SET_WIND_LOAD`: POST request to create a wind load object for a user.

- `/SET_SNOW_LOAD`: POST request to create a snow load object for a user.

- `/GET_WALL_LOAD_COMBINATIONS`: POST request to create a wall load combination object for a user.

- `/GET_ROOF_LOAD_COMBINATIONS`: POST request to get the roof load combinations for a user.

- `/USER_DATA`: POST request to get user data.

- `/GET_USER_PROFILE`: POST request to get user profile data.

- `/GET_ALL_USER_SAVE_DATA`: POST request to get all user save data.

- `/GET_USER_SAVE_FILE`: POST request to get a user save file.

- `/SET_USER_SAVE_DATA`: POST request to set user save data.

- `/SET_USER_CURRENT_SAVE_FILE`: POST request to set the current user save file.

- `/GET_USER_CURRENT_SAVE_FILE`: POST request to get the current user save file.

- `/DELETE_USER_CURRENT_SAVE_FILE`: POST request to delete a user save file.

- `/DOWNLOAD_USER_SAVE_FILE`: POST request to download a user save file.

- `/BAR_CHART`: POST request to generate a bar chart.

- `/LOAD_MODEL`: POST request to generate a load model.

- `/SIMPLE_MODEL`: POST request to generate a simple model.

- `/GET_BAR_CHART`: GET request to get a bar chart.

- `/GET_WIND_LOAD_MODEL`: GET request to get a wind load model.

- `/GET_SEISMIC_LOAD_MODEL`: GET request to get a seismic load model.

- `/GET_SIMPLE_MODEL`: GET request to get a simple model.

