import json
from functions import *




def main():
    pdf_path = "D:\\Data Science Test Task\\Text_Scrapping_Pdf_to_Json\\update\\Final\\Acetic_Acid_1N_3-10percent_SDS.pdf" # Replace with your PDF file path
    identification_section = extract_identification_section(pdf_path)
    hazard_identification_section = extract_hazards_identification_section(pdf_path)
    composition_information_section = extract_composition_section(pdf_path)
    first_aid_measures_section = extract_first_aid_measures_section(pdf_path)
    fire_fighting_measures_section = extract_firefighting_measures_section(pdf_path)
    accidental_release_measures_section = extract_accidental_release_measures_section(pdf_path)
    handling_and_storage_section = extract_handling_and_storage_section(pdf_path)
    exposure_controls_section = extract_exposure_controls_section(pdf_path)
    physical_and_chemical_properties_section = extract_physical_property_section(pdf_path)
    stability_and_reactivity_section = extract_stability_section(pdf_path)
    toxicological_information_section = extract_toxicological_section(pdf_path)
    ecological_information_section = extract_ecological_section(pdf_path)
    disposal_considerations_section = extract_disposal_section(pdf_path)
    transport_information_section = extract_transport_section(pdf_path)
    regulatory_information_section = extract_regulatory_section(pdf_path)
    other_information_section = extract_other_information_section(pdf_path)
    
    # Combine all sections
    complete_data = {**identification_section, **hazard_identification_section, **composition_information_section, **first_aid_measures_section, **fire_fighting_measures_section, **accidental_release_measures_section, **handling_and_storage_section, **exposure_controls_section, **physical_and_chemical_properties_section, **stability_and_reactivity_section, **toxicological_information_section, **ecological_information_section, **disposal_considerations_section, **transport_information_section, **regulatory_information_section, **other_information_section}
    


    # Save cleaned data to JSON
    json_path = 'update\\Final\\SDS.json'
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(complete_data, f, indent=4, ensure_ascii=False)

    # Print JSON response
    with open(json_path, 'r') as f:
        json_response = json.load(f)
        print(json.dumps(json_response, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()