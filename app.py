from flask import Flask, render_template, request, redirect, url_for, send_file,session,flash,json
import sql_functions
import data_class_aidriven
import smtplib
from email.mime.text import MIMEText

connection = sql_functions.make_sql_connection()


app = Flask(__name__)
#  SEcretkey : 
app.secret_key = "aidriven"


cursor = connection.cursor()
# ----------------------------------------------------------- Landing page ---------------------------------------------------

@app.route('/')
def registration():
    return render_template('landing.html')

#  ----------------------------------------- REgistration --------------------------------------------------------------

 # Route to handle the form submission
@app.route('/register_student')
def register_student():
    
    return render_template('student_registration.html')

@app.route('/register_admin')
def register_admin():
    
    return render_template('admin_registration.html')



@app.route('/register_data', methods=['POST'])
def register_data():
    if request.method=="POST":
        student = {
        "name" : request.form['username'],
        "email" : request.form['email'],
        "pass2" : request.form['pass2'],
        "Enrolno" : request.form['Enrolno'],
        "college" : request.form['college'],
        "course" : request.form['course'],
        "year" : request.form['year'],
        "rollno" : request.form['rollno']}
        
        
        sql_functions.insert_register_student(username=student['name'],email=student['email'],password=student['pass2'],enrollment_num=student['Enrolno'],college=student['college'],course=student['course'],year=student['year'],rollno=student['rollno'])
        session["user"] = student["email"]
        
    else:
        name = "not found"
        
    
    return redirect(url_for("redirect_to_student_dashboard"))

@app.route('/redirect', methods=['POST'])
def redirect_to_page():
    if request.method == "POST":
        selected_page = request.form['register_dropdown']
        if selected_page == 'Student':
            return redirect(url_for('register_student'))
        elif selected_page == 'Admin':
            return redirect(url_for('register_admin'))
        elif selected_page == 'Company':
            return redirect(url_for('register_company'))
        else:
            return redirect(url_for('home'))
 
# ----------------------------------------------------------------Student Login --------------------------------------- 

@app.route('/login',methods=["POST","GET"])
def login():
    
    return render_template('login.html')

    
@app.route('/student_dashboard', methods=['POST'])
def student_dashboard():
    # if "user" in session:
    #     return redirect(url_for(redirect_to_student_dashboard(),student_list = [session['user']]))
    
    if request.method == "POST":
        # session.clear()
        
        email = request.form['email']
        password = request.form['password']
        login_as = request.form['Login_dropdown']
        # session["user"] = email
        if login_as=="Student":
            student_register_Data_list = []
            student_register_Data_list.append(email)
            student_register_Data_list.append(password)
            validatiaon = sql_functions.login_student_val(email,password)
            if validatiaon[0]:
                session["user"] = email
                session["password"] = password
                return redirect(url_for("redirect_to_student_dashboard",student_list = [session["user"]]))
            else:
                return render_template("login.html",error_msg=validatiaon[1])
        
        elif login_as=="Admin":
            student_register_Data_list = []
            student_register_Data_list.append(email)
            student_register_Data_list.append(password)
            return redirect(url_for("redirect_to_student_dashboard",student_list = [session["user"]]))

        elif login_as=="Company":
           
            validation = sql_functions.validate_company_login(email=email,password=password)
            if validation:
                session["company"] = email
                session["password"] = password
                return redirect(url_for("company_dashboard1",company_name = [session["company"]]))
            else:
                return render_template("login.html",error_msg=validation)
        
        else:
            return redirect(url_for('login'))
        


@app.route('/student_dashboard1')
def redirect_to_student_dashboard():
    if "user" in session:
        
        return render_template("dashboard_student.html",student_list = [session["user"]] )
    return redirect(url_for("login"))

# --------------------------------------------- Quiz ------------------------------------------------------

# questions = sql_functions.fetch_quiz_question("mysql")
@app.route('/quiz_details')
def quiz_details():
    return render_template("quiz_details.html")



@app.route('/quiz_details_form',methods = ["POST"])
def quiz_details_form():
    if request.method == "POST":
        session['qno']=-1
        session['correct_answers'] = 0
        global qtype1
        qtype1 = 'mysql'
        qtype = request.form["qtype"]
        questions = sql_functions.fetch_quiz_question(qtype=qtype)
        session["allQuestions"] = questions
        print(qtype1)
        return redirect(url_for("quiz"))
    else:
        return redirect(url_for(quiz_details))
    


@app.route('/quiz')
def quiz():
    
    if session["qno"] >= len(session["allQuestions"]):
        return "no more test enjoy"
    
    questions = session["allQuestions"]
    print(len(session["allQuestions"]))
    session['curr_question'] = questions[session['qno']]
    
    return render_template("quiz.html",questions = questions[session['qno']])
    
@app.route('/submit_answer',methods=["POST"])
def submit_answer():
    if request.method == "POST":
        session['qno'] += 1
        if session['qno'] < 10:
            answer = request.form["answer"]
            print(answer)
            if session['curr_question']['correct']==answer:
                session['correct_answers'] +=1
            return redirect(url_for("quiz"))
        
        else:
            return render_template("results.html",result = session["correct_answers"],len = 10,percentage = ((session["correct_answers"]*100)/10))



# ------------------------------------------------ Details ----------------------------------------------------------

@app.route('/student_details')
def student_details():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        
        student_details = sql_functions.get_student_details(email=session['user'])
        print(student_details)
        if student_details != ():
            return render_template('update_student_details.html',student_details = student_details )
        else:
            student_details = [{ 'firstname': 'firstname', 'lastname': 'lastname', 'middlename': 'middlename', 'college': 'college', 'rollno': 'rollno', 'program': 'Computer Science', 'stream': 'AI', 'year': 0, 'backlog': 0, 'currentcgpa': '9.', 'email': 'john.doe@example.com', 'phoneno': '+919999999999', 'gender': 'Male/Female', 'dob': '2000, 1, 11', 'nationality': 'Indian', 'address': '123 road Area, City'}]
            return render_template('update_student_details.html',student_details = student_details)
        


    
@app.route('/edit_student_field/<field>')
def edit_student_field(field):
    return render_template("student_field_update.html",field=field)

@app.route('/update_field/<field>',methods=["POST"])
def update_field(field):
    if request.method == "POST":
        value = request.form["value"]

        sql_functions.update_student_details(email=session["user"],field=field,value=value)
        return redirect(url_for("student_details"))
    else:
        return redirect(url_for("edit_student_details"))
# ------------------------------------------------ REsume Upload -----------------------------------------------------
@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        pdf_path = None

        if request.method == 'POST':
            # Check if the POST request has the file part
            if 'file' not in request.files:
                return render_template('upload_resume.html', error='No file part', pdf_path=pdf_path)

            file = request.files['file']

            # If the user does not select a file, browser will submit an empty part
            if file.filename == '':
                return render_template('upload_resume.html', error='No selected file', pdf_path=pdf_path)
            

            # Check if the file is a PDF
            if sql_functions.if_resume_present(session['user']):
                if file and file.filename.lower().endswith('.pdf'):
                    # Save the PDF file
                    sql_functions.insert_resume(session['user'],file.filename)
                    file_path = 'static/' + file.filename
                    file.save(file_path)

                    # Set the PDF path for display
                    pdf_path = f'/view_pdf?file={file_path}'

                    # Render the template with the PDF path
                    return render_template('upload_resume.html', pdf_path=pdf_path)
                else:
                    return render_template('upload_resume.html', error='Invalid file format. Please upload a PDF file', pdf_path=pdf_path)
           

        return render_template('upload_resume.html', pdf_path=pdf_path)
   
        


@app.route('/view_pdf', methods=['GET'])
def view_pdf():
    file_path = request.args.get('file', '')
    return send_file(file_path, as_attachment=False)

# --------------------------------------------------------- view jobs ---------------------------------------
@app.route('/view_jobs')
def view_jobs():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    try:

        cursor.execute("select * from job_posting")
        jobs = cursor.fetchall()

        print(jobs)
    except Exception as e:
        print(e)
        # jobs = [1, 2, 3]*20

    return render_template('view_jobs.html', jobs=jobs)
@app.route('/apply_job/<job_id>')
def apply_job(job_id):
    try:
        cursor.execute(f'select * from job_posting where id = {job_id}')
        job = cursor.fetchall()
        print(job)
    except Exception as e:
        print(e)
    return render_template("apply_job.html",jobs = job)

@app.route("/job_applied/<job_id>",methods=["POST"])
def job_applied(job_id):
    try:
        if request.method == "POST":
            student_details = sql_functions.get_student_details(session['user'])
            student_id = student_details[0]['id']
            cursor.execute(f'select company_id from job_posting where job_id = {job_id}')
            company_id = cursor.fetchall()

            sql_functions.insert_applied_student_data(company_id=company_id[0]['id'],job_id=int(job_id),student_id=student_id)
            flash("applied successfully")
    except Exception as e:
        pass

    return redirect(url_for("view_jobs"))
# -------------------------------------------- view student details by company

@app.route('/fetch_student_details')
def fetch_student_details():
    students = sql_functions.get_student_details()
    print(students)

# --------------------------------------------- company dashboard -------------------------------------

@app.route('/register_company')
def register_company():
    
    return render_template('company_registration.html')

@app.route('/company_dashboard', methods = ["POST"])
def company_dashboard():
    if request.method == "POST":
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        company_name = request.form['companyName']
        registration_number = request.form['registrationNumber']
        address = request.form['address']
        phone_number = request.form['phoneNumber']
        email = request.form['email']
        industry_type = request.form['industryType']
        company_description = request.form['companyDescription']
        logo_upload = request.files['logoUpload']
        company_size = request.form['companySize']

        data = {
        'Username': username,
        'Password1': password1,
        'Password2': password2,
        'Company Name': company_name,
        'Registration Number': registration_number,
        'Address': address,
        'Phone Number': phone_number,
        'Email': email,
        'Industry Type': industry_type,
        'Company Description': company_description,
        'Logo Upload': logo_upload.filename,
        'Company Size': company_size,
            }
        print(data)
        session['company'] = data['Email']
        sql_functions.insert_company_data(username=username,password1=password1,password2=password2,company_name=company_name,registration_number=registration_number,address=address,phone_number=phone_number,email=email,industry_type=industry_type,company_description=company_description,logo_upload_filename=logo_upload.filename,company_size=company_size)
        return redirect(url_for("company_dashboard1"))
        
@app.route('/company_dashboard1') 
def company_dashboard1():
    name = session['company']
    return render_template('dashboard_company.html',company_name = name )

# ---------------------------------------------- Login company -------------------------------------------



@app.route('/post_job', methods=['POST', 'GET'])
def post_job():
    if request.method == 'POST':
        job_role = request.form['job_role']
        job_type = request.form['job_type']
        skills_required = request.form['skills_required']
        num_employees = request.form['num_employees']
        num_openings = request.form['num_openings']
        company_description = request.form['company_description']
        responsibilities = request.form['responsibilities']

        try:
                # SQL query to insert data into the job_postings table
                cursor.execute(f"select id from company_registration where email = '{session['company']}'")
                company_id = cursor.fetchall()
                print(company_id)

                sql_functions.insert_job_posting(company_id=company_id[0]['id'],job_role=job_role,job_type=job_type,skills_required=skills_required,num_employees=num_employees,num_openings=num_openings,company_description=company_description,responsibilities=responsibilities)

                # Notify all students about the new job posting
                notify_students_about_job_posting(job_role)

                flash('Job posting added successfully', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')

        return redirect(url_for('job_listings'))

    return render_template('post_job.html')

# Function to send notifications to all students about the new job posting
def notify_students_about_job_posting(job_role):
    try:
        with connection.cursor() as cursor:
            # Fetch all student emails from the database
            sql = "SELECT email FROM student_register"
            cursor.execute(sql)
            student_emails = [student['email'] for student in cursor.fetchall()]

        # Send email notifications to students
        subject = 'New Job Opening'
        body = f'There is a new job opening for the position of {job_role}. Check your dashboard for more details.'
        send_email(subject, body, student_emails)
    except Exception as e:
        flash(f'Error notifying students: {e}', 'danger')

# Function to send email
def send_email(subject, body, recipients):
    try:
        # SMTP Configuration (Update with your SMTP server details)
        smtp_server = 'smtp.gmail.com'  # Assuming you are using Gmail
        smtp_port = 587
        smtp_username = 'Projectdemo65@gmail.com'  # Your Gmail username
        smtp_password = 'nbknetqtvnrgwnjv'  # Your Gmail password

        # Create the email message
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'Projectdemo65@gmail.com'  # Replace with your sender email address
        msg['To'] = ', '.join(recipients)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], recipients, msg.as_string())

    except Exception as e:
        flash(f'Error sending email: {e}', 'danger')

@app.route('/view_students')
def view_students():
    # Fetch all records of students from the database
    
    try:
        
            # Replace this query with your actual query to fetch all students
            cursor.execute(f"select id from company_registration where email = '{session['company']}'")
            company_id = cursor.fetchall()
            # print(company_id)
            student = sql_functions.select_applied_student(company_id=company_id[0]['id'])
            # print(student)
            student_ids = [x["student_id"] for x in student]
            job_ids = [x["job_id"] for x in student]
            print(job_ids)
            # print(student_ids)
            fetched_students = []
            for i,id in zip(student_ids,job_ids):
                cursor.execute(f"select * from student_details where id = {i}")
                fetched_student = cursor.fetchall()
                print(fetched_student)
                fetched_student[0]["job_id"]=id
                fetched_students.append(fetched_student[0])
            # print(fetched_students)

    except Exception as e:
        flash(f'Error fetching students: {e}', 'danger')
        fetched_students = [{"firstname":"student not selected"}]
        

    return render_template('view_students.html', students=fetched_students,job_ids = job_ids)

@app.route('/placement_analytics')
def placement_analytics():
    data = {
        "year_wise_companies_visited": {
            2017: 0.7,
            2016: 0.7,
            2015: 0.7,
            2014: 0.55,
        },
        "top_packages_last_5_years": {
            "correct_answers": [100, 100, 100, 100, 100],
            "incorrect_answers": [2, 2, 2, 2, 2],
            "unattempted_questions": [30, 30, 30, 30, 30],
        },
        "top_recruiter": {
            "2015": "C",
            "2014": {"Mar": 20, "Apr": 15},
        },
        "year_wise_placements": {
            "2017": "Outcome 10",
            "2016": "Outcome 10",
            "2015": "Outcome 10",
            "2014": "Outcome 10",
        }
    }
    return render_template('placement_analytics.html', data=data, json_data=json.dumps(data))


interviews = []
@app.route('/schedule_interview', methods=['GET', 'POST'])
def schedule_interview():
    # Fetch the list of students from the database
    try:
            # Replace this query with your actual query to fetch students
            cursor.execute(f"select id from company_registration where email = '{session['company']}'")
            company_id = cursor.fetchall()
            # print(company_id)
            student = sql_functions.select_applied_student(company_id=company_id[0]['id'])
            # print(student)
            student_ids = [x["student_id"] for x in student]
            job_ids = [x["job_id"] for x in student]
            print(job_ids)
            # print(student_ids)
            fetched_students = []
            for i,id in zip(student_ids,job_ids):
                cursor.execute(f"select * from student_details where id = {i}")
                fetched_student = cursor.fetchall()
                print(fetched_student)
                fetched_student[0]["job_id"]=id
                fetched_students.append(fetched_student[0])
            # print(fetched_students)
    except Exception as e:
        flash(f'Error fetching students: {e}', 'danger')
        fetched_students = []

    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']

        selected_student = next((student for student in fetched_students if student['id'] == student_id), None)

        if selected_student:
            interview_details = {
                'student_name': selected_student['name'],
                'date': date,
                'time': time,
                'location': location
            }

            interviews.append(interview_details)

            try:
                with connection.cursor() as cursor:
                    # SQL query to insert data into the interviews table
                    sql = "INSERT INTO interviews (student_id, date, time, location) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (student_id, date, time, location))
                    connection.commit()

                    # Send email notification to the student
                    send_interview_notification(selected_student['email'], interview_details)

                    flash('Interview scheduled successfully', 'success')
            except Exception as e:
                flash(f'Error: {e}', 'danger')

        else:
            flash('Selected student not found', 'danger')

    return render_template('schedule_interview.html', students=fetched_students, interviews=interviews)



def send_interview_notification(student_email, interview_details):
    try:
        smtp_server = 'smtp.gmail.com'  # Assuming you are using Gmail
        smtp_port = 587
        smtp_username = 'Projectdemo65@gmail.com'  # Your Gmail username
        smtp_password = 'nbknetqtvnrgwnjv'
        
        # Create the email message
        subject = 'Interview Scheduled'
        body = f'Dear {interview_details["student_name"]},\n\nYour interview has been scheduled for the following details:\n\nDate: {interview_details["date"]}\nTime: {interview_details["time"]}\nLocation: {interview_details["location"]}\n\nBest Regards,\nYour Company Name'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = 'Projectdemo65@gmail.com'  # Replace with your sender email address
        msg['To'] = student_email

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())

        flash('Email notification sent successfully', 'success')

    except Exception as e:
        flash(f'Error sending email notification: {e}', 'danger')


@app.route('/admin_all_records')
def admin_all_records():
    # Fetch all records of students, interviews, and job postings from the database
    try:
        with connection.cursor() as cursor:
            # Fetch students
            sql_students = "SELECT id, name, email FROM students"
            cursor.execute(sql_students)
            fetched_students = cursor.fetchall()

            # Fetch interviews
            sql_interviews = "SELECT id, student_id, date, time, location FROM interviews"
            cursor.execute(sql_interviews)
            fetched_interviews = cursor.fetchall()

            # Fetch job postings
            sql_job_postings = "SELECT id, job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities FROM job_postings"
            cursor.execute(sql_job_postings)
            fetched_job_postings = cursor.fetchall()

    except Exception as e:
        flash(f'Error fetching records: {e}', 'danger')
        fetched_students = []
        fetched_interviews = []
        fetched_job_postings = []

    return render_template('all_records.html', students=fetched_students, interviews=fetched_interviews, job_postings=fetched_job_postings)
@app.route('/job_listings')
def job_listings():
    # Fetch all job postings from the database
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities FROM job_posting"
            cursor.execute(sql)
            job_postings = cursor.fetchall()
    except Exception as e:
        flash(f'Error fetching job postings: {e}', 'danger')
        job_postings = []

    return render_template('job_listings.html', job_postings=job_postings)

@app.route('/scheduled_interviews')
def scheduled_interviews():
    try:
        with connection.cursor() as cursor:
            # Fetch all scheduled interviews from the database
            sql = "SELECT id, student_id, date, time, location FROM interviews"
            cursor.execute(sql)
            scheduled_interviews = cursor.fetchall()
            return render_template('scheduled_interviews.html', interviews=scheduled_interviews)
    except Exception as e:
        flash(f'Error fetching scheduled interviews: {e}', 'danger')
        scheduled_interviews = []

    return render_template('scheduled_interviews.html')

# ------------------------------------------------------- Company Section job posting -----------------------
if __name__ == '__main__':
    app.run(debug=True)
