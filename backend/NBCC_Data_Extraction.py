########################################################################################################################
# NBCC_Data_Extraction.py
# This file contains functions that extract data from the National Building Code of Canada 2020 (NBCC2020) and store it
# in a Pandas dataframe. The data is then converted to a csv file and an Excel file and saved in the output directory.
# The data is extracted from the following tables:
#   - Table C1: Design Wind Pressures for Components and Cladding
#   - Table C2: Design Wind Pressures for Main Wind-Force Resisting Systems
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Owners: University of Toronto, SEEDA
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################
import re
import pandas as pd
from pypdf import PdfReader

########################################################################################################################
# CONSTANTS
########################################################################################################################

CANADIAN_PROVINCES_AND_TERRITORIES = {
    "Alberta",
    "British Columbia",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
    "Northwest Territories",
    "Nunavut",
    "Yukon"
}


########################################################################################################################
# PDF OPERATIONS
########################################################################################################################

def pdf_to_text(pdf: str) -> list[list[str]]:
    """
    Converts a PDF file to text organized by page and line.

    :param pdf: The name of the pdf file you would like to extract text from.
    :return: A nested list containing the extracted text from each page and line.
    """

    # Create a reader for the specified PDF
    reader = PdfReader(f"input/{pdf}")
    # Extract the text page by page and line by line.
    text = []
    for page in reader.pages:
        text.append(page.extract_text().split('\n'))

    # Return the extracted text.
    return text


########################################################################################################################
# PANDAS DATAFRAME CONVERSIONS
########################################################################################################################

def dataframe_to_csv(dataframe: pd.DataFrame, filename: str) -> None:
    """
    Convert Pandas dataframe to csv file and save it to the output directory.

    :param dataframe: The dataframe to save.
    :param filename: The filename of the csv file (ensure to include the .csv extension).
    """
    assert ".csv" in filename

    dataframe.to_csv(f"output/{filename}")


def dataframe_to_excel(dataframe: pd.DataFrame, filename: str) -> None:
    """
    Convert Pandas dataframe to Excel file and save it to the output directory.

    :param dataframe: The dataframe to save.
    :param filename: The filename of the Excel file (ensure to include the .xlsx extension).
    """
    assert ".xlsx" in filename

    dataframe.to_excel(f"output/{filename}")


########################################################################################################################
# DATA EXTRACTION
########################################################################################################################

def table_c1_extraction() -> pd.DataFrame:
    """
    Extracts data from Table C1 in NBCC2022 on page 649 and stores it as a Pandas dataframe.

    :return: A Pandas dataframe containing the extracted data.
    """

    # The extracted text
    text = pdf_to_text("NBCC2020-Table-C-1.pdf")

    # The regex used to extract data lines, in this case 8 numbers seperated by spaces
    data_pattern = r"^(-?\d+(\.\d+)?\s){7}-?\d+(\.\d+)?$"
    data_regex = re.compile(data_pattern)

    # Text is analyzed and lines deemed usable data are stored.
    processed = []
    errors = []
    for page in text:
        for line in page:
            # Save data
            if data_regex.match(line):
                # Convert to list of floats
                processed.append([float(x) for x in line.split(' ')])
            else:
                errors.append(line)

    # Headers for the data
    layer_one_headers = ['q', 'V', 'q', 'V', 'q', 'V', 'q', 'V']
    layer_two_headers = ['kPa', 'm/s', 'kPa', 'm/s', 'kPa', 'm/s', 'kPa', 'm/s']

    # Assertions to ensure program correctness
    assert len(layer_one_headers) == len(layer_two_headers) == 8
    assert all([len(x) == 8 for x in processed])

    # Optional option to display all rows
    pd.set_option('display.max_rows', None)

    # Save data in the form of a dataframe
    dataframe = pd.DataFrame(processed)
    header = [layer_one_headers, layer_two_headers]
    dataframe.columns = header

    # Return the dataframe
    return dataframe


def table_c2_extraction() -> pd.DataFrame:
    """
    Extracts data from Table C2 in NBCC2022 pages 650 - 676 and stores them as a Pandas dataframe.

    :return: A Pandas dataframe containing the extracted data.
    """

    # The computer vision extracted text by page and line
    text = pdf_to_text("NBCC2020-Table-C-2.pdf")

    # This regular expression matches a string that ends with a sequence of 16 floating point numbers. The numbers
    # are separated by spaces, with 15 of them followed by a space and the last one at the end of the string. The
    # string before the numbers can be any characters.
    # Example: 'Toronto 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16'
    data_pattern_1 = r".*\s(([-+]?[0-9]*\.?[0-9]+)\s){15}([-+]?[0-9]*\.?[0-9]+)"
    data_regex_1 = re.compile(data_pattern_1)

    # This regular expression matches a string that starts with any characters (including digits within parentheses)
    # followed by a sequence of 16 floating point numbers. The numbers are separated by spaces, with 15 of them
    # followed by a space and the last one at the end of the string.
    # Example: 'Vancouver(Granville St. & 41stAve) 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16'
    data_pattern_2 = r".*\(([^)]*)\)\D*(([-+]?[0-9]*\.?[0-9]+\s){15}([-+]?[0-9]*\.?[0-9]+))"
    data_regex_2 = re.compile(data_pattern_2)

    # Text is analyzed and lines deemed usable data are stored.
    processed = []
    errors = []
    for page in text:
        for line in page:
            line = line.replace('- ', ' -')
            line = line.replace(')', ') ')
            # Save location
            if "Region" in line or line in CANADIAN_PROVINCES_AND_TERRITORIES:
                processed.append([line] + [""] * 16)
            # Save data
            elif data_regex_1.match(line) or data_regex_2.match(line):
                # Separate numerical data from the location
                data = line.split(' ')
                numerical_data = [float(x) for x in data[-16:]]
                location = ' '.join(data[:-16])
                numerical_data.insert(0, location)
                processed.append(numerical_data)
            else:
                if len(line.split(' ')) > 10 and "Division" not in line and "National Research" not in line:
                    errors.append(line)

    print(len(errors))

    # Headers for the data
    layer_one_headers = ["Province and Location", "Elev., m", "Design Temperature", "", "", "",
                         "Degree-Days Below 18°C", "15 Min. Rain, mm", "One Day Rain, 1/50, mm",
                         "Ann. Rain, mm", "Moist Index", "Ann. Tot. Ppn., mm", "Driving Rain Wind Pressures, Pa, 1/5",
                         "Snow Load, kPa, 1/50", "", "Hourly Wind Pressures, kPa", ""]
    layer_two_headers = ["", "", "January", "", "July 2.5%", "", "", "", "", "", "", "", "", "Ss", "Sr", "1/10", "1/50"]
    layer_three_headers = ["", "", "2.5% °C", "1% °C", "Dry °C", "Wet °C", "", "", "", "", "", "", "", "", "", "", ""]

    # Assertions to ensure program correctness
    assert len(layer_one_headers) == len(layer_two_headers) == len(layer_three_headers) == 17
    assert all([len(x) == 17 for x in processed])

    # Optional option to display all rows
    pd.set_option('display.max_rows', None)

    # Save data in the form of a dataframe
    dataframe = pd.DataFrame(processed)
    header = [layer_one_headers, layer_two_headers, layer_three_headers]
    dataframe.columns = header

    # Return the dataframe
    return dataframe


if __name__ == '__main__':
    print(table_c1_extraction())
    print(table_c2_extraction())
    # dataframe_to_excel(table_c1_extraction(), "table_c1.xlsx")
    # dataframe_to_csv(table_c1_extraction(), "table_c1.csv")
    # dataframe_to_excel(table_c2_extraction(), "table_c2.xlsx")
    # dataframe_to_csv(table_c2_extraction(), "table_c2.csv")
