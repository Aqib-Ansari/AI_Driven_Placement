from PIL import Image
from pdf2image import convert_from_path
import google.generativeai as genai
import PIL.Image
import cv2
import numpy as np
import re

GOOGLE_API_KEY="AIzaSyDn3LTVkTF8oI6-3Z40Ax8X_nka6gfhnLg"

genai.configure(api_key=GOOGLE_API_KEY)

job_description1 = '''job_description =
Job Overview:
The DMLT (Diploma in Medical Laboratory Technology) Lab Assistant plays a crucial role in ensuring the smooth functioning of our diagnostic laboratory. Working under the supervision of laboratory technologists and pathologists, the Lab Assistant will contribute to the efficient processing of samples, maintenance of laboratory equipment, and adherence to quality control standards.

Responsibilities:

Sample Collection and Processing:

Collect, receive, and label specimens from patients following established protocols.
Prepare and process samples for various laboratory tests and procedures.
Equipment Maintenance:

Assist in the maintenance and calibration of laboratory equipment.
Monitor and report any equipment malfunctions or issues promptly.
Data Entry and Record-Keeping:

Accurately enter and maintain patient and test information in the laboratory information system.
Generate and maintain organized records of test results and other relevant data.
Quality Control:

Assist in implementing and maintaining quality control measures in the laboratory.
Follow standard operating procedures to ensure accuracy and precision in test results.
Inventory Management:

Monitor and manage laboratory supplies and reagents inventory.
Place orders for necessary supplies and ensure adequate stock levels.
Collaboration and Communication:

Collaborate with laboratory technologists, pathologists, and other team members to ensure smooth workflow.
Communicate effectively with healthcare professionals and colleagues.
Qualifications:

Diploma in Medical Laboratory Technology (DMLT) from a recognized institution.
Proven experience as a Lab Assistant or in a similar role is a plus.
Knowledge of laboratory safety and infection control protocols.
Familiarity with laboratory equipment and procedures.
Strong attention to detail and accuracy in sample handling and data entry.
Excellent organizational and multitasking skills.
Effective communication and interpersonal skills.
'''
job_description2 = ''' Job Description =
**Job Title: Data Scientist**

**Company Overview:**
Aqibeng ltd is a dynamic and innovative it company committed to Grow and help company with AI. We leverage cutting-edge technology and data-driven insights to make informed decisions and drive business success. As we continue to expand, we are seeking a talented and passionate Data Scientist to join our growing team.

**Job Overview:**
As a Data Scientist at Aqibeng ltd, you will play a crucial role in extracting meaningful insights from complex data sets to inform strategic business decisions. You will collaborate with cross-functional teams to design and implement advanced analytical solutions, contributing to the company's overall data-driven approach.

**Responsibilities:**

1. **Data Analysis and Modeling:**
   - Apply statistical and machine learning techniques to analyze large datasets and extract actionable insights.
   - Develop predictive models to support business goals and improve decision-making processes.

2. **Data Exploration and Preparation:**
   - Cleanse, preprocess, and validate raw data to ensure accuracy and reliability.
   - Collaborate with data engineers to design and implement data pipelines for efficient data extraction, transformation, and loading (ETL).

3. **Algorithm Development:**
   - Design and implement algorithms for data mining, pattern recognition, and predictive modeling.
   - Stay current with industry trends and advancements in data science to continuously enhance models and methodologies.

4. **Collaboration and Communication:**
   - Work closely with cross-functional teams, including business analysts and software developers, to understand business requirements and translate them into actionable insights.
   - Present findings and insights to both technical and non-technical stakeholders through clear and compelling visualizations and reports.

5. **Continuous Improvement:**
   - Proactively identify opportunities to enhance data quality, accuracy, and efficiency in analysis processes.
   - Contribute to the development and improvement of data science best practices within the organization.

**Qualifications:**

- Master's or Ph.D. in Computer Science, Statistics, Data Science, or a related field.
- Proven experience in data analysis, statistical modeling, and machine learning.
- Proficiency in programming languages such as Python or R.
- Strong knowledge of data manipulation and visualization tools (e.g., pandas, NumPy, Matplotlib, Seaborn).
- Experience with machine learning frameworks (e.g., TensorFlow, PyTorch) is a plus.
- Excellent problem-solving skills and the ability to work in a fast-paced, collaborative environment.
- Strong communication skills, with the ability to convey complex findings to both technical and non-technical stakeholders.

**How to Apply:**
Interested candidates are invited to submit their resume, a cover letter, and any relevant portfolio or project work to aqib@gmail.com. Please include "Data Scientist Application" in the subject line.

Aqibeng ltd is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees.'''

prompt_template = """
 You are an experienced Technical Human Resource Manager,you are provide with 'resume data' and 'Job description' .
 your task is to undertand the resume, give a Percentage Match ({percent_match : X%})  for the candidate based on his skills. Do not give higher percentage match for job roles in different sector. good or bad for the job role . percent match start from 10% and end at 100%
Job Description : \n {question} \n
Anwer in JSON Format like this : {"persent_match : x}

"""

path = "./Aqib Ansari Resume.pdf"
def create_image_of_pdf(path):

    image  = convert_from_path(path,fmt="png")
    for i,img in enumerate(image):
        img.save(f"./static/ats_resume/page_{i+1}.png")
    print(len(image))

create_image_of_pdf(path=path)

img = PIL.Image.open('./static/ats_resume/page_1.png')

def get_gemini_response(input_prompt,image,job_description):
  model = genai.GenerativeModel('gemini-pro-vision')
  response = model.generate_content([input_prompt,image,job_description])
  return response.text



# response = get_gemini_response(input_prompt=prompt_template,image=img,job_description=job_description)
# print(response)

def ATS(path,job_description):
    image  = convert_from_path(path,fmt="png")
    for i,img in enumerate(image):
        img.save(f"./static/ats_resume/page_{i+1}.png")
    image_list = []
    for i in range(len(image)):
        image_list.append(cv2.imread(f'./static/ats_resume/page_{i+1}.png'))
    
    appended_image = np.vstack(image_list)

    # Save the result
    output_path = "./static/ats_resume/output.png"
    cv2.imwrite(output_path, appended_image)

    img = PIL.Image.open(f'./static/ats_resume/output.png')

    response = get_gemini_response(input_prompt=prompt_template,image=img,job_description=job_description)

    numbers = re.findall(r'\d+', response)

    # Convert the list of strings to integers (if needed)
    numbers = [int(num) for num in numbers]

    # Print the extracted numbers
    print(numbers[0])
    return numbers[0]

if __name__ == "__main__":
    ATS(path=path,job_description=job_description1)

   

