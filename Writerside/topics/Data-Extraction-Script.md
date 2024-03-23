# NBCC Data Extraction Script Overview

## File: `NBCC_Data_Extraction.py`
This script extracts data from the National Building Code of Canada 2020 (NBCC2020) and converts it to a Pandas dataframe. The data is then saved as both CSV and Excel files in the output directory.

### Key Features
- Extracts data from Table C1 and Table C2.
- Table C1: Design Wind Pressures for Components and Cladding.
- Table C2: Design Wind Pressures for Main Wind-Force Resisting Systems.
- Uses `pypdf` for reading PDF files and `pandas` for data manipulation.

### Functions
- `pdf_to_text`: Converts PDF file to text organized by page and line.
- `dataframe_to_csv`: Converts dataframe to CSV and saves it.
- `dataframe_to_excel`: Converts dataframe to Excel format and saves it.
- `table_c1_extraction`: Extracts data from Table C1 into a dataframe.
- `table_c2_extraction`: Extracts data from Table C2 into a dataframe.

### Usage
On execution, the script extracts data from specified tables, converts them to dataframes, and saves them in CSV and Excel formats.

**Note:** This script is proprietary to the University of Toronto, SEEDA. Usage requires specific written permission from the owners.
