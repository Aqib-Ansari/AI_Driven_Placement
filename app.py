from flask import Flask, render_template, request, redirect, url_for, jsonify , send_file,g,session
import sql_functions


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

@app.route('/register_company')
def register_company():
    
    return render_template('company_registration.html')

@app.route('/register_data', methods=['POST'])
def register_data():
    if request.method=="POST":
        name = request.form['username']
        email = request.form['email']
        pass2 = request.form['pass2']
        Enrolno = request.form['Enrolno']
        college = request.form['college']
        course = request.form['course']
        year = request.form['year']
        rollno = request.form['rollno']
        
        student_register_Data_list = []
        student_register_Data_list.append(name)
        student_register_Data_list.append(email)
        student_register_Data_list.append(pass2)
        student_register_Data_list.append(Enrolno)
        student_register_Data_list.append(college)
        student_register_Data_list.append(course)
        student_register_Data_list.append(year)
        student_register_Data_list.append(rollno)
        
        
        sql_functions.insert_register_student(username=name,email=email,password=pass2,enrollment_num=Enrolno,college=college,course=course,year=year,rollno=rollno)
        session["user"] = email
        session["password"] = pass2
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
            student_register_Data_list = []
            student_register_Data_list.append(email)
            student_register_Data_list.append(password)
            return redirect(url_for("redirect_to_student_dashboard",student_list = [session["user"]]))
        
        else:
            return redirect(url_for('login'))
        


@app.route('/student_dashboard1')
def redirect_to_student_dashboard():
    if "user" in session:
        
        return render_template("dashboard_student.html",student_list = [session["user"]] )
    return redirect(url_for("login"))

# --------------------------------------------- Quiz ------------------------------------------------------
questions = [
    {
        'id': 1,
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Paris', 'Rome', 'Madrid'],
        'correct_answer': 'Paris'
    },
    {
        'id': 2,
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Paris', 'Rome', 'Madrid'],
        'correct_answer': 'Madrid'
    },
    {
        'id': 3,
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Paris', 'Rome', 'Madrid'],
        'correct_answer': 'Rome'
    },
    {
        'id': 4,
        'question': 'What is the capital of France?',
        'options': ['Berlin', 'Paris', 'Rome', 'Madrid'],
        'correct_answer': 'Berlin'
    }
    # Add more questions as needed
]

# questions = sql_functions.fetch_quiz_question("mysql")

# Keep track of user's score

questions = sql_functions.fetch_quiz_question("mysql")
# ids = reough.get_id_questions(questions)
ids = [i for i in range(10)]
current_question_index= ids[0]
user_score = 0
len_question = len(ids)

questions_id = 0

@app.route('/quiz_details')
def quiz_details():
    return render_template("quiz_details.html")

@app.route('/quiz')
def quiz():
    if "user" in session:
        
        global current_question_index

        if questions_id < len(ids):
            current_question = questions[questions_id]
            return render_template('quiz.html', questions=current_question)
        else:
            return redirect(url_for('results'))
    else:
        return redirect(url_for("login"))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if "user" in session:
    
        global current_question_index, user_score, questions_id

        user_answer = request.form.get('answer')
        current_question = questions[questions_id]
        print(user_answer,type(user_answer))
        print(current_question['correct'],type(current_question["correct"]))
        if str(user_answer) == str(current_question['correct']):
            user_score += 1

        questions_id += 1

        return redirect(url_for('quiz'))
    else: 
        return redirect(url_for("login"))

@app.route('/results')
def results():
    if "user" in session:
        
        global user_score
        global len_question
        Percentage = (user_score*100)/len_question
        return render_template('results.html', score=user_score,len = len_question,Percentage = Percentage)
    else:
        return redirect(url_for("login"))

# ------------------------------------------------ Details ----------------------------------------------------------

@app.route('/update_details')
def update_details():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    pass



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
            if file and file.filename.lower().endswith('.pdf'):
                # Save the PDF file
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
    row = [1, 2, 3]*20

    return render_template('view_jobs.html', row=row)

if __name__ == '__main__':
    app.run(debug=True)
