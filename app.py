from flask import Flask, render_template, request, redirect, url_for, send_file,session,flash, jsonify,json
import sql_functions
import data_class_aidriven
import smtplib
from email.mime.text import MIMEText
import ai_interviewer
from datetime import datetime, timedelta
import os
import ATSmain
from flask_socketio import SocketIO, emit


connection = sql_functions.make_sql_connection()


app = Flask(__name__)
#  SEcretkey : 
app.secret_key = "aidriven"
socketio = SocketIO(app)

cursor = connection.cursor()
# ----------------------------------------------------------- Landing page ---------------------------------------------------

@app.route('/')
def registration():
    session.clear()
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
        cursor.execute(f"select id from student_register where email = '{session['user']}'")
        id =cursor.fetchone()
        print(id["id"])
        cursor.execute("INSERT INTO student_details (id) VALUES (%s)", (int(id["id"]),))
        connection.commit()

        
        
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
    if "user" in session:
        return redirect(url_for("redirect_to_student_dashboard",student_list = [session['user']]))
    
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
            # validatiaon = sql_functions.validate_admin_login(email,password)
            if email == "geetamaam@gmail.com" and password == "KcAdminPassword":
                session["admin"] = email
                
            return redirect(url_for("admin_dashboard",admin_name = [session["admin"]]))

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
        
        student_details = sql_functions.get_student_details(session['user'])
        # print(student_details)
        if student_details != ():
            student_id = student_details[0]['id']
            # print(student_id)
            cursor.execute(f"select filename from student_profile_img where student_id = {student_id} ")
            profile_filename = cursor.fetchone()
            print(profile_filename)
            return render_template("dashboard_student.html",student_list = [session["user"]] , image_pro =  profile_filename)
        
        return render_template("dashboard_student.html",student_list = [session["user"]] , image_pro =  False , msg = "please Update Your Details")

    return redirect(url_for("login"))

# ----------------------------------------- Profile -------------------------------------------

UPLOAD_FOLDER = 'static/student/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def image_exists(filename):
    return os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename))


@app.route('/profile',methods=["POST","GET"])
def profile():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, display the file input again
        if file.filename == '':
            return render_template('profile.html', image_exists=image_exists)

        # Save the uploaded file to the UPLOAD_FOLDER
        if file:
            sql_functions.insert_student_profile_img(email=session["user"],filename=file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            connection.commit()
            return redirect(url_for('profile'))
    

    student_details = sql_functions.get_student_details(session['user'])

    if student_details == ():
        return redirect(url_for("student_details"))
    student_id = student_details[0]['id']
    cursor.execute(f"select filename from student_profile_img where student_id = {student_id} ")
    profile_filename = cursor.fetchone()
    # print(profile_filename)
    student_details = sql_functions.get_student_details(email=session["user"])
    if profile_filename == None or profile_filename == ():

        return render_template("profile.html",student = student_details)

    # print(profile_filename["filename"])

    return render_template("profile.html", image_pro=profile_filename["filename"],student = student_details )

@app.route('/profile_change_profile',methods= ["POST","GET"])
def profile_change_profile():
    if request.method == 'POST':
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, display the file input again
        if file.filename == '':
            return render_template('profile.html', image_exists=image_exists)

        # Save the uploaded file to the UPLOAD_FOLDER
        if file:
            sql_functions.insert_student_profile_img(email=session["user"],filename=file.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            connection.commit()
            return redirect(url_for('profile'))
        
    else:
        return render_template("update_image.html")
        

@app.route('/notifications')
def notifications():
    student_details = sql_functions.get_student_details(session['user'])
    student_id = student_details[0]['id']
    notifications = sql_functions.select_notification(student_id=student_id)
    # print(notifications)
    return render_template('notifications.html',notifications=notifications)

@app.route('/view_applied_jobs')
def view_applied_jobs():
    if "user" not in session:
        return redirect(url_for("login"))
    
    applied_jobs = []
    try:
        # Fetch the student's ID based on their email
        cursor.execute("SELECT id FROM student_register WHERE email = %s", (session['user'],))
        student_details = cursor.fetchone()
        
        if student_details:
            student_id = student_details['id']

            # Query the database to get the applied jobs for the student
            query = """
            SELECT jp.*
            FROM job_posting jp
            INNER JOIN applied_student ap ON jp.id = ap.job_id
            WHERE ap.student_id = %s
            """
            cursor.execute(query, (student_id,))
            applied_jobs = cursor.fetchall()

    except Exception as e:
        print(e)
        # Handle any exceptions or errors here
    
    return render_template('student_appliedjob.html', applied_jobs=applied_jobs)





# ------------------------------------------  quiz----------


# def get_remaining_time_in_seconds():
#     remaining_time = session["expiration_time"] - datetime.now()
#     remaining_time_in_seconds = remaining_time.total_seconds()
#     return remaining_time_in_seconds

# @app.route('/remaining_time')
# def remaining_time():
#     remaining_time_in_seconds = get_remaining_time_in_seconds()
#     return jsonify({'remaining_time_in_seconds': remaining_time_in_seconds})

app.config['expiration_time'] = datetime.now() + timedelta(minutes=10)

remaining_time = app.config['expiration_time'] - datetime.now()

def get_remaining_time_in_seconds():
    remaining_time = app.config['expiration_time'] - datetime.now()
    remaining_time_in_seconds = remaining_time.total_seconds()
    return remaining_time_in_seconds

@app.route('/remaining_time')
def remaining_time():
    remaining_time_in_seconds = get_remaining_time_in_seconds()
    return jsonify({'remaining_time_in_seconds': remaining_time_in_seconds})



@app.route('/quiz_details')
def quiz_details():
    student_details = sql_functions.get_student_details(session['user'])
    if student_details == ():
        return redirect(url_for("student_details"))
    return render_template("quiz_details.html")



@app.route('/quiz_details_form',methods = ["POST"])
def quiz_details_form():
    

    if request.method == "POST":
        session['qno']=-1
        session['correct_answers'] = []
        
        global qtype1
        qtype1 = 'mysql'
        qtype = request.form["qtype"]
        session["qtype"] = qtype
        testtime = request.form["testtime"]
        questions = sql_functions.fetch_quiz_question(qtype=qtype)
        session["allQuestions"] = questions[0:35]
        # print(session["allQuestions"])
        # print(len(session["allQuestions"]))


        if testtime =="10" :
            session["no_of_question"] = 8
            session["option_selected"] = [0]*40
           
            app.config['expiration_time'] = datetime.now() + timedelta(minutes=10)

            # print(session["option_selected"])

        elif testtime == "20":
            session["no_of_question"] = 14
            app.config['expiration_time'] = datetime.now() + timedelta(minutes=20)
            session["option_selected"] = [0]*40

            

        else:
            session["no_of_question"] = 20
            app.config['expiration_time'] = datetime.now() + timedelta(minutes=30)
            session["option_selected"] = [0]*40
            

        # print(qtype1)
        return redirect(url_for("quiz"))
    else:
        return redirect(url_for(quiz_details))
    


@app.route('/quiz')
def quiz():
    # print(session['qno'])
    if session['qno'] >= len(session["allQuestions"]):
        return "no more test enjoy"
    
    questions = session["allQuestions"]
    # print(len(session["allQuestions"]))
    session['curr_question'] = questions[session['qno']]
    # print("question  =", questions[session['qno']])
    # print("option = ",session["option_selected"][session["qno"]])
    
    return render_template("quiz.html",questions = questions[session['qno']],option=session["option_selected"][session["qno"]])
    
@app.route('/submit_answer',methods=["POST"])
def submit_answer():
    if request.method == "POST":
        session['qno'] += 1
        if session['qno'] < session["no_of_question"]:
            answer = request.form["answer"]
            session["option_selected"][(session["qno"])-1] = answer  
            # print(int(answer)," - ",int(session['curr_question']['correct']))

            if int(session['curr_question']['correct'])==int(answer):
                session['correct_answers'].append(1)
            else:
                session['correct_answers'].append(0)
            return redirect(url_for("quiz"))
        
        else:
            student_details = sql_functions.get_student_details(session['user'])
            student_id = student_details[0]['id']
            sql_functions.insert_notification(student_id=student_id,msg=f"your result is for subject {session['qtype']}: \n correct answers are {sum(session['correct_answers'])} / {session['no_of_question']} : percentage : {((sum(session['correct_answers'])*100)/10)}%",link="/student_dashboard1") 
            session["option_selected"] = [0]*40

            return render_template("results.html",result = sum(session["correct_answers"]),len = session["no_of_question"],percentage = ((sum(session["correct_answers"])*100)/session["no_of_question"]))

@app.route('/previous_question')
def previous_question():
    if session["qno"] >= 0:
        session["qno"] -= 1
    if session['correct_answers'] != []:
        session['correct_answers'].pop()

    return redirect(url_for("quiz"))

@app.route("/end_test")
def end_test():
    session["option_selected"] = [0]*40

    return render_template("results.html",result = sum(session["correct_answers"]),len = session["no_of_question"],percentage = ((sum(session["correct_answers"])*100)/10))

# ------------------------------------------------ Details ----------------------------------------------------------

@app.route('/student_details')
def student_details():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        
        student_details = sql_functions.get_student_details(email=session['user'])
        # print(student_details)
        if student_details != ():
            return render_template('update_student_details.html',student_details = student_details )
        else:
            student_details = [{'firstname': 'firstname',
                                 'lastname': 'lastname',
                                   'middlename': 'middlename',
                                     'college': 'college',
                                       'rollno': 'rollno',
                                         'program': 'Computer Science',
                                           'stream': 'AI',
                                             'year': 0,
                                               'backlog': 0,
                                                 'currentcgpa': '9.',
                                                   'email': 'john.doe@example.com',
                                                     'phoneno': '+919999999999',
                                                       'gender': 'Male/Female',
                                                         'dob': '2000, 1, 11',
                                                           'nationality': 'Indian',
                                                             'address': '123 road Area, City'}]
            return render_template('update_student_details.html',student_details = student_details)
        


    
@app.route('/edit_student_field/<field>')
def edit_student_field(field):
    return render_template("student_field_update.html",field=field)

@app.route('/update_field/<field>',methods=["POST"])
def update_field(field):
    if request.method == "POST":
        value = request.form["value"]
        # print(value)
        if field == "dob":
            value = datetime.strptime(value,f"%Y-%m-%d")
            print(value)
        # print(value)

        sql_functions.update_student_details(email=session["user"],field=field,value=value)
        return redirect(url_for("student_details"))
    else:
        return redirect(url_for("edit_student_details"))

@app.route('/add_skills', methods=['GET', 'POST'])
def add_skills():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == 'POST':
        # Each of these can be a comma-separated list
        skill = request.form['skill']
        soft_skills = request.form['soft_skills']
        certifications = request.form['certifications']
        student_email = session['user']

        try:
            cursor.execute("SELECT id FROM student_register WHERE email = %s", (student_email,))
            student_id_result = cursor.fetchone()

            if student_id_result:
                student_id = student_id_result['id']

                # Assuming skills and certifications are entered as comma-separated values
                # Directly store these CSV strings into the database
                insert_query = """
                INSERT INTO student_skills (student_id, skill, soft_skills, certifications) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (student_id, skill, soft_skills, certifications))
                connection.commit()

                flash('Skills and certifications added successfully!')
                return redirect(url_for('add_skills'))
        except Exception as e:
            print(e)
            flash('Error adding skills and certifications.')

    return render_template('add_skills.html')
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
            else:
                sql_functions.insert_resume(email=session["user"],filename=file.filename)
                file_path = 'static/' + file.filename
                file.save(file_path)
                connection.commit()
                return render_template('upload_resume.html', pdf_path=file_path)

            

            # Check if the file is a PDF
        if sql_functions.if_resume_present(session['user']):
                connection.commit()
                file_name = sql_functions.if_resume_present(session["user"])
                file_path = 'static/'+file_name
                return render_template('upload_resume.html', pdf_path=file_path)
        else:
                
                return render_template('upload_resume.html')
           

        
   
        


@app.route('/view_pdf', methods=['GET'])
def view_pdf():
    file_path = request.args.get('file', '')
    return send_file(file_path, as_attachment=False)

# --------------------------------------------------------- view jobs ---------------------------------------
@app.route('/view_jobs')
def view_jobs():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    # try:

        
        cursor.execute(f"select id from student_register where email = '{session['user']}'")
        student_details = cursor.fetchall()
        student_id = student_details[0]['id']
        cursor.execute(f"select job_id from applied_student where student_id = {student_id} ")
        # print("\n\n")
        job_applied = cursor.fetchall()
        # print(job_applied)
        job_applied_array = [i["job_id"] for i in job_applied]
        id_string = ', '.join(map(str, job_applied_array))
        # print(id_string)
        # cursor.execute(f"select * from job_posting where id not in ({id_string})")
        cursor.execute(f"select * from job_posting")
        # applied_array = [x for x in range()]
        jobs = cursor.fetchall()
        for i,j in zip(jobs,job_applied_array):

            if i["id"] == int(j):
                i["applied"] = "Applied"
            else:
                i['applied'] = False

        # for i in range()


        

        # print(jobs)
    # except Exception as e:
    #     print(e)
    #     # jobs = [1, 2, 3]*20

        return render_template('view_jobs.html', jobs=jobs)



@app.route('/apply_job/<job_id>')
def apply_job(job_id):
    # try:
        if sql_functions.if_resume_present(email=session["user"]):
            cursor.execute(f'select * from job_posting where id = {job_id}')
            job = cursor.fetchall()
        # print(job)
    # except Exception as e:
    #     print(e)
            return render_template("apply_job.html",jobs = job)
        else:
            cursor.execute(f"select id from student_register where email = '{session['user']}'")
            student_details = cursor.fetchall()
            student_id = student_details[0]['id']
            sql_functions.insert_notification(student_id=student_id,msg="First Upload Your resume to Apply a job" , link='/upload_resume')
            connection.commit()
            return redirect(url_for("upload_resume"))

@app.route("/job_applied/<job_id>",methods=["POST"])
def job_applied(job_id):

        if request.method == "POST":
            print("this is job id",job_id)
            
            # print(student_dashboard)
            cursor.execute(f"select id from student_register where email = '{session['user']}'")
            student_details = cursor.fetchall()
            student_id = student_details[0]['id']
            
            print(student_id)
            cursor.execute(f'select company_id from job_posting where id = {int(job_id)}')
            company_id = cursor.fetchall()

            cursor.execute(f'select * from job_posting where id = {job_id}')
            job = cursor.fetchall()

            jd = job[0]["job_role"] +"\n"+ job[0]["skills_required"] +"\n"+ job[0]["responsibilities"]
            if sql_functions.if_resume_present(session['user']):
                file_name = sql_functions.if_resume_present(session["user"])
                file_path = 'static/'+file_name
            percent_match = ATSmain.ATS(path=file_path,job_description=jd)

            sql_functions.insert_percent_match(student_id=student_id,job_id=job_id,percent_match=percent_match)

            sql_functions.insert_applied_student_data(company_id=company_id[0]['company_id'],job_id=int(job_id),student_id=student_id)
            flash("applied successfully")
            student_details = sql_functions.get_student_details(session['user'])
            student_id = student_details[0]['id']

            cursor.execute(f'select job_role from job_posting where id = {int(job_id)}')
            job_name = cursor.fetchall()
            sql_functions.insert_notification(student_id=student_id,msg=f"Succesfully Applied for job role {job_name[0]['job_role']}",link="/view_jobs") 
            connection.commit()

    

        return redirect(url_for("view_jobs"))


# -------------------------------------------- Ai Interviewer -------------------------------------
subject = ""

prompt2 = '''
give the result of mock interview in a json format having fields "correct answers" , "any Feedback for technical " 
'''
@app.route('/start_interview', methods=['GET', 'POST'])
def start_interview():
    global   subject
    if request.method == "POST":
        subject = request.form["interview_topic"]
        prompt = f"""
            You are an experienced Technical Human Resource Manager,your task is to ask interview question for job role {subject}. 
            Please do not provide answer . only ask one question at a time. some time ask about the project done by candidate
            """

    
        response = ai_interviewer.start_interview(prompt=prompt)
        session["last_answer"] = False

    
        return render_template('interviewer.html', result=response, inter_pro = False, start = True)
    

@app.route('/interview_process',methods= ["POST","GET"])
def interview_process():
    
    global subject
    if request.method == "POST":
        answer = request.form["answer"]
        response = ai_interviewer.chat.send_message(answer)
        session["last_answer"] = response.text
        print(response.text)
        prompt = f"""
            You are an experienced Technical Human Resource Manager,your task is to ask interview question for job role {subject}. 
            Please do not provide answer . only ask one question at a time. some time ask about the project done by candidate.
             
            """
        question = ai_interviewer.chat.send_message(["Ask me only 1 interview question" , prompt])
        return render_template('interviewer.html', result=response.text, question = question.text,inter_pro = True)
    else:
        prompt = f"""
            You are an experienced Technical Human Resource Manager,your task is to ask interview question for job role {subject}. 
            Please do not provide answer . only ask one question at a time. some time ask about the project done by candidate.
             
            """
        question = ai_interviewer.chat.send_message(["Ask me only 1 interview question" , prompt])
        return render_template('interviewer.html', result=session["last_answer"], question = question.text, inter_pro = True)


@app.route('/end_interview')
def end_interview():
    end_test_text = ai_interviewer.end_interview()
    print(end_test_text)
    return render_template("end_interview.html" ,text = end_test_text)


# -------------------------------------------- training resources --------------------------------------------------

@app.route('/training')
def training():
    result = sql_functions.select_training_resources()
    
    return render_template("training.html", training_resources=result)
# -------------------------------------------- alumni -------------------------------------------------
# Dummy data storage (replace with a database in a real application)
alumni_data = [{
        'name': 'John Doe',
        'batch': '2020',
        'placement_status': 'Placed',
        'company': 'TechCorp Inc',
        'linkedin': 'https://www.linkedin.com/in/johndoe/',
        'email': 'johndoe@example.com',
        'about_alumni': 'John Doe is a computer science graduate from the class of 2020. He is currently working at TechCorp Inc. His expertise includes software development and machine learning.'
    },
    
    {
        'name': 'Jane Smith',
        'batch': '2019',
        'placement_status': 'Not Placed',
        'company': None,
        'linkedin': 'https://www.linkedin.com/in/janesmith/',
        'email': 'jane.smith@example.com',
        'about_alumni': 'Jane Smith graduated in 2019 and is exploring opportunities in the tech industry. She has a strong background in data analysis and is actively seeking positions in data science.'
    }]

@app.route('/alumni_list')
def alumni_list():
    alumni_info=sql_functions.select_alumni_data()
    return render_template('alumni_list.html', alumni_data=alumni_info)


@app.route('/add_alumni', methods=['GET', 'POST'])
def add_alumni():
    if request.method == 'POST':
        name = request.form.get('name')
        batch = request.form.get('batch')
        placement_status = request.form.get('placement_status')
        company = request.form.get('company')
        linkedin = request.form.get('linkedin')
        email = request.form.get('email')
        about_alumni = request.form.get('about_alumni')

        alumni_info = {
            'name': name,
            'batch': batch,
            'placement_status': placement_status,
            'company': company,
            'linkedin': linkedin,
            'email': email,
            'about_alumni': about_alumni
        }
        
        sql_functions.insert_alumni_data(data=alumni_info)

        # Redirect to the alumni list page after adding alumni
        return redirect(url_for('alumni_list'))

    return render_template('add_alumni.html')



@app.route('/contact_alumni')
def contact_alumni():
    alumni_data = sql_functions.select_alumni_data()
    return render_template('contact_alumni.html', alumni_data=alumni_data)

@socketio.on('update_alumni_data')
def handle_update_alumni_data():
    emit('refresh_alumni_data', alumni_data, broadcast=True)


#  --------------------------------------- change password ---------------------------
@app.route('/change_pass',methods= ["POST"])
def change_pass():
    if request.method == "POST":
        currentPassword = request.form["currentPassword"]
        newPassword = request.form["newPassword"]
        confirmPassword = request.form["confirmPassword"]
        # print(currentPassword,newPassword,confirmPassword)
        cursor.execute(f"select password from student_register where email = '{session['user']}'")
        original_pass = cursor.fetchall()
        # print(original_pass[0]["password"])
        if currentPassword == original_pass[0]["password"]:
            if newPassword == confirmPassword:
                cursor.execute(f"update student_register set password = '{newPassword}' where email = '{session['user']}'")
                connection.commit()
                student_details = sql_functions.get_student_details(session['user'])
                student_id = student_details[0]['id']
                sql_functions.insert_notification(student_id=student_id,msg="Password Updated Succesfully",link="/profile")
                connection.commit()
                return redirect(url_for("profile"))
            else:
                return render_template("change_pass.html",error = "both password should be same")
            
        return render_template("change_pass.html",error = "Both Password should be same")
    return render_template("change_pass.html",error = "both password should be same")

@app.route('/change_pass_page')
def change_pass_page():
    return render_template("change_pass.html")
    


@app.route('/interview_option',methods = ["POST" , "GET"])
def interview_option():
    if request.method == "POST":
        subject = request.form["interview_topic"]
        return redirect(url_for("start_interview"))

    return render_template("interview_options.html")


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

        if logo_upload.filename == '':
                return 'No selected file'

        # Ensure the 'static/company' folder exists, create it if not
        upload_folder = 'static/company'
        os.makedirs(upload_folder, exist_ok=True)

        # Save the uploaded file to the 'static/company' folder
        print(logo_upload.filename)
        # if session["company"]:
        #     logo_upload.filename = extract_name_from_email(session["company"]) + ".jpg"
        #     file_path = os.path.join(upload_folder, logo_upload.filename)
        #     logo_upload.save(file_path)

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
        sql_functions.insert_company_data(username=username,
                                          password1=password1,
                                          password2=password2,
                                          company_name=company_name,
                                          registration_number=registration_number,
                                          address=address,
                                          phone_number=phone_number,
                                          email=email,
                                          industry_type=industry_type,
                                          company_description=company_description,
                                          logo_upload_filename=logo_upload.filename,
                                          company_size=company_size)
        return redirect(url_for("company_dashboard1"))
        
@app.route('/company_dashboard1') 
def company_dashboard1():
    name = session['company']
    logo = f'/static/company/{extract_name_from_email(session["company"]) + ".jpg"}'
    return render_template('dashboard_company.html',company_name = name ,company_logo = logo)

import re

def extract_name_from_email(email):
    # Define a regular expression pattern to extract the name before '@'
    pattern = re.compile(r'^([^@]+)@')
    
    # Use the pattern to search for a match in the email
    match = pattern.search(email)
    
    # Check if a match is found and return the extracted name
    if match:
        return match.group(1)
    else:
        return None

# Example usage:


# add this to the end of the app.py file after the training resources

@app.route('/back_to_dashboard')
def back_to_dashboard():
    # Redirect to the desired page
    return redirect(url_for('company_dashboard1')) 

def get_current_logged_in_company_id():
    if 'company' in session:
        company_email = session['company']
        cursor.execute("SELECT id FROM company_registration WHERE email = %s", [company_email])
        company_id = cursor.fetchone()
        return company_id['id'] if company_id else None
    else:
        return None

@app.route('/company_view_profile')
def company_view_profile():
    company_id = get_current_logged_in_company_id()

    if company_id:
        cursor.execute("SELECT * FROM company_registration WHERE id = %s", [company_id])
        company_data = cursor.fetchone()

        if company_data:
            company = {
                "id": company_data['id'],
                "username": company_data['username'],
                "company_name": company_data['company_name'],
                "registration_number": company_data['registration_number'],
                "address": company_data['address'],
                "phone_number": company_data['phone_number'],
                "email": company_data['email'],
                "industry_type": company_data['industry_type'],
                "company_size": company_data['company_size']
            }
            return render_template('company_view_profile.html', company=company)
        else:
            flash("Company details not found")
            return redirect(url_for("some_fallback_route"))  # Redirect to a fallback route
    else:
        flash("You need to log in to view this page")
        return redirect(url_for("login"))
# ------------------------------------------------------- Company Section job posting -----------------------

@app.route('/post_job', methods=['POST', 'GET'])
def post_job():
    if request.method == 'POST':
        job_role = request.form['job_role']
        job_type = request.form['job_type']
        skills_required = request.form['skills_required']
        num_employees = request.form['num_employees']
        num_openings = request.form['num_openings']
        responsibilities = request.form['responsibilities']
        eligibility_10th_value = request.form['eligibility_10th_value']
        eligibility_12th_value = request.form['eligibility_12th_value']
        additional_information = request.form['additional_information']

        try:
            # SQL query to insert data into the job_postings table
            cursor = sql_functions.cursor

            cursor.execute(f"SELECT id FROM company_registration WHERE email = '{session['company']}'")
            company_id = cursor.fetchall()

            # Print or log the values to verify correctness
            print(f"Company ID: {company_id[0]['id']}")
            print(f"Job Role: {job_role}")
            print(f"Job Type: {job_type}")
            print(f"Skills Required: {skills_required}")
            print(f"Number of Employees: {num_employees}")
            print(f"Number of Openings: {num_openings}")
            print(f"Responsibilities: {responsibilities}")
            print(f"Eligibility 10th Value:{eligibility_10th_value}")
            print(f"Eligibility 12th Value:{eligibility_12th_value}")
            print(f"Additional Information:{additional_information}")
            # SQL query using parameterized query
            query = """
                INSERT INTO job_posting (company_id, job_role, job_type, skills_required, num_employees,
                                        num_openings, responsibilities, eligibility_10th_value, eligibility_12th_value, additional_information)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (company_id[0]['id'], job_role, job_type, skills_required,
                                   num_employees, num_openings, responsibilities, eligibility_10th_value, eligibility_12th_value, additional_information))

            # Commit the changes to the database
            sql_functions.connection.commit()

            # Notify all students about the new job posting
            notify_students_about_job_posting(job_role)

            flash('Job posting added successfully', 'success')
            connection.commit()
        except Exception as e:
            # Print or log the error for debugging
            print(f'Error: {e}')
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
    
    # try:
        
            # Replace this query with your actual query to fetch all students
            print("|",session['company'],"|")
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
                # fetched_student[0]["job_id"]=id
                cursor.execute(f"select job_role from job_posting where id = {id}")
                job_name = cursor.fetchall()
                fetched_student[0]["job_id"]=job_name[0]["job_role"]
                fetched_students.append(fetched_student[0])
            # print(fetched_students)
            session["fetched_students"] = fetched_students
            return render_template('view_students.html', students=fetched_students,job_ids = job_ids)
    # except Exception as e:
    #     flash(f'Error fetching students: {e}', 'danger')
    #     fetched_students = [{"firstname":"student not selected"}]
        

    # return render_template('view_students.html', students=fetched_students,job_ids = job_ids)

@app.route("/view_student_applied_job/<student_id>")
def view_student_applied_job(student_id):
    cursor.execute(f"select * from student_details where id = {student_id}")
    student_details = cursor.fetchall()
    return render_template("view_applied_student.html",students=student_details)


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

# ------------------------------------------------------- Company Section scheduling and viewing job postings ---------------------------------------

# interviews = []
# @app.route('/schedule_interview', methods=['GET', 'POST'])
# def schedule_interview():
#     # Fetch the list of students from the database
#     try:
#             # Replace this query with your actual query to fetch students
#             cursor.execute(f"select id from company_registration where email = '{session['company']}'")
#             company_id = cursor.fetchall()
#             # print(company_id)
#             student = sql_functions.select_applied_student(company_id=company_id[0]['id'])
#             print(student)
#             # print(student)
#             student_ids = [x["student_id"] for x in student]
#             job_ids = [x["job_id"] for x in student]
#             print(job_ids)
#             # print(student_ids)
#             fetched_students = []
#             for i,id in zip(student_ids,job_ids):
#                 cursor.execute(f"select * from student_details where id = {i}")
#                 fetched_student = cursor.fetchall()
#                 print(fetched_student)
#                 fetched_student[0]["job_id"]=id
#                 fetched_students.append(fetched_student[0])
#             print(fetched_students)
#     except Exception as e:
#         flash(f'Error fetching students: {e}', 'danger')
#         fetched_students = []

#     if request.method == 'POST':
#         student_id = int(request.form['student_id'])
#         date = request.form['date']
#         time = request.form['time']
#         location = request.form['location']

#         selected_student = next((student for student in fetched_students if student['id'] == student_id), None)

#         if selected_student:
#             interview_details = {
#                 'student_name': selected_student['name'],
#                 'date': date,
#                 'time': time,
#                 'location': location
#             }

#             interviews.append(interview_details)

#             try:
#                 with connection.cursor() as cursor:
#                     # SQL query to insert data into the interviews table
#                     sql = "INSERT INTO interviews (student_id, date, time, location) VALUES (%s, %s, %s, %s)"
#                     cursor.execute(sql, (student_id, date, time, location))
#                     connection.commit()

#                     # Send email notification to the student
#                     send_interview_notification(selected_student['email'], interview_details)

#                     flash('Interview scheduled successfully', 'success')
#             except Exception as e:
#                 flash(f'Error: {e}', 'danger')

#         else:
#             flash('Selected student not found', 'danger')

#     return render_template('schedule_interview.html', students=fetched_students, interviews=interviews)
@app.route('/schedule_interview' , methods=['POST',"GET"])
def schedule_interview():

    if request.method == "POST":
        inter_job = request.form.get("job")
        inter_date = request.form.get("date")
        inter_time = request.form.get("time")
        inter_location = request.form.get("location")

        cursor.execute(f"select id from job_posting where job_role = '{inter_job}'")
        job_id = cursor.fetchone()
        print(job_id["id"])

        cursor.execute(f"select * from student_percent_match where job_id = {job_id['id']}")
        selected_students = cursor.fetchall()
        print(selected_students)

        if selected_students != ():
            cursor.execute(f"insert into scheduled_interviews (job_id,date,time,location) values ({job_id['id']} , '{inter_date}','{inter_time}' , '{inter_location}')")
            connection.commit()
            for i in selected_students:

                print(i)
                cursor.execute(f"select email from student_register where id = {i['student_id']}")
                email = cursor.fetchone()
                print(email)
                details = "Your interview have scheduled for \n "+ "\n Job Role : "+inter_job+ "\nDate :  "+ inter_date+"\nTime : "+ inter_time + "\nLocation : " + inter_location
                # send_interview_notification(student_email=email["email"],interview_details=details)
                send_email(subject=f"Your Interview has been scheduled for job role {inter_job}",body=details,recipients=email["email"])
                connection.commit()
        return redirect(url_for("company_dashboard1"))


    cursor.execute(f"select id from company_registration where email = '{session['company']}'")
    company_id = cursor.fetchall()
    cursor.execute(f"select * from job_posting where company_id = {company_id[0]['id']} ")
    jobs = cursor.fetchall()

    job_role = []
    for job in jobs:
        job_role.append(job["job_role"])
    connection.commit()
    
    return render_template("schedule_interview.html",job_roles = job_role)



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


@app.route('/job_listings')
def job_listings():
    # Fetch all job postings from the database
            connection.commit()
            cursor.execute(f"select id from company_registration where email = '{session['company']}'")
            company_id = cursor.fetchall()
            print(company_id)
            sql = f"SELECT * FROM job_posting where company_id = {company_id[0]['id']}"
            cursor.execute(sql)
            job_postings = cursor.fetchall()

            return render_template('job_listings.html', job_postings=job_postings)

@app.route('/scheduled_interviews')
def scheduled_interviews():
    # try:
        # with connection.cursor() as cursor:
            # Fetch all scheduled interviews from the database
            connection.commit()
            cursor.execute(f"select id from company_registration where email = '{session['company']}'  ")
            id = cursor.fetchone()
            print(id["id"])
            # for i in
            sql = "SELECT * FROM scheduled_interviews"
            cursor.execute(sql)
            scheduled_interviews = cursor.fetchall()
            print(scheduled_interviews)

            interviews = []
            for i in scheduled_interviews:
                print(i)
                cursor.execute(f"select job_role from job_posting where id = {i['job_id']} AND company_id = {id['id']}")
                job_role = cursor.fetchall()
                if job_role != ():
                    i["job_role"] = job_role[0]["job_role"]
                    interviews.append(i)

            return render_template('scheduled_interviews.html', interviews=interviews)
    # except Exception as e:
    #     flash(f'Error fetching scheduled interviews: {e}', 'danger')
    #     scheduled_interviews = []

    # return render_template('scheduled_interviews.html')

# ------------------------------------------------------- admin Dashboard ---------------------------------------

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

@app.route('/register_admin1',methods = ["POST","GET"])
def register_admin1():
    if request.method == "POST":
        name = request.form["admin_name"]
        email = request.form["admin_email"]
        password = request.form["admin_password"]
        colname = request.form["college_name"]
        coladdress = request.form["college_address"]
        colid = request.form["college_id"]

        sql_functions.insert_admin(name=name,email=email,password=password,college_name=colname,college_Address=coladdress,college_id=colid)

        return redirect(url_for("admin_dashboard"))
    else:
        return redirect(url_for("/register_admin"))

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('dashboard_admin.html')

@app.route('/admin_students')
def students():
     # Fetch data from applied_student table
    cursor.execute("SELECT * FROM applied_student")
    applied_student_data = cursor.fetchall()
    for i in applied_student_data:
        print(i["student_id"])
        print()
    

    print("student Id is : ",applied_student_data[0]["student_id"])
    app_student = []
    for i in applied_student_data:
        student = {}
        cursor.execute(f'select firstname,lastname from student_details where id = {i["student_id"]}')
        result = cursor.fetchone()
        student["name"] = result["firstname"] 

        cursor.execute(f"select job_role from job_posting where id = {i['job_id']}")
        result = cursor.fetchone()
        student["job_role"] = result["job_role"]

        cursor.execute(f"select company_name from company_registration where id = {i['company_id']}")
        result = cursor.fetchone()
        student["company_name"] = result["company_name"]
        app_student.append(student)
    


    
    # Fetch data from student_details table
    cursor.execute("SELECT * FROM student_details")
    student_details_data = cursor.fetchall()
    
    # Fetch data from student_resume table
    cursor.execute("SELECT * FROM student_resume")
    student_resume_data = cursor.fetchall()
    
    # Fetch data from student_register table
    cursor.execute("SELECT * FROM student_register")
    student_register_data = cursor.fetchall()
    return render_template('admin_student.html', 
                           applied_students=app_student, 
                           student_details=student_details_data, 
                           student_resume=student_resume_data, 
                           student_register=student_register_data)

@app.route('/companies')
def companies():
    
    company_registration, interviews, job_posting= sql_functions.admin_sql_query()
    print(company_registration, interviews, job_posting)

    # Add logic to fetch company data from database
    return render_template('companies.html', company_registration=company_registration,job_posting=job_posting,interviews=interviews)

@app.route('/training_resources',methods = ["POST","GET"])
def training_resources():
    if request.method == "POST":
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        author = request.form.get('author')
        format = request.form.get('format')
        duration = request.form.get('duration')
        language = request.form.get('language')
        level = request.form.get('level')
        tags = request.form.get('tags')
        status = request.form.get('status')
        youtube_link = request.form.get('link')
        sql_functions.insert_training_resources(title = title,
                                                category= category,
                                                description = description,
                                                author = author,
                                                format = format,
                                                duration = duration ,
                                                language = language,
                                                level  = level,
                                                tags = tags,
                                                status = status,
                                                link = youtube_link)
        return redirect(url_for("admin_dashboard"))
    return render_template("training_resources.html")


if __name__ == '__main__':
    app.run(debug=True)
