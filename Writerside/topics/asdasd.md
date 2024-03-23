# Climatic Data Population

## File: populate_climate_data.py

### Features
- Manages climatic data in the database.
- Connects to the database with different privileges using `DatabaseConnection`.
- Utilizes `tqdm` for progress bars and `geopy` for geolocation.

### Main Functions
1. `create_climatic_data_table`: Creates the `ClimaticData` table if it does not exist.
2. `clean_climatic_data_table`: Clears the `ClimaticData` table and resets its sequence.
3. `populate_climatic_data_table`: Populates the `ClimaticData` table from a CSV file.
4. `update_location`: Updates latitude and longitude in `ClimaticData` using `Nominatim` geolocator.

### Execution
- On running, the script performs table creation, data cleaning, populating with climatic data, and updating location coordinates.
