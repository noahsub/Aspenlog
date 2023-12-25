# Test API Implementation

## Overview
This document describes the basic setup and functionalities of a FastAPI application for the SEEDA-UOFT Backend.

## FastAPI Setup
- Utilizes the FastAPI framework.
- Configured to run with Uvicorn.

## Endpoints
- `GET /`: Returns a message indicating that the SEEDA-UOFT Backend is running.
- `GET /table_c2`: Serves the `table_c2.csv` file located in the `./output` directory.

## Running the Application
- The application is set to run on `host=0.0.0.0` and `port=42613`.
- Uvicorn is used to run the application, making it accessible via the specified host and port.

_Note: This setup is for testing purposes and demonstrates the basic functionality of serving files and responses through a FastAPI application._
