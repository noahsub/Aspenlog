# Database Entities

## climatic_data.py
- A SQLAlchemy Object Relational Mapping (ORM) class representing climatic data in the database.
- Fields: `ID`, `ProvinceAndLocation`, `Latitude`, `Longitude`, `Elev_m`, various temperature, rain, and snow load fields.

## database_connection.py
- Manages database connections with different privileges (admin, write, read) using credentials from environment variables.
- Provides functions to establish connections, get cursors, and create SQLAlchemy engines.
- Uses `psycopg2` for PostgreSQL connections and `sqlalchemy` for ORM functionalities.

## wind_speed_data.py
- A SQLAlchemy ORM class for storing wind speed data.
- Fields: `ID`, `q_KPa` (pressure in kilopascals), `V_ms` (wind speed in meters per second).
