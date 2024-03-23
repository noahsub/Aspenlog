# Wind Speed Data Population

## File: populate_wind_speed_data.py

### Features
- Manages wind speed data in the database.
- Utilizes SQLAlchemy and `tqdm` for database operations and progress tracking.
- Connects to the database using `DatabaseConnection`.

### Main Functions
1. `create_wind_speed_data_table`: Creates the `WindSpeedData` table if not present.
2. `clean_wind_speed_data_table`: Clears the `WindSpeedData` table and resets its sequence.
3. `populate_wind_speed_data_table`: Fills the `WindSpeedData` table from a CSV file, processing wind speed and pressure data.

### Execution
- Executes table creation, data cleaning, and data population for wind speed data upon running.
