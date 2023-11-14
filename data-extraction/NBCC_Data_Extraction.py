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

    # text[0].append('Ladner Fort 3  -6  -8 2 7 1 92 6 0 01 0 8 01 0 0 01 . 11 0 5 0 1 6 01 . 3 0 . 20 . 3 7 0 . 4 6')

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

    # Analyzed lines deemed usable data are stored.
    processed = []
    # Iterating through the pages
    for page in text:
        # Iterating through the lines
        for line in page:
            # Replace '- ' with ' -' to account for negative number errors
            line = line.replace('- ', ' -')
            # Replace ')' with ') ' to account for numbers placed adjacent to a closing parenthesis
            line = line.replace(')', ') ')
            # Add a space between letters and numbers
            line = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', line)
            # Add a space between numbers and letters
            line = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', line)

            # Convert line to a list, splitting at spaces
            data = line.split(' ')
            # Process location line
            # Ex: 'British Columbia' or 'Vancouver Region'
            if "Region" in line or line in CANADIAN_PROVINCES_AND_TERRITORIES:
                processed.append([line] + [""] * 16)
            # Process data line
            # These are lines the OCR was able to read correctly and contain no formatting errors
            # Ex: 'Ocean Falls 10 -10 -12 23 17 3400 13 260 4150 4.2 4300 350 3.9 0.8 0.44 0.59'
            elif data_regex_1.match(line) or data_regex_2.match(line):
                # Separate numerical data from the location
                numerical_data = [float(x) for x in data[-16:]]
                # Get the location from the data by joining all strings before numerical data
                location = ' '.join(data[:-16])
                location = location.strip()

                numerical_data.insert(0, location)
                processed.append(numerical_data)
            # Process error line
            # These are lines that the OCR was not able to read correctly and contain formatting errors
            # There should be very few of these lines, but will require manual correction in the output
            # data, error lines are those whose numerical data is filled with -99
            # Ex: 'Ladner 3  -6  -8 2 7 1 92 6 0 01 0 8 01 0 0 01 . 11 0 5 0 1 6 01 . 3 0 . 20 . 3 7 0 . 4 6'
            elif len(data) > 10 and "Division" not in line and "National Research" not in line:
                data = [x for x in data if '.' and '-' not in x not in x and x != '']
                n = len(data) - 1
                number_regex = re.compile(r'\b\.?\d+(\.\d+)?\b')
                while number_regex.match(data[n]):
                    a = data[n]
                    n -= 1

                location = ' '.join(data[0:n])

                error_data = [location] + [-99 for _ in range(16)]
                processed.append(error_data)

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
