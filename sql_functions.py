import pymysql
import pymysql.cursors
import os
import csv
from datetime import datetime, timedelta , date , time

# import data_class_aidriven
def make_sql_connection():
    connection = pymysql.connect(host='sql6.freesqldatabase.com',
                                user='sql6682320',
                                password='zGRcDLE2gC',
                                database='sql6682320',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

connection = make_sql_connection()
cursor = connection.cursor()
cursor.execute("SET SESSION time_zone = '+5:30';")
# with connection:
#     # with connection.cursor() as cursor:
#         # Create a new record
#     #     sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#     #     cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

#     # # connection is not autocommit by default. So you must commit to save
#     # # your changes.
#     # connection.commit()

#     with connection.cursor() as cursor:
#         # Read a single record

# sql = "SELECT `id`, `password` FROM `student_register` WHERE `email`=%s"
# cursor.execute(sql, ('aqibnsri@gmail.com',))
# result = cursor.fetchone()
# print(result['id'])

# username = "Aqib"
# email = "aabba@gmail.com"
# password = "veerzaara"
# enrollment_num = "334AGANA"
# college = "KC college"
# course = "BSC CS"
# year = "TY"
# rollno = 45


def insert_register_student(username,email,password,enrollment_num,college,course,year,rollno):
    cursor = connection.cursor()
    sql = f"INSERT INTO student_register (username, email, password, enrollment_num, college, course, year, rollno) VALUES ('{username}', '{email}', '{password}', '{enrollment_num}', '{college}', '{course}','{year}', {rollno});"
    cursor.execute(sql)
    result = cursor.fetchall()
    # print(result)
    connection.commit()

# def select_register_student()

# def upload_resume():
    # with open('static/AQIB resume kc college.pdf', 'rb') as file:
    #     file_data = file.read()
    # # Insert the file into the database
    # query = "INSERT INTO resume (filename, pdf_data) VALUES (%s, %s)"
    # values = ('AQIB resume kc college.pdf', file_data)
    # cursor.execute(query, values)

    # # Commit the transaction
    # connection.commit()

    # Retrieve the file from the database
    # file_id = 1  # Replace with the ID of the file you want to retrieve
    # query = "SELECT filename, pdf_data FROM resume WHERE id = %s"
    # cursor.execute(query, (file_id,))
    # result = cursor.fetchone()

    # if result:
    #     filename, file_data = result

    #     # Write the file to the disk
    #     with open(filename, 'wb') as file:
    #         file.write((file_data.encode('utf-8')))

    # # Close the cursor and connection
    # cursor.close()



def insert_question(q):
# Connect to MySQL
    # cursor = connection.cursor()

    # Insert questions into the quiz_questions table
    
        # Extracting data from the question dictionary
    q_id = q.id
    q_type = q.qtype
    q_text = q.question
    q_option1 = q.option1
    q_option2 = q.option2
    q_option3 = q.option3
    q_option4 = q.option4
    q_correct_answer = q.correct

        # Forming and executing the SQL query
    sql_query = f"INSERT INTO quiz_questions (id, qtype ,question, option1, option2, option3, option4, correct) VALUES ({q_id }, '{q_type}' , '{q_text}', '{q_option1}', '{q_option2}','{q_option3}','{q_option4}',{q_correct_answer})"
    cursor.execute(sql_query)

    # Commit the changes and close the connection
    connection.commit()

def login_student_val(email,password):
    try:
        sql  = "SELECT  `id`,`password` FROM `student_register` WHERE `email`=%s"
        cursor.execute(sql,(email))
        
        result = cursor.fetchone()
        # print("sql_functions : ",result["password"], "\nuser input :",password)
        if result["password"] == password:
            print("Login successfull")
            return True,"correct_password"
        else:
            print("Incorrect password")
            return False,"Incorrect password"
    except:
            return False,"Incorrect email"
    
# ----------------------------------------------- insert quiz questions -------------------------------------
    
def insert_data(connection, data):
    # cursor = connection.cursor()
    insert_query = '''
    INSERT INTO quiz_questions (qtype, question, option1, option2, option3, option4, correct)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''
    with connection.cursor() as cursor:
        cursor.executemany(insert_query, data)
    connection.commit()

def read_data_from_tsv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        next(tsv_reader)  # Skip header
        data = [tuple(row) for row in tsv_reader]
    return data

def insert_quiz_question(tsv_file_path):
    try:
        # Connect to MySQL
        # connection = make_sql_connection()
        
        # Create table if not exists
        # sql  = '''CREATE TABLE quiz_questions (
        #             id INT AUTO_INCREMENT PRIMARY KEY,
        #             qType VARCHAR(255),
        #             question TEXT,
        #             option1 VARCHAR(255),
        #             option2 VARCHAR(255),
        #             option3 VARCHAR(255),
        #             option4 VARCHAR(255),
        #             correct VARCHAR(255)
        #         );'''
        # with connection.cursor() as cursor:
        #     cursor.execute(sql)
        # connection.commit()

        # Read data from TSV file
        data_to_insert = read_data_from_tsv(tsv_file_path)

        # Insert data into MySQL
        insert_data(connection, data_to_insert)

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if connection:
            connection.close()

# ---------------------------------------------------- selecting quiz questions ---------------------------------------------
def fetch_quiz_question(qtype):     
    try:
        # Connect to the MySQL server

        # Define the SQL query to select all data from the quiz_questions table
        select_query = "SELECT * FROM quiz_questions where qtype = %s;"

        # Execute the query
        cursor.execute(select_query,qtype)

        # Fetch all the rows
        rows = cursor.fetchall()

        # Display the retrieved data
        # for row in rows:
        #     print(row)

        return rows

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def get_student_details(email):
    try:
        global connection 
        global cursor

        # Replace with your actual table schema
        
        cursor.execute("select id from student_register where email = %s;",email)
        id = cursor.fetchall()
        # print(id)
        cursor.execute("SELECT * FROM student_details where id = %s;",id[0]['id'])
        
        student_details = cursor.fetchall()
        # print(student_details)
        return student_details

    except Exception as err:
        print(f"Error: {err}")
        return err

def update_student_details(email, field,value):
    try:
        global connection 
        global cursor

        
        
        cursor.execute("select id from student_register where email = %s;",email)
        id = cursor.fetchall()
        # print(id)
        id= id[0]["id"]
        # print("field : : : : : : : : " ,field)
        student_details = get_student_details(email=email)
       
        if student_details != ():
            # print(field)
            if field in ["year","phoneno","backlog","currentcgpa"]:
                cursor.execute(f"update student_details set {field} ={value} where id = {id}")
                student_details = cursor.fetchall()
                connection.commit()
            else:
                cursor.execute(f"update student_details set {field} ='{value}' where id = {id}")
                student_details = cursor.fetchall()
                connection.commit()

            # print(student_details)
            return student_details
        else:
            # print(field)
            sql_query = f"INSERT INTO student_details (id,{field}) VALUES ( {id}, '{value}');"

            cursor.execute(sql_query)
            connection.commit()
            return student_details

    except Exception as err:
        print(f"Error: {err}")
        return err

# ------------------------------------------------------------- resume --------------------------------------
def insert_resume(email,filename):
    global connection 
    global cursor

    
    cursor.execute("select id from student_register where email = %s;",email)
    id = cursor.fetchall()
    # print(id)
    id= id[0]["id"]

    if if_resume_present(email=email) == False:
        cursor.execute(f"insert into student_resume (id, file_name) values ({id} ,'{filename}' )")
        success = cursor.fetchall()
        connection.commit()
        return success
    else:
        cursor.execute(f"UPDATE student_resume SET file_name = '{filename}' WHERE id = {id};")
    
    
    

def if_resume_present(email):
    global connection 
    global cursor

    cursor.execute("select id from student_register where email = %s;",email)
    id = cursor.fetchall()
    # print(id)
    id= id[0]["id"]

    cursor.execute(f"select file_name from student_resume where id = {id}")
    result = cursor.fetchall()
    # print(result)
      
    if result == ():
        return False
    else:
        return result[0]['file_name']



def insert_company_data(username, password1, password2, company_name, registration_number, address,
                        phone_number, email, industry_type, company_description, logo_upload_filename,
                        company_size):
   
        # Create a cursor object to interact with the database
        # global connection
        # global cursor

        # SQL query to insert data into the table
        sql = """INSERT INTO company_registration 
                 (username, password1, password2, company_name, registration_number, address,
                  phone_number, email, industry_type, company_description, logo_upload_filename,
                  company_size) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # Data to be inserted into the table
        data = (username, password1, password2, company_name, registration_number, address,
                phone_number, email, industry_type, company_description, logo_upload_filename,
                company_size)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and connection
        # cursor.close()
        # connection.close()

      


def validate_company_login(email, password):
    # try:
        
        global connection
        global cursor
        

        # SQL query to check if the provided email and password match any record
        sql = """SELECT * FROM company_registration
                 WHERE email = %s AND password1 = %s"""

        # Data to be used in the query
        data = (email, password)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Fetch the result
        result = cursor.fetchone()
        # print(result)

        # Close the cursor and connection

        # Check if a matching record was found
        if result:
            return True  # Login successful
        else:
            return False  # Login failed

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return False  # Return False in case of an error

# Example usage



def insert_job_posting(company_id,job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities):
    try:
        # Establish a connection to the MySQL database
        global connection,cursor

        # SQL query to insert data into the table
        sql = '''
        INSERT INTO job_posting (company_id,job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # Data to be inserted into the table
        data = (company_id, job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

   

# Example usage

def insert_applied_student_data(student_id, company_id, job_id):
    
        # Establish a connection to the MySQL database
        global connection,cursor

        # SQL query to insert data into the applied_student table
        sql = '''
        INSERT INTO applied_student (student_id, company_id, job_id)
        VALUES (%s, %s, %s)
        '''

        # Data to be inserted into the table
        data = (student_id, company_id, job_id)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted into applied_student successfully!")

    


def select_applied_student(company_id):
    global connection,cursor

    sql = f'''select * from applied_student where company_id = {int(company_id)}'''

    cursor.execute(sql)
    applied_students = cursor.fetchall()
    return applied_students



def insert_interview_data( student_id, job_id, date, time, location):
    try:
        # Create a cursor object to interact with the database
        global connection,cursor

        # SQL query to insert data into the interviews table
        sql = '''
        INSERT INTO interviews (student_id, job_id, date, time, location)
        VALUES (%s, %s, %s, %s, %s)
        '''

        # Data to be inserted into the table
        data = (student_id, job_id, date, time, location)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted into interviews successfully!")

    except Exception as e:
        print(f"Error: {e}")




#  ------------------------- admin -------------------------------------
        
def insert_admin(name,email,password,college_name,college_Address,college_id):
    cursor.execute(f"insert into admin ( admin_name,admin_email,password,college_name,college_address,college_id) values ('{name}',  '{email}','{password}','{college_name}','{college_Address}',{college_id})")
    output = cursor.fetchall()
    connection.commit()
    return output
def validate_admin_login(email, password):
    # try:
        
        global connection
        global cursor
        

        # SQL query to check if the provided email and password match any record
        sql = f"""SELECT * FROM admin
                 WHERE admin_email = '{email}' AND password = '{password}'"""

        # Data to be used in the query
        

        # Execute the SQL query
        cursor.execute(sql)

        # Fetch the result
        result = cursor.fetchone()
        # print(result)

        # Close the cursor and connection

        # Check if a matching record was found
        if result:
            return True  # Login successful
        else:
            return False  # Login failed
        

# --------------------------------------------- View students in admin Panel -------------------------------
   

# ------------------------------------------------------------------------ View Company ----------------------------------------------------------
        
def admin_sql_query():
        global connection,cursor

        with connection.cursor() as cursor:
            # Execute the SQL query
            sql_company_registration = "SELECT * FROM company_registration"
            sql_interviews = "SELECT * FROM interviews"
            sql_job_posting = "SELECT * FROM job_posting"
            # Fetch all the data
            cursor.execute(sql_company_registration)
            company_registration_data = cursor.fetchall()
            cursor.execute(sql_interviews)
            interviews_data = cursor.fetchall()
            cursor.execute(sql_job_posting)
            job_posting_data = cursor.fetchall()

        return company_registration_data, interviews_data, job_posting_data 

#  --------------------------------------- notification ----------------------------------------------

def insert_notification(student_id,msg,link):
    global connection
    global cursor
    insert_query = """
        INSERT INTO notification (student_id, msg, link) 
        VALUES (%s, %s, %s)
        """
    data_to_insert = (student_id, msg, link)
    cursor.execute(insert_query, data_to_insert)
    output = cursor.fetchall()
        # Commit the changes
    connection.commit()
    return output

def select_notification(student_id):
    global connection
    global cursor

    cursor.execute(f"select * from notification where student_id = {student_id}")
    notifications = cursor.fetchall()
    return notifications

# --------------------------- training Resources ----------------------------------------

def insert_training_resources(title,category,description,author,format,duration,language,level,tags,status,link):
    data = (title,category,description,author,format,duration,language,level,tags,status,link)

    insert_query = """
        INSERT INTO training_resources (title, category, description, author, format, duration, language, level, tags, status, youtube_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    cursor.execute(insert_query, data)

        # Commit changes to the database
    connection.commit()

    return "inserted successfully"

def select_training_resources():
    
    query = "select * from training_resources"

    cursor.execute(query=query)
    training_resources = cursor.fetchall()
    return training_resources

def insert_student_profile_img(email,filename):
            student_details = get_student_details(email)
            student_id = student_details[0]['id']
            cursor.execute(f"select filename from student_profile_img where student_id = {student_id}")
            profile_filename=cursor.fetchall()
            # print(profile_filename)
            if profile_filename == None or profile_filename == ():
                 
                cursor.execute(f"insert into student_profile_img (student_id,filename) values ({student_id} , '{filename}')")
                connection.commit()
            else:
                os.remove(f'./static/student/{profile_filename[0]["filename"]}')
                cursor.execute(f"update student_profile_img set filename = '{filename}' where student_id = {student_id}" )
            connection.commit()

def insert_interviews(job,date,time,location):
    job_id = job # Replace with the actual job_id
    interview_date = date  # Replace with the actual date
    interview_time = time  # Replace with the actual time
    location = location  # Replace with the actual location

        # SQL query to insert a record into the scheduled_interviews table
    sql = '''INSERT INTO scheduled_interviews (job_id, date, time, location)
                 VALUES (%s, %s, %s, %s)  '''

        # Execute the SQL query
    cursor.execute(sql, (job_id, interview_date, interview_time, location))

    # Commit the changes to the database
    connection.commit()

def insert_percent_match(student_id, job_id, percent_match):
    try:
        # SQL query to insert data
        sql_insert = "INSERT INTO student_percent_match (student_id, job_id, percent_match) VALUES (%s, %s, %s)"

        # Values to be inserted
        values = (student_id, job_id, percent_match)

        # Execute the query
        cursor.execute(sql_insert, values)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully!")

    except Exception as e:
        print("Error inserting data:", e)

def select_percent_match():
    try:
        # SQL query to select data
        sql_select = "SELECT * FROM student_percent_match"

        # Execute the query
        cursor.execute(sql_select)

        # Fetch all the rows
        rows = cursor.fetchall()

        # Display the results
        # for row in rows:
        #     print(row)
        return rows
    except Exception as e:
        print("Error selecting data:", e)

def insert_alumni_data( data):
    try:
            global connection, cursor
            # SQL statement for insertion
            sql = "INSERT INTO alumni (name, batch, placement_status, company, linkedin, email, about_alumni) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            # Data for insertion
            values = (
                data['name'],
                data['batch'],
                data['placement_status'],
                data['company'],
                data['linkedin'],
                data['email'],
                data['about_alumni']
            )

            # Execute the SQL statement
            cursor.execute(sql, values)

        # Commit the changes to the database
            connection.commit()

            print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

def select_alumni_data():
    try:

            # SQL statement for selection
            sql = "SELECT * FROM alumni"

            # Execute the SQL statement
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()

            
            return result

    except Exception as e:
        print(f"Error: {e}")

connection.commit()
if __name__ == "__main__":
   
    # insert_job_posting('Software Engineer', 'Full Time', 'Java, Python, SQL', 50, 5, 'A leading tech company', 'Develop and maintain software applications')
    # insert_job_posting('Marketing Specialist', 'Part Time', 'Digital Marketing, Social Media', 20, 3, 'A creative marketing agency', 'Plan and execute marketing campaigns')
    # insert_quiz_question('data/java_questions.tsv')
#     cursor.execute('''
# CREATE TABLE alumni (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     name VARCHAR(255) NOT NULL,
#     batch VARCHAR(4) NOT NULL,
#     placement_status VARCHAR(20) NOT NULL,
#     company VARCHAR(255),
#     linkedin VARCHAR(255),
#     email VARCHAR(255),
#     about_alumni TEXT
# )
# ''')
    # print(validate_company_login(email='company2@gmail.com',password="password"))
    # insert_applied_student_data(3, 1, 1)
    # print(insert_interview_data( 1, 2, '2024-02-10', '15:30:00', 'Company HQ'))
#     cursor.execute('''
# CREATE TABLE student_percent_match (
#                     id INT PRIMARY KEY AUTO_INCREMENT,
#                     student_id INT,
#                     job_id INT,
#                     percent_match DECIMAL(5,2), 

#                     FOREIGN KEY (student_id) REFERENCES student_register(id),
                    # FOREIGN KEY (job_id) REFERENCES job_posting(id))''')
    # print(insert_job_posting(company_id=1,job_role="a",job_type="b",skills_required="c",num_employees=500,num_openings=4,company_description="abc",responsibilities="response"))
    # insert_resume(email="aqib@gmail.com",filename="aqib.pdf")
    # update_student_details(email="aqibansari22298@gmail.com",field="dob",value="2002-10-12")
    # cursor.execute("UPDATE notification SET date_time = CONVERT_TZ(NOW(), 'UTC', 'Asia/Kolkata')")
    # insert_training_resources(title="Ai ML",category="any",description="Learn how to create a Chatbots",
    #                           author="Nivedita",format="Online",duration=5.30,language="English",level="beginner",tags="Resume,placements",status="active",link="https://youtube.com")
    # insert_interviews(job=19,date=date(2024, 3, 10),time=time(14, 30),location="Mumbai")
    # cursor.execute("drop table student_percent_match")
    output = cursor.fetchall()
    for i in output:
        print('\n')
        print(i)
        print('____'*20)
        print('\n')
    # print(select_applied_student(1))
    # print(output)
    # print(validate_company_login('aqibansari22298@gmail.com',password="password"))
    # insert_notification(student_id=1,msg="go to dashboard",link='/student_dashboard1')
    # print(select_notification(student_id=1))
    # print(if_resume_present(email="aqibansari22298@gmail.com"))
    # insert_percent_match(job_id=2,student_id=1,percent_match=80)
    print(select_percent_match())
   
    connection.commit()