from resume_to_json import extract_resume_data
from resume_to_json import process_all_resumes
import pandas as pd
from job_description_to_json import process_job_description
from get_matched_resumes import get_matching_resumes
from get_matched_resumes import check_experience
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import display, HTML
from sklearn.metrics.pairwise import cosine_similarity
 
def give_resumes():
    for i in range (0,100):
        resp = input("Do you want to recreate the resume_data.json file? (type y for yes and n for no) : ")
        resp=resp.capitalize()
        if resp=='Y':
            process_all_resumes("resume_data")
            break
        elif resp=='N':
            break
        else:
            print("give answer to the question specifically")
    
    dataframe=pd.read_json("resume_data.json")
    dataframe = dataframe.drop_duplicates(subset=['resume_id'])
    dataframe = dataframe.reset_index(drop=True)
    job_desc = input("Enter Job Description : ")
    process_job_description(job_desc)

    jd_dataframe=pd.read_json("jd_data.json")

    met_experience_resumes = check_experience(dataframe, jd_dataframe)
    boolean = dataframe['resume_id'].isin(met_experience_resumes)
    new_dataframe = dataframe[boolean]
    new_dataframe = pd.concat([new_dataframe, jd_dataframe], axis=0)
    ps = PorterStemmer()

    def stem(text):
      y=[]
      for i in text.split():
        y.append(ps.stem(i))

      return " ".join(y)

    def apply_stemming_to_list(list_of_strings):
        if isinstance(list_of_strings, list):
            return [stem(str(item)) for item in list_of_strings]
        else:
            return stem(str(list_of_strings))

    new_dataframe['Category/Work Domain'] = new_dataframe['Category/Work Domain'].apply(apply_stemming_to_list)
    new_dataframe['Skills'] = new_dataframe['Skills'].apply(apply_stemming_to_list)
    new_dataframe['Projects'] = new_dataframe['Projects'].apply(apply_stemming_to_list)
    new_dataframe['Education'] = new_dataframe['Education'].apply(apply_stemming_to_list)
    new_dataframe['Work Experience'] = new_dataframe['Work Experience'].apply(apply_stemming_to_list)
  
    def lower_list_elements(list_of_strings):
        if isinstance(list_of_strings, list):
            return [str(item).lower() for item in list_of_strings]
        else:
            # Handle cases where the cell might not contain a list
            return str(list_of_strings).lower()

    new_dataframe['Category/Work Domain'] = new_dataframe['Category/Work Domain'].apply(lower_list_elements)
    new_dataframe['Skills'] = new_dataframe['Skills'].apply(lower_list_elements)
    new_dataframe['Projects'] = new_dataframe['Projects'].apply(lower_list_elements)
    new_dataframe['Education'] = new_dataframe['Education'].apply(lower_list_elements)
    new_dataframe['Work Experience'] = new_dataframe['Work Experience'].apply(lower_list_elements)

    new_dataframe['Category/Work Domain'] = new_dataframe['Category/Work Domain'].apply(lambda x:[i.replace(" ", "") for i in x])
    new_dataframe['Skills'] = new_dataframe['Skills'].apply(lambda x:[i.replace(" ", "") for i in x])
    new_dataframe['Projects'] = new_dataframe['Projects'].apply(lambda x:[i.replace(" ", "") for i in x])
    new_dataframe['Education'] = new_dataframe['Education'].apply(lambda x:[i.replace(" ", "") for i in x])
    new_dataframe['Work Experience'] = new_dataframe['Work Experience'].apply(lambda x:[i.replace(" ", "") for i in x])

    new_dataframe['tags'] = new_dataframe['Category/Work Domain'] + new_dataframe['Skills'] + new_dataframe['Projects'] + new_dataframe['Education'] + new_dataframe['Work Experience']
    new_dataframe['tags'] = new_dataframe['tags'].apply(lambda x: " ".join(x))

    new_dataframe = new_dataframe.drop_duplicates(subset='Phone Number', keep='first')
    new_dataframe = new_dataframe.reset_index(drop=True)

    cv=CountVectorizer(max_features=5000, stop_words='english')
    vectors=cv.fit_transform(new_dataframe['tags']).toarray()
    similarity = cosine_similarity(vectors)

    distances = similarity[-1]
    distances = distances[:-1]
    cv_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)

    count = 0
    for i in cv_list:
        if count >= 5:
            break
        count += 1
        row = new_dataframe.iloc[i[0]]  # If cv_list contains tuples like (index,)

        print(row.get("Name"))
        print(row.get("Phone Number"))
        print(row.get("Email"))
        print(row.get("resume_id"))
        print("")

        # html_output = f"""
        # <div style="margin-bottom: 15px;">
        #     <b>Name:</b> {name}<br>
        #     <b>Phone:</b> {phone}<br>
        #     <b>Email:</b> {email}<br>
        #     <b>Resume Link:</b> <a href="{resume_link}" target="_blank">View Resume</a>
        # </div>
        # """
        # display(HTML(html_output))

    if count < 5:
        print("Try modifying the job description to get more resumes (particularly work experience).")

    print("DISCLAIMER - If the Profiles are not matching the Job Description, the resume data does not contain relevant resumes to Job Description. This problem can be solved if we use paid version of API as we can hit it any number of times there.")
    
if __name__ == "__main__":
    give_resumes()