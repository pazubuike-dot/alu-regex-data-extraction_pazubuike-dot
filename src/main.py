import os
import json
import re

def read_raw_data(file_path):
    """
    Safely reads the content of the raw text log file.
    Raises a FileNotFoundError if the path is incorrect.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found at: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_and_validate(text):
    """
    Core engine that handles data extraction via regular expressions,
    performs security checks, and masks sensitive financial information.
    """

    extracted_data = {
        "emails": {
            "official": [],
            "alumni": [],
            "si": []
        },
        "credit_cards": [],
        "urls": [],
        "currency_amounts": []
    }
    
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    potential_emails = re.findall(email_pattern, text)
    
    for email in potential_emails:
        
        if "<" in email or ">" in email or "script" in email.lower():
            print(f"[SECURITY ALERT] Malicious email structure blocked: {email}")
            continue
            
        
        if email.endswith("@alueducation.com"):
            if email not in extracted_data["emails"]["official"]:
                extracted_data["emails"]["official"].append(email)
        elif email.endswith("@alumni.alueducation.com"):
            if email not in extracted_data["emails"]["alumni"]:
                extracted_data["emails"]["alumni"].append(email)
        elif email.endswith("@si.alueducation.com"):
            if email not in extracted_data["emails"]["si"]:
                extracted_data["emails"]["si"].append(email)
            
    
    cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    potential_cards = re.findall(cc_pattern, text)
    
    for card in potential_cards:
        clean_card = card.replace(" ", "").replace("-", "")
        
        if len(clean_card) in [13, 14, 15, 16]:
            masked_card = f"XXXX-XXXX-XXXX-{clean_card[-4:]}"
            if masked_card not in extracted_data["credit_cards"]:
                extracted_data["credit_cards"].append(masked_card)

    url_pattern = r'https?://[a-zA-Z0-9./?=-]+'
    raw_urls = re.findall(url_pattern, text)
  
    extracted_data["urls"] = list(set(raw_urls))

    currency_pattern = r'\$[0-9,]+\.[0-9]{2}'
    raw_currency = re.findall(currency_pattern, text)
    extracted_data["currency_amounts"] = list(set(raw_currency))
            
    return extracted_data

def save_output(data, output_path):
    """
    Saves the extracted structures neatly back into a formatted JSON document.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    print(f"[SUCCESS] Extraction completed. Data written to: {output_path}")

def main():
    """
    Main controller setting up absolute environments paths to execute safely.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.abspath(os.path.join(current_dir, "..", "input", "raw-text.txt"))
    output_file = os.path.abspath(os.path.join(current_dir, "..", "output", "sample-output.json"))
    
    try:
        raw_text = read_raw_data(input_file)
        results = extract_and_validate(raw_text)
        save_output(results, output_file)
    except Exception as e:
        print(f"[ERROR] Run failed: {e}")

if __name__ == "__main__":
    main()