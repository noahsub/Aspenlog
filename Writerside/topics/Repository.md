# Repository Structure

This section provides a detailed overview of the repository structure, helping users navigate and understand the various components of the project.

- **Root Directory**
    - `.gitignore`: Specifies files to be ignored by Git.
    - `config.py`: Configuration file for the project.
    - `README.md`: Introduction and overview of the project.
    - `requirements.txt`: Lists dependencies required for the project.

- **Backend Directory**
    - `test.py`: Script for testing backend functionalities.
    - `algorithms`: Contains algorithms for load calculations (`snow_load_algorithms.py`, `wind_load_algorithms.py`).
    - `Constants`: Includes constants (`importance_factor_constants.py`, `snow_constants.py`, `wind_constants.py`).
    - `Entities`: Defines entities like `building.py`, `snow.py`, `wind.py`.

- **Data Extraction Directory**
    - `NBCC_Data_Extraction.py`: Script for extracting data from NBCC tables.
    - `input`: Contains input files like `NBCC2020-Table-C-1.pdf`.
    - `output`: Stores extracted data in formats like CSV, XLSX.

- **Database Directory**
    - `Constants`: Houses database connection constants (`connection_constants.py`).
    - `Entities`: Includes database entities and connection setup (`climatic_data.py`, `database_connection.py`, `wind_speed_data.py`).
    - `Population`: Scripts to populate the database (`populate_climate_data.py`, `populate_database.py`, `populate_wind_speed_data.py`).
    - `Warnings`: Contains database warnings (`database_warnings.py`).

This structure ensures a clear separation of concerns and easy navigation for contributors and users alike.


<seealso>
    <!--Provide links to related how-to guides, overviews, and tutorials.-->
</seealso>