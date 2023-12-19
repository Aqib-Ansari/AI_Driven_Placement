from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

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
        

    else:
        name = "not found"
        
    
    return render_template('student_dashboard.html',student_list=student_register_Data_list)

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

@app.route('/login')
def login():
    
    return render_template('login.html')

@app.route('/redirect_to_Dashboard',  methods=['POST'])
def redirect_to_dashboard():
    selected_page = request.form['Login_dropdown']
    if selected_page == 'Student':
        return redirect(url_for('student_dashboard'))
    elif selected_page == 'Admin':
        return redirect(url_for('student_dashboard'))
    elif selected_page == 'Company':
        return redirect(url_for('student_dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template("student_dashboard.html" )
    
@app.route('/student_dashboard', methods=['POST'])
def student_dashboard():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        login_as = request.form['Login_dropdown']
        student_register_Data_list = []
        student_register_Data_list.append(username)
        student_register_Data_list.append(password)
        student_register_Data_list.append(login_as)
    return render_template("student_dashboard.html",student_list=student_register_Data_list)


@app.route('/student_dashboard1')
def redirect_to_student_dashboard():
    return render_template("student_dashboard.html" )

if __name__ == '__main__':
    app.run(debug=True)
