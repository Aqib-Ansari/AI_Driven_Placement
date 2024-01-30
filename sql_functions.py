import pymysql
import pymysql.cursors
import os
import csv
import data_class_aidriven
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
    # cursor = connection.cursor()
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

# ------------------------------------------------------------- student_details --------------------------------------


if __name__ == "__main__":
    # insert_register_student(username='aqib',email='aqib@gamil.com',password="asdfasfdasdf",enrollment_num="aa3330909",college="KC college",course="BSC CS",year="FY",rollno=4)
    # print("\n\n\n\n\nhello\n\n\n\n\n")
    # upload_resume()
    # print(login_student_val("aqib11@gmail.com","Aqib@22298")[1])
    # insert_quiz_question("webdev_question.tsv")
    # print(fetch_quiz_question("webdev")[0])
    # connection = make_sql_connection()
    # cursor = connection.cursor()
    # connection.close()
#     # get_student_details('aqib@gamil.com')
# #     cursor.execute('''INSERT INTO student_details (
# #     id,
# #     firstname,
# #     lastname,
# #     middlename,
# #     college,
# #     rollno,
# #     program,
# #     stream,
# #     year,
# #     backlog,
# #     currentcgpa,
# #     email,
# #     phoneno,
# #     gender,
# #     dob,
# #     nationality,
# #     address
# # ) VALUES (
# #     14,
# #     'John',
# #     'Doe',
# #     'M',
# #     'Example College',
# #     'tycs003',
# #     'Computer Science',
# #     'AI',
# #     3,
# #     0,
# #     3.75,
# #     'john.doe@example.com',
# #     '+1234567890',
# #     'Male',
# #     '1995-05-15',
# #     'USA',
# #     '123 Main St, City'
# # )
# #  ''')
# # #     cursor.execute('''ALTER TABLE student_details
# # # ADD CONSTRAINT unique_id_rollno
# # # UNIQUE (id, rollno);
# # # ''')
# #     cursor.execute("select * from student_details")
# #     student_details = cursor.fetchall()
# #     print(student_details)
# #     connection.commit()
#     get_student_details('aqibansari22298@gmail.com')
#     # update_student_details(email='student1@gmail.com',field='lastname',value='Ansari')
#     # cursor.execute('update student_details set firstname  = "Aqib" where id = 14')
#     # sql = cursor.fetchone()
#     sql=update_student_details(email='aqibansari22298@gmail.com',field="lastname",value="Aqib")
#     get_student_details('aqibansari22298@gmail.com')
#     print(sql)
    cursor.execute('select * from quiz_questions')
    questions = cursor.fetchall()
    print(questions[-1]['qType'])