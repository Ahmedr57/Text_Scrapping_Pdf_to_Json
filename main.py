import json
from extract_data import extract_data_from_pdf
from cleaners import clean_data

def main():
    pdf_path = "D:\\Data Science Test Task\\Acetic_Acid_1N_3-10percent_SDS.pdf"  # Replace with your PDF file path
    extracted_data = extract_data_from_pdf(pdf_path)
    cleaned_data = clean_data(extracted_data)

    # Save cleaned data to JSON
    json_path = 'cleaned_data11.json'
    with open(json_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    # Print JSON response
    with open(json_path, 'r') as f:
        json_response = json.load(f)
        print(json.dumps(json_response, indent=4))

if __name__ == "__main__":
    main()
