# PDF Data Extraction and Cleaning

This project extracts structured data from PDF documents (such as safety data sheets) using the `pdfplumber` library. The extracted data includes text sections and tables, which are then cleaned and saved as a JSON file.

## Project Structure

- **`extract_data.py`**: Handles the extraction of text and tables from a PDF document.
- **`parsers.py`**: Contains functions to parse the extracted data into structured formats such as dictionaries and lists.
- **`cleaners.py`**: Responsible for cleaning and formatting the extracted data.
- **`main.py`**: The entry point of the project, coordinating the extraction, cleaning, and saving of data.

## Setup

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Install required packages:**
    ```bash
    pip install pdfplumber
    ```

## Usage

1. Place your PDF file in the desired location.
2. Update the `pdf_path` variable in `main.py` with the path to your PDF file.
3. Run the script:
    ```bash
    python main.py
    ```
4. The extracted and cleaned data will be saved as a JSON file (e.g., `cleaned_data11.json`).

## Modularization

The code is organized into different modules to ensure clean separation of concerns:

- **Extraction (`extract_data.py`)**:
  - Opens the PDF and extracts both text and table data.
  - Identifies sections using predefined headers and extracts corresponding content.

- **Parsing (`parsers.py`)**:
  - Converts extracted text and tables into structured formats (e.g., key-value pairs, lists of dictionaries).

- **Cleaning (`cleaners.py`)**:
  - Cleans and formats the extracted data, handling empty values and trimming whitespace.

## Example Output

The output of the script will be a structured JSON file with sections and tables extracted from the PDF. Example:

```json
{
    "IDENTIFICATION": {
        "Product Name": "Acetic Acid",
        "CAS Number": "64-19-7"
    },
    "Table_1_1": [
        {
            "Component": "Acetic Acid",
            "Concentration": "3-10%"
        }
    ]
}
