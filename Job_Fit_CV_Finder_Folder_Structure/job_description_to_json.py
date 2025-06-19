from extract_from_text import extract_resume_data
import json

def process_job_description(jd):
    job_description_result = []
    resume_data = extract_resume_data(jd, "job_description")
    job_description_result.append(resume_data)

    with open("jd_data.json", "w", encoding="utf-8") as f:
        json.dump(job_description_result, f, indent=2, ensure_ascii=False)

    print("[✅] Saved job description to jd_data.json")