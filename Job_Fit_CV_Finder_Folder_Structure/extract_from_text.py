import google.generativeai as genai
import json
import ast
import time # Import the time module

genai.configure(api_key="AIzaSyA7zFbjqAlejM6VTtqfZU81wUzXkku1A8w")

model = genai.GenerativeModel("gemini-1.5-flash-latest")
def extract_resume_data(resume_text, resume_id, retries=3, delay=5):
    prompt = f"""
Extract the following fields from the resume below in JSON format only.
For each field, return a list of **keywords only** (not full sentences or raw text).
Focus on extracting meaningful keywords that represent the actual content in short form.
Avoid names of colleges, companies, or grades unless specifically required.

Fields:
- Name: Return as string. FirstName + " " + LastName format. Return "Name not Disclosed" string if name is not defined
- Category/Work Domain: Keywords like Data Science, Web Dev, ML, HR etc.
- Email: Single keyword - the email address. it should be a string
- Phone Number: Single keyword - 10 digit or international format. give only 10 digit string for this. remove std code, any hyphens etc. give blank number.
- Work Experience: Action/role-based keywords like 'software development', 'client handling', 'team lead'.
- No. of Years Worked: Return **numeric value only** (integer, not binned). if not defined in the resume, then try to get it seeing the work experience, projects etc...
- No. of Projects: Return a .
- Education: Return **only degree names** like B.Tech, M.Tech, MBA, B.Sc etc.
- Projects: Only **core keywords** that describe the nature or domain of the projects (like NLP, React, Chatbot, etc.)
- Skills: Write all the skills of the person here

Return output strictly in this JSON format:

{{
  "Name": str,
  "Category/Work Domain": [...],
  "Email": str,
  "Phone Number": str,
  "Work Experience": [...],
  "No. of Years Worked": int,
  "No. of Projects": int,
  "Education": [...],
  "Projects": [...],
  "Skills": [...]
}}
Resume:
\"\"\"{resume_text}\"\"\"
"""

    if resume_id=="job_description":
        prompt = f"""
Extract the following fields from the job description below in JSON format only.
For each field, return a list of **keywords only** (not full sentences or raw text).
Focus on extracting meaningful keywords that represent the actual content in short form.
Avoid names of colleges, companies, or grades unless specifically required.
if the resume description is insufficient and contains very less words, then in Category column, add similar keywords from the resume. in skills, add the relevent skills to the category/work domain if already not disclosed in the job description.

Fields:
- Name: Return as string. FirstName + " " + LastName format. Return "Name not Disclosed" string if name is not defined
- Category/Work Domain: Keywords like Data Science, Web Dev, ML, HR etc.
- Email: Single keyword - the email address. it should be a string. Return "Email not Disclosed" string if name is not defined
- Phone Number: Single keyword - 10 digit or international format. give only 10 digit string for this. remove std code, any hyphens etc. give blank number. Return "Phone Number not Disclosed" string if Phone Number is not defined
- Work Experience: Action/role-based keywords like 'software development', 'client handling', 'team lead'. Return "Required Work Experience not Defined" string if Work Experience is not defined
- No. of Years Worked: Return **numeric value only** (integer, not binned).
- No. of Projects: Return a .
- Education: Return **only degree names** like B.Tech, M.Tech, MBA, B.Sc etc.
- Projects: Only **core keywords** that describe the nature or domain of the projects (like NLP, React, Chatbot, etc.).
- Skills: Write all the skills of the person here

Return output strictly in this JSON format:

{{
  "Name": str,
  "Category/Work Domain": [...],
  "Email": str,
  "Phone Number": str,
  "Work Experience": [...],
  "No. of Years Worked": int,
  "No. of Projects": int,
  "Education": [...],
  "Projects": [...],
  "Skills": [...]
}}
Resume:
\"\"\"{resume_text}\"\"\"
"""
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            cleaned_text = response.text.strip()

            # Remove markdown formatting if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:-3].strip()
            elif cleaned_text.startswith("```python"):
                cleaned_text = cleaned_text[9:-3].strip()
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:-3].strip()

            data = json.loads(cleaned_text)
            data["resume_id"] = resume_id
            return data
        except (json.JSONDecodeError, ConnectionError) as e:
            print(f"[ERROR] Attempt {attempt + 1} for resume {resume_id}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"[ERROR] Failed to process resume {resume_id} after {retries} attempts.")
                return {"resume_id": resume_id, "error": str(e)}
    return {"resume_id": resume_id, "error": "Unknown error after retries"}