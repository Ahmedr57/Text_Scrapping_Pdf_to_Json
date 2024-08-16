import re

def clean_data(data):
    """Recursively clean extracted data."""
    cleaned_data = {}
    
    for key, value in data.items():
        if isinstance(value, dict):
            cleaned_data[key] = clean_data(value)
        elif isinstance(value, list):
            cleaned_data[key] = [clean_data(item) if isinstance(item, dict) else item for item in value]
        elif value.strip():
            cleaned_data[key] = re.sub(r'\s+', ' ', value.strip())
        else:
            cleaned_data[key] = "Not Provided"
    
    return cleaned_data
