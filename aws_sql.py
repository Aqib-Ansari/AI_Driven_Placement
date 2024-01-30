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

# sql = '''CREATE TABLE student_register (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         username VARCHAR(255),
#                         email VARCHAR(255) UNIQUE,
#                         password VARCHAR(255),
#                         enrollment_num VARCHAR(255) UNIQUE,
#                         college VARCHAR(255),
#                         course VARCHAR(255),
#                         year VARCHAR(4),
#                         rollno INT
#                     );'''

sql = "select * from student_register"
cursor.execute(sql)
result = cursor.fetchone()
print(result)

connection.close()