import re

def parse_section_data(section_data):
    """Parse textual data from a section into key-value pairs, handling multiline keys and values."""
    lines = section_data.split('\n')
    section_data_dict = {}
    current_key = None
    current_value = ''
    is_key_line = False

    # Regular expression pattern to match key-value pairs
    key_value_pattern = re.compile(r'^([^\n]+?):\s*(.*)$', re.MULTILINE)

    for line in lines:
        line = line.strip()
        # Check if line matches the key-value pattern
        if key_value_pattern.match(line):
            if current_key:
                # Save the previous key-value pair
                section_data_dict[current_key] = current_value.strip()
                # Special processing for "product code"
                if current_key == "Product Code(s)":
                    section_data_dict[current_key] = [item.strip() for item in current_value.split(',')]
            
            # Extract new key and value
            match = key_value_pattern.match(line)
            current_key, current_value = match.groups()
            current_key = current_key.strip()
            current_value = current_value.strip()
            is_key_line = True
        else:
            # Accumulate multiline values
            if is_key_line:
                current_value += ' ' + line.strip()
                is_key_line = False
            else:
                current_value += ' ' + line.strip()

    # Add the last key-value pair
    if current_key:
        section_data_dict[current_key] = current_value.strip()
        # Special processing for "product code"
        if current_key.lower() == "product code":
            section_data_dict[current_key] = [item.strip() for item in current_value.split(',')]

    return section_data_dict


def parse_table(table):
    """Convert a table extracted by pdfplumber to a list of dictionaries, using column names as keys."""
    if len(table) < 2:
        return table  # Not enough rows for header and data, return as is

    headers = table[0]  # First row as headers
    table_data = []
    
    for row in table[1:]:
        if len(row) == len(headers):
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            table_data.append(row_dict)
        else:
            # Handle rows that do not match header length (e.g., malformed rows)
            # Append as a list of values
            row_dict = {f"Column_{i+1}": cell for i, cell in enumerate(row)}
            table_data.append(row_dict)
    
    return table_data

