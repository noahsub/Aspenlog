# Repository Structure

This section provides a detailed overview of the repository structure, helping users navigate and understand the various components of the project.

- **Root Directory**
    - `.gitignore`: Specifies files to be ignored by Git.
    - `config.py`: Configuration file for the project.
    - `README.md`: Introduction and overview of the project.
    - `requirements.txt`: Lists dependencies required for the project.
    - `main.py`: Main function to run our program.
    - `DISCLAIMER`: Disclaimer for the project.
    - `LICENSE`: Mozilla Public License 2.0 for the project.
    - `guide.md`: Setup Guide.
    - `linux_run_backend.sh`: Runs the Aspenlog 2020 backend on a Linux server.
    - `linux_server_install.sh`: Installs the necessary packages and sets up the environment for the Aspenlog 2020 backend on a Linux server.
    - `requirements_linux.txt`: Lists dependencies required for the linux server.

- **.github/workflows**
  - `mac-node-build.yml`:  Workflow will do a clean installation of node dependencies, cache/restore them, build the source code and run tests across different versions of node.
  - `ubuntu-node-build.yml`:  Workflow will do a clean installation of node dependencies, cache/restore them, build the source code and run tests across different versions of node.
  - `windows-node-build.yml`:  Workflow will do a clean installation of node dependencies, cache/restore them, build the source code and run tests across different versions of node.

- **assets/images**
  - Contains logos for the project.

- **Backend Directory**
    - `test.py`: Script for testing backend functionalities.
    - **algorithms**: Contains algorithms for load calculations (`snow_load_algorithms.py`, `wind_load_algorithms.py`).
    - **Constants**: Includes constants (`importance_factor_constants.py`, `snow_constants.py`, `wind_constants.py`).
    - **Entities**: Defines entities like `building.py`, `snow.py`, `wind.py`.
    - **API**: Contains code for managing endpoints and making calls to other APIs.
    - **output**: Location for output of rendered images and bar charts.
    - **visualizations**: Contains code for creating 3D bar chart.

- **Data Extraction Directory**
    - `NBCC_Data_Extraction.py`: Script for extracting data from NBCC tables.
    - **input**: Contains input files like `NBCC2020-Table-C-1.pdf`.
    - **output**: Stores extracted data in formats like CSV, XLSX.

- **Database Directory**
    - **Constants**: Houses database connection constants (`connection_constants.py`).
    - **Entities**: Includes database entities and connection setup (`climatic_data.py`, `database_connection.py`, `wind_speed_data.py`).
    - **Population**: Scripts to populate the database (`populate_climate_data.py`, `populate_database.py`, `populate_wind_speed_data.py`).
    - **Warnings**: Contains database warnings (`database_warnings.py`).

- **Frontend Directory**
  - `assets/images`: Contains logo and background colour.
  - **Renderer**: Contains all HTML, CSS and JS files for the frontend pages.


This structure ensures a clear separation of concerns and easy navigation for contributors and users alike.


<seealso>
    <!--Provide links to related how-to guides, overviews, and tutorials.-->
</seealso>