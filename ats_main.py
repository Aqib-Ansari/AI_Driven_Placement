from langchain_community.document_loaders import PyPDFLoader
import google.generativeai as genai
import json
import re
def load_pdf(path):
    pdf_loader = PyPDFLoader(path)
    pages = pdf_loader.load_and_split()
    return [i.page_content for i in pages]
    
GOOGLE_API_KEY="AIzaSyDn3LTVkTF8oI6-3Z40Ax8X_nka6gfhnLg"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


prompt_template = """
 You are an experienced Technical Human Resource Manager,you are provide with 'resume data' and 'Job description' .
 your task is to undertand the resume, give a Percentage Match ({percent_match : X%})  for the candidate based on his skills. Do not give higher percentage match for job roles in different sector. good or bad for the job role . percent match start from 10% and end at 100%
Job Description = \n {job description} \n
x = integer range(10,100)
Anwer in JSON Format like this = {"percent_match : x}

"""

def ATS(path,job_description):
    pdf_loader = PyPDFLoader(path)
    pages = pdf_loader.load_and_split()
    all_pages =[i.page_content for i in pages]
    response =chat.send_message([pages[0].page_content,job_description,prompt_template])
    # response = model.generate_content([pages[0].page_content,job_description,prompt_template])

    numbers = re.findall(r'\d+', response.text)

    # Convert the list of strings to integers (if needed)
    numbers = [int(num) for num in numbers]

    # Print the extracted numbers
    # print(numbers)
    return numbers



if __name__ == "__main__":
    jd1 = ''' Job Description =
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

    jd2 = ''' job description =
**Job Title: Software Engineer**

**Company Overview:**
[Company Name] is a dynamic and innovative [industry/sector] company dedicated to pushing the boundaries of technology. We are seeking a talented Software Engineer to join our growing team. As a Software Engineer at [Company Name], you will play a crucial role in designing, developing, and implementing cutting-edge software solutions that drive our success in the industry.

**Position Overview:**
We are looking for a highly skilled and motivated Software Engineer to contribute to the development and maintenance of our software applications. The ideal candidate will have a strong background in software engineering principles, excellent problem-solving abilities, and a passion for staying up-to-date with the latest technologies. You will work collaboratively with cross-functional teams to deliver high-quality software solutions that meet our business and customer needs.

**Responsibilities:**
1. Collaborate with product managers, software architects, and other team members to understand project requirements and translate them into efficient and scalable software solutions.
2. Design, develop, and maintain software applications using industry best practices and coding standards.
3. Write clean, well-documented, and efficient code across multiple programming languages and frameworks.
4. Conduct code reviews and provide constructive feedback to maintain code quality and ensure adherence to coding standards.
5. Participate in the full software development lifecycle, including requirements gathering, design, implementation, testing, deployment, and maintenance.
6. Debug and troubleshoot software defects and issues, collaborating with cross-functional teams to identify and implement solutions.
7. Stay informed about emerging technologies, tools, and trends in software engineering, and advocate for their adoption when appropriate.
8. Contribute to the improvement of development processes, tools, and methodologies.
9. Collaborate with quality assurance teams to ensure the delivery of high-quality, reliable software.
10. Demonstrate a commitment to continuous learning and professional development.

**Qualifications:**
1. Bachelor's or higher degree in Computer Science, Software Engineering, or a related field.
2. Proven experience as a Software Engineer, with a strong portfolio showcasing successful software projects.
3. Proficiency in multiple programming languages, such as Java, Python, C++, or JavaScript.
4. Experience with software development frameworks and tools (e.g., Spring, React, Angular, Docker).
5. Solid understanding of software architecture, design patterns, and best practices.
6. Knowledge of database systems and SQL.
7. Familiarity with version control systems (e.g., Git) and CI/CD pipelines.
8. Strong problem-solving and analytical skills.
9. Excellent communication and collaboration abilities.
10. Commitment to writing secure, scalable, and maintainable code.

If you are a motivated and talented Software Engineer looking to be part of a dynamic team shaping the future of [industry/sector], we encourage you to apply and join us at [Company Name].'''
    
    jd3 = ''' job description = **Job Title: Electrical Engineer**

**Company Overview:**
[Company Name] is a leading [industry/sector] company committed to innovation, sustainability, and excellence in [specific field]. We are seeking a highly skilled and motivated Electrical Engineer to join our dynamic team. As an Electrical Engineer at [Company Name], you will have the opportunity to work on cutting-edge projects, contribute to the development of innovative solutions, and be a key player in advancing our industry.

**Position Overview:**
We are looking for an experienced Electrical Engineer to design, develop, and maintain electrical systems and components. The successful candidate will be responsible for ensuring the effective performance, reliability, and safety of electrical systems in our projects. The role involves collaboration with cross-functional teams, project management, and hands-on involvement in the design and implementation of electrical solutions.

**Responsibilities:**
1. Design and develop electrical systems for [specific applications/projects] adhering to industry standards and regulations.
2. Collaborate with cross-functional teams, including mechanical engineers, software engineers, and project managers, to integrate electrical components into overall project designs.
3. Conduct feasibility studies and provide technical guidance on electrical system implementations.
4. Create and review technical specifications, drawings, and documentation for electrical systems.
5. Perform simulations, analyses, and testing to ensure the performance and reliability of electrical components and systems.
6. Troubleshoot and resolve electrical issues during development, testing, and implementation phases.
7. Stay abreast of industry trends, emerging technologies, and best practices in electrical engineering.
8. Collaborate with external suppliers and vendors to source components and ensure compliance with project requirements.
9. Participate in design reviews and provide constructive feedback to enhance the overall quality of projects.
10. Contribute to continuous improvement initiatives, process optimization, and knowledge sharing within the engineering team.

**Qualifications:**
1. Bachelor's degree in Electrical Engineering or a related field. Master's degree is a plus.
2. Proven experience in the design and development of electrical systems for [industry/sector].
3. Strong knowledge of relevant industry standards, codes, and regulations.
4. Proficiency in using CAD software for electrical design (e.g., AutoCAD, SolidWorks Electrical).
5. Experience with simulation tools (e.g., SPICE, MATLAB) and familiarity with PLC programming.
6. Excellent problem-solving skills and the ability to troubleshoot complex electrical issues.
7. Effective communication skills, both written and verbal, with the ability to convey technical concepts to non-technical stakeholders.
8. Ability to work collaboratively in a team environment and manage multiple priorities.
9. Professional Engineer (PE) license is a plus.
10. Commitment to safety, quality, and continuous improvement.

If you are a passionate Electrical Engineer looking for a challenging and rewarding opportunity to contribute to groundbreaking projects, we invite you to apply and join our innovative team at [Company Name].'''

    jd4 = '''job_description =
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
    
    # result1 = ATS(path="./static/Aqib Ansari Resume.pdf",job_description=jd1)
    # result2 = ATS(path="./static/Aqib Ansari Resume.pdf",job_description=jd2)
    # result3 = ATS(path="./static/Aqib Ansari Resume.pdf",job_description=jd3)
    # result4 = ATS(path="./static/Aqib Ansari Resume.pdf",job_description=jd4)

    # print(f"Data Science : {result1} ") 
    # print(f"\n Software Engineer : {result2} \n ") #Electrical Engineer : {result3} \n 
#     print(f"data Science : {result1}")

#     import re

# # Your input string
#     input_string = 'This is a sample string with 123 and 456.78'

#     # Use regex to extract numbers
    # numbers = re.findall(r'\d+', result1)

    # # Convert the list of strings to integers (if needed)
    # numbers = [int(num) for num in numbers]

    # # Print the extracted numbers
    # print(numbers)

    path="./static/Aqib Ansari Resume.pdf"
    percent_match = ATS(path=path,job_description=jd1)
    print(percent_match)