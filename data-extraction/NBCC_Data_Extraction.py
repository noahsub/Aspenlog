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
    Convert Pandas dataframe to excel file and save it to the output directory.

    :param dataframe: The dataframe to save.
    :param filename: The filename of the excel file (ensure to include the .xlsx extension).
    """
    assert ".xlsx" in filename

    dataframe.to_excel(f"output/{filename}")


########################################################################################################################
# DATA EXTRACTION
########################################################################################################################

def table_c1_extraction() -> pd.DataFrame:
    text = pdf_to_text("NBCC2020-Table-C-1.pdf")

    data_pattern = r"^(-?\d+(\.\d+)?\s){7}-?\d+(\.\d+)?$"
    data_regex = re.compile(data_pattern)

    processed = []
    for page in text:
        for line in page:
            if data_regex.match(line):
                processed.append([float(x) for x in line.split(' ')])

    layer_one_headers = ['q', 'V', 'q', 'V', 'q', 'V', 'q', 'V']
    layer_two_headers = ['kPa', 'm/s', 'kPa', 'm/s', 'kPa', 'm/s', 'kPa', 'm/s']

    assert len(layer_one_headers) == len(layer_two_headers) == 8
    assert all([len(x) == 8 for x in processed])

    # optional option to display all rows
    pd.set_option('display.max_rows', None)

    # save data in the form of a dataframe
    dataframe = pd.DataFrame(processed)
    header = [layer_one_headers, layer_two_headers]
    dataframe.columns = header

    # return the dataframe
    return dataframe


def table_c2_extraction() -> pd.DataFrame:
    """
    Extracts data from Table C2 in NBCC2022 pages 650 - 676 and stores them as a Pandas dataframe.

    :return: A Pandas dataframe containing the extracted data.
    """
    # The extracted text
    text = pdf_to_text("NBCC2020-Table-C-2.pdf")

    # The regex used to extract data lines
    data_pattern = r".*\s(([-+]?[0-9]*\.?[0-9]+)\s){15}([-+]?[0-9]*\.?[0-9]+)"
    data_regex = re.compile(data_pattern)

    # Text is analyzed and lines deemed usable data are stored.
    processed = []
    for page in text:
        for line in page:
            # Save location
            if "Region" in line or line in CANADIAN_PROVINCES_AND_TERRITORIES:
                # processed.append(line)
                processed.append([line] + [""] * 16)
            # Save data
            elif data_regex.match(line):
                # Separate numerical data from the location
                data = line.split(' ')
                numerical_data = data[-16:]
                location = ' '.join(data[:-16])
                numerical_data.insert(0, location)
                processed.append(numerical_data)

    # Headers for the data
    layer_one_headers = ["Province and Location", "Elev., m", "Design Temperature", "", "", "",
                         "Degree-Days Below 18°C", "15 Min. Rain, mm", "One Day Rain, 1/50, mm",
                         "Ann. Rain, mm", "Moist Index", "Ann. Tot. Ppn., mm", "Driving Rain Wind Pressures, Pa, 1/5",
                         "Snow Load, kPa, 1/50", "", "Hourly Wind Pressures, kPa", ""]
    layer_two_headers = ["", "", "January", "", "July 2.5%", "", "", "", "", "", "", "", "", "Ss", "Sr", "1/10", "1/50"]
    layer_three_headers = ["", "", "2.5% °C", "1% °C", "Dry °C", "Wet °C", "", "", "", "", "", "", "", "", "", "", ""]

    # assertions to ensure program correctness
    assert len(layer_one_headers) == len(layer_two_headers) == len(layer_three_headers) == 17
    assert all([len(x) == 17 for x in processed])

    # optional option to display all rows
    pd.set_option('display.max_rows', None)

    # save data in the form of a dataframe
    dataframe = pd.DataFrame(processed)
    header = [layer_one_headers, layer_two_headers, layer_three_headers]
    dataframe.columns = header

    # return the dataframe
    return dataframe


if __name__ == '__main__':
    print(table_c1_extraction())
    print(table_c2_extraction())
    # dataframe_to_excel(table_c2_extraction(), "table_c2.xlsx")
