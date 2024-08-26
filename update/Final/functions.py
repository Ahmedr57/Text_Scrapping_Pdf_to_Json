import pdfplumber

schema = {
    "Identification": {
        "Product Identifier": "",
        "Product Code": [],
        "Synonyms": [],
        "Recommended Use": "",
        "Uses Advised Against": "",
        "Supplier": {
            "Name": "",
            "Address": "",
            "Phone": "",
            "Fax": ""
        },
        "Emergency Phone Number": {
            "For health emergency, call poison control" : ""
        }
    },
    "Hazards Identification": {
        "Hazard Classifications": {
            "Skin Corrosion/Irritation": "",
            "Eye Damage/Irritation": ""
        },
        "Signal Word": "",
        "Hazard Statements": "",
        "Picogram": "Not Available",
        "Precautionary Statements": {
            "Prevention": [],
            "Response": {
                "call":"",
                "If swallowed": "",
                "If on skin (or hair)": [],
                "If inhaled": "",
                "If in eyes": [],
            },
            "Storage": "",
            "Disposal": ""
        },
        "Hazards Not Otherwise Classified": [],
        "Toxicity Statement": ""
    },
    "Composition and Information on Ingredients": {
    },
    "First-Aid Measures": {
        "Inhalation": "",
        "Ingestion": "",
        "Skin Contact": "",
        "Eye Contact": "",
        "General Advice" :"",
        "Symptoms and Effects":"",
        "Immediate Medical Care/ Special Treatment": ""

    },
    "Firefighting Measures": {
        "Suitable Extinguishing Media": [],
        "Unsuitable Extinguishing Media": "",
        "Hazardous Combustion Products": "",
        "Specific Hazards": "",
        "Special Protective Equipment/ Precautions for Firefighters": ""
    },
    "Accidental Release Measures": {
        "Personal Precautions and Protective Equipment": "",
        "Emergency Procedures":"",
        "Methods for Containment": "",
        "Methods for Cleanup": ""
    },
    "Handling and Storage": {
        "Handling": "",
        "Storage": ""
    },
    "Exposure Controls and Personal Protection": {
        "Exposure Limits": {
            "water": "",
            "Acetic Acid": {
                "ACGIH": {
                    "TWA": "",
                    "STEL": ""
                },
                "OSHA": {
                    "PEL": ""
                },
                "NIOSH": {
                    "IDLH": "",
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
        },
        "Specific Requirements for Personal Protective Equipment" : ""
    },
    "Physical and Chemical Properties": {
        "properties": "",
        "Appearance": [],
        "Odor": "",
        "Odor Threshold": "",
        "Formula Weight": "",
        "pH": "",
        "Melting/Freezing Point": "",
        "Boiling Point/Range": "",
        "Decomposition Temperature": "",
        "Flash Point": "",
        "Auto-ignition Temperature": "",
        "Flammability": "",
        "Flammability/Explosive Limits": "",       
        "Solubility": "",
        "Vapor Pressure": "",
        "Vapor Density": "",
        "Specific Gravity": "",
        "Evaporation Rate": "",
        "Viscosity": "",
        "Partition Coefficient (n-octanol/water)": "",
    },
    "Stability and Reactivity": {
        "Reactivity Data": "",
        "Chemical Stability": "",
        "Conditions to Avoid": [],
        "Incompatible Materials": [],
        "Hazardous Decomposition Products": [],
        "Possibility of Hazardous Reactions": "",
        "Hazardous Polymerization": ""
    },
    "Toxicological Information": {
        "Routes of Exposure": [],
        "Acute Effects": [],
        "Chronic Effects": [],
        "Toxicological Data": {
            "Water": "",
            "Acetic Acid": {
                "LD50, Oral, Rat": "",
                "LC50, Inhalation, Rat": "",
                "LD50, Dermal, Rabbit": "",
                "based" : ""
            }
        },
        "Symptoms of Exposure": [],
        "Carcinogenic Effects": ""
    },
    "Ecological Information": {
        "Ecotoxicological Data": {
            "Water": "",
            "Acetic Acid": {
                "EC50, Water Flea (Daphnia magna)": "",
                "LC50, Fathead Minnow (Pimephales promelas)": "",
                "LC50, Rainbow Trout (Oncorhynchus mykiss)": ""
            }
        },
        "Persistence and Degradability": [],
        "Environmental Effects": []
    },
    "Disposal Information": {
        "Disposal Instructions": "",
        "Contaminated Packaging": "",
        "Waste Codes": "",
    },
    "Transport Information": {
        "DOT": {
            "< 10% w/w":"",
            "A1006":{
                "UN Number": "",
                "Proper Shipping Name": "",
                "Hazard Class": "",
                "Packing Group": "",
                "ERG Number": ""
            },
        "Environmental Hazard Regulations": "",
        "Other Transport Precautions": {
            "Acetic Acid": {
                "DOT Reportable Quantity": "",
                }
            }
        }
    },
    "Regulatory Information": {
        "U.S. Federal Regulations": {
            "OSHA": "",
            "TSCA Inventory": ""
        },
        "U.S. EPCRA (SARA Title III)": {
            "Section 302":"",
            "Section 311/312": {},
            "Section 313": ""  
        },
        "CERCLA Reportable Quantities": {
            "Acetic Acid, Glacial": ""
        },
        "International Inventories": {},
        "listed": "",
    },"Other Information": {
        "Disclaimer": "",
        "Issue Date": "",
        "Reason for Revision": ""
    }
}

def parse_table(table):
    """Convert a table extracted by pdfplumber to a list of dictionaries, using column names as keys."""
    if len(table) < 2:
        return table  # Not enough rows for header and data, return as is

    headers = table[0]  # First row as headers
    table_data = []
    
    for row in table[1:]:
        if len(row) == len(headers) and row:
            row_dict = {headers[i]: row[i] for i in range(len(headers))}
            table_data.append(row_dict)
        else:
            # Handle rows that do not match header length (e.g., malformed rows)
            # Append as a list of values
            row_dict = {f"Column_{i+1}": cell for i, cell in enumerate(row)}
            table_data.append(row_dict)
    
    return table_data

# 1st Section
def extract_identification_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_identification = False
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            for i, line in enumerate(lines):
                if "IDENTIFICATION" in line.upper() and not found_identification:
                    found_identification = True
                    continue  # Skip the section heading

                if found_identification:
                    if "Product Identifier" in line:
                        schema["Identification"]["Product Identifier"] = line.split(":", 1)[-1].strip()
                    
                    elif "Product Code" in line:
                        schema["Identification"]["Product Code"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                    
                    elif "Synonyms" in line:
                        schema["Identification"]["Synonyms"] = [item.strip() for item in line.split(":", 1)[-1].split(";")]

                    elif "Recommended Use" in line:
                        schema["Identification"]["Recommended Use"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Uses Advised Against" not in lines[i + 1]:
                            schema["Identification"]["Recommended Use"] += " " + lines[i + 1].strip()

                    elif "Uses Advised Against" in line:
                        schema["Identification"]["Uses Advised Against"] = line.split(":", 1)[-1].strip()
                    
                    elif "Supplier" in line:
                        schema["Identification"]["Supplier"]["Name"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Address" not in lines[i + 1]:
                            schema["Identification"]["Supplier"]["Address"] += " " + lines[i + 1].strip()
                    
                    if "Phone" in line:
                        # Split the line by "Fax" to separate phone and fax parts
                        phone_fax_parts = line.split("Fax", 1)
                        
                        # Extract the phone number by splitting the first part by ":"
                        if not schema["Identification"]["Supplier"]["Phone"]:
                            schema["Identification"]["Supplier"]["Phone"] = phone_fax_parts[0].split(":", 1)[-1].strip()
    
                        # Extract the fax number by splitting the second part by ":"
                        if len(phone_fax_parts) > 1:
                            schema["Identification"]["Supplier"]["Fax"] = phone_fax_parts[1].split(":", 1)[-1].strip()                  
                    if "Emergency Phone Number" in line:
                        if "For health emergency, call poison control" in line:
                            schema["Identification"]["Emergency Phone Number"]["For health emergency, call poison control"] = line.split(":", 6)[-1].strip()

                    #stop when the next section is reached
                    if any(keyword in line.upper() for keyword in ["HAZARDS IDENTIFICATION"]):
                        return schema

    return schema
# 2nd Section
def extract_hazards_identification_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_hazards_identification = False
        fulltext = ""
        for page in pdf.pages[:2]:
            text = page.extract_text()
            if text:
                fulltext+=text + "\n"
            lines = fulltext.split("\n")

            
    
        for i, line in enumerate(lines):
            if "HAZARDS IDENTIFICATION" in line.upper() and not found_hazards_identification:
                found_hazards_identification = True
                continue

            if found_hazards_identification:

                if "Skin Corrosion/Irritation" in line:
                    schema["Hazards Identification"]["Hazard Classifications"]["Skin Corrosion/Irritation"] = line.split(":", 3)[-1].strip()
                elif "Eye Damage/Irritation" in line:
                    schema["Hazards Identification"]["Hazard Classifications"]["Eye Damage/Irritation"] = line.split(":", 1)[-1].strip()
                elif "Signal Word" in line:
                    schema["Hazards Identification"]["Signal Word"] = line.split(":", 1)[-1].strip()
                elif "Hazard Statements" in line:
                    schema["Hazards Identification"]["Hazard Statements"] = line.split(":", 1)[-1].strip()
            
                if "Prevention" in line:
                        schema["Hazards Identification"]["Precautionary Statements"]["Prevention"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Response" not in lines[i + 1]:
                            schema["Hazards Identification"]["Precautionary Statements"]["Prevention"] += " " + lines[i + 1].strip()
                            j = i + 2
                            while j < len(lines) and not any(keyword in lines[j] for keyword in ["Response", "Storage", "Disposal"]):
                                schema["Hazards Identification"]["Precautionary Statements"]["Prevention"] += " " + lines[j].strip()
                                j += 1
                            schema["Hazards Identification"]["Precautionary Statements"]["Prevention"] = [item.strip() for item in schema["Hazards Identification"]["Precautionary Statements"]["Prevention"].split(".")]
                elif "Response" in line:
                        if "call" in line:
                            schema["Hazards Identification"]["Precautionary Statements"]["Response"]["call"] = line.split(":", 1)[-1].strip()
                if "If swallowed" in line:
                    schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If swallowed"] = [item.strip() for item in line.split(":", 1)[-1].split(".")]
                elif "If on skin (or hair)" in line:
                    schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If on skin (or hair)"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "If inhaled" not in lines[i + 1]:
                        schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If on skin (or hair)"] += " " + lines[i + 1].strip()
                        schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If on skin (or hair)"] = [item.strip() for item in schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If on skin (or hair)"].split(".")]
                elif "If inhaled" in line:
                    schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If inhaled"] = line.split(":", 1)[-1].strip()
                elif "If in eyes" in line:
                    schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If in eyes"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Storage" not in lines[i + 1]:
                        schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If in eyes"] += " " + lines[i + 1].strip()
                        schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If in eyes"] = [item.strip() for item in schema["Hazards Identification"]["Precautionary Statements"]["Response"]["If in eyes"].split(".")]
                elif "Storage" in line:
                        schema["Hazards Identification"]["Precautionary Statements"]["Storage"] = line.split(":", 1)[-1].strip()
                elif "Disposal" in line:
                        schema["Hazards Identification"]["Precautionary Statements"]["Disposal"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Hazards Not Otherwise" not in lines[i + 1]:
                            schema["Hazards Identification"]["Precautionary Statements"]["Disposal"] += " " + lines[i + 1].strip()
                            
                elif "Hazards Not Otherwise" in line:
                    schema["Hazards Identification"]["Hazards Not Otherwise Classified"] = line.split(" ", 3)[-1].strip()
                    if i + 1 < len(lines) and "Toxicity Statement" not in lines[i + 1]:
                        schema["Hazards Identification"]["Hazards Not Otherwise Classified"] += " " + lines[i + 1].strip()
                        schema["Hazards Identification"]["Hazards Not Otherwise Classified"] = [item.strip() for item in schema["Hazards Identification"]["Hazards Not Otherwise Classified"].split(".")]
                elif "Toxicity Statement" in line:
                    schema["Hazards Identification"]["Toxicity Statement"] = line.split(":", 1)[-1].strip()
                
                if any(keyword in line.upper() for keyword in ["COMPOSITION AND INFORMATION ON INGREDIENTS"]):
                    return schema

    return schema
# 3rd Section
def extract_composition_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_composition = False
        page = pdf.pages[1]
        text = page.extract_text()
        lines = text.split("\n")

        tables = page.extract_tables()

        for line in lines:
            if "COMPOSITION AND INFORMATION ON INGREDIENTS" in line.upper() and not found_composition:
                found_composition = True
                continue
            
            if found_composition:
                
                if tables:
                    # Extract the first table found in the section
                    for table in tables:
                        schema["Composition and Information on Ingredients"]["Composition and Information on Ingredients"] = parse_table(table)
                      # Assuming only one table is present; stop further processing
                if "Trade Secret Statement" in line:
                    schema["Composition and Information on Ingredients"]["Trade Secret Statement"] = line.split(":", 1)[-1].strip()
                    
                if any(keyword in line.upper() for keyword in ["FIRST AID MEASURES"]):
                    return schema
            

    return schema
# 4th Section
def extract_first_aid_measures_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_first_aid_measures = False
        pager = pdf.pages[1]
        text = pager.extract_text()
        lines = text.split("\n")

        for i, line in enumerate(lines):
            if "FIRST AID MEASURES" in line.upper() and not found_first_aid_measures:
                found_first_aid_measures = True
                continue  # Skip the section heading

            if found_first_aid_measures:

                if "Inhalation" in line:
                    if not schema["First-Aid Measures"]["Inhalation"]:
                        schema["First-Aid Measures"]["Inhalation"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Ingestion" not in lines[i + 1]:
                            schema["First-Aid Measures"]["Inhalation"] += " " + lines[i + 1].strip()
                            j = i + 2
                            while j < len(lines) and not any(keyword in lines[j] for keyword in ["Ingestion", "Skin Contact", "Eye Contact", "General Advice", "Symptoms and Effects", "Immediate Medical Care/ Special Treatment"]):
                                schema["First-Aid Measures"]["Inhalation"] += " " + lines[j].strip()
                                j += 1
                                    
                elif "Ingestion" in line:
                    schema["First-Aid Measures"]["Ingestion"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Skin Contact" not in lines[i + 1]:
                        schema["First-Aid Measures"]["Ingestion"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Skin Contact", "Eye Contact", "General Advice", "Symptoms and Effects", "Immediate Medical Care/ Special Treatment"]):
                            schema["First-Aid Measures"]["Ingestion"] += " " + lines[j].strip()
                            j += 1
                elif "Skin Contact" in line:
                    schema["First-Aid Measures"]["Skin Contact"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Eye Contact" not in lines[i + 1]:
                        schema["First-Aid Measures"]["Skin Contact"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Eye Contact", "General Advice", "Symptoms and Effects", "Immediate Medical Care/ Special Treatment"]):
                            schema["First-Aid Measures"]["Skin Contact"] += " " + lines[j].strip()
                            j += 1
                elif "Eye Contact" in line:
                    schema["First-Aid Measures"]["Eye Contact"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "General Advice" not in lines[i + 1]:
                        schema["First-Aid Measures"]["Eye Contact"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["General Advice", "Symptoms and Effects", "Immediate Medical Care/ Special Treatment"]):
                            schema["First-Aid Measures"]["Eye Contact"] += " " + lines[j].strip()
                            j += 1
                elif "General Advice" in line:
                    schema["First-Aid Measures"]["General Advice"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Symptoms and Effects" not in lines[i + 1]:
                        schema["First-Aid Measures"]["General Advice"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Symptoms and Effects", "Immediate Medical Care/ Special Treatment"]):
                            schema["First-Aid Measures"]["General Advice"] += " " + lines[j].strip()
                            j += 1
                if "Symptoms and Effects" in line:
                    schema["First-Aid Measures"]["Symptoms and Effects"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Immediate Medical Care" not in lines[i + 1]:
                        schema["First-Aid Measures"]["Symptoms and Effects"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Immediate Medical Care", "Special Treatment"]):
                            schema["First-Aid Measures"]["Symptoms and Effects"] += " " + lines[j].strip()
                            j += 1
                elif "Immediate Medical Care" in line:
                    schema["First-Aid Measures"]["Immediate Medical Care"] = line.split("/", 1)[-1].strip()
                elif "Special Treatment" in line:
                    schema["First-Aid Measures"]["Special Treatment"] = line.split(":", 1)[-1].strip()
                        
                    
                # Stop when encountering a new section header
                if any(keyword in line.upper() for keyword in ["FIREFIGHTING MEASURES"]):
                    return schema
                    
            if "Immediate Medical Care" in schema["First-Aid Measures"] and "Special Treatment" in schema["First-Aid Measures"]:
                combined_value = f"{schema['First-Aid Measures']['Immediate Medical Care']} {schema['First-Aid Measures']['Special Treatment']}"
                schema["First-Aid Measures"]["Immediate Medical Care/ Special Treatment"] = combined_value

                # Optionally remove the original keys
                del schema["First-Aid Measures"]["Immediate Medical Care"]
                del schema["First-Aid Measures"]["Special Treatment"]
    return schema
# 5th Section
def extract_firefighting_measures_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_firefighting_measures = False
        pager = pdf.pages[2]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "FIREFIGHTING MEASURES" in line.upper() and not found_firefighting_measures:
                found_firefighting_measures = True
                continue  # Skip the section heading
            
            if found_firefighting_measures:
                                    
                if "Suitable Extinguishing Media" in line:
                    schema["Firefighting Measures"]["Suitable Extinguishing Media"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                elif "Unsuitable Extinguishing Media" in line:
                    schema["Firefighting Measures"]["Unsuitable Extinguishing Media"] = line.split(":", 1)[-1].strip()
                elif "Hazardous Combustion" in line:
                    schema["Firefighting Measures"]["Hazardous Combustion"] = line.split(" ", 2)[-1].strip()
                elif "Products" in line:
                    schema["Firefighting Measures"]["Products"] = line.split(":", 1)[-1].strip()
                elif "Specific Hazards" in line:
                    schema["Firefighting Measures"]["Specific Hazards"] = line.split(":", 1)[-1].strip()
                elif "Special Protective Equipment" in line:
                    schema["Firefighting Measures"]["Special Protective Equipment"] = line.split("/", 1)[-1].strip()
                elif "Precautions for Firefighters" in line:
                    schema["Firefighting Measures"]["Precautions for Firefighters"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Suitable Extinguishing Media" not in lines[i + 1]:
                        schema["Firefighting Measures"]["Precautions for Firefighters"] += " " + lines[i + 1].strip()
                        
                    
                # Stop when encountering a new section header
                if any(keyword in line.upper() for keyword in ["ACCIDENTAL RELEASE MEASURES"]):
                    return schema
                    
            if "Special Protective Equipment" in schema["Firefighting Measures"] and "Precautions for Firefighters" in schema["Firefighting Measures"]:
                combined_value = f"{schema['Firefighting Measures']['Special Protective Equipment']} {schema['Firefighting Measures']['Precautions for Firefighters']}"
                schema["Firefighting Measures"]["Special Protective Equipment/ Precautions for Firefighters"] = combined_value

                # Optionally remove the original keys
                del schema["Firefighting Measures"]["Special Protective Equipment"]
                del schema["Firefighting Measures"]["Precautions for Firefighters"]
            if "Hazardous Combustion" in schema["Firefighting Measures"] and "Products" in schema["Firefighting Measures"]:
                combined_value = f"{schema['Firefighting Measures']['Hazardous Combustion']} {schema['Firefighting Measures']['Products']}"
                schema["Firefighting Measures"]["Hazardous Combustion Products"] = combined_value

                # Optionally remove the original keys
                del schema["Firefighting Measures"]["Hazardous Combustion"]
                del schema["Firefighting Measures"]["Products"]
    return schema
# 6th Section
def extract_accidental_release_measures_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_accidental_release_measures = False
        pager = pdf.pages[2]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "ACCIDENTAL RELEASE MEASURES" in line.upper() and not found_accidental_release_measures:
                found_accidental_release_measures = True
                continue  # Skip the section heading


            if found_accidental_release_measures:
                                    
                if "Personal Precautions and" in line:
                    schema["Accidental Release Measures"]["Personal Precautions and"] = line.split(" ", 3)[-1].strip()
                    if i + 1 < len(lines) and "Protective Equipment" not in lines[i + 1]:
                        schema["Accidental Release Measures"]["Personal Precautions and"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Protective Equipment","Emergency Procedures", "Methods for Containment", "Methods for Cleanup"]):
                            schema["Accidental Release Measures"]["Personal Precautions and"] += " " + lines[j].strip()
                            j += 1
                elif "Protective Equipment" in line:
                    schema["Accidental Release Measures"]["Protective Equipment"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Protective Equipment" not in lines[i + 1]:
                        schema["Accidental Release Measures"]["Protective Equipment"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Emergency Procedures", "Methods for Containment", "Methods for Cleanup"]):
                            schema["Accidental Release Measures"]["Protective Equipment"] += " " + lines[j].strip()
                            j += 1
                elif "Emergency Procedures" in line:
                    schema["Accidental Release Measures"]["Emergency Procedures"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Methods for Containment" not in lines[i + 1]:
                        schema["Accidental Release Measures"]["Emergency Procedures"] += " " + lines[i + 1].strip()
                elif "Methods for Containment" in line:
                    schema["Accidental Release Measures"]["Methods for Containment"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Methods for Cleanup" not in lines[i + 1]:
                        schema["Accidental Release Measures"]["Methods for Containment"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Methods for Cleanup"]):
                            schema["Accidental Release Measures"]["Methods for Containment"] += " " + lines[j].strip()
                            j += 1
                elif "Methods for Cleanup" in line:
                    schema["Accidental Release Measures"]["Methods for Cleanup"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines):
                        schema["Accidental Release Measures"]["Methods for Cleanup"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["HANDLING AND STORAGE"]):
                            schema["Accidental Release Measures"]["Methods for Cleanup"] += " " + lines[j].strip()
                            j += 1                        
                        
                    
                # Stop when encountering a new section header
                if any(keyword in line.upper() for keyword in ["HANDLING AND STORAGE"]):
                    return schema
                    
            if "Personal Precautions and" in schema["Accidental Release Measures"] and "Protective Equipment" in schema["Accidental Release Measures"]:
                combined_value = f"{schema['Accidental Release Measures']['Personal Precautions and']} {schema['Accidental Release Measures']['Protective Equipment']}"
                schema["Accidental Release Measures"]["Personal Precautions and Protective Equipment"] = combined_value

                # Optionally remove the original keys
                del schema["Accidental Release Measures"]["Personal Precautions and"]
                del schema["Accidental Release Measures"]["Protective Equipment"]


    return schema
# 7th Section
def extract_handling_and_storage_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_handling_and_storage = False
        pager = pdf.pages[2]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "HANDLING AND STORAGE" in line.upper() and not found_handling_and_storage:
                found_handling_and_storage = True
                continue  # Skip the section heading


            if found_handling_and_storage:
                if "Handling" in line:
                    schema["Handling and Storage"]["Handling"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Storage" not in lines[i + 1]:
                        schema["Handling and Storage"]["Handling"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Storage"]):
                            schema["Handling and Storage"]["Handling"] += " " + lines[j].strip()
                            j += 1
                elif "Storage" in line:
                    schema["Handling and Storage"]["Storage"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines):
                        schema["Handling and Storage"]["Storage"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["EXPOSURE CONTROLS AND PERSONAL PROTECTION"]):
                            schema["Handling and Storage"]["Storage"] += " " + lines[j].strip()
                            j += 1
                                    
                
                    
                # Stop when encountering a new section header
                if any(keyword in line.upper() for keyword in ["HEXPOSURE CONTROLS AND PERSONAL PROTECTION"]):
                    return schema
                    


    return schema
# 8th Section
def extract_exposure_controls_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_exposure_controls = False
        fulltext = ""
        for page in pdf.pages[2:4]:
            text = page.extract_text()
            if text:
                fulltext+=text + "\n"
            lines = fulltext.split("\n")
    
        for i, line in enumerate(lines):
            if "EXPOSURE CONTROLS AND PERSONAL PROTECTION" in line.upper() and not found_exposure_controls:
                found_exposure_controls = True
                continue

            if found_exposure_controls:
                if "Exposure Limits" in line:
                    schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["water"] = line.split(":", 2)[-1].strip()
                elif "Acetic Acid" in line:
                    if "ACGIH" in line:
                        if "TWA" in line:
                            schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["ACGIH"]["TWA"] = line.split(":", 3)[-1].strip()
                elif "STEL" in line:
                    schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["ACGIH"]["STEL"] = line.split(":", 1)[-1].strip()
                elif "OSHA" in line:
                    schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["OSHA"]["PEL"] = line.split(":", 2)[-1].strip()
                elif "NIOSH" in line:
                    if "IDLH" in line:
                        schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["NIOSH"]["IDLH"] = line.split(":", 2)[-1].strip()
                elif "TWA" in line:
                    schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["NIOSH"]["TWA"] = line.split(":", 1)[-1].strip()
                if "STEL" in line:
                    schema["Exposure Controls and Personal Protection"]["Exposure Limits"]["Acetic Acid"]["NIOSH"]["STEL"] = line.split(":", 1)[-1].strip()
                elif "Engineering Controls" in line:
                    schema["Exposure Controls and Personal Protection"]["Engineering Controls"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Personal Protective Measures" not in lines[i + 1]:
                        schema["Exposure Controls and Personal Protection"]["Engineering Controls"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Personal Protective Measures"]):
                            schema["Exposure Controls and Personal Protection"]["Engineering Controls"] += " " + lines[j].strip()
                            j += 1
                if "Eye/Face Protection" in line:
                        schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Eye/Face Protection"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Skin Protection" not in lines[i + 1]:
                            schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Eye/Face Protection"] += " " + lines[i + 1].strip()
                            j = i + 2
                            while j < len(lines) and not any(keyword in lines[j] for keyword in ["Skin Protection"]):
                                schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Eye/Face Protection"] += " " + lines[j].strip()
                                j += 1
                elif "Skin Protection" in line:
                        schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Skin Protection"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Respiratory Protection" not in lines[i + 1]:
                            schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Skin Protection"] += " " + lines[i + 1].strip()
                            j = i + 2
                            while j < len(lines) and not any(keyword in lines[j] for keyword in ["Respiratory Protection"]):
                                schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Skin Protection"] += " " + lines[j].strip()
                                j += 1
                elif "Respiratory Protection" in line:
                        schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Respiratory Protection"] = line.split(":", 1)[-1].strip()
                        if i + 1 < len(lines) and "Specific Requirements" not in lines[i + 1]:
                            schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Respiratory Protection"] += " " + lines[i + 1].strip()
                            j = i + 2
                            while j < len(lines) and not any(keyword in lines[j] for keyword in ["Specific Requirements"]):
                                schema["Exposure Controls and Personal Protection"]["Personal Protective Measures"]["Respiratory Protection"] += " " + lines[j].strip()
                                j += 1
                elif "Specific Requirements" in line:
                    schema["Exposure Controls and Personal Protection"]["Specific Requirements"] = line.split(" ", 2)[-1].strip()
                elif "for Personal Protective" in line:
                    schema["Exposure Controls and Personal Protection"]["for Personal Protective"] = line.split(" ", 3)[-1].strip()
                elif "Equipment" in line:
                    schema["Exposure Controls and Personal Protection"]["Equipment"] = line.split(":", 1)[-1].strip()
                    

                if any(keyword in line.upper() for keyword in ["PHYSICAL AND CHEMICAL PROPERTIES"]):
                    return schema
                if "Specific Requirements" in schema["Exposure Controls and Personal Protection"] and "for Personal Protective" in schema["Exposure Controls and Personal Protection"] and "Equipment" in schema["Exposure Controls and Personal Protection"]:
                    combined_value = f"{schema['Exposure Controls and Personal Protection']['Specific Requirements']} {schema['Exposure Controls and Personal Protection']['for Personal Protective']} {schema['Exposure Controls and Personal Protection']['Equipment']}"
                    schema["Exposure Controls and Personal Protection"]["Specific Requirements for Personal Protective Equipment"] = combined_value

                    # Optionally remove the original keys
                    del schema["Exposure Controls and Personal Protection"]["Specific Requirements"]
                    del schema["Exposure Controls and Personal Protection"]["for Personal Protective"]
                    del schema["Exposure Controls and Personal Protection"]["Equipment"]
                  


    return schema
# 9th Section
def extract_physical_property_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_physical_property = False
        fulltext = ""
        for page in pdf.pages[3:5]:
            text = page.extract_text()
            if text:
                fulltext+=text + "\n"
            lines = fulltext.split("\n")
    
        for i, line in enumerate(lines):
            if " PHYSICAL AND CHEMICAL PROPERTIES" in line.upper() and not found_physical_property:
                found_physical_property = True
                continue

            if found_physical_property:
                if "properties" in line:
                    schema["Physical and Chemical Properties"]["properties"] = line.strip()
                if "Appearance" in line:
                    schema["Physical and Chemical Properties"]["Appearance"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                elif "Odor" in line:
                    # Only set the value if it's not already set
                    if not schema["Physical and Chemical Properties"]["Odor"]:
                        schema["Physical and Chemical Properties"]["Odor"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]

                if "Odor Threshold" in line:
                    schema["Physical and Chemical Properties"]["Odor Threshold"] = line.split(":", 1)[-1].strip()
                elif "Formula Weight" in line:
                    schema["Physical and Chemical Properties"]["Formula Weight"] = line.split(":", 1)[-1].strip()
                elif "pH" in line:
                    schema["Physical and Chemical Properties"]["pH"] = line.split(":", 1)[-1].strip()
                elif "Melting/Freezing Point" in line:
                    schema["Physical and Chemical Properties"]["Melting/Freezing Point"] = line.split(":", 1)[-1].strip()
                elif "Boiling Point/Range" in line:
                    schema["Physical and Chemical Properties"]["Boiling Point/Range"] = line.split(":", 1)[-1].strip()
                elif "Decomposition Temperature" in line:
                    schema["Physical and Chemical Properties"]["Decomposition Temperature"] = line.split(":", 1)[-1].strip()
                elif "Flash Point" in line:
                    schema["Physical and Chemical Properties"]["Flash Point"] = line.split(":", 1)[-1].strip()
                elif "Auto-ignition Temperature" in line:
                    schema["Physical and Chemical Properties"]["Auto-ignition Temperature"] = line.split(":", 1)[-1].strip()
                elif "Flammability" in line:
                    schema["Physical and Chemical Properties"]["Flammability"] = line.split(":", 1)[-1].strip()
                if "Flammability/Explosive Limits" in line:
                    schema["Physical and Chemical Properties"]["Flammability/Explosive Limits"] = line.split(":", 1)[-1].strip()
                elif "Solubility" in line:
                    schema["Physical and Chemical Properties"]["Solubility"] = line.split(":", 1)[-1].strip()
                elif "Vapor Pressure" in line:
                    schema["Physical and Chemical Properties"]["Vapor Pressure"] = line.split(":", 1)[-1].strip()
                elif "Vapor Density" in line:
                    schema["Physical and Chemical Properties"]["Vapor Density"] = line.split(":", 1)[-1].strip()
                elif "Specific Gravity" in line:
                    schema["Physical and Chemical Properties"]["Specific Gravity"] = line.split(":", 1)[-1].strip()
                elif "Evaporation Rate" in line:
                    schema["Physical and Chemical Properties"]["Evaporation Rate"] = line.split(":", 1)[-1].strip()
                elif "Viscosity" in line:
                    schema["Physical and Chemical Properties"]["Viscosity"] = line.split(":", 1)[-1].strip()
                elif "Partition Coefficient" in line:
                    schema["Physical and Chemical Properties"]["Partition Coefficient (n-octanol/water)"] = line.split(" ", 2)[-1].strip()


                if any(keyword in line.upper() for keyword in ["STABILITY AND REACTIVITY"]):
                    return schema
                  
    return schema
# 10th Section
def extract_stability_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_stability = False
        pager = pdf.pages[4]
        text = pager.extract_text()
        lines = text.split("\n")


        for i, line in enumerate(lines):
            if "STABILITY AND REACTIVITY" in line.upper() and not found_stability:
                found_stability = True
                continue  # Skip the section heading
            
            if found_stability:

                if "Reactivity Data" in line:
                    schema["Stability and Reactivity"]["Reactivity Data"] = line.split(":", 1)[-1].strip()
                elif "Chemical Stability" in line:
                    schema["Stability and Reactivity"]["Chemical Stability"] = line.split(":", 1)[-1].strip()
                elif "Conditions to Avoid" in line:
                    schema["Stability and Reactivity"]["Conditions to Avoid"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                elif "Incompatible Materials" in line:
                    schema["Stability and Reactivity"]["Incompatible Materials"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                elif "Hazardous Decomposition" in line:
                    schema["Stability and Reactivity"]["Hazardous Decomposition Products"] = [item.strip() for item in line.split(" ", 2)[-1].split(",")]
                elif "Possibility of Hazardous" in line:
                    schema["Stability and Reactivity"]["Possibility of Hazardous Reactions"] = line.split(" ", 3)[-1].strip()
                    if i + 1 < len(lines) and "Hazardous Polymerization" not in lines[i + 1]:
                        schema["Stability and Reactivity"]["Possibility of Hazardous Reactions"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Hazardous Polymerization"]):
                            schema["Stability and Reactivity"]["Possibility of Hazardous Reactions"] += " " + lines[j].strip()
                            j += 1
                elif "Hazardous Polymerization" in line:
                    schema["Stability and Reactivity"]["Hazardous Polymerization"] = line.split(":", 1)[-1].strip()
                    

                # Stop when encountering a new section header
                if any(keyword in line.upper() for keyword in ["TOXICOLOGICAL INFORMATION"]):
                    return schema



    return schema
# 11th Section
def extract_toxicological_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_toxicological = False
        pager = pdf.pages[4]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "TOXICOLOGICAL INFORMATION" in line.upper() and not found_toxicological:
                found_toxicological = True
                continue  # Skip the section heading

                
            if found_toxicological:

                if "Routes of Exposure" in line:
                    schema["Toxicological Information"]["Routes of Exposure"] = [item.strip() for item in line.split(":", 1)[-1].split(",")]
                elif "Acute Effects" in line:
                    schema["Toxicological Information"]["Acute Effects"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Chronic Effects" not in lines[i + 1]:
                        schema["Toxicological Information"]["Acute Effects"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Chronic Effects"]):
                            schema["Toxicological Information"]["Acute Effects"] += " " + lines[j].strip()
                            j += 1
                        schema["Toxicological Information"]["Acute Effects"] = [item.strip() for item in schema["Toxicological Information"]["Acute Effects"].split(".")]
                elif "Chronic Effects" in line:
                    schema["Toxicological Information"]["Chronic Effects"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Toxicological Data" not in lines[i + 1]:
                        schema["Toxicological Information"]["Chronic Effects"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Toxicological Data"]):
                            schema["Toxicological Information"]["Chronic Effects"] += " " + lines[j].strip()
                            j += 1
                        schema["Toxicological Information"]["Chronic Effects"] = [item.strip() for item in schema["Toxicological Information"]["Chronic Effects"].split(".")]
                elif "Water" in line:
                        if not schema["Toxicological Information"]["Toxicological Data"]["Water"]:
                            schema["Toxicological Information"]["Toxicological Data"]["Water"] = line.split(":", 1)[-1].strip()
                if "LD50, Oral, Rat" in line:
                        schema["Toxicological Information"]["Toxicological Data"]["Acetic Acid"]["LD50, Oral, Rat"] = line.split(":", 3)[-1].strip()
                elif "LC50, Inhalation, Rat" in line:
                        schema["Toxicological Information"]["Toxicological Data"]["Acetic Acid"]["LC50, Inhalation, Rat"] = line.split(":", 1)[-1].strip()
                elif "LD50, Dermal, Rabbit" in line:
                        schema["Toxicological Information"]["Toxicological Data"]["Acetic Acid"]["LD50, Dermal, Rabbit"] = line.split(":", 1)[-1].strip()
                elif "based" in line:
                        schema["Toxicological Information"]["Toxicological Data"]["Acetic Acid"]["based"] = line.split(":", 1)[-1].strip()
                elif "Symptoms of Exposure" in line:
                    schema["Toxicological Information"]["Symptoms of Exposure"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Carcinogenic Effects" not in lines[i + 1]:
                        schema["Toxicological Information"]["Symptoms of Exposure"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Carcinogenic Effects"]):
                            schema["Toxicological Information"]["Symptoms of Exposure"] += " " + lines[j].strip()
                            j += 1
                        schema["Toxicological Information"]["Symptoms of Exposure"] = [item.strip() for item in schema["Toxicological Information"]["Symptoms of Exposure"].split(",")]
                elif "Carcinogenic Effects" in line:
                    schema["Toxicological Information"]["Carcinogenic Effects"] = line.split(":", 1)[-1].strip()
          
                


    return schema
# 12th Section
def extract_ecological_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_ecological = False
        fulltext = ""
        for page in pdf.pages[4:6]:
            text = page.extract_text()
            if text:
                fulltext+=text + "\n"
            lines = fulltext.split("\n")
    
        for i, line in enumerate(lines):
            if "ECOLOGICAL INFORMATION" in line.upper() and not found_ecological:
                found_ecological = True
                continue

            if found_ecological:


                if "Water" in line:
                        if not schema["Ecological Information"]["Ecotoxicological Data"]["Water"]:
                            schema["Ecological Information"]["Ecotoxicological Data"]["Water"] = line.split(":", 1)[-1].strip()
                if "EC50, Water Flea (Daphnia magna)" in line:
                        schema["Ecological Information"]["Ecotoxicological Data"]["Acetic Acid"]["EC50, Water Flea (Daphnia magna)"] = line.split(":", 5)[-1].strip()
                elif "LC50, Fathead Minnow (Pimephales promelas)" in line:
                        schema["Ecological Information"]["Ecotoxicological Data"]["Acetic Acid"]["LC50, Fathead Minnow (Pimephales promelas)"] = line.split(":", 1)[-1].strip()
                elif "LC50, Rainbow Trout (Oncorhynchus mykiss)" in line:
                        schema["Ecological Information"]["Ecotoxicological Data"]["Acetic Acid"]["LC50, Rainbow Trout (Oncorhynchus mykiss)"] = line.split(":", 1)[-1].strip()
                elif "Persistence and Degradability" in line:
                    schema["Ecological Information"]["Persistence and Degradability"] = [item.strip() for item in line.split(":", 1)[-1].split(".")]
                elif "Environmental Effects" in line:
                    schema["Ecological Information"]["Environmental Effects"] = [item.strip() for item in line.split(":", 1)[-1].split(".")]
                

                if any(keyword in line.upper() for keyword in ["DISPOSAL INFORMATION"]):
                    return schema
                  
    return schema
# 13th Section
def extract_disposal_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_disposal = False
        pager = pdf.pages[5]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "DISPOSAL INFORMATION" in line.upper() and not found_disposal:
                found_disposal = True
                continue  # Skip the section heading

                
            if found_disposal:

                if "Disposal Instructions" in line:
                    schema["Disposal Information"]["Disposal Instructions"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Contaminated Packaging" not in lines[i + 1]:
                        schema["Disposal Information"]["Disposal Instructions"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Contaminated Packaging", "Waste Codes"]):
                            schema["Disposal Information"]["Disposal Instructions"] += " " + lines[j].strip()
                            j += 1
                elif "Contaminated Packaging" in line:
                    schema["Disposal Information"]["Contaminated Packaging"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Waste Codes" not in lines[i + 1]:
                        schema["Disposal Information"]["Contaminated Packaging"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Waste Codes"]):
                            schema["Disposal Information"]["Contaminated Packaging"] += " " + lines[j].strip()
                            j += 1
                elif "Waste Codes" in line:
                    schema["Disposal Information"]["Waste Codes"] = line.split(":", 1)[-1].strip()


                if any(keyword in line.upper() for keyword in ["TRANSPORT INFORMATION"]):
                    return schema                     
                


    return schema
# 14th Section
def extract_transport_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_transport = False
        pager = pdf.pages[5]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "TRANSPORT INFORMATION" in line.upper() and not found_transport:
                found_transport = True
                continue  # Skip the section heading

                
            if found_transport:

                if "< 10% w/w" in line:
                    schema["Transport Information"]["DOT"]["< 10% w/w"] = line.split(":", 1)[-1].strip()
                elif "A1006" in line:
                    if "UN Number" in line:
                        schema["Transport Information"]["DOT"]["A1006"]["UN Number"] = line.split(":", 1)[-1].strip()
                if "Proper Shipping Name" in line:
                    schema["Transport Information"]["DOT"]["A1006"]["Proper Shipping Name"] = line.split(":", 1)[-1].strip()
                elif "Hazard Class" in line:
                    schema["Transport Information"]["DOT"]["A1006"]["Hazard Class"] = line.split(":", 1)[-1].strip()
                elif "Packing Group" in line:
                    schema["Transport Information"]["DOT"]["A1006"]["Packing Group"] = line.split(":", 1)[-1].strip()
                elif "ERG Number" in line:
                    schema["Transport Information"]["DOT"]["A1006"]["ERG Number"] = line.split(":", 1)[-1].strip()
                elif "Environmental Hazard" in line:
                    schema["Transport Information"]["DOT"]["Environmental Hazard Regulations"] = line.split(" ", 2)[-1].strip()
                if "Other Transport Precautions" in line:
                    if "Acetic Acid" in line:
                        if "DOT Reportable Quantity" in line:
                            schema["Transport Information"]["DOT"]["Other Transport Precautions"]["Acetic Acid"]["DOT Reportable Quantity"] = line.split(":", 5)[-1].strip()
                


                if any(keyword in line.upper() for keyword in ["REGULATORY INFORMATION"]):
                    return schema                     
                


    return schema
# 15th Section
def extract_regulatory_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_regulatory = False
        fulltext = ""
        for page in pdf.pages[5:7]:
            text = page.extract_text()
            if text:
                fulltext+=text + "\n"
            lines = fulltext.split("\n")

        tables = page.extract_tables()

        for i, line in enumerate(lines):
            
            if "REGULATORY INFORMATION" in line.upper() and not found_regulatory:
                found_regulatory = True
                continue

            if found_regulatory:
                
                if "OSHA" in line:
                    schema["Regulatory Information"]["U.S. Federal Regulations"]["OSHA"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "TSCA Inventory" not in lines[i + 1]:
                        schema["Regulatory Information"]["U.S. Federal Regulations"]["OSHA"] += " " + lines[i + 1].strip()
                elif "TSCA Inventory" in line:
                    schema["Regulatory Information"]["U.S. Federal Regulations"]["TSCA Inventory"] = line.split(":", 1)[-1].strip()
                elif "Section 302" in line:
                    schema["Regulatory Information"]["U.S. EPCRA (SARA Title III)"]["Section 302"] = line.split(":", 1)[-1].strip()
                elif "Section 313" in line:
                    schema["Regulatory Information"]["U.S. EPCRA (SARA Title III)"]["Section 313"] = line.split(":", 1)[-1].strip()
                elif "CERCLA Reportable Quantities" in line:
                    schema["Regulatory Information"]["CERCLA Reportable Quantities"]["Acetic Acid, Glacial"] = line.split(":", 3)[-1].strip()
                elif "listed" in line:
                    schema["Regulatory Information"]["listed"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "OTHER INFORMATION" not in lines[i + 1]:
                        schema["Regulatory Information"]["listed"] += " " + lines[i + 1].strip()
                
                if tables:
                    idx = ["Section 311/312", "International Inventories"]
                    # Extract the first table found in the section
                    for i, table in enumerate(tables):
                        schema["Regulatory Information"][idx[i]] = parse_table(table)
                
                schema["Regulatory Information"]["U.S. EPCRA (SARA Title III)"]["Section 311/312"] = schema["Regulatory Information"]["Section 311/312"]
                del schema["Regulatory Information"]["Section 311/312"]



        if any(keyword in line.upper() for keyword in ["OTHER INFORMATION"]):
            return schema
            

    return schema
# 16th Section
def extract_other_information_section(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        found_other_information = False
        pager = pdf.pages[6]
        text = pager.extract_text()
        lines = text.split("\n")
    

        for i, line in enumerate(lines):
            if "OTHER INFORMATION" in line.upper() and not found_other_information:
                found_other_information = True
                continue  # Skip the section heading

                
            if found_other_information:

                if "Disclaimer" in line:
                    schema["Other Information"]["Disclaimer"] = line.split(":", 1)[-1].strip()
                    if i + 1 < len(lines) and "Issue Date" not in lines[i + 1]:
                        schema["Other Information"]["Disclaimer"] += " " + lines[i + 1].strip()
                        j = i + 2
                        while j < len(lines) and not any(keyword in lines[j] for keyword in ["Issue Date", "Reason for Revision"]):
                            schema["Other Information"]["Disclaimer"] += " " + lines[j].strip()
                            j += 1
                elif "Issue Date" in line:
                    schema["Other Information"]["Issue Date"] = line.split(":", 1)[-1].strip()
                elif "Reason for Revision" in line:
                    schema["Other Information"]["Reason for Revision"] = line.split(":", 1)[-1].strip()
                                   
                


    return schema
















