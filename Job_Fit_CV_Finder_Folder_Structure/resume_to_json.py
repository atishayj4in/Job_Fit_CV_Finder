import pdfplumber
from extract_from_text import extract_resume_data
import os
import pandas as pd
import json

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def process_all_resumes(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            resume_text = extract_text_from_pdf(full_path)
            resume_data = extract_resume_data(resume_text, filename)
            results.append(resume_data)

    with open("resume_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("[✅] Saved all data to resume_data.json")


