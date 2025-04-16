import spacy
import re
import os

MODEL_DIR = "./backend/output/model-best"
if os.path.exists(MODEL_DIR):
    nlp = spacy.load(MODEL_DIR)
else:
    nlp = spacy.load("en_core_web_sm")
date_pattern = re.compile(r'(\d{1,2}[a-z]{2}\s+\w+\s+\d{4}|\d{1,2}/\d{1,2}/\d{2,4}|\w+\s+\d{1,2},\s+\d{4})')
name_pattern = re.compile(r'Dear\s+([A-Z][a-z]+\s+[A-Z][a-z]+)')
company_pattern = re.compile(r'(welcome to|at)\s+([A-Z][\w\s&]+(?:Ltd|Inc|Corporation|Corp|Technologies)?)', re.IGNORECASE)
salary_pattern = re.compile(r'(\$|Rs\.?)[\s]?\d+[\d,]*(\s?per annum|/year|pa)?', re.IGNORECASE)
ref_id_pattern = re.compile(r'(Reference ID|Ref No|Ref):\s?\w+')

def extract_info(text):
    doc = nlp(text)
    result = {
        "employee_name": None,
        "company_name": None,
        "joining_date": None,
        "reference_id": None,
        "salary": None
    }

    # First: Try to extract via NER
    for ent in doc.ents:
        if ent.label_ == "EMPLOYEE" and not result["employee_name"]:
            result["employee_name"] = ent.text
        elif ent.label_ == "COMPANY" and not result["company_name"]:
            result["company_name"] = ent.text
        elif ent.label_ == "JOINING_DATE" and not result["joining_date"]:
            result["joining_date"] = ent.text
        elif ent.label_ == "SALARY" and not result["salary"]:
            result["salary"] = ent.text
        elif ent.label_ == "REF_ID" and not result["reference_id"]:
            result["reference_id"] = ent.text

    # Second: Regex fallbacks
    if not result["employee_name"]:
        name_match = name_pattern.search(text)
        if name_match:
            result["employee_name"] = name_match.group(1)

    if not result["company_name"]:
        company_match = company_pattern.search(text)
        if company_match:
            result["company_name"] = company_match.group(2).strip()

    if not result["joining_date"]:
        date_match = date_pattern.search(text)
        if date_match:
            result["joining_date"] = date_match.group()

    if not result["reference_id"]:
        ref_match = ref_id_pattern.search(text)
        if ref_match:
            result["reference_id"] = ref_match.group()

    if not result["salary"]:
        salary_match = salary_pattern.search(text)
        if salary_match:
            result["salary"] = salary_match.group()

    return result
