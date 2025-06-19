import json
from extract_from_text import model

def get_matching_resumes():
    with open("resume_data.json", "r") as f:
        resume_data = json.load(f)

    with open("jd_data.json", "r") as f:
        jd_data = json.load(f)

    jd_domain = jd_data[0].get("Category/Work Domain", "")

    matching_resume_ids = []

    for resume in resume_data:
        resume_domain = resume.get("Category/Work Domain", "")
        resume_id = resume.get("resume_id", "")

        prompt = (
            f"You are a recruiter. The job requires expertise in: {jd_domain}.\n"
            f"The candidate's expertise is in: {resume_domain}.\n"
            f"Does this candidate fit the job domain? Respond only with 'Yes' or 'No'."
        )

        response = model.generate_content(prompt)
        answer = response.text.strip().lower()

        if answer == "yes":
            matching_resume_ids.append(resume_id)

    return matching_resume_ids

def check_experience(dataframe, jd_dataframe):
    jd_experience = jd_dataframe["No. of Years Worked"][0]
    met_required_experience = []
    for index, row in dataframe.iterrows():
        resume_experience = row["No. of Years Worked"]
        # Assuming resume_experience is already an integer or can be treated as one
        if resume_experience >= jd_experience:
            met_required_experience.append(row["resume_id"])

    return met_required_experience