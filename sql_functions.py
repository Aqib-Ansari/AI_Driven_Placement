import pymysql
import pymysql.cursors
import os
import data_class_aidriven
def make_sql_connection():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Aqib@22298',
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

def upload_resume(resume_path):
    with open(resume_path, 'rb') as pdf_file:
        pdf_data = pdf_file.read()
    sql = "INSERT INTO resume (id,pdf_data) VALUES ( %s,%s)"
    cursor.execute(sql, (15,pdf_data))
    connection.commit()
   

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


if __name__ == "__main__":
    insert_register_student(username='aqin',email='aqib@gamil.com',password="asdfasfdasdf",enrollment_num="aa3330909",college="KC college",course="BSC CS",year="FY",rollno=4)
    print("\n\n\n\n\nhello\n\n\n\n\n")
    upload_resume("./static/MH01AT 7102 AKBAR.pdf")
#    insert_question()