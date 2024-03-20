<p align="center">
  <img src="assets/images/aspenlog2020logo.png" />
</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
    <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1">
    <img src="https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
    <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
    <img src="https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white">
</p>

# Application of Specified Environmental Load Generator
The Application of Specified Environmental Load Generator (Aspenlog 2020) is an
online desktop application designed to calculate environmental loads (wind,
seismic, and snow) on building cladding components. These calculations are based
on Chapter 4 of the National Building Code of Canada (NBCC) 2020. The
application was developed by the University of Toronto Institute for
Multidisciplinary Design & Innovation (UT-IMDI) for SEEDA.

## Overview
- Automatically get site parameters from an address
- Efficiently input building parameters
- Calculate environmental loads
- Calculate load combinations
- 3D visualizations of the building, loads, and load combinations
- Export all data to an Excel file
- User accounts to save and load projects and access them from any device anywhere with an internet connection

![aspenlog2020](assets/images/aspenlog_demo_slower.gif)


## Hosting the Backend
Refer to the backend guide in the `installation` directory.

## Running the Application
To run the frontend application simply install the latest release for your operating system from the releases page.
Currently, there is support for x86 architecture on Windows, MacOS, and Linux however, the application can be run on
many other platforms by running the following:

```bash
cd frontend
npm install electron
npm start
```

## Documentation
You can see how the program is structured and how to use it in the `documentation` directory.

