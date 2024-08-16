import pdfplumber
from parsers import parse_section_data, parse_table
import re

def extract_data_from_pdf(pdf_path, sections=None):
    data = {}

    # Default sections if none provided
    if sections is None:
        sections = [
            "IDENTIFICATION", "HAZARDS IDENTIFICATION", "COMPOSITION AND INFORMATION ON INGREDIENTS",
            "FIRST AID MEASURES", "FIREFIGHTING MEASURES", "ACCIDENTAL RELEASE MEASURES",
            "HANDLING AND STORAGE", "EXPOSURE CONTROLS AND PERSONAL PROTECTION",
            "PHYSICAL AND CHEMICAL PROPERTIES", "STABILITY AND REACTIVITY",
            "TOXICOLOGICAL INFORMATION", "ECOLOGICAL INFORMATION", "DISPOSAL INFORMATION",
            "TRANSPORT INFORMATION", "REGULATORY INFORMATION", "OTHER INFORMATION"
        ]

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            full_text += text + "\n"
            
            # Extract tables from the page
            tables = page.extract_tables()
            if tables:
                for idx, table in enumerate(tables):
                    data[f'Table_{page.page_number}_{idx + 1}'] = parse_table(table)

        # Extract sections based on predefined patterns
        section_data = extract_sections(full_text, sections)
        data.update(section_data)

    return data

def extract_sections(full_text, sections):
    data = {}
    section_pattern = '|'.join([re.escape(section) for section in sections])
    matches = list(re.finditer(section_pattern, full_text, re.IGNORECASE))

    for i, match in enumerate(matches):
        section_name = match.group().strip()
        start_index = match.end()
        end_index = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        section_data = full_text[start_index:end_index].strip()
        parsed_data = parse_section_data(section_data)
        data[section_name] = parsed_data

    return data
