<p align="center">
  <img src="assets/images/aspenlog2020logo.png" />
</p>

<p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a>
    <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1"></a>
    <a href="https://www.electronjs.org/"><img src="https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white"></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"></a>
    <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"></a>
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"></a>
    <a href="https://www.blender.org/"><img src="https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white"></a>
</p>

<p align="center">
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <a href="https://github.com/prettier/prettier"><img src="https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square" alt="code style: prettier"></a>
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
Refer to [Setup and Installation](https://noahsub.github.io/Aspenlog/setup-and-installation.html) in the documentation.

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
You can see how the program is structured and how to use here: [Documentation](https://noahsub.github.io/Aspenlog/)

## Authors
<table>
  <tr>
    <td align="center" class="author"><a href="https://github.com/noahsub"><img src="assets/images/profile/noahsub.png" alt=""/><br /><sub><b>noahsub</b></sub></a><br /></td>
    <td align="center" class="author"><a href="https://github.com/alastairsim"><img src="assets/images/profile/alastairsim.png" alt=""/><br /><sub><b>alastairsim</b></sub></a><br /></td>
    <td align="center" class="author"><a href="https://github.com/kinheychan"><img src="assets/images/profile/kinheychan.png" alt=""/><br /><sub><b>kinheychan</b></sub></a><br /></td>
    <td align="center" class="author"><a href="https://github.com/lishujie2000"><img src="assets/images/profile/lishujie2000.png" alt=""/><br /><sub><b>lishujie2000</b></sub></a><br /></td>
    <td align="center" class="author"><a href="https://github.com/myraliym"><img src="assets/images/profile/myraliym.png" alt=""/><br /><sub><b>myraliym</b></sub></a><br /></td>
  </tr>
</table>

## LICENSE
This project is licensed under the Mozilla Public License 2.0 - see the [LICENSE](LICENSE) and [DISCLAIMER](DISCLAIMER) files for details.







