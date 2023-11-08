from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)


@app.route('/')
def registration():
    return render_template('landing.html')

# Route to handle the form submission
@app.route('/register')
def register():
    
    return render_template('Registration.html')

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
    selected_page = request.form['register_dropdown']
    if selected_page == 'Student':
        return redirect(url_for('register'))
    elif selected_page == 'Admin':
        return redirect(url_for('register'))
    elif selected_page == 'Company':
        return redirect(url_for('register'))
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
