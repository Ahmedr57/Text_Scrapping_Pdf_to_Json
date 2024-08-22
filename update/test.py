import pdfplumber
import json



def match_schema_with_extracted_data(schema, extracted_text):
    matched_data = {}

    lines = extracted_text.splitlines()

    for key, value in schema.items():
        if isinstance(value, dict):
            # Recursively handle nested dictionaries
            nested_data = match_schema_with_extracted_data(value, extracted_text)
            if nested_data:
                matched_data[key] = nested_data

        elif isinstance(value, list):
            # Handle lists (assume each list item is a dictionary)
            matched_list = []
            for item in value:
                matched_item = {}
                for sub_key in item:
                    for line in lines:
                        if sub_key in line:
                            item_value = line.split(":", 1)[-1].strip()
                            matched_item[sub_key] = item_value
                            break
                if matched_item:
                    matched_list.append(matched_item)
            if matched_list:
                matched_data[key] = matched_list

        else:
            # Handle simple key-value pairs
            for line in lines:
                if key in line:
                    matched_data[key] = line.split(":", 1)[-1].strip()
                    break

    return matched_data

# Define your schema (keys with empty or placeholder values)
sds_template = {
    "Identification": {
        "Product Identifier": "",
        "Product Code": [],
        "Synonyms": [],
        "Recommended Use": "",
        "Uses Advised Against": "",
        "Supplier Information": {
            "Name": "",
            "Address": "",
            "Phone": "",
            "Fax": ""
        },
        "Emergency Phone Number": ""
    },
    "Hazards Identification": {
        "Hazard Classifications": {
            "Skin Corrosion/Irritation": "",
            "Eye Damage/Irritation": ""
        },
        "Signal Word": "",
        "Hazard Statements": "",
        "Precautionary Statements": {
            "Prevention": [],
            "Response": [],
            "Storage": "",
            "Disposal": ""
        },
        "Hazards Not Otherwise Classified": []
    },
    "Composition/Information on Ingredients": {
        "Components": [
            {
                "Name": "",
                "Common Names": [],
                "CAS Number": "",
                "Chemical Formula": "",
                "Percent by Weight": ""
            }
        ]
    },
    "First-Aid Measures": {
        "Inhalation": "",
        "Ingestion": "",
        "Skin Contact": "",
        "Eye Contact": ""
    },
    "Firefighting Measures": {
        "Suitable Extinguishing Media": [],
        "Unsuitable Extinguishing Media": "",
        "Hazardous Combustion Products": "",
        "Specific Hazards": "",
        "Special Protective Equipment": ""
    },
    "Accidental Release Measures": {
        "Personal Precautions": "",
        "Methods for Containment": "",
        "Methods for Cleanup": ""
    },
    "Handling and Storage": {
        "Handling": "",
        "Storage": ""
    },
    "Exposure Controls/Personal Protection": {
        "Exposure Limits": {
            "Acetic Acid": {
                "ACGIH": {
                    "TWA": "",
                    "STEL": ""
                },
                "OSHA": {
                    "PEL": ""
                },
                "NIOSH": {
                    "IDL": "",
                    "TWA": "",
                    "STEL": ""
                }
            }
        },
        "Engineering Controls": "",
        "Personal Protective Measures": {
            "Eye/Face Protection": "",
            "Skin Protection": "",
            "Respiratory Protection": ""
        }
    },
    "Physical and Chemical Properties": {
        "Appearance": "",
        "Odor": "",
        "Odor Threshold": "",
        "Formula Weight": "",
        "pH": "",
        "Melting/Freezing Point": "",
        "Boiling Point/Range": "",
        "Decomposition Temperature": "",
        "Flash Point": "",
        "Auto-Ignition Temperature": "",
        "Flammability": "",
        "Solubility": "",
        "Specific Gravity": ""
    },
    "Stability and Reactivity": {
        "Reactivity Data": "",
        "Chemical Stability": "",
        "Conditions to Avoid": [],
        "Incompatible Materials": [],
        "Hazardous Decomposition Products": [],
        "Hazardous Polymerization": ""
    },
    "Toxicological Information": {
        "Routes of Exposure": [],
        "Acute Effects": "",
        "Chronic Effects": "",
        "Toxicological Data": {
            "Acetic Acid": {
                "LD50 Oral Rat": "",
                "LC50 Inhalation Rat": "",
                "LD50 Dermal Rabbit": ""
            }
        },
        "Carcinogenic Effects": ""
    },
    "Ecological Information": {
        "Ecotoxicological Data": {
            "Acetic Acid": {
                "EC50 Water Flea": "",
                "LC50 Fathead Minnow": "",
                "LC50 Rainbow Trout": ""
            }
        },
        "Persistence and Degradability": "",
        "Environmental Effects": ""
    },
    "Disposal Considerations": {
        "Disposal Instructions": "",
        "Contaminated Packaging": ""
    },
    "Transport Information": {
        "DOT": {
            "UN Number": "",
            "Proper Shipping Name": "",
            "Hazard Class": "",
            "Packing Group": "",
            "ERG Number": ""
        }
    },
    "Regulatory Information": {
        "U.S. Federal Regulations": {
            "OSHA": "",
            "TSCA Inventory": ""
        },
        "EPCRA SARA Title III": {
            "Section 311/312": {
                "Hazardous Chemical": "",
                "Immediate Hazard": "",
                "Delayed Hazard": "",
                "Fire Hazard": "",
                "Pressure Hazard": "",
                "Reactivity Hazard": ""
            },
            "CERCLA Reportable Quantities": ""
        },
        "International Inventories": {
            "Australia": "",
            "Canada DSL": "",
            "Canada NDSL": "",
            "China IECSC": "",
            "Europe EINECS": "",
            "Europe ELINCS": "",
            "Japan ENCS": "",
            "Korea ECL": "",
            "Philippines PICCS": ""
        }
    },
    "Other Information": {
        "Disclaimer": "",
        "Issue Date": "",
        "Reason for Revision": ""
    }
}




def extract_data_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:  # Ensure that the text is not None
                full_text += text + "\n"
    return full_text

pdf_path = "D:\\Data Science Test Task\\Acetic_Acid_1N_3-10percent_SDS.pdf"  # Replace with your PDF file path
extracted_data = extract_data_from_pdf(pdf_path)


# Match schema with extracted data
matched_data = match_schema_with_extracted_data(sds_template, extracted_data)

# The matched data now contains the key-value pairs based on the schema
print("Matched Data:", matched_data)

json_output = json.dumps(matched_data, indent=4)
with open("update\\sds.json", "w") as json_file:
    json_file.write(json_output)
