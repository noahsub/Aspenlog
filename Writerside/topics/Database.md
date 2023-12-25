# Database

## Database Structure
The database contains tables for storing climatic data (such as temperature, rainfall, and wind speed) and wind speed data, which likely relate to different geographical regions or conditions. The database is designed to be populated through specific scripts, suggesting a dynamic and updatable structure. This setup is ideal for applications requiring real-time or regularly updated environmental data, particularly in the context of building design or environmental analysis.

## Repository Structure
- Organized into four main subdirectories: Constants, Entities, Population, and Warnings.

### Constants Directory
- `connection_constants.py`: Defines constants for database connections.

### Entities Directory
- Contains Python scripts modeling database entities.
    - `climatic_data.py`: Defines climatic data structure.
    - `database_connection.py`: Manages database connections.
    - `wind_speed_data.py`: Defines wind speed data structure.

### Population Directory
- Scripts for populating the database.
    - `populate_climate_data.py`: Populates climate data.
    - `populate_database.py`: General database population script.
    - `populate_wind_speed_data.py`: Populates wind speed data.

### Warnings Directory
- `database_warnings.py`: Handles warning messages related to the database.

## Purpose
- This structure enables organized management of database components, including connection settings, entity definitions, data population scripts, and warning handling.
