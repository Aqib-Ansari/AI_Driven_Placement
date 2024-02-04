import pymysql
import pymysql.cursors
import os
import csv
# import data_class_aidriven
def make_sql_connection():
    connection = pymysql.connect(host='aidriven.cdhiotv5c9su.us-east-1.rds.amazonaws.com',
                                user='admin',
                                password='aidriven',
                                database='aidriven',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

connection = make_sql_connection()
cursor = connection.cursor()
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
    print(result)
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
        print(id)
        cursor.execute("SELECT * FROM student_details where id = %s;",id[0]['id'])
        
        student_details = cursor.fetchall()
        print(student_details)
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
        print(id)
        id= id[0]["id"]

        student_details = get_student_details(email=email)
       
        if student_details != ():
            cursor.execute(f"update student_details set {field} ='{value}' where id = {id}")
            connection.commit()
            student_details = cursor.fetchall()
            print(student_details)
            return student_details
        else:
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
    print(id)
    id= id[0]["id"]

    if if_resume_present(email=email) == True:
        cursor.execute(f"insert into student_resume (id, file_name) values ({id} ,'{filename}' )")
        success = cursor.fetchall()
        connection.commit()
        return success
    
    
    

def if_resume_present(email):
    global connection 
    global cursor

    cursor.execute("select id from student_register where email = %s;",email)
    id = cursor.fetchall()
    print(id)
    id= id[0]["id"]

    cursor.execute(f"select file_name from student_resume where id = {id}")
    result = cursor.fetchall()
    print(result)
      
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



def insert_job_posting(job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities):
    try:
        # Establish a connection to the MySQL database
        global connection,cursor

        # SQL query to insert data into the table
        sql = '''
        INSERT INTO job_postings (job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        # Data to be inserted into the table
        data = (job_role, job_type, skills_required, num_employees, num_openings, company_description, responsibilities)

        # Execute the SQL query
        cursor.execute(sql, data)

        # Commit the changes to the database
        connection.commit()

        print("Data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

   

# Example usage

def insert_applied_student_data(student_id, company_id, job_id):
    try:
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

    except Exception as e:
        print(f"Error: {e}")


def select_applied_student(company_id):
    global connection,cursor

    sql = f'''select * from applied_student where company_id = {company_id}'''

    cursor.execute(sql)
    applied_students = cursor.fetchall()
    return applied_students


   
connection.commit()
if __name__ == "__main__":
   
    # insert_job_posting('Software Engineer', 'Full Time', 'Java, Python, SQL', 50, 5, 'A leading tech company', 'Develop and maintain software applications')
    # insert_job_posting('Marketing Specialist', 'Part Time', 'Digital Marketing, Social Media', 20, 3, 'A creative marketing agency', 'Plan and execute marketing campaigns')
#     cursor.execute('''CREATE TABLE interviews (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     student_id INT,
#     date DATE,
#     time VARCHAR(20),
#     location VARCHAR(255),
#     FOREIGN KEY (student_id) REFERENCES student_details(id)
# );''')
    cursor.execute("desc interviews")
    # print(validate_company_login(email='company2@gmail.com',password="password"))
    # insert_applied_student_data(3, 1, 1)
    output = cursor.fetchall()
    for i in output:
        print('\n')
        print(i)
        print('____'*20)
        print('\n')
    # print(validate_company_login('aqibansari22298@gmail.com',password="password"))
   
    connection.commit()