# Overview
The University of Toronto Capstone Team (ID: SEEDA) was retained by SEEDA (“Client”) to design an online desktop application for calculating environmental loads (Wind, Seismic and Snow) on the building cladding component based on the National Building Code of Canada (NBCC) 2020 Chapter 4. This project delivery is the Application of Specified Environmental Load Generator (ASPENLOG 2020) that includes 3D model visualization features. The ASPENLOG 2020  streamlines the design process for cladding components in Canadian buildings ensuring compliance with NBCC 2020 Standards. 
Given the intricate nature of this task, we need a comprehensive programming solution that includes a database, backend, and two frontends. This involves not only hosting our own database and APISs but also leveraging public APIs and frameworks.

Breaking down the software development into components instead of placing everything into a single offline application greatly increases the modularity of the program allowing for easier maintenance, better scalability, and improved flexibility. By leveraging databases and APIs, we can ensure that each component of the software can be developed, tested, and updated independently allowing for multiple developers to work on different parts of the program simultaneously without making disruptions to the entire application.

## **Application of Specified Environmental Load Generator (ASPENLOG 2020)**


### Programming Solution
- Requires a database and a backend running on a server.
- Utilization of both private and public APIs.

### Software Development Approach
- Modular approach for easier maintenance and scalability.
- Independent development, testing, and updating of software components.

### Private Server
- Hosting of the database and backend during the project.
- Post-completion, software can be hosted on any provider chosen by SEEDA.

### Backend and Database
- PostgreSQL database for storing data.
- Python code integrated with REST API.
- Frontend applications will retrieve data in JSON format.
- Use of Python modules (Seaborn, Matplotlib) and public APIs through the backend.
- Capability to export data in Excel format.
- Save and resume functionality using JSON serialization.

### Frontend
- Built using Electron platform and JavaScript.
- Compatibility across major platforms.
- Notable Electron framework use (e.g., Microsoft Teams, VS Code, Slack).

### Graphics
- Graphical User Interface (GUI) for interaction.
- SPENLOG Electron Frontend with 3D bar chart and tables.
- 3D model frontend for visualizing height zones and loads.
- Initial support for structures with simple shapes.
