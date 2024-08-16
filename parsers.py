import re

def parse_section_data(section_data):
    """Parse textual data from a section into key-value pairs."""
    lines = section_data.split('\n')
    section_data_dict = {}
    key = None
    value = ''

    key_value_pattern = re.compile(r'^[\w\s\-/]+:')

    for line in lines:
        line = line.strip()
        if key_value_pattern.match(line):
            if key:
                section_data_dict[key] = value.strip()
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
        else:
            value += ' ' + line.strip()

    if key:
        section_data_dict[key] = value.strip()

    return section_data_dict

def parse_table(table):
    """Convert a table extracted by pdfplumber to a list of dictionaries."""
    if len(table) < 2:
        return table  # Not enough rows for header and data, return as is

    headers = table[0]
    table_data = []
    
    for row in table[1:]:
        if len(row) == len(headers):
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            table_data.append(row_dict)
        else:
            table_data.append(row)
    
    return table_data
